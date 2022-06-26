#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import numpy
import pathlib
from setuptools import setup, Extension, find_packages


# Package meta-data.
NAME            = 'PyOptik'
DESCRIPTION     = 'A package to import refractive indexes from RefractiveIndex.INFO'
URL             = 'https://github.com/paaube/PyRI'
EMAIL           = 'martin.poinsinet-de-sivry@polymtl.ca, pierre-alexandre.aube@polymtl.ca'
AUTHOR          = 'Martin Poinsinet de Sivry, Pierre-Alexandre Aubé',
REQUIRES_PYTHON = '>3.8.0'
EXTRAS = {}



Major, Mid, Minor = 0, 5, 0

if '--NewMajor' in sys.argv:
    Major += 1
    sys.argv.remove('--NewMajor')
if '--NewMid' in sys.argv:
    Mid += 1
    sys.argv.remove('--NewMidr')
if '--NewMinor' in sys.argv:
    Minor += 1
    sys.argv.remove('--NewMinor')

Version = f'{Major}.{Mid}.{Minor}'

print(f"PyMieSim Version: {Version}")



# What packages are required for this module to be executed?
REQUIRED = ['matplotlib', 'numpy', 'bs4']

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


about = {}
if not Version:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = Version


# Where the magic happens:
setup(
    name                          = NAME,
    version                       = about['__version__'],
    description                   = DESCRIPTION,
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    author                        = AUTHOR,
    author_email                  = EMAIL,
    setup_requires                = ['numpy'],
    python_requires               = '>=3.6',
    url                           = URL,
    packages                      = find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires              = REQUIRED,
    extras_require                = EXTRAS,
    dependency_links              = [],
    include_package_data          = True,
    ext_modules                   = None,
    license                       = 'MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ],
)
