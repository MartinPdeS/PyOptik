from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.material_type import MaterialType
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def download_yml_file(url: str, filename: str, location: MaterialType) -> None:
    """
    Downloads a .yml file from a specified URL and saves it locally.
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
