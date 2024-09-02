#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from PyOptik.utils import build_default_library, remove_element, download_yml_file
from PyOptik.directories import tabulated_data_path, sellmeier_data_path

def test_download_yml():
    download_yml_file(
        filename='test',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=tabulated_data_path
    )

    download_yml_file(
        filename='test',
        url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
        location=sellmeier_data_path
    )

def test_build_default_library():
    build_default_library()

def test_remove_element():
    remove_element(filename='test', location='any')

if __name__ == "__main__":
    pytest.main([__file__])
