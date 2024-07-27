#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Union, Iterable, NoReturn
from MPSTools.material_catalogue.loader import get_material_index
import matplotlib.pyplot as plt
from MPSTools.tools.directories import measurements_file_path
from pydantic.dataclasses import dataclass


def valid_name(string: str) -> bool:
    """Check if the provided string is a valid material name."""
    return not string.startswith('_')


# List of available materials
list_of_available_files = os.listdir(measurements_file_path)
material_list = [element[:-5] for element in list_of_available_files]
material_list = list(filter(valid_name, material_list))


@dataclass
class DataMeasurement:
    """
    A class for computing the refractive index using locally saved measurement data for specified materials.

    Attributes:
        material_name (str): The name of the material.

    Methods:
        reference: Returns the bibliographic reference for the material's data.
        get_refractive_index: Computes the refractive index for given wavelength(s).
        plot: Visualizes the refractive index as a function of wavelength.
    """
    material_name: str

    def __post_init__(self):
        """
        Initializes the DataMeasurement object with a specified material name.

        Raises:
            ValueError: If the material_name is not in the list of available materials.
        """
        if self.material_name not in material_list:
            raise ValueError(f"{self.material_name} is not in the list of available materials.")

    @property
    def reference(self) -> str:
        """
        Retrieves the bibliographic reference for the material's data.

        Returns:
            str: The bibliographic reference for the material's measurement data.

        Raises:
            NotImplementedError: If the feature is not implemented yet.
        """
        raise NotImplementedError("Feature not implemented yet.")

    def get_refractive_index(self, wavelength_range: Union[float, Iterable[float]]) -> Union[float, Iterable[float]]:
        """
        Computes the refractive index for the specified wavelength range using the material's measurement data.

        Parameters:
            wavelength_range (Union[float, Iterable[float]]): The wavelength(s) in meters.

        Returns:
            Union[float, Iterable[float]]: The refractive index or indices for the specified wavelength(s).
        """
        return get_material_index(
            material_name=self.material_name,
            wavelength=wavelength_range,
            subdir='measurements'
        )

    def plot(self, wavelength_range: Iterable[float]) -> NoReturn:
        """
        Generates a plot of the refractive index as a function of wavelength for the specified material.

        Parameters:
            wavelength_range (Iterable[float]): The range of wavelengths to plot.
        """
        figure, ax = plt.subplots(1, 1)
        ax.set_xlabel('Wavelength [m]')
        ax.set_ylabel('Refractive index')

        refractive_index = self.get_refractive_index(wavelength_range)
        ax.plot(wavelength_range, refractive_index.real, linewidth=2, label='real part')
        ax.plot(wavelength_range, refractive_index.imag, linewidth=2, label='imag part')

        plt.show()

    def __repr__(self) -> str:
        """
        Provides a formal string representation of the DataMeasurement object.

        Returns:
            str: Formal representation of the object, showing the material name.
        """
        return f"DataMeasurement(material_name='{self.material_name}')"

    def __str__(self) -> str:
        """
        Provides an informal string representation of the DataMeasurement object.

        Returns:
            str: Informal representation of the object.
        """
        return self.material_name
