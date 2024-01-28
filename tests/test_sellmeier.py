#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from unittest.mock import patch
import pytest
from PyOptik import Sellmeier
from PyOptik.sellmeier_material import list_materials
list_materials()

material_name_list = [
    'BK7',
    'BAK1',
    'SF5',
    'silica',
    'fluorine_doped_silica_2%',
    'borosilicate',
    'fluorine_doped_silica_1%',
    'ZBLAN'
]


@pytest.mark.parametrize('material_name', material_name_list, ids=material_name_list)
@patch("matplotlib.pyplot.show")
def test_material_plot(patch, material_name: str):
    material = Sellmeier(material_name)

    wavelength_range = numpy.linspace(400e-9, 1000e-9, 30)

    _ = material.plot(wavelength_range=wavelength_range)

    # figure.show()

# -
