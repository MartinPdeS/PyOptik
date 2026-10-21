#!/usr/bin/env python
# -*- coding: utf-8 -*-

from martinpdes_docs import configure


package_name = "PyOptik"
project = package_name
author = "Martin Poinsinet de Sivry-Houle"
autodoc_mock_imports = ["numpy", "matplotlib"]

examples_files = [
    "sellmeier",
    "tabulated",
    "group_properties",
    "custom_materials",
    "interfaces",
    "thin_films",
    "catalog",
]

globals().update(
    configure(
        project=project,
        package=package_name,
        author=author,
        repository="MartinPdeS/PyOptik",
        logo="../images/logo.svg",
        favicon="_static/pyoptik-symbol.png",
        prefer_installed_package=True,
        gallery_sections=examples_files,
        gallery_default_thumb="_static/pyoptik-symbol.png",
        logo_text="",
    )
)


napoleon_google_docstring = False
napoleon_numpy_docstring = True
