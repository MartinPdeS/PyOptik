#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io, os, sys, numpy
from setuptools import setup, Extension, find_packages


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'VERSION'), "r+") as f:
    Version = f.read().rstrip("\n").split(".")
    Major, Mid, Minor = int(Version[0]), int(Version[1]), int(Version[2])

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


print(f" ---------------- PyOptik Version: {Version} ----------------")

with open(os.path.join(__location__, 'Version'), "w+") as f:
    f.writelines(Version)

setup()
