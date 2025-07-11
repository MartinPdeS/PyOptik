#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import numpy
import itertools
from MPSPlots.styles import mps
import matplotlib.pyplot as plt
from typing import Optional, Union
from PyOptik.units import micrometer, Quantity
from PyOptik.directories import sellmeier_data_path
from PyOptik.material.base_class import BaseMaterial


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
    def __init__(self, filename: str):
        """
        Initializes the SellmeierMaterial with a filename.

        Parameters
        ----------

        filename : str
            The name of the YAML file containing material properties.
        """
        self.filename = filename

        self.coefficients = None
        self.wavelength_bound = None
        self.reference = None
        self.formula_type = None

        self._load_coefficients()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.filename

    def _load_coefficients(self) -> None:
        """
        Loads the Sellmeier coefficients, wavelength range, formula type, and reference from the specified YAML file.
        """
        file_path = sellmeier_data_path / f'{self.filename}'

        if not file_path.with_suffix('.yml').exists():
            raise FileNotFoundError(f"YAML file {file_path} not found.")

        with file_path.with_suffix('.yml').open('r') as file:
            parsed_yaml = yaml.safe_load(file)

        # Extract the formula type
        self.formula_type = int(parsed_yaml['DATA'][0]['type'].split()[-1])

        # Extract coefficients and ensure the list has exactly 7 coefficients by padding with zeros if necessary
        coefficients_str = parsed_yaml['DATA'][0]['coefficients']
        coefficients = list(map(float, coefficients_str.split()))
        if len(coefficients) < 7:
            coefficients.extend([0.0] * (7 - len(coefficients)))
        self.coefficients = numpy.array(coefficients)

        # Extract wavelength range
        if 'wavelength_range' in parsed_yaml['DATA'][0]:
            data_str = parsed_yaml['DATA'][0]['wavelength_range'].split()

            self.wavelength_bound = numpy.array([float(val) for val in data_str]) * micrometer

        else:
            self.wavelength_bound = None

        # # Extract reference
        self.reference = parsed_yaml.get('REFERENCES', None)

    @BaseMaterial.ensure_units
    def compute_refractive_index(self, wavelength: Union[Quantity]) -> Union[float, numpy.ndarray]:
        r"""
        Computes the refractive index n(\u03bb) using the appropriate formula (either Formula 1, 2, 5, or 6).

        Parameters
        ----------
        wavelength : Union[Quantity]
            The wavelength \u03bb in meters, can be a single float or a numpy array.

        Returns
        -------
        Union[Quantity]
            The refractive index n(\u03bb) for the given wavelength or array of wavelengths.

        Raises
        ------
        ValueError
            If the wavelength is outside the specified range or if an unsupported formula type is encountered.
        """
        return_as_scalar = numpy.isscalar(wavelength.magnitude)

        wavelength = numpy.atleast_1d(wavelength)
        self._check_wavelength(wavelength)

        # Compute the refractive index based on the formula type
        zipped_coefficients = itertools.zip_longest(*[iter(self.coefficients[1:])] * 2)

        match self.formula_type:
            case 1:  # Formula 1 computation (standard Sellmeier)
                n_squared = 1.0
                for (B, C) in zipped_coefficients:
                    n_squared += (B * wavelength.to(micrometer).magnitude**2) / (wavelength.to(micrometer).magnitude**2 - C**2)

                n = numpy.sqrt(n_squared)

            case 2:  # Formula 2 computation (extended Sellmeier)
                n_squared = 1 + self.coefficients[0]
                for (B, C) in zipped_coefficients:
                    n_squared += (B * wavelength.to(micrometer).magnitude**2) / (wavelength.to(micrometer).magnitude**2 - C)
                n = numpy.sqrt(n_squared)

            case 5:  # Formula 5 computation (extended Sellmeier)
                n = 1 + self.coefficients[0]
                for (B, C) in zipped_coefficients:
                    n += B * wavelength.to(micrometer).magnitude**C

            case 6:
                n = 1 + self.coefficients[0]
                for (B, C) in zipped_coefficients:
                    n = B / (C - wavelength.to(micrometer).magnitude**-2)

            case _:
                raise ValueError(f"Unsupported formula type: {self.formula_type}")

        return n[0] if return_as_scalar else n

    @BaseMaterial.ensure_units
    def plot(self, wavelength: Optional[Quantity] = None) -> None:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Parameters
        ----------
        wavelength : Optional[Quantity]
            The range of wavelengths to plot, in meters. If not provided, the entire allowable wavelength range is used.

        Raises
        ------
        ValueError
            If the wavelength is not a 1D array or list of float values.
        """
        if wavelength.ndim != 1:
            raise ValueError("wavelength must be a 1D array or list of float values.")

        # Calculate the refractive index over the wavelength range
        refractive_index = self.compute_refractive_index(wavelength)

        with plt.style.context(mps):
            fig, ax = plt.subplots()

        ax.set(
            ylabel='Refractive Index',
            xlabel=r'Wavelength [$\mu$m]',
            title=f"Refractive Index vs. Wavelength: [{self.filename}]"
        )
        ax.plot(wavelength.to(micrometer).magnitude, refractive_index.real, linewidth=2, label='Real Part')
        ax.legend()

        plt.show()

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
