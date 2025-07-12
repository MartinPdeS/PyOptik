#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convenience paths used throughout the :mod:`PyOptik` package.

This module exposes commonly referenced directories such as the project
root, documentation and data folders.  It is imported by other modules to
construct absolute paths in a centralised manner and therefore simplifies
file handling across the code base.
"""

from pathlib import Path
import PyOptik


__all__ = [
    'root_path',
    'project_path',
    'doc_path',
    'doc_css_path',
    'logo_path'
]

root_path = Path(PyOptik.__path__[0])

project_path = root_path.parents[0]

example_directory = root_path.joinpath('examples')

doc_path = project_path.joinpath('docs')

doc_css_path = doc_path.joinpath('source/_static/default.css')

logo_path = doc_path.joinpath('images/logo.png')

examples_path = root_path.joinpath('examples')

sellmeier_data_path = root_path.joinpath('data/sellmeier')

tabulated_data_path = root_path.joinpath('data/tabulated')

data_path = root_path.joinpath('data')

libraries_path = root_path.joinpath('libraries')


if __name__ == '__main__':
    for path_name in __all__:
        path = locals()[path_name]
        print(path)
        assert path.exists(), f"Path {path_name} do not exists"

# -
