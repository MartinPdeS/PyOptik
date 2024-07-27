"""
Plot the Refractive Index of Optical Material: Ti02
===================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material SF5 over a specified range of wavelengths.

"""

import numpy
from PyOptik import DataMeasurement

# Initialize the material with the Sellmeier model
material = DataMeasurement('tio2')

# Calculate refractive index at specific wavelengths
RI = material.get_refractive_index(wavelength_range=[1310e-9, 1550e-9])

# Display calculated refractive indices at sample wavelengths
figure = material.plot(
    wavelength_range=numpy.linspace(10e-9, 3500e-9, 300)
)

figure.show()
