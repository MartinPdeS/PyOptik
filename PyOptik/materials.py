#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyOptik.material_class import Material
from PyOptik.default import default_material

local = locals()
for name in default_material.keys():
    local[name] = Material(name)
