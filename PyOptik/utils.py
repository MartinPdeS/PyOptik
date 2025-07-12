from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.material_type import MaterialType
import requests
import logging
from pathlib import Path
import PyOptik
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def download_yml_file(
    url: str,
    filename: str,
    save_location: MaterialType,
    max_retries: int = 5,
    retry_delay: float = 2.0,
    backoff_factor: float = 2.0,
) -> None:
    """
    Download a YAML material file from the given URL and save it locally.

    If the file already exists, the function will skip downloading.
    Retries are performed on connection or timeout errors.

    Parameters
    ----------
    url : str
        Direct link to the YAML file to download.
    filename : str
        File name to save (without .yml extension).
    save_location : MaterialType
        The target material type (SELLMEIER or TABULATED).
    max_retries : int, optional
        Maximum number of retry attempts (default is 3).
    retry_delay : float, optional
        Delay (in seconds) between retries (default is 2.0).
    backoff_factor : float, optional
        Multiplier applied to delay after each failed attempt (default is 2.0).

    Raises
    ------
    ValueError
        If an invalid MaterialType is passed.
    requests.exceptions.RequestException
        For non-retriable HTTP or connection errors.
    """
    # Determine save save_location
    if save_location == MaterialType.SELLMEIER:
        file_path: Path = sellmeier_data_path / f"{filename}.yml"
    elif save_location == MaterialType.TABULATED:
        file_path: Path = tabulated_data_path / f"{filename}.yml"
    else:
        raise ValueError(f"Invalid save_location: {save_location}. Must be SELLMEIER or TABULATED.")

    # Skip if already downloaded
    if file_path.exists():
        logging.info(f"File already exists: {file_path}. Skipping download.")
        return

    # Create directory if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Retry logic
    attempt = 0
    delay = retry_delay

    while attempt < max_retries:
        attempt += 1
        try:
            logging.info(f"Attempt {attempt} of {max_retries}: downloading {url}")
            response = requests.get(url, timeout=PyOptik.TIMEOUT)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                f.write(response.content)

            logging.info(f"Successfully downloaded and saved to: {file_path}")
            return

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logging.warning(f"Download attempt {attempt} failed due to network error: {e}")
            if attempt < max_retries:
                logging.info(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
                delay *= backoff_factor
            else:
                logging.error(f"Exceeded maximum retries for {url}")
                raise
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error while downloading {url}: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while saving {url} to {file_path}: {e}")
            raise