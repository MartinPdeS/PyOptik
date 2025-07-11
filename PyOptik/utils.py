from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.material_type import MaterialType
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def download_yml_file(url: str, filename: str, location: MaterialType) -> None:
    """Download a YAML file and store it in the local data directory.

    Parameters
    ----------
    url : str
        The fully qualified URL to download.
    filename : str
        Name of the file (without extension) under which the data will be saved.
    location : MaterialType
        Destination folder identifier. Use ``MaterialType.SELLMEIER`` for
        Sellmeier materials or ``MaterialType.TABULATED`` for tabulated ones.

    Raises
    ------
    ValueError
        If ``location`` is not a supported :class:`~PyOptik.material_type.MaterialType`.
    requests.exceptions.Timeout
        If the request times out after 10 seconds.
    requests.exceptions.HTTPError
        If the server returns an HTTP error status.
    Exception
        Propagates any unexpected error that occurred during download or file
        writing.
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
