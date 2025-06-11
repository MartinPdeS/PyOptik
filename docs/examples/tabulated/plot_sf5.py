"""
Plot the Refractive Index of Optical Material: SF5
==================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material SF5 glass over a specified range of wavelengths.

"""

# %%
import numpy
from PyOptik import MaterialBank

# Initialize the material with the Sellmeier model
material = MaterialBank.polyetylene

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[1310e-9, 1550e-9])

# Display calculated refractive indices at sample wavelengths
material.plot(
    wavelength=numpy.linspace(400e-9, 1500e-9, 300)
)
