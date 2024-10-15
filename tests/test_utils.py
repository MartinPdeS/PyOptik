#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import PyOptik
from PyOptik import MaterialBank
from PyOptik.directories import tabulated_data_path, sellmeier_data_path
from PyOptik.utils import download_yml_file

def test_main():
    import subprocess

    subprocess.run(["python", "-m", "PyOptik"])


def test_download_yml_files():
    """
    Test downloading YAML files to different locations. Ensures that files are
    correctly downloaded from a given URL to the specified directory.
    """
    download_yml_file(
        filename='test_tabulated',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=tabulated_data_path
    )

    download_yml_file(
        filename='test_sellmeier',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=sellmeier_data_path
    )

def test_build_library():
    """
    Test the creation of the default library. Ensures that the default library
    is built without errors.
    """
    MaterialBank.build_library('minimal')

def test_remove_item():
    """
    Test the removal of an element from a library. Ensures that an element can
    be removed without errors.
    """
    with pytest.raises(ValueError):
        MaterialBank.remove_item(filename='test', location='invalid_location')

    download_yml_file(
        filename='test_sellmeier',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=sellmeier_data_path
    )

    MaterialBank.remove_item(filename='test_sellmeier', location='sellmeier')

    download_yml_file(
        filename='test_tabulated',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=tabulated_data_path
    )

    MaterialBank.remove_item(filename='test_tabulated', location='tabulated')

    download_yml_file(
        filename='test_sellmeier',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=sellmeier_data_path
    )

    MaterialBank.clean_data_files(regex='test*', location='sellmeier')


    download_yml_file(
        filename='test_tabulated',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=tabulated_data_path
    )

    MaterialBank.clean_data_files(regex='test*', location='tabulated')

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

if __name__ == "__main__":
    pytest.main(["-W error", __file__])
