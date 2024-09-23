#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyOptik.directories import tabulated_data_path as material_path

# Get a list of all filenames in the directory
material_list = [os.path.splitext(f)[0] for f in os.listdir(material_path) if os.path.isfile(os.path.join(material_path, f)) and f.endswith('.yml') and 'test' not in f]
