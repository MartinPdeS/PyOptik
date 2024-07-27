#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy
from typing import Union, Iterable, NoReturn
from MPSTools.material_catalogue.loader import get_material_index
import matplotlib.pyplot as plt
from MPSTools.tools.directories import sellmeier_file_path
from pydantic.dataclasses import dataclass


def valid_name(string: str) -> bool:
    """Check if the provided string is a valid material name."""
    return not string.startswith('_')


# List of available materials
list_of_available_files = os.listdir(sellmeier_file_path)
material_list = [element[:-5] for element in list_of_available_files]
material_list = list(filter(valid_name, material_list))


@dataclass
class Sellmeier:
    """
    A class for computing the refractive index using the Sellmeier equation based on locally stored Sellmeier coefficients.

    Attributes:
        material_name (str): Name of the material.

    Methods:
        reference: Returns the reference for the Sellmeier coefficients.
        get_refractive_index: Computes the refractive index for given wavelengths.
        plot: Plots the refractive index as a function of the wavelength.
    """
    material_name: str

    def __post_init__(self):
        """
        Initializes the Sellmeier object with a specified material name.

        Raises:
            ValueError: If the material_name is not in the list of available materials.
        """
        if self.material_name not in material_list:
            raise ValueError(f"{self.material_name} is not in the list of available materials.")
        self.sellmeier_coefficients = get_material_index(
            material_name=self.material_name,
            wavelength=numpy.array([1.0]),  # Dummy wavelength to load coefficients
            subdir='sellmeier'
        )

    @property
    def reference(self) -> str:
        """
        Returns the bibliographic reference for the Sellmeier coefficients.

        Returns:
            str: The bibliographic reference.
        """
        return self.sellmeier_coefficients['sellmeier']['reference']

    def get_refractive_index(self, wavelength_range: Union[float, Iterable]) -> Union[float, numpy.ndarray]:
        """
        Computes the refractive index for the specified wavelength(s) using the Sellmeier equation.

        Parameters:
            wavelength_range (Union[float, Iterable]): The wavelength(s) in meters for which to compute the refractive index.

        Returns:
            Union[float, numpy.ndarray]: The computed refractive index, either as a scalar or a NumPy array.
        """
        return_scalar = numpy.isscalar(wavelength_range)
        wavelength_array = numpy.atleast_1d(wavelength_range).astype(float)

        refractive_index = get_material_index(
            material_name=self.material_name,
            wavelength=wavelength_array,
            subdir='sellmeier'
        )

        return refractive_index.item() if return_scalar else refractive_index

    def plot(self, wavelength_range: Iterable) -> NoReturn:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Parameters:
            wavelength_range (Iterable): The range of wavelengths to plot, in meters.
        """
        figure, ax = plt.subplots(1, 1)
        ax.set_xlabel('Wavelength [m]')
        ax.set_ylabel('Refractive index')

        refractive_index = self.get_refractive_index(wavelength_range)
        ax.plot(wavelength_range, refractive_index, linewidth=2)
        plt.show()

    def __repr__(self) -> str:
        """
        Provides a formal string representation of the Sellmeier object.

        Returns:
            str: Formal representation of the object, showing the material name.
        """
        return f"Sellmeier(material_name='{self.material_name}')"

    def __str__(self) -> str:
        """
        Provides an informal string representation of the Sellmeier object.

        Returns:
            str: Informal representation of the object.
        """
        return self.material_name


Material = Sellmeier
