#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from typing import Union, Iterable
from MPSTools.material_catalogue.loader import get_material_index
from MPSPlots.render2D import SceneList
from MPSTools.tools.directories import sellmeier_file_path
from pydantic.dataclasses import dataclass


def valid_name(string):
    return not string.startswith('_')


list_of_available_files = os.listdir(sellmeier_file_path)

material_list = [element[:-5] for element in list_of_available_files]

material_list = list(filter(valid_name, material_list))


@dataclass
class Sellmeier():
    """
    A class for computing the refractive index using the Sellmeier equation based on locally stored Sellmeier coefficients.

    Attributes:
        material_name (str): Name of the material.
        sellmeier_coefficients (dict): Sellmeier coefficients for the material loaded from a local source.

    Methods:
        reference: Returns the reference for the Sellmeier coefficients.
        get_refractive_index: Computes the refractive index for given wavelengths.
        plot: Plots the refractive index as a function of the wavelength.
    """
    material_name: str

    def __post_init__(self):
        """
        Initializes the DataMeasurement object with a specified material name.

        Parameters:
            material_name (str): The name of the material for which to compute the refractive index.
        """
        if self.material_name not in material_list:
            raise ValueError(f"{self.material_name} is not in the list of available materials.")

    @property
    def reference(self) -> str:
        """
        Returns the bibliographic reference for the Sellmeier coefficients.

        Returns:
            str: The bibliographic reference.
        """
        return self.sellmeier_coefficients['sellmeier']['reference']

    def get_refractive_index(self, wavelength_range: Union[float, Iterable]) -> Union[float, np.ndarray]:
        """
        Computes the refractive index for the specified wavelength(s) using the Sellmeier equation.

        Parameters:
            wavelength_range (Union[float, Iterable]): The wavelength(s) in meters for which to compute the refractive index.

        Returns:
            Union[float, np.ndarray]: The computed refractive index, either as a scalar or a NumPy array.
        """
        return_scalar = np.isscalar(wavelength_range)
        wavelength_array = np.atleast_1d(wavelength_range).astype(float)

        refractive_index = get_material_index(
            material_name=self.material_name,
            wavelength=wavelength_array,
            subdir='sellmeier'
        )

        return refractive_index.item() if return_scalar else refractive_index

    def plot(self, wavelength_range: Iterable) -> SceneList:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Parameters:
            wavelength_range (Iterable): The range of wavelengths to plot, in meters.

        Returns:
            SceneList: A SceneList object containing the plot.
        """
        scene = SceneList()
        ax = scene.append_ax(x_label='Wavelength [m]', y_label='Refractive index')

        refractive_index = self.get_refractive_index(wavelength_range)

        ax.add_line(x=wavelength_range, y=refractive_index, line_width=2)

        return scene

    def __repr__(self) -> str:
        """
        Provides a formal string representation of the DataMeasurement object.

        Returns:
            str: Formal representation of the object, showing the material name.
        """
        return str(self.material_name)

    def __str__(self) -> str:
        """
        Provides an informal string representation of the DataMeasurement object.

        Returns:
            str: Informal representation of the object.
        """
        return self.__repr__()

# -
