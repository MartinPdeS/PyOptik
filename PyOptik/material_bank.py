#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import os
import re
import yaml
import logging
from pathlib import Path
from typing import List, Union, Optional, Tuple
from PyOptik.directories import data_path
from PyOptik.material.sellmeier_class import SellmeierMaterial
from PyOptik.material.tabulated_class import TabulatedMaterial
from PyOptik.utils import download_yml_file
from tabulate import tabulate
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class _MaterialBank():
    """
    A class representing a centralized material bank for common optical materials available in the PyOptik library.

    The `_MaterialBank` class provides access to a predefined list of materials used in optical simulations,
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

    >>> material = _MaterialBank
    >>> bk7_material = material.BK7  # Dynamically retrieves the BK7 material.

    To add a new material to the Sellmeier bank:

    >>> material.add_sellmeier_to_bank("new_material.yml", "http://example.com/material.yml")

    To remove a material from the bank:

    >>> MaterialBank.remove_item("obsolete_material.yml")

    Raises
    ------
    FileNotFoundError
        If a material is not found in either the Sellmeier or Tabulated material lists.
    """

    def __getattr__(self, material_name: str) -> Union[SellmeierMaterial, TabulatedMaterial]:
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
        if material_name in self.sellmeier:
            return SellmeierMaterial(filename=material_name)

        if material_name in self.tabulated:
            return TabulatedMaterial(filename=material_name)

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{material_name}'")

    def get(self, filename: str) ->  Union[SellmeierMaterial, TabulatedMaterial]:
        return self.__getattr__(filename)

    @property
    def sellmeier(self) -> List[str]:
        return [
            os.path.splitext(f)[0] for f in os.listdir(data_path / 'sellmeier') if os.path.isfile(os.path.join(data_path / 'sellmeier', f)) and f.endswith('.yml')
        ]

    @property
    def tabulated(self) -> List[str]:
        return [
            os.path.splitext(f)[0] for f in os.listdir(data_path / 'tabulated') if os.path.isfile(os.path.join(data_path / 'tabulated', f)) and f.endswith('.yml')
        ]

    @property
    def all(self) -> List[str]:
        return self.sellmeier + self.tabulated

    def print_materials(cls) -> None:
        """
        Prints out all the available Sellmeier and Tabulated materials in a tabulated format.
        """
        sellmeier_materials = cls.sellmeier
        tabulated_materials = cls.tabulated

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
        return download_yml_file(filename=filename, url=url, location=data_path / 'sellmeier')

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
        return download_yml_file(filename=filename, url=url, location=data_path / 'tabulated')

    @classmethod
    def remove_item(cls, filename: str, location: str = 'any') -> None:
        """
        Remove a file associated with a given element name from the specified location.

        Parameters
        ----------
        filename : str
            The name of the file to remove, without the '.yml' suffix.
        location : str
            The location to search for the file, either 'sellmeier', 'tabulated', or 'any' (default is 'any').

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        ValueError
            If an invalid location is provided.
        """
        location = location.lower()

        if location not in ['any', 'sellmeier', 'tabulated']:
            raise ValueError("Invalid location. Please choose 'sellmeier', 'tabulated', or 'any'.")

        if location in ['any', 'sellmeier']:
            sellmeier_file = data_path / 'sellmeier' / f"{filename}.yml"
            if sellmeier_file.exists():
                sellmeier_file.unlink()

        if location in ['any', 'tabulated']:
            tabulated_file = data_path / 'tabulated' / f"{filename}.yml"
            if tabulated_file.exists():
                tabulated_file.unlink()

    def clean_data_files(self, regex: str, location: str = 'any') -> None:
        """
        Remove all files matching the given regex from the specified location.

        Parameters
        ----------
        regex : str
            The regex pattern to match the filenames (without the '.yml' suffix).
        location : str
            The location to search for files, either 'sellmeier', 'tabulated', or 'any' (default is 'any').

        Raises
        ------
        ValueError
            If an invalid location is provided.
        """
        # Compile the regex pattern
        pattern = re.compile(regex)

        # Normalize the location parameter
        location = location.lower()

        if location not in ['any', 'sellmeier', 'tabulated']:
            raise ValueError("Invalid location. Please choose 'sellmeier', 'tabulated', or 'any'.")

        # Function to remove matching files in a given directory
        def remove_matching_files(directory: Path):
            for file in directory.glob("*.yml"):
                if pattern.match(file.stem):
                    logging.info(f"Removing file: {file}")
                    file.unlink()

        # Remove files from the sellmeier location if specified
        if location in ['any', 'sellmeier']:
            remove_matching_files(data_path / 'sellmeier')

        # Remove files from the tabulated location if specified
        if location in ['any', 'tabulated']:
            remove_matching_files(data_path / 'tabulated')


    def build_library(self, library: Union[str, List[str]] = 'classics', remove_previous: bool = False) -> None:
        """
        Downloads and saves materials data from the specified URLs.

        Parameters
        ----------
        library : str | list[str]
            The name or list of names of the libraries to download.
        remove_previous : bool
            If True, removes existing files before downloading new ones.
        """
        AVAILABLE_LIBRARIES = {'classics', 'glasses', 'metals', 'organics', 'others', 'minimal'}

        libraries_to_download = AVAILABLE_LIBRARIES if library == 'all' else set(numpy.atleast_1d(library))

        # Ensure the requested library exists
        assert libraries_to_download.issubset(AVAILABLE_LIBRARIES), f"Library value should be in {AVAILABLE_LIBRARIES}"

        # Remove previous files if the flag is set
        if remove_previous:
            logging.info(f"Removing previous files from the library.")
            self.clean_data_files(regex=".*", location="sellmeier")  # Remove all sellmeier files
            self.clean_data_files(regex=".*", location="tabulated")  # Remove all tabulated files

        for lib in libraries_to_download:
            file_path = data_path / lib
            with open(file_path.with_suffix('.yml'), 'r') as file:
                data_dict = yaml.safe_load(file)

            # Download new files for sellmeier
            if data_dict.get('sellmeier', False):
                for element_name, url in data_dict['sellmeier'].items():
                    download_yml_file(url=url, filename=element_name, location=data_path / 'sellmeier')

            # Download new files for tabulated
            if data_dict.get('tabulated', False):
                for element_name, url in data_dict['tabulated'].items():
                    download_yml_file(url=url, filename=element_name, location=data_path / 'tabulated')

    def create_sellmeier_file(
        self,
        filename: str,
        formula_type: int,
        coefficients: List[float],
        wavelength_range: Optional[Tuple[float, float]] = None,
        reference: Optional[str] = None,
        comments: Optional[str] = None,
        specs: Optional[dict] = None) -> None:
        """
        Creates a YAML file with custom Sellmeier coefficients in the correct format.

        Parameters
        ----------
        filename : str
            The name of the file to create (without the extension).
        formula_type : int
            The type of Sellmeier formula.
        coefficients :  list[float]
            A list of coefficients for the Sellmeier equation.
        wavelength_range : Tuple[float, float]
            The range of wavelengths, in micrometers.
        reference : str
            A reference for the material data.
        comments : Optional[str]
            Additional comments about the material.
        specs : Optional[dict]
            Additional specifications, such as temperature and whether the wavelength is in a vacuum.
        """
        reference = 'None' if reference is None else reference

        # Create the data dictionary for YAML
        data = {}
        data['REFERENCES'] = reference
        data['DATA'] = dict(
            type=f'formula {formula_type}',
            coefficients=" ".join(map(str, coefficients))
        )

        if wavelength_range is not None:
            min_bound, max_bound = wavelength_range
            data['DATA'].update({'wavelength_range': f"{min_bound} {max_bound}"})

        data['DATA'] = [data['DATA']]
        # Add comments if provided
        if comments:
            data['COMMENTS'] = comments

        # Add specs if provided
        if specs:
            data['SPECS'] = specs

        # Define the file path
        file_path = data_path / 'sellmeier' / f"{filename}.yml"

        # Write the data to a YAML file
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        logging.info(f"Sellmeier data saved to {file_path}")

    def create_tabulated_file(
        self,
        filename: str,
        data: List[Tuple[float, float, float]],
        reference: Optional[str] = None,
        comments: Optional[str] = None) -> None:
        """
        Creates a YAML file with tabulated nk data in the correct format.

        Parameters
        ----------
        filename : str)
            The name of the file to create (without the extension).
        data : List[Tuple[float, float, float]])
            The tabulated nk data.
        reference : Optional[str])
            A reference for the material data.
        comments : Optional[str])
            Additional comments about the material.
        """
        reference = 'None' if reference is None else reference

        # Convert the data list to a formatted string
        data_str = "\n".join(" ".join(map(str, row)) for row in data)

        # Create the data dictionary for YAML
        yaml_data = {
            'REFERENCES': reference,
            'DATA': [
                {
                    'type': 'tabulated nk',
                    'data': data_str,
                }
            ]
        }

        # Add comments if provided
        if comments:
            yaml_data['COMMENTS'] = comments

        # Define the file path
        file_path = data_path / 'tabulated' / f"{filename}.yml"

        # Write the data to a YAML file
        with open(file_path, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False)

        logging.info(f"Tabulated nk data saved to {file_path}")

MaterialBank = _MaterialBank()