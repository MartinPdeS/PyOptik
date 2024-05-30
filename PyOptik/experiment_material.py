#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Union, Iterable
from MPSTools.material_catalogue.loader import get_material_index
from MPSPlots.render2D import SceneList

from MPSTools.tools.directories import measurements_file_path
from pydantic.dataclasses import dataclass


def valid_name(string):
    return not string.startswith('_')


list_of_available_files = os.listdir(measurements_file_path)

material_list = [element[:-5] for element in list_of_available_files]

material_list = list(filter(valid_name, material_list))


@dataclass
class DataMeasurement():
    """
    A class for computing the refractive index using locally saved measurement data for specified materials.

    Attributes:
        material_name (str): The name of the material.

    Methods:
        reference (str): Returns the bibliographic reference for the material's data.
        get_refractive_index: Computes the refractive index for given wavelength(s).
        plot: Visualizes the refractive index as a function of wavelength.
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
        Retrieves the bibliographic reference for the material's data.

        Returns:
            str: The bibliographic reference for the material's measurement data.
        """
        raise NotImplementedError("Feature not implemented yet.")

    def get_refractive_index(self, wavelength_range: Union[float, Iterable]) -> Union[float, Iterable]:
        """
        Computes the refractive index for the specified wavelength range using the material's measurement data.

        Parameters:
            wavelength_range (Union[float, Iterable]): The wavelength(s) in meters.

        Returns:
            Union[float, Iterable]: The refractive index or indices for the specified wavelength(s).
        """
        return get_material_index(
            material_name=self.material_name,
            wavelength=wavelength_range,
            subdir='measurements'
        )

    def plot(self, wavelength_range: Iterable) -> SceneList:
        """
        Generates a plot of the refractive index as a function of wavelength for the specified material.

        Parameters:
            wavelength_range (Iterable): The range of wavelengths to plot.

        Returns:
            SceneList: An object containing the plot of refractive index against wavelength.
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
