#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class MaterialType(Enum):
    """Enumeration of material data representations."""

    SELLMEIER = "sellmeier"
    TABULATED = "tabulated"
