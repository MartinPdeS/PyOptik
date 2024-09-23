#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from PyOptik.material import SellmeierMaterial as Material
from PyOptik.data.sellmeier import material_list
import matplotlib.pyplot as plt


def test_init_material():
    material = Material('water')

    material.__str__()

    material.__repr__()

    material.print()

    assert material is not None

@pytest.mark.parametrize('material', material_list, ids=material_list)
@patch("matplotlib.pyplot.show")
def test_material_plot(mock_show, material: str):
    material = Material(material)

    material.plot(wavelength=[500e-9])

    plt.close()


if __name__ == "__main__":
    pytest.main([__file__])




# -˙