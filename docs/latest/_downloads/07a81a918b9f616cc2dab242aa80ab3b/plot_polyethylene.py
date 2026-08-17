"""
Plot the Refractive Index of Optical Material: Polyethylene
===========================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of polyethylene over a specified range of wavelengths.

"""

# %%
from TypedUnit import ureg

from PyOptik import MaterialCatalog

# Load the tabulated Smith polyethylene dataset
catalog = MaterialCatalog.from_snapshot()
material = catalog.get("organic/polyethylene/Smith").load()

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[1310, 1550] * ureg.nanometer)

# Display calculated refractive indices at sample wavelengths
material.plot()
