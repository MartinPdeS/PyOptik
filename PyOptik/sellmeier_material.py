import numpy as np
from typing import Union, Iterable
from MPSTools.material_catalogue.loader import get_material_index
from MPSPlots.render2D import SceneList
from MPSTools.material_catalogue.material_files.sellmeier import __list__ as material_list


class Sellmeier:
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

    def __init__(self, material_name: str) -> None:
        """
        Initializes the Sellmeier object with material parameters loaded from a local source.

        Parameters:
            material_name (str): The name of the material.
        """
        self.material_name = material_name

    @property
    def reference(self) -> str:
        """
        Returns the bibliographic reference for the Sellmeier coefficients.

        Returns:
            str: The bibliographic reference.
        """
        return self.sellmeier_coefficients['sellmeier']['reference']

    def get_refractive_index(self, wavelength: Union[float, Iterable]) -> Union[float, np.ndarray]:
        """
        Computes the refractive index for the specified wavelength(s) using the Sellmeier equation.

        Parameters:
            wavelength (Union[float, Iterable]): The wavelength(s) in meters for which to compute the refractive index.

        Returns:
            Union[float, np.ndarray]: The computed refractive index, either as a scalar or a NumPy array.
        """
        return_scalar = np.isscalar(wavelength)
        wavelength_array = np.atleast_1d(wavelength).astype(float)

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
        """Represents the Sellmeier object as the material name."""
        return f"Sellmeier(material_name={self.material_name})"

    def __str__(self) -> str:
        """Returns a string representation of the Sellmeier object."""
        return self.__repr__()
