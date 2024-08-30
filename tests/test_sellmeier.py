#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from PyOptik import Material
from PyOptik.material import material_list
from PyOptik.usual_materials import water
import matplotlib.pyplot as plt


@pytest.mark.parametrize('material_name', material_list, ids=material_list)
@patch("matplotlib.pyplot.show")
def test_material_plot(patch, material_name: str):
    material = Material(material_name)

    # wavelength_range = numpy.linspace(400e-9, 1000e-9, 30)
    wavelength_range = [1000e-9]

    material.plot(wavelength_range=wavelength_range)

    print(repr(material))

    print(material)

    plt.close()


if __name__ == "__main__":
    pytest.main([__file__])


# -˙