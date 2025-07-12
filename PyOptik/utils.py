from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.material_type import MaterialType
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def download_yml_file(url: str, filename: str, location: MaterialType) -> None:
    """Download and store a material YAML file.

    Parameters
    ----------
    url : str
        Direct link to the YAML file to download.
    filename : str
        Name (without extension) used when saving the file locally.
    location : MaterialType
        Target directory; either ``MaterialType.SELLMEIER`` or
        ``MaterialType.TABULATED``.

    Raises
    ------
    ValueError
        If ``location`` does not correspond to a known directory.
    requests.exceptions.Timeout
        If the download does not finish within 10 seconds.
    requests.exceptions.HTTPError
        If the server returns an HTTP error code.
    Exception
        For any other unexpected error during download or write.
    """
    match location:
        case MaterialType.SELLMEIER:
            file_path = sellmeier_data_path / f"{filename}.yml"
        case MaterialType.TABULATED:
            file_path = tabulated_data_path / f"{filename}.yml"
        case _:
            raise ValueError(f"Location [{location}] is invalid, it can be either MaterialType.SELLMEIER or MaterialType.TABULATED")


    logging.info(f"Starting download of {url!r} → {file_path!s}")
    try:
        response = requests.get(url, timeout=10)
        logging.info(f"Received response: HTTP {response.status_code}")
        response.raise_for_status()

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(response.content)
        logging.info(f"File downloaded and saved to {file_path}")

    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout after 10 s when fetching {url!r}: {e}")
        raise
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error while fetching {url!r}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
