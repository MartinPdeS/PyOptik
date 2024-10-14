
import yaml
from typing import Optional, List, Tuple
import requests
from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.data.sellmeier.default import default_material as sellmeier_default
from PyOptik.data.tabulated.default import default_material as tabulated_default

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

def build_default_library() -> None:
    """
    Downloads and saves the default materials from the specified URLs.
    """
    from PyOptik.utils import download_yml_file

    for name, url in sellmeier_default.items():
        download_yml_file(url=url, filename=name, location=sellmeier_data_path)

    for name, url in tabulated_default.items():
        download_yml_file(url=url, filename=name, location=tabulated_data_path)


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
    wavelength_range = [None, None] if wavelength_range is None else wavelength_range
    # Create the data dictionary for YAML
    data = {
        'REFERENCES': reference,
        'DATA': [
            {
                'type': f'formula {formula_type}',
                'wavelength_range': f"{wavelength_range[0]} {wavelength_range[1]}",
                'coefficients': " ".join(map(str, coefficients)),
            }
        ]
    }

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