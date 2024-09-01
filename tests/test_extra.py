#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch
from PyOptik.utils import build_default_library

def test_build_default_library():
    build_default_library()

if __name__ == "__main__":
    pytest.main([__file__])
