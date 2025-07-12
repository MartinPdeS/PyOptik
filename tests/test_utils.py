#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from PyOptik import MaterialBank, MaterialType
from PyOptik.utils import download_yml_file

MaterialBank.set_filter(use_sellmeier=True, use_tabulated=True)

def test_dummy():
    """Dummy test to ensure pytest runs correctly."""
    assert True

def test_main():
    MaterialBank.build_library('minimal', remove_previous=True)

url_water = 'https://refractiveindex.info/database/data/main/H2O/nk/Daimon-19.0C.yml'

def test_download_yml_files():
    """
    Test downloading YAML files to different locations. Ensures that files are
    correctly downloaded from a given URL to the specified directory.
    """
    download_yml_file(
        filename='test_tabulated',
        url=url_water,
        save_location=MaterialType.TABULATED
    )

    download_yml_file(
        filename='test_sellmeier',
        url=url_water,
        save_location=MaterialType.SELLMEIER
    )


def test_add_custom():
    MaterialBank.add_tabulated_to_bank(
        filename='test_tabulated',
        url=url_water,
    )

    MaterialBank.add_sellmeier_to_bank(
        filename='test_sellmeier',
        url=url_water,
    )


def test_fail_add_custom():
    with pytest.raises(ValueError):
        MaterialBank.add_material_to_bank(
            filename='test_tabulated',
            url=url_water,
            material_type='invalid_location'
        )


def test_remove_item():
    """
    Test the removal of an element from a library. Ensures that an element can
    be removed without errors.
    """
    with pytest.raises(ValueError):
        MaterialBank.remove_item(filename='test', save_location='invalid_location')

    download_yml_file(
        filename='test_sellmeier',
        url=url_water,
        save_location=MaterialType.SELLMEIER
    )

    MaterialBank.remove_item(filename='test_sellmeier', save_location=MaterialType.SELLMEIER)

    download_yml_file(
        filename='test_tabulated',
        url=url_water,
        save_location=MaterialType.TABULATED
    )

    MaterialBank.remove_item(filename='test_tabulated', save_location=MaterialType.TABULATED)

    download_yml_file(
        filename='test_sellmeier',
        url=url_water,
        save_location=MaterialType.SELLMEIER
    )

    MaterialBank.clean_data_files(regex='test*', save_location=MaterialType.SELLMEIER)

    download_yml_file(
        filename='test_tabulated',
        url=url_water,
        save_location=MaterialType.TABULATED
    )

    MaterialBank.clean_data_files(regex='test*', save_location=MaterialType.TABULATED)


def test_create_custom_sellmeier_file():
    """
    Test the creation of a custom Sellmeier YAML file. Ensures that the file
    is created with the correct coefficients and formula type.
    """
    with pytest.raises(ValueError):
        MaterialBank.create_sellmeier_file(
            filename='test_sellmeier_file',
            coefficients=[0, 1, 2, 3, 4],
            formula_type=9,
            wavelength_range=[1, 1.2],
            comments='Dummy comment',
            specs='Random specs'
        )

        MaterialBank.test_sellmeier_file.compute_refractive_index(1.1e-6)


def test_fail_with_wrong_formula_type():
    """
    Test the creation of a custom Sellmeier YAML file. Ensures that the file
    is created with the correct coefficients and formula type.
    """
    MaterialBank.create_sellmeier_file(
        filename='test_sellmeier_file',
        coefficients=[0, 10.6684293, 0.301516485, 0.0030434748, 1.13475115, 1.54133408, 1104],
        formula_type=2,
        wavelength_range=[1, 1.2],
        comments='Dummy comment',
        specs='Random specs'
    )

    MaterialBank.test_sellmeier_file.compute_refractive_index(1.1e-6)


def test_create_custom_tabulated_file():
    """
    Test the creation of a custom tabulated YAML file. Ensures that the file
    is created with the correct tabulated data, reference, and comments.
    """
    MaterialBank.create_tabulated_file(
        filename="test_tabulated_file",
        data=[
            (0.1879, 0.94, 1.337),
            (0.1916, 0.95, 1.388),
            (0.1953, 0.97, 1.440)
        ],
        reference="Example of tabulated test file",
        comments="Room temperature"
    )


def test_download_yml_file_http_error_log(caplog):
    with pytest.raises(ValueError):
        download_yml_file(
            filename='example_download',
            url='__invalid_url__.com',
            save_location=MaterialType.SELLMEIER
        )

def test_main():
    MaterialBank.build_library('classics', remove_previous=False)

if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])
