#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import yaml
import logging
from matplotlib import pyplot as plt
from TypedUnit import Length, validate_units, ureg

from PyOptik.material.base_class import BaseMaterial
from PyOptik.directories import material_paths
from PyOptik.material_type import MaterialType

logger = logging.getLogger(__name__)


class TabulatedMaterial(BaseMaterial):
    """
    Class representing a material with tabulated refractive index (n) and absorption (k) values.

    Attributes
    ----------
    filename : str
        The name of the YAML file containing material properties.
    wavelength : numpy.ndarray
        Array of wavelengths in micrometers for which the refractive index and absorption values are tabulated.
    n_values : numpy.ndarray
        Array of tabulated refractive index values (n) corresponding to the wavelengths.
    k_values : numpy.ndarray
        Array of tabulated absorption values (k) corresponding to the wavelengths.
    reference : Optional[str]
        Reference information for the material data.
    """

    def __init__(self, filename: str, file_path=None, interpolation: str = "linear"):
        """
        Initializes the TabulatedMaterial with a filename.

        Parameters
        ----------
        filename : str
            The name of the YAML file containing material properties.
        file_path : pathlib.Path, optional
            Explicit YAML path for hierarchy-preserving catalog pages. When
            omitted, the user material directory is searched.
        interpolation : {"linear", "pchip"}, optional
            Interpolation method. ``"linear"`` is the default;
            ``"pchip"`` provides monotonic piecewise-cubic interpolation.
        """
        self.filename = filename
        self.file_path = file_path
        if interpolation not in {"linear", "pchip"}:
            raise ValueError("interpolation must be 'linear' or 'pchip'.")
        self.interpolation = interpolation

        # Initialize attributes
        self.wavelength_bound = None
        self.wavelength = None
        self.n_values = None
        self.k_values = None
        self.reference = None
        self.conditions = None
        self.comments = None
        self._n_wavelength = None
        self._k_wavelength = None

        # Load tabulated data from the YAML file
        self._load_tabulated_data()

    def __str__(self) -> str:
        """Return the material name and ``Tabulated`` model type."""
        return self.filename + '[Tabulated]'

    def _load_tabulated_data(self) -> None:
        """
        Loads the tabulated refractive index and absorption values from the specified YAML file.

        Raises
        ------
        FileNotFoundError
            If the specified YAML file does not exist.
        ValueError
            If the YAML data is malformed or missing required keys.
        """
        file_path = self.file_path or next(
            (directory / f"{self.filename}.yml"
             for directory in material_paths(MaterialType.TABULATED)
             if (directory / f"{self.filename}.yml").exists()),
            None,
        )
        if file_path is None:
            raise FileNotFoundError(f"Tabulated YAML file '{self.filename}.yml' not found.")

        with file_path.with_suffix('.yml').open('r') as file:
            parsed_yaml = yaml.safe_load(file)
        logger.debug("Loaded tabulated data from %s", file_path)

        try:
            for entry in parsed_yaml['DATA']:
                kind = str(entry.get('type', '')).lower().split()
                if len(kind) != 2 or kind[0] != 'tabulated' or kind[1] not in {'n', 'k', 'nk'}:
                    continue
                data = numpy.array(
                    [[float(value) for value in row.split()] for row in entry['data'].strip().splitlines()]
                )
                expected_columns = 3 if kind[1] == 'nk' else 2
                if data.ndim != 2 or data.shape[1] != expected_columns or len(data) < 2:
                    raise ValueError(f"tabulated {kind[1]} data must contain at least two valid rows")
                if not numpy.all(numpy.isfinite(data)) or numpy.any(numpy.diff(data[:, 0]) <= 0):
                    raise ValueError("tabulated wavelengths must be finite and strictly increasing")
                wavelengths = data[:, 0] * ureg.micrometer
                if kind[1] in {'n', 'nk'}:
                    self._n_wavelength = wavelengths
                    self.n_values = data[:, 1]
                if kind[1] == 'k':
                    self._k_wavelength = wavelengths
                    self.k_values = data[:, 1]
                elif kind[1] == 'nk':
                    self._k_wavelength = wavelengths
                    self.k_values = data[:, 2]
            if self.n_values is None and self.k_values is None:
                raise ValueError("no supported tabulated n, k, or nk dataset found")
            self.wavelength = self._n_wavelength if self._n_wavelength is not None else self._k_wavelength
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid or missing data in YAML file {file_path}")

        ranges = [values for values in (self._n_wavelength, self._k_wavelength) if values is not None]
        self.wavelength_bound = [min(values.min().magnitude for values in ranges), max(values.max().magnitude for values in ranges)] * ureg.micrometer

        # Extract reference
        self.reference = parsed_yaml.get('REFERENCES', None)
        self.conditions = parsed_yaml.get('CONDITIONS', {})
        self.comments = parsed_yaml.get('COMMENTS', None)
        logger.debug("Validated tabulated material '%s' with %s points", self.filename, len(self.wavelength))

    @validate_units
    def compute_refractive_index(self, wavelength: Length | float, out_of_range: str = "warn") -> numpy.ndarray:
        """
        Interpolates the refractive index (n) and absorption (k) values for the given wavelength(s).

        Parameters
        ----------
        wavelength : Length | float
            Wavelength(s) in micrometers for which to interpolate n and k.
        out_of_range : {"warn", "raise", "clip"}, optional
            Policy for wavelengths outside the tabulated range.

        Returns
        -------
        complex or numpy.ndarray
            Complex refractive index values (n + i*k). A scalar input returns
            a scalar complex value; array-like input returns an array.

        Raises
        ------
        ValueError
            If the wavelength is outside the tabulated range.
        """
        if not isinstance(wavelength, Length):
            wavelength = wavelength * ureg.meter

        return_as_scalar = numpy.isscalar(wavelength.magnitude)

        wavelength = numpy.atleast_1d(wavelength)

        self._check_wavelength(wavelength, out_of_range)

        if out_of_range == "clip":
            wavelength = self._clip_wavelength(wavelength)
        elif out_of_range == "raise":
            # _check_wavelength has already raised if needed; this keeps the
            # behavior explicit for future range implementations.
            pass

        values = wavelength.to(ureg.meter).magnitude
        n_interp = self._interpolate(values, self._n_wavelength, self.n_values, default=1.0)
        k_interp = self._interpolate(values, self._k_wavelength, self.k_values, default=0.0)

        index = n_interp + 1j * k_interp

        return index[0] if return_as_scalar else index

    def _interpolate(self, values, wavelengths, data, default: float):
        """Interpolate one optical-constant component with endpoint extrapolation."""
        if wavelengths is None or data is None:
            return numpy.full(values.shape, default, dtype=float)
        x = wavelengths.to(ureg.meter).magnitude
        if self.interpolation == "linear":
            result = numpy.interp(values, x, data)
            left = values < x[0]
            right = values > x[-1]
            result[left] = data[0] + (values[left] - x[0]) * (data[1] - data[0]) / (x[1] - x[0])
            result[right] = data[-1] + (values[right] - x[-1]) * (data[-1] - data[-2]) / (x[-1] - x[-2])
            return result
        return self._pchip(values, x, data)

    @staticmethod
    def _pchip(values, x, y):
        """Evaluate monotonic cubic Hermite interpolation with linear extrapolation."""
        h = numpy.diff(x)
        delta = numpy.diff(y) / h
        slopes = numpy.empty_like(y, dtype=float)
        slopes[0], slopes[-1] = delta[0], delta[-1]
        for index in range(1, len(y) - 1):
            if delta[index - 1] * delta[index] <= 0:
                slopes[index] = 0.0
            else:
                w1, w2 = 2 * h[index] + h[index - 1], h[index] + 2 * h[index - 1]
                slopes[index] = (w1 + w2) / (w1 / delta[index - 1] + w2 / delta[index])
        intervals = numpy.clip(numpy.searchsorted(x, values, side='right') - 1, 0, len(x) - 2)
        step = h[intervals]
        t = (values - x[intervals]) / step
        result = ((2*t**3 - 3*t**2 + 1) * y[intervals] + (t**3 - 2*t**2 + t) * step * slopes[intervals] + (-2*t**3 + 3*t**2) * y[intervals + 1] + (t**3 - t**2) * step * slopes[intervals + 1])
        return result

    def plot(self, axes=None, samples: int = 100) -> None:
        """
        Plots the tabulated refractive index (n) and absorption (k) as a function of wavelength.

        Parameters
        ----------
        axes : matplotlib.axes.Axes, optional
            Axes on which to draw the curves. A compact, styled figure is
            created when omitted.
        samples : int
            The number of samples to use for the wavelength range.

        Returns
        -------
        None
            The supplied axes and its absorption twin are modified in place.

        Raises
        ------
        ValueError
            If the wavelength is not a 1D array or list of float values.
        """
        if axes is None:
            figure, axes = plt.subplots(figsize=(7, 4.5), layout="constrained")
        else:
            figure = axes.figure
        figure.set_size_inches(7, 4.5, forward=True)
        wavelength = numpy.linspace(
            self.wavelength_bound[0].magnitude,
            self.wavelength_bound[1].magnitude,
            samples
        ) * self.wavelength_bound.units

        n_values, k_values = self.compute_refractive_index(wavelength).real, self.compute_refractive_index(wavelength).imag

        axes.set(
            title=f"Optical constants: {self.filename}",
            xlabel='Wavelength [µm]',
            ylabel='Refractive Index (n)',
        )

        axes.set_title(axes.get_title(), fontsize=14, pad=12)
        axes.set_xlabel(axes.get_xlabel(), fontsize=11)
        axes.set_ylabel(axes.get_ylabel(), fontsize=11)
        axes.tick_params(labelsize=10)
        axes.grid(alpha=0.25, linewidth=0.7)
        axes.plot(wavelength.to(ureg.micrometer).magnitude, n_values, '-', color='tab:blue', label='n')

        ax2 = axes.twinx()

        ax2.set(
            ylabel='Absorption (k)',
        )
        ax2.set_ylabel('Absorption (k)', fontsize=11)
        ax2.tick_params(labelsize=10)

        ax2.plot(wavelength.to(ureg.micrometer).magnitude, k_values, '-', color='tab:red', label='k')
        return None

    def print(self) -> str:
        """
        Provides a formal string representation of the TabulatedMaterial object, including key attributes.

        Returns
        -------
        str
            Formal representation of the TabulatedMaterial object.
        """
        return (
            f"\nTabulatedMaterial: '{self.filename}',\n"
            f"wavelength_range: [{self.wavelength.min()} µm, {self.wavelength.max()} µm],\n"
            f"reference: '{self.reference}')"
        )
