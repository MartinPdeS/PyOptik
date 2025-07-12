#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy as np
from unittest.mock import patch
from PyOptik.material import TabulatedMaterial
from PyOptik.units import Quantity, micrometer, meter
import matplotlib.pyplot as plt
from PyOptik import MaterialBank


# MaterialBank.build_library('minimal', remove_previous=True)
MaterialBank.set_filter(use_sellmeier=True, use_tabulated=True)
material_list = MaterialBank.tabulated


def test_init_material():
    """Test initialization of TabulatedMaterial."""
    material = TabulatedMaterial('zinc')

    assert material.filename == 'zinc'
    assert material.wavelength is not None
    assert isinstance(material.wavelength, Quantity)
    assert material.n_values is not None
    assert material.k_values is not None
    assert isinstance(material.n_values, np.ndarray)
    assert isinstance(material.k_values, np.ndarray)
    assert material.reference is None or isinstance(material.reference, str)

    assert len(material.wavelength) == len(material.n_values) == len(material.k_values)


def test_load_tabulated_data():
    """Test loading tabulated data from YAML file."""
    material = TabulatedMaterial('zinc')
    material._load_tabulated_data()

    assert material.wavelength is not None
    assert isinstance(material.wavelength, Quantity)
    assert material.n_values is not None
    assert isinstance(material.n_values, np.ndarray)
    assert material.k_values is not None
    assert isinstance(material.k_values, np.ndarray)
    assert len(material.wavelength) == len(material.n_values) == len(material.k_values)


def test_check_wavelength():
    """Test checking if wavelength is within tabulated range."""
    material = TabulatedMaterial('zinc')
    material._load_tabulated_data()

    # Test within range
    wavelength = material.wavelength.mean()
    material._check_wavelength(wavelength)

    # Test outside range, expecting a warning
    with pytest.warns(UserWarning, match="Wavelength range goes from.*"):
        wavelength = material.wavelength.max() + 10 * micrometer
        material._check_wavelength(wavelength)


def test_compute_refractive_index():
    """Test computation of refractive index for given wavelengths."""
    material = TabulatedMaterial('zinc')
    material._load_tabulated_data()

    # Test single wavelength input
    wavelength = 500e-9 * meter
    refractive_index = material.compute_refractive_index(wavelength)
    assert isinstance(refractive_index, complex)

    # Test array of wavelengths input
    wavelengths = np.array([400e-9, 500e-9, 600e-9]) * meter
    refractive_indices = material.compute_refractive_index(wavelengths)
    assert isinstance(refractive_indices, np.ndarray)
    assert refractive_indices.shape == wavelengths.shape


def test_compute_refractive_index_inputs():
    """Test computation of refractive index for given wavelengths."""
    material = TabulatedMaterial('zinc')

    # Test single wavelength input
    wavelength = 500e-9
    refractive_index = material.compute_refractive_index(wavelength)

    assert np.isscalar(refractive_index), f"Refractive index [{refractive_index}] should return scalar value when wavelength [{wavelength}] input is scalar"

    wavelength = [500e-9, 800e-9] * meter
    refractive_index = material.compute_refractive_index(wavelength)

    assert isinstance(refractive_index, np.ndarray), f"Refractive index [{refractive_index}] should return an array when wavelength [{wavelength}] input is an array"


@patch("matplotlib.pyplot.show")
def test_plot(mock_show):
    """Test plotting method of TabulatedMaterial."""
    material = TabulatedMaterial('zinc')
    material._load_tabulated_data()

    # Test plotting the entire range
    material.plot()
    mock_show.assert_called_once()
    plt.close()

    # Test plotting a specific range of wavelengths
    wavelength_range = np.linspace(material.wavelength.min().magnitude, material.wavelength.max().magnitude, 50) * micrometer
    material.plot(wavelength=wavelength_range)
    mock_show.assert_called()
    plt.close()


def test_material_string_representation():
    """Test string representation methods of TabulatedMaterial."""
    material = TabulatedMaterial('zinc')
    material_str = str(material)
    material_repr = repr(material)
    material_print = material.print()

    assert isinstance(material_str, str)
    assert isinstance(material_repr, str)
    assert isinstance(material_print, str)
    assert "TabulatedMaterial: 'zinc'" in material_print


if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])
