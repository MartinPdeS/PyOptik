#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import numpy
from typing import Tuple, Optional, Union, NoReturn, List
import yaml
from PyOptik.directories import sellmeier_data_path
import itertools
import warnings
from PyOptik.base_class import Material


@dataclass
class SellmeierMaterial(Material):
    filename: str
    coefficients: numpy.ndarray = field(init=False)
    wavelength_range: Optional[Tuple[float, float]] = field(init=False)
    reference: Optional[str] = field(init=False)
    formula_type: int = field(init=False)

    def __post_init__(self) -> None:
        """
        Post-initialization method to load coefficients, wavelength range, formula type, and reference from a YAML file.
        """
        self.load_coefficients()

    def load_coefficients(self) -> None:
        """
        Loads the Sellmeier coefficients, wavelength range, formula type, and reference from the specified YAML file.
        """
        file_path = sellmeier_data_path / f'{self.filename}.yml'

        with open(file_path, 'r') as file:
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
            self.wavelength_range = tuple(map(float, parsed_yaml['DATA'][0]['wavelength_range'].split()))
        else:
            self.wavelength_range = None

        # Extract reference
        self.reference = parsed_yaml.get('REFERENCES', None)

    def check_wavelength_range(self, wavelength: float) -> None:
        """
        Checks if a wavelength is within the material's allowable range and raises an error if it is not.

        Args:
            wavelength (float): The wavelength to check in meters.

        Raises:
            ValueError: If the wavelength is outside the allowable range.
        """
        if self.wavelength_range is not None:
            wavelength_um = wavelength * 1e6
            min_value, max_value = self.wavelength_range
            if not min_value <= wavelength_um <= max_value:
                warnings.warn(f"Wavelength {wavelength_um} µm is outside the allowable range of {min_value} µm to {max_value} µm. [{self.filename}]")

    def compute_refractive_index(self, wavelength: Union[float, numpy.ndarray]) -> Union[float, numpy.ndarray]:
        """
        Computes the refractive index n(λ) using the appropriate formula (either Formula 1 or Formula 2).

        Args:
            wavelength (Union[float, numpy.ndarray]): The wavelength λ in meters, can be a single float or a numpy array.

        Returns:
            Union[float, numpy.ndarray]: The refractive index n(λ) for the given wavelength or array of wavelengths.

        Raises:
            ValueError: If the wavelength is outside the specified range or if an unsupported formula type is encountered.
        """
        # Ensure that wavelength is within the allowable range if it's a single value
        if isinstance(wavelength, float):
            self.check_wavelength_range(wavelength)
        else:  # If it's an array, ensure all values are within range
            for wl in numpy.nditer(wavelength):
                self.check_wavelength_range(float(wl))

        # Convert wavelength to micrometers
        lambda_um = wavelength * 1e6

        # Compute the refractive index based on the formula type
        match self.formula_type:
            case 1:  # Formula 1 computation (standard Sellmeier)
                n_squared = self.coefficients[0]
                for (B, C) in itertools.zip_longest(*[iter(self.coefficients[1:])] * 2):
                    n_squared += (B * lambda_um**2) / (lambda_um**2 - C**2)

                n = numpy.sqrt(n_squared)

            case 2:  # Formula 2 computation (extended Sellmeier)
                n_squared = 1 + self.coefficients[0]

                for (B, C) in itertools.zip_longest(*[iter(self.coefficients[1:])] * 2):
                    n_squared += (B * lambda_um**2) / (lambda_um**2 - C)

                n = numpy.sqrt(n_squared)

            case 5:  # Formula 5 computation (extended Sellmeier)
                n = 1 + self.coefficients[0]

                for (B, C) in itertools.zip_longest(*[iter(self.coefficients[1:])] * 2):
                    n = B * lambda_um**(C)

            case 6:
                n = 1 + self.coefficients[0]

                for (B, C) in itertools.zip_longest(*[iter(self.coefficients[1:])] * 2):
                    n = B / (C - lambda_um**-2)

            case _ :
                raise ValueError(f"Unsupported formula type: {self.formula_type}")

        return n


    def plot(self, wavelength_range: Union[List[float], numpy.ndarray]) -> NoReturn:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Args:
            wavelength_range (Union[List[float], numpy.ndarray]): The range of wavelengths to plot, in meters.
        """
        if isinstance(wavelength_range, list):
            wavelength_range = numpy.array(wavelength_range)

        if wavelength_range.ndim != 1:
            raise ValueError("wavelength_range must be a 1D array or list of float values.")

        # Calculate the refractive index over the wavelength range
        refractive_index = self.compute_refractive_index(wavelength_range)

        # Plotting
        fig, ax = plt.subplots()
        ax.set_xlabel('Wavelength [m]')
        ax.set_ylabel('Refractive Index')
        ax.plot(wavelength_range, refractive_index.real, linewidth=2, label='Real Part')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        plt.show()

    def print(self) -> str:
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns:
            str: Formal representation of the Material object.
        """
        return (
            f"\nMaterial: '{self.filename}',\n"
            f"coefficients: {self.coefficients},\n"
            f"wavelength_range: {self.wavelength_range},\n"
            f"formula_type: {self.formula_type},\n"
            f"reference: '{self.reference}')"
        )

