#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import os
import re
import yaml
import logging
from pathlib import Path
from typing import List, Union, Optional, Tuple
from PyOptik.directories import data_path, libraries_path
from PyOptik.material.sellmeier_class import SellmeierMaterial
from PyOptik.material.tabulated_class import TabulatedMaterial
from PyOptik.utils import download_yml_file
from tabulate import tabulate
from PyOptik.material_type import MaterialType


class _MaterialBank():
    """
    A class representing a centralized material bank for common optical materials available in the PyOptik library.

    The `_MaterialBank` class provides access to a predefined list of materials used in optical simulations,
    categorized into Sellmeier and Tabulated materials. It allows users to dynamically retrieve materials
    based on their names without the need to instantiate the class.  The material bank can be expanded
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

    >>> material.add_sellmeier_to_bank("new_material.yml", "https://refractiveindex.info/database/data-nk/main/SiO2/Malitson.yml")

    To remove a material from the bank:

    >>> MaterialBank.remove_item("obsolete_material.yml")

    Raises
    ------
    FileNotFoundError
        If a material is not found in either the Sellmeier or Tabulated material lists.
    """

    use_tabulated: bool = True
    use_sellmeier: bool = True

    def __getattr__(self, material_name: str) -> Union[SellmeierMaterial, TabulatedMaterial]:
        """
        Retrieve a material by name dynamically at the class level, respecting filter options.

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
        AttributeError
            If the material is not found in the filtered or unfiltered lists.
        """
        # Apply the filtering logic based on class-level attributes
        if material_name in self.sellmeier:
            return SellmeierMaterial(filename=material_name)
        elif material_name in self.tabulated:
            return TabulatedMaterial(filename=material_name)

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{material_name}'")

    def get(self, material_name: str) -> Union[SellmeierMaterial, TabulatedMaterial]:
        """
        Retrieve a material by name, respecting filter options.

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
        AttributeError
            If the material is not found in the filtered or unfiltered lists.
        """
        return self.__getattr__(material_name)

    @classmethod
    def set_filter(cls, use_tabulated: bool = False, use_sellmeier: bool = False) -> None:
        """
        Set the filter for the MaterialBank.

        Parameters
        ----------
        use_tabulated : bool
            If True, restricts retrieval to tabulated materials only.
        use_sellmeier : bool
            If True, restricts retrieval to sellmeier materials only.

        Raises
        ------
        ValueError
            If both use_tabulated and use_sellmeier are set to True.
        """
        if not use_tabulated and not use_sellmeier:
            raise ValueError("Cannot set both 'use_tabulated' and 'use_sellmeier' to False.")

        cls.use_tabulated = use_tabulated
        cls.use_sellmeier = use_sellmeier

    def _list_materials(self, material_type: MaterialType) -> List[str]:
        """Return available material names for a given type.

        Parameters
        ----------
        material_type : MaterialType
            The type of materials to list (MaterialType.SELLMEIER or MaterialType.TABULATED).

        Returns
        -------
        List[str]
            A list of material names of the specified type.
        """
        directory = data_path / material_type.value
        return [
            os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(directory / f) and f.endswith('.yml')
        ]

    @property
    def sellmeier(self) -> List[str]:
        """
        List all available Sellmeier materials.

        Returns
        -------
        List[str]
            A list of all Sellmeier material names.
        """
        return self._list_materials(MaterialType.SELLMEIER) if self.use_sellmeier else []

    @property
    def tabulated(self) -> List[str]:
        """
        List all available Tabulated materials.

        Returns
        -------
        List[str]
            A list of all Tabulated material names.
        """
        return self._list_materials(MaterialType.TABULATED) if self.use_tabulated else []

    @property
    def all(self) -> List[str]:
        """
        List all available materials, including both Sellmeier and Tabulated materials.

        Returns
        -------
        List[str]
            A combined list of all Sellmeier and Tabulated material names.
        """
        return self.sellmeier + self.tabulated

    def print_available(cls) -> None:
        """Display all available materials in a table.

        The method lists both Sellmeier and tabulated materials currently
        stored in the local database and prints them in two columns using
        :func:`tabulate.tabulate`.
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
    def add_material_to_bank(cls, filename: str, url: str, material_type: MaterialType) -> None:
        """
        Add a material to the material bank.

        Downloads a YAML file containing the material data from a specified URL and stores it
        in the specified materials directory.

        Parameters
        ----------
        filename : str
            The name of the file to be saved in the material bank.
        url : str
            The URL from where the material file is downloaded.
        material_type : MaterialType
            The type of material (MaterialType.SELLMEIER or MaterialType.TABULATED).

        Returns
        -------
        None
        """
        if material_type not in [MaterialType.SELLMEIER, MaterialType.TABULATED]:
            raise ValueError("Invalid material type. Please choose MaterialType.SELLMEIER or MaterialType.TABULATED.")

        return download_yml_file(filename=filename, url=url, save_location=material_type)

    @classmethod
    def add_sellmeier_to_bank(cls, filename: str, url: str) -> None:
        return cls.add_material_to_bank(filename=filename, url=url, material_type=MaterialType.SELLMEIER)

    @classmethod
    def add_tabulated_to_bank(cls, filename: str, url: str) -> None:
        return cls.add_material_to_bank(filename=filename, url=url, material_type=MaterialType.TABULATED)

    @classmethod
    def remove_item(cls, filename: str, save_location: Union[str, MaterialType] = 'any') -> None:
        """
        Remove a file associated with a given element name from the specified location.

        Parameters
        ----------
        filename : str
            The name of the file to remove, without the '.yml' suffix.
        save_location : Union[str, MaterialType]
            The save_location to search for the file, either 'sellmeier', 'tabulated', 'any', or a MaterialType enum (default is 'any').

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        ValueError
            If an invalid save_location is provided.
        """
        if isinstance(save_location, MaterialType):
            save_location = save_location.value

        save_location = save_location.lower()

        if save_location not in ['any', 'sellmeier', 'tabulated']:
            raise ValueError("Invalid save_location. Please choose 'sellmeier', 'tabulated', or 'any'.")

        if save_location in ['any', 'sellmeier']:
            sellmeier_file = data_path / 'sellmeier' / f"{filename}.yml"
            if sellmeier_file.exists():
                sellmeier_file.unlink()

        if save_location in ['any', 'tabulated']:
            tabulated_file = data_path / 'tabulated' / f"{filename}.yml"
            if tabulated_file.exists():
                tabulated_file.unlink()

    def clean_data_files(self, regex: str, save_location: Union[str, MaterialType] = 'any') -> None:
        """
        Remove all files matching the given regex from the specified location.

        Parameters
        ----------
        regex : str
            The regex pattern to match the filenames (without the '.yml' suffix).
        location : Union[str, MaterialType]
            The location to search for files, either 'sellmeier', 'tabulated', or 'any' (default is 'any').

        Raises
        ------
        ValueError
            If an invalid location is provided.
        """
        if isinstance(save_location, MaterialType):
            save_location = save_location.value

        save_location = save_location.lower()

        if save_location not in ['any', 'sellmeier', 'tabulated']:
            raise ValueError("Invalid save_location. Please choose 'sellmeier', 'tabulated', or 'any'.")

        # Compile the regex pattern
        pattern = re.compile(regex)

        # Function to remove matching files in a given directory
        def remove_matching_files(directory: Path):
            for file in directory.glob("*.yml"):
                if pattern.match(file.stem):
                    logging.info(f"Removing file: {file}")
                    file.unlink()

        # Remove files from the sellmeier location if specified
        if save_location in ['any', 'sellmeier']:
            remove_matching_files(data_path / 'sellmeier')

        # Remove files from the tabulated location if specified
        if save_location in ['any', 'tabulated']:
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
        AVAILABLE_LIBRARIES = set([os.path.splitext(f)[0] for f in os.listdir(libraries_path) if f.endswith('.yml')])

        libraries_to_download = AVAILABLE_LIBRARIES if library == 'all' else set(numpy.atleast_1d(library))

        # Ensure the requested library exists
        assert libraries_to_download.issubset(AVAILABLE_LIBRARIES), f"Library value should be in {AVAILABLE_LIBRARIES}"


        repertoire_file = libraries_path / 'repertoire.yml'
        with open(repertoire_file, 'r') as file:
            repertoire_dict = yaml.safe_load(file)

        # Remove previous files if the flag is set
        if remove_previous:
            logging.info("Removing previous files from the library.")
            self.clean_data_files(regex=".*", save_location="sellmeier")  # Remove all sellmeier files
            self.clean_data_files(regex=".*", save_location="tabulated")  # Remove all tabulated files

        for lib in libraries_to_download:
            file_path = libraries_path / lib
            with open(file_path.with_suffix('.yml'), 'r') as file:
                data_dict = yaml.safe_load(file)

            # Download new files for sellmeier
            if data_dict.get('sellmeier', False):
                for element_name in data_dict['sellmeier']:
                    url = repertoire_dict['sellmeier'][element_name]
                    download_yml_file(url=url, filename=element_name, save_location=MaterialType.SELLMEIER)

            # Download new files for tabulated
            if data_dict.get('tabulated', False):
                for element_name in data_dict['tabulated']:
                    url = repertoire_dict['tabulated'][element_name]
                    download_yml_file(url=url, filename=element_name, save_location=MaterialType.TABULATED)

    def create_sellmeier_file(
            self,
            filename: str,
            formula_type: int,
            coefficients: List[float],
            wavelength_range: Optional[Tuple[float, float]] = None,
            reference: Optional[str] = None,
            comments: Optional[str] = None,
            specs: Optional[dict] = None) -> None:
        """Create a custom Sellmeier material definition.

        Parameters
        ----------
        filename : str
            Name of the output file without extension.
        formula_type : int
            Identifier of the Sellmeier formula to use.
        coefficients : list[float]
            Coefficients of the selected Sellmeier equation.
        wavelength_range : tuple[float, float], optional
            Minimum and maximum wavelength in micrometers.
        reference : str, optional
            Reference or citation for the data.
        comments : str, optional
            Additional comments stored in the file.
        specs : dict, optional
            Extra specifications such as temperature or vacuum information.

        Notes
        -----
        The YAML file is written to ``data/sellmeier`` within the package
        directory.
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
        """Create a tabulated ``n``/``k`` material definition.

        Parameters
        ----------
        filename : str
            Name of the output file without extension.
        data : list[tuple[float, float, float]]
            Sequence of ``(wavelength, n, k)`` tuples.
        reference : str, optional
            Reference or citation for the data.
        comments : str, optional
            Additional comments stored in the file.

        Notes
        -----
        The YAML file is written to ``data/tabulated`` within the package
        directory.
        """
        reference = 'None' if reference is None else reference

        # Convert the data list to a formatted string
        data_str = "\n".join(" ".join(map(str, row)) for row in data)

        # Create the data dictionary for YAML
        yaml_data = {}
        yaml_data['REFERENCES'] = reference
        yaml_data['DATA'] = [
            dict(type='tabulated nk', data=data_str)
        ]

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
