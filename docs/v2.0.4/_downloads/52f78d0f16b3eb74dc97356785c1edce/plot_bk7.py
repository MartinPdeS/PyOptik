"""
Plot the Refractive Index of Optical Material: BK7
=====================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material BK7 glass over a specified range of wavelengths.

"""

# %%
from PyOptik import MaterialBank
from TypedUnit import ureg

# Initialize the material with the Sellmeier model
material = MaterialBank.BK7

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[5_000] * ureg.nanometer)

# Display calculated refractive indices at sample wavelengths
material.plot()
