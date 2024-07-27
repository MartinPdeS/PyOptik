#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from unittest.mock import patch
import pytest
from PyOptik import DataMeasurement
from PyOptik.experiment_material import material_list


@pytest.mark.parametrize('material_name', material_list, ids=material_list)
@patch("matplotlib.pyplot.show")
def test_material_plot(patch, material_name: str):
    material = DataMeasurement(material_name)

    wavelength_range = numpy.linspace(400e-9, 1000e-9, 30)

    figure = material.plot(wavelength_range=wavelength_range)

# -
