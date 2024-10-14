#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyOptik.material.sellmeier_class import SellmeierMaterial
from PyOptik.data.sellmeier import material_list as sellmeier_material_list
from PyOptik.data.tabulated import material_list as tabulated_material_list
from PyOptik.material.tabulated_class import TabulatedMaterial
from PyOptik import data
from PyOptik.utils import download_yml_file, remove_element
from PyOptik.directories import tabulated_data_path, sellmeier_data_path



class MaterialBankMeta(type):
    """
    Metaclass to handle dynamic material lookup for the MaterialBank class.
    """
    def __getattr__(cls, material_name: str):
        """
        Retrieve a material by name dynamically at the class level.

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


class MaterialBank(metaclass=MaterialBankMeta):
    """
    A class representing a centralized material bank for common optical materials available in the PyOptik library.

    The `MaterialBank` class provides access to a predefined list of materials used in optical simulations,
    categorized into Sellmeier and Tabulated materials. It allows users to dynamically retrieve materials
    based on their names without the need to instantiate the class. The material bank can be expanded
    or modified by adding or removing materials from the bank, and it provides utilities to fetch material data
    dynamically when accessed as class attributes.

    Attributes
    ----------
    all : list
        A combined list of all materials, including both Sellmeier and Tabulated materials.

    Usage
    -----
    Materials can be accessed directly as class attributes:

    >>> material = MaterialBank
    >>> bk7_material = material.BK7  # Dynamically retrieves the BK7 material.

    To add a new material to the Sellmeier bank:

    >>> material.add_sellmeier_to_bank("new_material.yml", "http://example.com/material.yml")

    To remove a material from the bank:

    >>> material.remove_item_from_bank("obsolete_material.yml")

    Raises
    ------
    FileNotFoundError
        If a material is not found in either the Sellmeier or Tabulated material lists.
    """

    all = [*sellmeier_material_list, *tabulated_material_list]

    @classmethod
    def add_sellmeier_to_bank(cls, filename: str, url: str) -> None:
        """
        Add a Sellmeier material to the material bank.

        Downloads a YAML file containing the Sellmeier material data from a specified URL and stores it
        in the Sellmeier materials directory.

        Parameters
        ----------
        filename : str
            The name of the file to be saved in the Sellmeier material bank.
        url : str
            The URL from where the material file is downloaded.

        Returns
        -------
        None
        """
        return download_yml_file(filename=filename, url=url, location=sellmeier_data_path)

    @classmethod
    def add_tabulated_to_bank(cls, filename: str, url: str) -> None:
        """
        Add a Tabulated material to the material bank.

        Downloads a YAML file containing the Tabulated material data from a specified URL and stores it
        in the Tabulated materials directory.

        Parameters
        ----------
        filename : str
            The name of the file to be saved in the Tabulated material bank.
        url : str
            The URL from where the material file is downloaded.

        Returns
        -------
        None
        """
        return download_yml_file(filename=filename, url=url, location=tabulated_data_path)

    @classmethod
    def remove_item_from_bank(cls, filename: str, location: str = 'any') -> None:
        """
        Remove a material file from the material bank.

        Deletes a material file from either the Sellmeier, Tabulated, or both directories based on the location.
        If `location` is set to 'any', it will search for the material file in both directories and remove it.

        Parameters
        ----------
        filename : str
            The name of the material file to be removed.
        location : str, optional
            The location to search for the material ('sellmeier', 'tabulated', or 'any').
            Default is 'any'.

        Returns
        -------
        None
        """
        remove_element(filename=filename, location=location)
