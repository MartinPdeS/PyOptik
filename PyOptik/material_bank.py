#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union
from dataclasses import dataclass
from PyOptik.material.sellmeier_class import SellmeierMaterial
from PyOptik.data.sellmeier import material_list as sellmeier_material_list
from PyOptik.data.tabulated import material_list as tabulated_material_list
from PyOptik.material.tabulated_class import TabulatedMaterial
from PyOptik import data
from PyOptik.utils import download_yml_file, remove_element
from PyOptik.directories import tabulated_data_path, sellmeier_data_path


class staticproperty(property):
    """
    A descriptor that mimics the behavior of a @property but for class-level access.

    This allows a method to be accessed like a static property without the need to instantiate the class.
    """
    def __get__(self, owner_self, owner_cls):
        return self.fget()

@dataclass(unsafe_hash=True)
class _MaterialBank:
    """
    A class representing common materials available in the PyOptik library.

    This class provides easy access to a predefined list of materials, either through static properties or
    a dynamic getter method. Materials are categorized into Sellmeier and Tabulated materials.
    """

    all = [*sellmeier_material_list, *tabulated_material_list]


    def __getattr__(self, material_name: str) -> Union[SellmeierMaterial, TabulatedMaterial]:
        """
        Retrieve a material by name.

        Parameters
        ----------
        material_name : str
            The name of the material to retrieve.

        Returns
        -------
        Union[SellmeierMaterial, TabulatedMaterial]
            An instance of the material if found.

        Raises
        ------
        FileNotFoundError
            If the material is not found in either the Sellmeier or Tabulated lists.
        """
        if material_name in data.sellmeier.material_list:
            return SellmeierMaterial(material_name)

        if material_name in data.tabulated.material_list:
            return TabulatedMaterial(material_name)

        raise FileNotFoundError(f'Material: [{material_name}] could not be found.')


    def add_sellmeier_to_bank(self, filename: str, url: str) -> None:
        return download_yml_file(filename=filename, url=url, location=sellmeier_data_path)

    def add_tabulated_to_bank(self, filename: str, url: str) -> None:
        return download_yml_file(filename=filename, url=url, location=tabulated_data_path)

    def remove_item_from_bank(self, filename: str, location: str ='any') -> None:
        remove_element(filename=filename, location=location)

