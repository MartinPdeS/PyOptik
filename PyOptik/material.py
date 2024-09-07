#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union
from PyOptik.sellmeier_class import SellmeierMaterial
from PyOptik.tabulated_class import TabulatedMaterial
from PyOptik import data

class staticproperty(property):
    """
    A descriptor that mimics the behavior of a @property but for class-level access.

    This allows a method to be accessed like a static property without the need to instantiate the class.
    """
    def __get__(self, owner_self, owner_cls):
        return self.fget()

class Material:
    """
    A class representing common materials available in the PyOptik library.

    This class provides easy access to a predefined list of materials, either through static properties or
    a dynamic getter method. Materials are categorized into Sellmeier and Tabulated materials.
    """

    all_materials = [
        'silver',
        'gold',
        'aluminium',
        'copper',
        'zinc',
        'iron',
        'argon',
        'water',
        'silicon',
        'BK7',
        'fused_silica',
        'germanium',
        'polystyren'
    ]

    @staticmethod
    def get(material_name: str) -> Union[SellmeierMaterial, TabulatedMaterial]:
        """
        Retrieve a material by name.

        Args:
            material_name (str): The name of the material to retrieve.

        Returns:
            Union[SellmeierMaterial, TabulatedMaterial]: An instance of the material if found.

        Raises:
            FileNotFoundError: If the material is not found in either the Sellmeier or Tabulated lists.
        """
        if material_name in data.sellmeier.material_list:
            return SellmeierMaterial(material_name)

        if material_name in data.tabulated.material_list:
            return TabulatedMaterial(material_name)

        raise FileNotFoundError(f'Material: [{material_name}] could not be found.')

    # Static properties for each material

    @staticproperty
    def silver() -> TabulatedMaterial:
        """Get the TabulatedMaterial instance for silver."""
        return TabulatedMaterial('silver')

    @staticproperty
    def gold() -> TabulatedMaterial:
        """Get the TabulatedMaterial instance for gold."""
        return TabulatedMaterial('gold')

    @staticproperty
    def aluminium() -> TabulatedMaterial:
        """Get the TabulatedMaterial instance for aluminium."""
        return TabulatedMaterial('aluminium')

    @staticproperty
    def copper() -> TabulatedMaterial:
        """Get the TabulatedMaterial instance for copper."""
        return TabulatedMaterial('copper')

    @staticproperty
    def zinc() -> TabulatedMaterial:
        """Get the TabulatedMaterial instance for zinc."""
        return TabulatedMaterial('zinc')

    @staticproperty
    def iron() -> TabulatedMaterial:
        """Get the TabulatedMaterial instance for iron."""
        return TabulatedMaterial('iron')

    @staticproperty
    def polystyren() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for polystyren."""
        return SellmeierMaterial('polystyren')

    @staticproperty
    def argon() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for argon."""
        return SellmeierMaterial('argon')

    @staticproperty
    def water() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for water."""
        return SellmeierMaterial('water')

    @staticproperty
    def silicon() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for silicon."""
        return SellmeierMaterial('silicon')

    @staticproperty
    def BK7() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for BK7."""
        return SellmeierMaterial('BK7')

    @staticproperty
    def fused_silica() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for fused_silica."""
        return SellmeierMaterial('fused_silica')

    @staticproperty
    def germanium() -> SellmeierMaterial:
        """Get the SellmeierMaterial instance for germanium."""
        return SellmeierMaterial('germanium')
