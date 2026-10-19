"""
Plot the Refractive Index of Optical Material: Silica
=====================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material Silica glass over a specified range of wavelengths.

"""

# %%
from TypedUnit import ureg
from PyOptik import MaterialCatalog

# Initialize the material with the Sellmeier model
catalog = MaterialCatalog.from_snapshot()
material = catalog.get("main/SiO2/Malitson").load()

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[1310, 1550] * ureg.nanometer)

# Display calculated refractive indices at sample wavelengths
material.plot()
