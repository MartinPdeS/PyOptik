#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
import numpy as np
from PyOptik.material import SellmeierMaterial as Material
from PyOptik import MaterialBank
import matplotlib.pyplot as plt
from PyOptik.units import meter, micrometer, Quantity

# MaterialBank.build_library('minimal', remove_previous=True)
MaterialBank.set_filter(use_sellmeier=True, use_tabulated=True)
material_list = MaterialBank.sellmeier


def test_init_material():

    """Test initialization of SellmeierMaterial."""
    material = Material('water')

    assert material.filename == 'water'
    assert material.coefficients is not None
    assert isinstance(material.coefficients, np.ndarray)
    assert material.formula_type in [1, 2, 5, 6]
    assert material.wavelength_bound is None or isinstance(material.wavelength_bound, Quantity)
    assert material.reference is None or isinstance(material.reference, str)

    material.__str__()
    material.__repr__()
    material.print()


@pytest.mark.parametrize('material', material_list, ids=material_list)
@patch("matplotlib.pyplot.show")
def test_material_plot(mock_show, material: str):
    """Test plotting method of SellmeierMaterial with both float and pint.Quantity inputs."""
    material = Material(material)

    # Test with float values
    wavelength = np.linspace(
        material.wavelength_bound.to(meter)[0].magnitude,
        material.wavelength_bound.to(meter)[1].magnitude,
        num=10
    )

    material.plot(wavelength=wavelength)
    mock_show.assert_called_once()
    plt.close()

    # Test with pint.Quantity values
    wavelength = np.linspace(
        material.wavelength_bound.to(micrometer)[0].magnitude,
        material.wavelength_bound.to(micrometer)[1].magnitude,
        num=10
    ) * micrometer

    material.plot(wavelength=wavelength)
    mock_show.assert_called()
    plt.close()


def test_load_coefficients():
    """Test loading Sellmeier coefficients from YAML file."""
    material = Material('water')

    assert material.coefficients is not None
    assert len(material.coefficients) == 9
    assert isinstance(material.coefficients, np.ndarray)

    assert material.formula_type in [1, 2, 5, 6]

    if material.wavelength_bound is not None:
        assert isinstance(material.wavelength_bound, Quantity)
        assert len(material.wavelength_bound) == 2
        assert material.wavelength_bound[0] < material.wavelength_bound[1]

    if material.reference is not None:
        assert isinstance(material.reference, str)


def test_check_wavelength():
    """Test checking if wavelength is within allowable range."""
    material = Material('water')

    if material.wavelength_bound is not None:
        within_range = (material.wavelength_bound[0] + material.wavelength_bound[1]) / 2
        outside_range = material.wavelength_bound[1] * 1.1

        # Test wavelength within range
        material._check_wavelength(within_range)

        # Test wavelength outside range, expecting a warning
        with pytest.warns(UserWarning):
            material._check_wavelength(outside_range)


def test_compute_refractive_index():
    """Test computation of refractive index for given wavelengths."""
    material = Material('water')

    # Test single wavelength input
    wavelength = [800e-9, 500e-9] * meter
    refractive_index = material.compute_refractive_index(wavelength)
    assert isinstance(refractive_index, np.ndarray)

    # Test array of wavelengths input
    min_wl, max_wl = material.wavelength_bound
    wavelength = np.linspace(min_wl.to(meter).magnitude, max_wl.to(meter).magnitude, 50)

    refractive_indices = material.compute_refractive_index(wavelength)
    assert isinstance(refractive_indices, np.ndarray)
    assert refractive_indices.shape == wavelength.shape


def test_compute_refractive_index_inputs():
    """Test computation of refractive index for given wavelengths."""
    material = Material('water')

    # Test single wavelength input
    wavelength = 500e-9
    refractive_index = material.compute_refractive_index(wavelength)

    assert np.isscalar(refractive_index), f"Refractive index [{refractive_index}] should return scalar value when wavelength [{wavelength}] input is scalar"

    wavelength = [500e-9, 800e-9] * meter
    refractive_index = material.compute_refractive_index(wavelength)

    assert isinstance(refractive_index, np.ndarray), f"Refractive index [{refractive_index}] should return an array when wavelength [{wavelength}] input is an array"


def test_formula_type_5_accumulation():
    """Ensure formula type 5 accumulates all terms when computing the index."""
    material = Material('acetone')

    wl = 0.5 * micrometer
    calculated = material.compute_refractive_index(wl)

    expected = 1 + material.coefficients[0]
    for B, C in zip(material.coefficients[1::2], material.coefficients[2::2]):
        expected += B * wl.to(micrometer).magnitude ** C

    assert np.isclose(calculated, expected)


def test_invalid_formula_type():
    """Test handling of unsupported material types."""
    with pytest.raises(FileNotFoundError):
        Material('invalid_material')


@pytest.mark.parametrize('material', material_list, ids=material_list)
@patch("matplotlib.pyplot.show")
def test_plot_within_range(mock_show, material: str):
    """Test plotting refractive index within the wavelength range."""
    material_instance = Material(material)

    if material_instance.wavelength_bound is not None:
        min_wl, max_wl = material_instance.wavelength_bound
        wavelength = np.linspace(min_wl.to(meter).magnitude, max_wl.to(meter).magnitude, 50)
        material_instance.plot(wavelength=wavelength)

        mock_show.assert_called_once()
        plt.close()


def test_material_string_representation():
    """Test string representation methods of SellmeierMaterial."""
    material = Material('water')
    material_str = str(material)
    material_repr = repr(material)
    material_print = material.print()

    assert isinstance(material_str, str)
    assert isinstance(material_repr, str)
    assert isinstance(material_print, str)


if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])

