#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union, List
import yaml
from scipy.interpolate import interp1d
import warnings
from PyOptik.directories import tabulated_data_path
from PyOptik.base_class import BaseMaterial
from MPSPlots.styles import mps
import matplotlib.pyplot as plt

@dataclass
class TabulatedMaterial(BaseMaterial):
    filename: str
    wavelength: numpy.ndarray = field(init=False)
    n_values: numpy.ndarray = field(init=False)
    k_values: numpy.ndarray = field(init=False)
    reference: Optional[str] = field(init=False)

    def __post_init__(self) -> None:
        """
        Post-initialization method to load the tabulated data from the YAML file.
        """
        self.load_tabulated_data()

    def load_tabulated_data(self) -> None:
        """
        Loads the tabulated refractive index and absorption values from the specified YAML file.
        """
        file_path = tabulated_data_path / f'{self.filename}'

        with open(file_path.with_suffix('.yml'), 'r') as file:
            parsed_yaml = yaml.safe_load(file)

        # Extract data points
        data_points = parsed_yaml['DATA'][0]['data'].strip().split('\n')
        data = numpy.array([[float(value) for value in point.split()] for point in data_points])

        self.wavelength = data[:, 0]
        self.n_values = data[:, 1]
        self.k_values = data[:, 2]

        # Extract reference
        self.reference = parsed_yaml.get('REFERENCES', None)

    def compute_refractive_index(self, wavelength: Union[float, numpy.ndarray]) -> Tuple[numpy.ndarray, numpy.ndarray]:
        """
        Interpolates the refractive index (n) and absorption (k) values for the given wavelength(s).

        Args:
            wavelength (Union[float, numpy.ndarray]): Wavelength(s) in micrometers for which to interpolate n and k.

        Returns:
            Tuple[numpy.ndarray, numpy.ndarray]: Interpolated refractive index (n) and absorption (k) values.

        Raises:
            ValueError: If the wavelength is outside the tabulated range.
        """
        wavelength = numpy.asarray(wavelength)

        wavelength_um = wavelength * 1e6

        if numpy.any(wavelength_um < self.wavelength.min()) or numpy.any(wavelength > self.wavelength.max()):
            warnings.warn(f"Wavelength: {wavelength} is outside the tabulated range of {self.wavelength.min()} µm to {self.wavelength.max()} µm. [{self.filename}]")

        n_interp = interp1d(self.wavelength, self.n_values, kind='cubic', fill_value='extrapolate')
        k_interp = interp1d(self.wavelength, self.k_values, kind='cubic', fill_value='extrapolate')

        return n_interp(wavelength_um) + 1j * k_interp(wavelength_um)

    def plot(self, wavelength: Optional[List[float]] = None) -> None:
        """
        Plots the tabulated refractive index (n) and absorption (k) as a function of wavelength.
        """
        if wavelength is None:
            wavelength = self.wavelength
            index = self.compute_refractive_index(wavelength=self.wavelength)
            n_values = index.real
            k_values = index.imag
        else:
            wavelength = self.wavelength
            n_values = self.n_values
            k_values = self.k_values

        with plt.style.context(mps):
            fig, ax1 = plt.subplots()

            ax1.set_xlabel('Wavelength [µm]')
            ax1.set_ylabel('Refractive Index (n)', color='tab:blue')
            ax1.plot(wavelength, n_values, 'o-', color='tab:blue', label='n')
            ax1.tick_params(axis='y', labelcolor='tab:blue')

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            ax2.set_ylabel('Absorption (k)', color='tab:red')  # we already handled the x-label with ax1
            ax2.plot(wavelength, k_values, 'o-', color='tab:red', label='k')
            ax2.tick_params(axis='y', labelcolor='tab:red')

            fig.tight_layout()  # to prevent the right y-label from being slightly clipped
            plt.show()

    def print(self) -> str:
        """
        Provides a formal string representation of the TabulatedMaterial object, including key attributes.

        Returns:
            str: Formal representation of the TabulatedMaterial object.
        """
        return (
            f"\nTabulatedMaterial: '{self.filename}',\n"
            f"wavelength_range: [{self.wavelength.min()} µm, {self.wavelength.max()} µm],\n"
            f"reference: '{self.reference}')"
        )