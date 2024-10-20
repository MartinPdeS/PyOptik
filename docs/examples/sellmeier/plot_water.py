"""
Plot the Refractive Index of Optical Material: Water
=====================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material water over a specified range of wavelengths.

"""

# %%
import numpy
from PyOptik import MaterialBank

# Initialize the material with the Sellmeier model
material = MaterialBank.water

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[800e-9, 900e-9])

# Display calculated refractive indices at sample wavelengths
material.plot(
    wavelength=numpy.linspace(300e-9, 1000e-9, 300)
)
