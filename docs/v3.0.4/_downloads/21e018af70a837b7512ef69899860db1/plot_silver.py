"""
Plot the Refractive Index of Optical Material: Silver
=====================================================

This module demonstrates the usage of the PyOptik library to calculate and plot the refractive index of the optical material silver over a specified range of wavelengths.

"""

# %%
import numpy
from TypedUnit import ureg

from PyOptik import MaterialCatalog

# Load the tabulated Johnson silver dataset
catalog = MaterialCatalog.from_snapshot()
material = catalog.get("main/Ag/Johnson").load()

# Calculate refractive index at specific wavelengths
RI = material.compute_refractive_index(wavelength=[1310, 1550] * ureg.nanometer)

# Display calculated refractive indices at sample wavelengths
material.plot()
