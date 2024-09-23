"""
Plot refractive index of material: BK7
======================================

"""

import numpy
from PyOptik import Sellmeier


material = Sellmeier('BK7')

RI = material.get_refractive_index(wavelength=[1310e-9, 1550e-9])

figure = material.plot(
    wavelength_range=numpy.linspace(300e-9, 3500e-9, 300)
)

figure.show()
