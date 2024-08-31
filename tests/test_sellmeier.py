#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from PyOptik import Material
from PyOptik.materials import material_list
from PyOptik.utils import download_yml_file
import matplotlib.pyplot as plt


def test_init_material():
    material = Material('water')

    assert material is not None

@pytest.mark.parametrize('material', material_list, ids=[m.filename for m in material_list])
@patch("matplotlib.pyplot.show")
def test_material_plot(patch, material: str):
    # wavelength_range = numpy.linspace(400e-9, 1000e-9, 30)
    wavelength_range = [1000e-9]

    material.plot(wavelength_range=wavelength_range)

    print(repr(material))

    print(material)

    plt.close()


def test_download_yml():
    download_yml_file(filename='test', url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml')

if __name__ == "__main__":
    pytest.main([__file__])




# -˙