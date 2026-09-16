#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import logging
import csv
from pathlib import Path
from matplotlib import pyplot as plt
from TypedUnit import Length, validate_units, ureg

from PyOptik.material.base_class import BaseMaterial
from PyOptik.material.dataset import MaterialDocument, MaterialMetadata, TabulatedDataset, parse_material
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

        file_path = file_path.with_suffix('.yml')
        try:
            document = parse_material(file_path)
        except ValueError as error:
            raise ValueError(f"Invalid or missing data in YAML file {file_path}: {error}") from error
        logger.debug("Loaded tabulated data from %s", file_path)
        if not document.tabulated_datasets:
            raise ValueError(f"No tabulated dataset found in {file_path}")
        self._apply_document(document)
        logger.debug("Validated tabulated material '%s' with %s points", self.filename, len(self.wavelength))

    def _apply_document(self, document: MaterialDocument) -> None:
        """Populate interpolation arrays from a validated document."""
        self._document = document
        for dataset in document.tabulated_datasets:
            wavelengths = numpy.asarray(dataset.wavelength_um) * ureg.micrometer
            values = numpy.asarray(dataset.values)
            if dataset.kind in {'n', 'nk'}:
                self._n_wavelength, self.n_values = wavelengths, values[:, 0]
            if dataset.kind == 'k':
                self._k_wavelength, self.k_values = wavelengths, values[:, 0]
            elif dataset.kind == 'nk':
                self._k_wavelength, self.k_values = wavelengths, values[:, 1]
        self.wavelength = self._n_wavelength if self._n_wavelength is not None else self._k_wavelength
        ranges = [values for values in (self._n_wavelength, self._k_wavelength) if values is not None]
        lower = max(values.min().magnitude for values in ranges)
        upper = min(values.max().magnitude for values in ranges)
        if lower >= upper:
            raise ValueError("tabulated n and k wavelength ranges do not overlap")
        self.wavelength_bound = [lower, upper] * ureg.micrometer
        self.reference = document.metadata.reference
        self.conditions = dict(document.metadata.conditions)
        self.comments = document.metadata.comments

    @classmethod
    def from_arrays(
        cls, name, wavelength, *, n=None, k=None, interpolation="linear",
        reference=None, conditions=None, comments=None,
    ):
        """Construct a tabulated material from wavelength, ``n``, and ``k`` arrays."""
        if n is None and k is None:
            raise ValueError("at least one of n or k must be provided")
        if isinstance(wavelength, ureg.Quantity):
            wavelength_um = numpy.asarray(wavelength.to(ureg.micrometer).magnitude, dtype=float)
        else:
            wavelength_um = numpy.asarray(wavelength, dtype=float)
        if wavelength_um.ndim != 1:
            raise ValueError("wavelength must be a one-dimensional sequence")
        n_values = None if n is None else numpy.asarray(n, dtype=float)
        k_values = None if k is None else numpy.asarray(k, dtype=float)
        for label, values in (("n", n_values), ("k", k_values)):
            if values is not None and (values.ndim != 1 or values.shape != wavelength_um.shape):
                raise ValueError(f"{label} must be one-dimensional and match wavelength")
        if n_values is not None and k_values is not None:
            kind = "nk"
            rows = tuple((float(real), float(imag)) for real, imag in zip(n_values, k_values))
        else:
            kind = "n" if n_values is not None else "k"
            component = n_values if n_values is not None else k_values
            rows = tuple((float(value),) for value in component)
        document = MaterialDocument(
            (TabulatedDataset(kind, tuple(float(value) for value in wavelength_um), rows),),
            MaterialMetadata(reference, dict(conditions or {}), comments),
        )
        material = cls.__new__(cls)
        material.filename, material.file_path, material.interpolation = name, None, interpolation
        if interpolation not in {"linear", "pchip"}:
            raise ValueError("interpolation must be 'linear' or 'pchip'.")
        material.wavelength_bound = material.wavelength = None
        material.n_values = material.k_values = None
        material._n_wavelength = material._k_wavelength = None
        material._apply_document(document)
        return material

    @classmethod
    def from_csv(
        cls, path, *, name=None, wavelength_unit=ureg.micrometer,
        wavelength_column="wavelength", n_column="n", k_column="k", **kwargs,
    ):
        """Construct a material from a header-based CSV file."""
        path = Path(path)
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        if not rows or wavelength_column not in rows[0]:
            raise ValueError(f"CSV must contain a '{wavelength_column}' column")
        wavelength = numpy.asarray([float(row[wavelength_column]) for row in rows]) * wavelength_unit
        n = [float(row[n_column]) for row in rows] if n_column in rows[0] and rows[0][n_column] != "" else None
        k = [float(row[k_column]) for row in rows] if k_column in rows[0] and rows[0][k_column] != "" else None
        return cls.from_arrays(name or path.stem, wavelength, n=n, k=k, **kwargs)

    def to_yaml(self, path):
        """Export this material as a validated, reloadable YAML document."""
        return self._document.to_yaml(path)

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
