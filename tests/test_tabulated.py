#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from PyOptik.material import TabulatedMaterial as Material
from PyOptik.data.tabulated import material_list
from PyOptik.utils import download_yml_file
from PyOptik.directories import tabulated_data_path
import matplotlib.pyplot as plt

def test_init_material():
    material = Material('silver')

    assert material is not None

@pytest.mark.parametrize('material', material_list, ids=material_list)
@patch("matplotlib.pyplot.show")
def test_material_plot(mock_show, material: str):
    material = Material(material)

    material.plot()

    plt.close()

    print(material)

    material.print()



def test_download_yml():
    download_yml_file(
        filename='test',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=tabulated_data_path
    )

if __name__ == "__main__":
    pytest.main([__file__])




# -˙