#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import numpy
import itertools
import logging
from MPSPlots import helper
from TypedUnit import Length, RefractiveIndex, validate_units, ureg

from PyOptik.directories import material_paths
from PyOptik.material_type import MaterialType
from PyOptik.material.base_class import BaseMaterial

logger = logging.getLogger(__name__)


class SellmeierMaterial(BaseMaterial):
    """
    Class representing a material with Sellmeier coefficients for refractive index computation.

    Attributes
    ----------
    filename : str
        The name of the YAML file containing material properties.
    coefficients : numpy.ndarray
        The Sellmeier coefficients used for calculating the refractive index.
    wavelength_range : Optional[Tuple[float, float]]
        The allowable wavelength range for the material in micrometers.
    reference : Optional[str]
        Reference information for the material data.
    formula_type : int
        The formula type to use for refractive index calculation.
    """
    def __init__(self, filename: str, file_path=None):
        """
        Initializes the SellmeierMaterial with a filename.

        Parameters
        ----------

        filename : str
            The name of the YAML file containing material properties.
        file_path : pathlib.Path, optional
            Explicit YAML path for hierarchy-preserving catalog pages. When
            omitted, the user material directory is searched.
        """
        self.filename = filename
        self.file_path = file_path

        self.coefficients = None
        self.wavelength_bound = None
        self.reference = None
        self.formula_type = None

        self._load_coefficients()

    def __str__(self) -> str:
        """Return the material name and ``Sellmeier`` model type."""
        return self.filename + '[Sellmeier]'

    def _load_coefficients(self) -> None:
        """
        Loads the Sellmeier coefficients, wavelength range, formula type, and reference from the specified YAML file.
        """
        file_path = self.file_path or next(
            (directory / f"{self.filename}.yml"
             for directory in material_paths(MaterialType.SELLMEIER)
             if (directory / f"{self.filename}.yml").exists()),
            None,
        )
        if file_path is None:
            raise FileNotFoundError(f"Sellmeier YAML file '{self.filename}.yml' not found.")

        with file_path.with_suffix('.yml').open('r') as file:
            parsed_yaml = yaml.safe_load(file)
        logger.debug("Loaded Sellmeier data from %s", file_path)

        # Extract the formula type
        try:
            data = parsed_yaml["DATA"][0]
            self.formula_type = int(data["type"].split()[-1])
            coefficients = list(map(float, data["coefficients"].split()))
        except (KeyError, IndexError, AttributeError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid Sellmeier data in YAML file {file_path}") from error
        if self.formula_type not in {1, 2, 5, 6}:
            raise ValueError(f"Unsupported formula type: {self.formula_type}")
        if not coefficients or not numpy.all(numpy.isfinite(coefficients)):
            raise ValueError(f"Sellmeier coefficients must be finite in {file_path}")

        # Extract coefficients and ensure the list has exactly 7 coefficients by padding with zeros if necessary
        if len(coefficients) < 7:
            coefficients.extend([0.0] * (7 - len(coefficients)))
        self.coefficients = numpy.array(coefficients)

        # Extract wavelength range
        if 'wavelength_range' in parsed_yaml['DATA'][0]:
            data_str = data['wavelength_range'].split()

            bounds = numpy.array([float(val) for val in data_str])
            if len(bounds) != 2 or not numpy.all(numpy.isfinite(bounds)) or bounds[0] >= bounds[1]:
                raise ValueError(f"Invalid wavelength_range in {file_path}")
            self.wavelength_bound = bounds * ureg.micrometer

        else:
            self.wavelength_bound = None

        # # Extract reference
        self.reference = parsed_yaml.get('REFERENCES', None)
        logger.debug("Validated Sellmeier material '%s' with formula %s", self.filename, self.formula_type)

    @validate_units
    def compute_refractive_index(self, wavelength: Length | float, out_of_range: str = "warn") -> RefractiveIndex:
        r"""
        Computes the refractive index n(\u03bb) using the appropriate formula (either Formula 1, 2, 5, or 6).

        Parameters
        ----------
        wavelength : Length | float
            The wavelength \u03bb in meters, can be a single float or a numpy array.
        out_of_range : {"warn", "raise", "clip"}, optional
            Policy for wavelengths outside the source validity range.

        Returns
        -------
        RefractiveIndex
            The refractive index n(\u03bb) for the given wavelength or array of wavelengths.

        Raises
        ------
        ValueError
            If the wavelength is outside the specified range or if an unsupported formula type is encountered.
        """
        if not isinstance(wavelength, Length):
            wavelength = wavelength * ureg.meter

        return_as_scalar = numpy.isscalar(wavelength.magnitude)

        wavelength = numpy.atleast_1d(wavelength)
        self._check_wavelength(wavelength, out_of_range)
        if out_of_range == "clip":
            wavelength = self._clip_wavelength(wavelength)

        # Compute the refractive index based on the formula type
        zipped_coefficients = itertools.zip_longest(*[iter(self.coefficients[1:])] * 2)

        match self.formula_type:
            case 1:  # Formula 1 computation (standard Sellmeier)
                n_squared = 1.0
                for (B, C) in zipped_coefficients:
                    n_squared += (B * wavelength.to(ureg.micrometer).magnitude**2) / (wavelength.to(ureg.micrometer).magnitude**2 - C**2)

                n = numpy.sqrt(n_squared)

            case 2:  # Formula 2 computation (extended Sellmeier)
                n_squared = 1 + self.coefficients[0]
                for (B, C) in zipped_coefficients:
                    n_squared += (B * wavelength.to(ureg.micrometer).magnitude**2) / (wavelength.to(ureg.micrometer).magnitude**2 - C)
                n = numpy.sqrt(n_squared)

            case 5:  # Formula 5 computation (extended Sellmeier)
                n = 1 + self.coefficients[0]
                for (B, C) in zipped_coefficients:
                    n += B * wavelength.to(ureg.micrometer).magnitude**C

            case 6:
                n = 1 + self.coefficients[0]
                for (B, C) in zipped_coefficients:
                    n = B / (C - wavelength.to(ureg.micrometer).magnitude**-2)

            case _:
                raise ValueError(f"Unsupported formula type: {self.formula_type}")

        return n[0] if return_as_scalar else n

    @helper.pre_plot(nrows=1, ncols=1)
    def plot(self, axes, samples: int = 100) -> None:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            Axes on which to draw the dispersion curve.
        samples : int
            The number of samples to use for the wavelength range.

        Returns
        -------
        None
            The supplied axes are modified in place.

        Raises
        ------
        ValueError
            If the wavelength is not a 1D array or list of float values.
        """
        wavelength = numpy.linspace(
            self.wavelength_bound[0].magnitude,
            self.wavelength_bound[1].magnitude,
            samples
        ) * self.wavelength_bound.units

        # Calculate the refractive index over the wavelength range
        refractive_index = self.compute_refractive_index(wavelength)

        axes.set(
            ylabel='Refractive Index',
            xlabel=r'Wavelength [$\mu$m]',
            title=f"Refractive Index vs. Wavelength: [{self.filename}]"
        )
        axes.plot(wavelength.to(ureg.micrometer).magnitude, refractive_index.real, linewidth=2, label='Real Part')
        axes.legend()

    def print(self) -> str:
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns
        -------
        str
            Formal representation of the Material object.
        """
        return (
            f"\nMaterial: '{self.filename}',\n"
            f"coefficients: {self.coefficients},\n"
            f"wavelength_range: {self.wavelength_bound},\n"
            f"formula_type: {self.formula_type},\n"
            f"reference: '{self.reference}')"
        )
