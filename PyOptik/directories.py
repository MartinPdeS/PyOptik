#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import PyOptik


__all__ = [
    'root_path',
    'project_path',
    'doc_path',
    'doc_css_path',
    'logo_path',
    'version_path',
]

root_path = Path(PyOptik.__path__[0])

project_path = root_path.parents[0]

example_directory = root_path.joinpath('examples')

doc_path = project_path.joinpath('docs')

doc_css_path = doc_path.joinpath('source/_static/default.css')

logo_path = doc_path.joinpath('images/logo.png')

version_path = root_path.joinpath('VERSION')

examples_path = root_path.joinpath('examples')

ZeroPath = os.path.dirname(root_path)

DataPath = os.path.join(root_path, 'Data')

NPZPath = os.path.join(DataPath, 'npz')


if __name__ == '__main__':
    for path_name in __all__:
        path = locals()[path_name]
        print(path)
        assert path.exists(), f"Path {path_name} do not exists"

# -
