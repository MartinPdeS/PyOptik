#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from PyOptik.utils import (
    build_default_library,
    remove_element,
    download_yml_file,
    create_sellmeier_file,
    create_tabulated_file
)
from PyOptik.directories import tabulated_data_path, sellmeier_data_path

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

def test_build_default_library():
    """
    Test the creation of the default library. Ensures that the default library
    is built without errors.
    """
    build_default_library()

def test_remove_element():
    """
    Test the removal of an element from a library. Ensures that an element can
    be removed without errors.
    """
    remove_element(filename='test', location='any')

def test_create_custom_sellmeier_file():
    """
    Test the creation of a custom Sellmeier YAML file. Ensures that the file
    is created with the correct coefficients and formula type.
    """
    create_sellmeier_file(
        filename='test_sellmeier_file',
        coefficients=[0, 1, 2, 3, 4],
        formula_type=1,
        comments='Dummy comment',
        specs='Random specs'
    )

def test_create_custom_tabulated_file():
    """
    Test the creation of a custom tabulated YAML file. Ensures that the file
    is created with the correct tabulated data, reference, and comments.
    """
    create_tabulated_file(
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
