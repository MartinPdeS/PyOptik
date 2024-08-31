#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyOptik.material_class import Material
from PyOptik.directories import sellmeier_data_path

# Get a list of all filenames in the directory
material_file_list = [os.path.splitext(f)[0] for f in os.listdir(sellmeier_data_path) if os.path.isfile(os.path.join(sellmeier_data_path, f)) and f.endswith('.yml')]
material_list = []

local = locals()
for name in material_file_list:
    material = Material(name)
    local[name] = material
    material_list.append(material)

