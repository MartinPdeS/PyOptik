#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from typing import Optional, Union
import yaml
from PyOptik.directories import tabulated_data_path
from PyOptik.material.base_class import BaseMaterial
from MPSPlots.styles import mps
import matplotlib.pyplot as plt
from PyOptik.units import Quantity, micrometer, meter



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

    def __init__(self, filename: str):
        """
        Initializes the TabulatedMaterial with a filename.

        Parameters
        ----------
        filename : str
            The name of the YAML file containing material properties.
        """
        self.filename = filename

        # Initialize attributes
        self.wavelength_bound = None
        self.wavelength = None
        self.n_values = None
        self.k_values = None
        self.reference = None

        # Load tabulated data from the YAML file
        self._load_tabulated_data()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.filename

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
        file_path = tabulated_data_path / f'{self.filename}'

        if not file_path.with_suffix('.yml').exists():
            raise FileNotFoundError(f"YAML file {file_path} not found.")

        with file_path.with_suffix('.yml').open('r') as file:
            print(file)
            parsed_yaml = yaml.safe_load(file)

        try:
            # Extract data points
            data_points = parsed_yaml['DATA'][0]['data'].strip().split('\n')
            data = numpy.array([[float(value) for value in point.split()] for point in data_points])

            self.wavelength = data[:, 0] * micrometer
            self.n_values = data[:, 1]
            self.k_values = data[:, 2]
        except (KeyError, IndexError, ValueError):
            raise ValueError(f"Invalid or missing data in YAML file {file_path}")

        self.wavelength_bound = [self.wavelength.min().magnitude, self.wavelength.max().magnitude] * micrometer

        # Extract reference
        self.reference = parsed_yaml.get('REFERENCES', None)

    @BaseMaterial.ensure_units
    def compute_refractive_index(self, wavelength: Union[float, Quantity]) -> numpy.ndarray:
        """
        Interpolates the refractive index (n) and absorption (k) values for the given wavelength(s).

        Parameters
        ----------
        wavelength : Union[float, Quantity]
            Wavelength(s) in micrometers for which to interpolate n and k.

        Returns
        -------
        numpy.ndarray
            Complex refractive index values (n + i*k) for the given wavelength(s).

        Raises
        ------
        ValueError
            If the wavelength is outside the tabulated range.
        """
        return_as_scalar = numpy.isscalar(wavelength.magnitude)

        wavelength = numpy.atleast_1d(wavelength)

        self._check_wavelength(wavelength)

        n_interp = numpy.interp(wavelength.to(meter).magnitude, self.wavelength.to(meter).magnitude, self.n_values)
        k_interp = numpy.interp(wavelength.to(meter).magnitude, self.wavelength.to(meter).magnitude, self.k_values)

        index = n_interp + 1j * k_interp

        return index[0] if return_as_scalar else index

    @BaseMaterial.ensure_units
    def plot(self, wavelength: Optional[Quantity] = None) -> None:
        """
        Plots the tabulated refractive index (n) and absorption (k) as a function of wavelength.

        Parameters
        ----------
        wavelength : Optional[Quantity]
            The range of wavelengths to plot, in micrometers. If not provided, the entire tabulated wavelength range is used.

        Raises
        ------
        ValueError
            If the wavelength is not a 1D array or list of float values.
        """
        n_values, k_values = self.compute_refractive_index(wavelength).real, self.compute_refractive_index(wavelength).imag

        with plt.style.context(mps):
            _, ax1 = plt.subplots()

        ax1.set(
            title=f"Refractive Index and Absorption vs. Wavelength [{self.filename}]",
            xlabel='Wavelength [µm]',
            ylabel='Refractive Index (n)',
        )

        ax1.plot(wavelength.to(micrometer).magnitude, n_values, 'o-', color='tab:blue', label='n')

        ax2 = ax1.twinx()

        ax2.set(
            xlabel='Wavelength [µm]',
            ylabel='Absorption (k)',
        )

        ax2.plot(wavelength.to(micrometer).magnitude, k_values, 'o-', color='tab:red', label='k')

        plt.show()

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
