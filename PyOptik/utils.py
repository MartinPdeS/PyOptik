
import yaml
from typing import Optional, List, Tuple, Union
import requests
import re
from pathlib import Path
from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.directories import data_path
import numpy

def download_yml_file(url: str, filename: str, location: str) -> None:
    """
    Downloads a .yml file from a specified URL and saves it locally.

    Parameters
    ----------
    url : str
        The URL of the .yml file to download.
    save_path : str
        The local path where the .yml file should be saved.

    Raises
    ------
        HTTPError: If the download fails due to an HTTP error.
    """
    file_path = location / f"{filename}.yml"
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the content of the response as a file
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded and saved to {file_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def build_library(library: Union[str, List[str]] = 'classics', remove_previous: bool = False) -> None:
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
        print(f"Removing previous files from the library.")
        clean_data_files(regex=".*", location="sellmeier")  # Remove all sellmeier files
        clean_data_files(regex=".*", location="tabulated")  # Remove all tabulated files

    for lib in libraries_to_download:
        file_path = data_path / lib
        with open(file_path.with_suffix('.yml'), 'r') as file:
            data_dict = yaml.safe_load(file)

        # Download new files for sellmeier
        if data_dict.get('sellmeier', False):
            for element_name, url in data_dict['sellmeier'].items():
                download_yml_file(url=url, filename=element_name, location=sellmeier_data_path)

        # Download new files for tabulated
        if data_dict.get('tabulated', False):
            for element_name, url in data_dict['tabulated'].items():
                download_yml_file(url=url, filename=element_name, location=tabulated_data_path)


def remove_element(filename: str, location: str = 'any') -> None:
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
        sellmeier_file = sellmeier_data_path / f"{filename}.yml"
        if sellmeier_file.exists():
            sellmeier_file.unlink()

    if location in ['any', 'tabulated']:
        tabulated_file = tabulated_data_path / f"{filename}.yml"
        if tabulated_file.exists():
            tabulated_file.unlink()

def create_sellmeier_file(
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
    file_path = sellmeier_data_path / f"{filename}.yml"

    # Write the data to a YAML file
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f"Sellmeier data saved to {file_path}")

def create_tabulated_file(
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
    file_path = tabulated_data_path / f"{filename}.yml"

    # Write the data to a YAML file
    with open(file_path, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)

    print(f"Tabulated nk data saved to {file_path}")

def clean_data_files(regex: str, location: str = 'any') -> None:
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
        if not directory.exists():
            return
        for file in directory.glob("*.yml"):
            if pattern.match(file.stem):
                print(f"Removing file: {file}")  # Debug print or logging
                file.unlink()

    # Remove files from the sellmeier location if specified
    if location in ['any', 'sellmeier']:
        remove_matching_files(sellmeier_data_path)

    # Remove files from the tabulated location if specified
    if location in ['any', 'tabulated']:
        remove_matching_files(tabulated_data_path)
