#!/usr/bin/env python
# -*- coding: utf-8 -*-

from martinpdes_docs import configure


package_name = "PyOptik"
project = package_name
author = "Martin Poinsinet de Sivry-Houle"
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
        version="auto",
        author=author,
        repository="MartinPdeS/PyOptik",
        logo="../images/logo.png",
        favicon="../images/favicon.png",
        prefer_installed_package=True,
        gallery_sections=examples_files,
        gallery_default_thumb="../images/icon.png",
        logo_text="",
        logo_alt_text="PyOptik — RefractiveIndex.info",
        html_css_files=["branding.css"],
    )
)


napoleon_google_docstring = False
napoleon_numpy_docstring = True
