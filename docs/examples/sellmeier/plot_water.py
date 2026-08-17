"""
Plot the Refractive Index of Optical Material: Water
=====================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material water over a specified range of wavelengths.

"""

# %%
import numpy
from TypedUnit import ureg

from PyOptik import MaterialCatalog

# Initialize the material with the Sellmeier model
catalog = MaterialCatalog.from_snapshot()
material = catalog.get("main/H2O/Daimon-19.0C").load()

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[800, 900] * ureg.nanometer)

# Display calculated refractive indices at sample wavelengths
material.plot()
