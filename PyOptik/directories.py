#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Filesystem paths used by :mod:`PyOptik`.

Material data is downloaded into the per-user data directory; PyOptik does
not provide a bundled material database.
"""

from pathlib import Path
import os
import sys
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

logo_path = doc_path.joinpath('images/logo.svg')

examples_path = root_path.joinpath('examples')


def _default_user_data_path() -> Path:
    """Return the per-user directory for downloaded/custom material data."""
    configured = os.environ.get("PYOPTIK_DATA_DIR")
    if configured:
        return Path(configured).expanduser()
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "PyOptik"


user_data_path = _default_user_data_path()
user_sellmeier_data_path = user_data_path / "sellmeier"
user_tabulated_data_path = user_data_path / "tabulated"

def material_paths(material_type):
    """Return the user data directory for a material type.

    Parameters
    ----------
    material_type : MaterialType
        Material representation whose directories should be returned.

    Returns
    -------
    tuple of pathlib.Path
        The user data directory. The tuple form is retained for callers that
        iterate over search locations.
    """
    directory_name = material_type.value
    return (user_data_path / directory_name,)


if __name__ == '__main__':
    for path_name in __all__:
        path = locals()[path_name]
        print(path)
        assert path.exists(), f"Path {path_name} do not exists"

# -
