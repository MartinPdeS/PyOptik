#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Ensure gallery examples import this checkout rather than an installed copy.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import PyOptik
from PyOptik.directories import doc_css_path
from martinpdes_docs import configure
from sphinx_gallery.sorting import FileNameSortKey


package_name = "PyOptik"
project = package_name
author = "Martin Poinsinet de Sivry-Houle"
version = PyOptik.__version__

def setup(app):
    app.add_css_file(str(doc_css_path))


autodoc_mock_imports = ["numpy", "matplotlib", "numpydoc"]

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
        version=os.getenv("tag", "latest"),
        extensions=[
            "sphinx.ext.mathjax",
            "sphinx_gallery.gen_gallery",
            "sphinx.ext.autodoc",
            "sphinx.ext.napoleon",
            "sphinx.ext.viewcode",
            "sphinx.ext.autosectionlabel",
            "sphinx.ext.intersphinx",
        ],
        html_theme_options={
            "logo": {"text": "", "image": "../images/logo.svg"},
        },
        sphinx_gallery_conf={
            "default_thumb_file": str(
                Path(__file__).resolve().parent / "_static" / "pyoptik-symbol.png"
            ),
            "reset_modules_order": "after",
            "examples_dirs": [f"../examples/{name}" for name in examples_files],
            "gallery_dirs": [f"gallery/{name}" for name in examples_files],
            "within_subsection_order": FileNameSortKey,
        },
    )
)


napoleon_google_docstring = False
napoleon_numpy_docstring = True
