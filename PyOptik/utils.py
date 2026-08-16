import requests
import logging
from pathlib import Path
import time

from PyOptik.directories import user_sellmeier_data_path, user_tabulated_data_path
from PyOptik.material_type import MaterialType
import PyOptik

# Backwards-compatible names; callers may monkeypatch these to redirect downloads.
sellmeier_data_path = user_sellmeier_data_path
tabulated_data_path = user_tabulated_data_path

logger = logging.getLogger(__name__)


def download_yml_file(
    url: str,
    filename: str,
    save_location: MaterialType,
    max_retries: int = 5,
    retry_delay: float = 2.0,
    backoff_factor: float = 2.0,
    destination: Path | None = None,
    overwrite: bool = False,
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
        Maximum number of retry attempts (default is 5).
    retry_delay : float, optional
        Delay (in seconds) between retries (default is 2.0).
    backoff_factor : float, optional
        Multiplier applied to delay after each failed attempt (default is 2.0).
    destination : pathlib.Path or str, optional
        Explicit output path for hierarchical catalog downloads.
    overwrite : bool, optional
        Replace an existing file instead of resuming from the local copy.

    Raises
    ------
    ValueError
        If an invalid MaterialType is passed.
    requests.exceptions.RequestException
        For non-retriable HTTP or connection errors.
    """
    # Determine save save_location
    if destination is not None:
        file_path = Path(destination)
    elif save_location == MaterialType.SELLMEIER:
        file_path: Path = sellmeier_data_path / f"{filename}.yml"
    elif save_location == MaterialType.TABULATED:
        file_path: Path = tabulated_data_path / f"{filename}.yml"
    else:
        raise ValueError(f"Invalid save_location: {save_location}. Must be SELLMEIER or TABULATED.")

    # Skip if already downloaded
    if file_path.exists() and not overwrite:
        logger.info("File already exists: %s. Skipping download.", file_path)
        return

    # Retry logic
    attempt = 0
    delay = retry_delay

    while attempt < max_retries:
        attempt += 1
        try:
            logger.info("Attempt %s of %s: downloading %s", attempt, max_retries, url)
            response = requests.get(url, timeout=PyOptik.TIMEOUT)
            response.raise_for_status()

            # Only create a directory after a successful response. This keeps
            # failed/offline downloads side-effect free.
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info("Successfully downloaded and saved to: %s", file_path)
            return

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning("Download attempt %s failed due to network error: %s", attempt, e)
            if attempt < max_retries:
                logger.info("Retrying in %.1f seconds...", delay)
                time.sleep(delay)
                delay *= backoff_factor
            else:
                logger.error("Exceeded maximum retries for %s", url)
                raise
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error while downloading %s: %s", url, e)
            raise
        except Exception as e:
            logger.exception("Unexpected error while saving %s to %s", url, file_path)
            raise
