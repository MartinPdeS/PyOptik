from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.material_type import MaterialType
import requests
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def download_yml_file(url: str, filename: str, save_location: MaterialType) -> None:
    """
    Downloads a YAML material file from a specified URL and saves it locally.

    If the file already exists at the target save_location, the download is skipped.

    Parameters
    ----------
    url : str
        Direct link to the YAML file to download.
    filename : str
        Name to use when saving the file locally (without extension).
    save_location : MaterialType
        Target data type (SELLMEIER or TABULATED), which determines the save directory.

    Raises
    ------
    ValueError
        If ``save_location`` does not correspond to a known data path.
    requests.exceptions.Timeout
        If the server does not respond within 10 seconds.
    requests.exceptions.HTTPError
        If the server responds with an error code (e.g., 404, 500).
    Exception
        For any other unexpected issues during download or file write.
    """
    # Resolve the destination path based on material type
    if save_location == MaterialType.SELLMEIER:
        file_path: Path = sellmeier_data_path / f"{filename}.yml"
    elif save_location == MaterialType.TABULATED:
        file_path: Path = tabulated_data_path / f"{filename}.yml"
    else:
        raise ValueError(
            f"Invalid location: {save_location}. Must be MaterialType.SELLMEIER or MaterialType.TABULATED."
        )

    # Skip download if file already exists
    if file_path.exists():
        logging.info(f"File already exists: {file_path}. Skipping download.")
        return

    logging.info(f"Downloading file from {url} to {file_path}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(response.content)

        logging.info(f"File successfully saved to: {file_path}")

    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout occurred while fetching {url}: {e}")
        raise
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error while fetching {url}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while downloading or saving {url}: {e}")
        raise