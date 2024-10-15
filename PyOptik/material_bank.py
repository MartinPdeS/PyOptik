#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from typing import List
from PyOptik.material.sellmeier_class import SellmeierMaterial
from PyOptik.material.tabulated_class import TabulatedMaterial
from PyOptik.utils import download_yml_file, remove_element
from PyOptik.directories import tabulated_data_path, sellmeier_data_path
from tabulate import tabulate


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

        if material_name in cls.sellmeier():
            print('--'*50, material_name, material_name.__class__)
            return SellmeierMaterial(filename=material_name)

        if material_name in cls.tabulated():
            return TabulatedMaterial(filename=material_name)

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

    @classmethod
    def sellmeier(cls) -> List[str]:
        return [
            os.path.splitext(f)[0] for f in os.listdir(sellmeier_data_path) if os.path.isfile(os.path.join(sellmeier_data_path, f)) and f.endswith('.yml')
        ]

    @classmethod
    def tabulated(cls) -> List[str]:
        return [
            os.path.splitext(f)[0] for f in os.listdir(tabulated_data_path) if os.path.isfile(os.path.join(tabulated_data_path, f)) and f.endswith('.yml')
        ]

    @classmethod
    def all(self) -> List[str]:
        return self.sellmeier() + self.tabulated()

    @classmethod
    def print_materials(cls) -> None:
        """
        Prints out all the available Sellmeier and Tabulated materials in a tabulated format.
        """
        sellmeier_materials = cls.sellmeier()
        tabulated_materials = cls.tabulated()

        # Create data for the table
        table_data = []
        max_len = max(len(sellmeier_materials), len(tabulated_materials))
        for i in range(max_len):
            sellmeier = sellmeier_materials[i] if i < len(sellmeier_materials) else ""
            tabulated = tabulated_materials[i] if i < len(tabulated_materials) else ""
            table_data.append([sellmeier, tabulated])

        # Define headers
        headers = ["Sellmeier Materials", "Tabulated Materials"]

        # Print the table using tabulate
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

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
