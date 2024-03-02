#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Union, Iterable
from MPSTools.material_catalogue.loader import get_material_index
from MPSPlots.render2D import SceneList
from MPSTools.material_catalogue.material_files.measurements import __list__ as material_list


class DataMeasurement:
    """
    A class for computing the refractive index using locally saved measurement data for specified materials.

    Attributes:
        material_name (str): The name of the material.

    Methods:
        reference (str): Returns the bibliographic reference for the material's data.
        get_refractive_index: Computes the refractive index for given wavelength(s).
        plot: Visualizes the refractive index as a function of wavelength.
    """

    def __init__(self, material_name: str) -> None:
        """
        Initializes the DataMeasurement object with a specified material name.

        Parameters:
            material_name (str): The name of the material for which to compute the refractive index.
        """
        if material_name not in material_list:
            raise ValueError(f"{material_name} is not in the list of available materials.")
        self.material_name = material_name

    @property
    def reference(self) -> str:
        """
        Retrieves the bibliographic reference for the material's data.

        Returns:
            str: The bibliographic reference for the material's measurement data.
        """
        # Assuming there's a way to fetch the reference from the material's configuration
        # This part of the code would need to be implemented based on how references are stored
        return "Reference not implemented"  # Placeholder

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
        return f"DataMeasurement(material_name={self.material_name})"

    def __str__(self) -> str:
        """
        Provides an informal string representation of the DataMeasurement object.

        Returns:
            str: Informal representation of the object.
        """
        return self.__repr__()

