import requests
from PyOptik.directories import sellmeier_data_path, tabulated_data_path
from PyOptik.data.sellmeier.default import default_material as sellmeier_default
from PyOptik.data.tabulated.default import default_material as tabulated_default

def download_yml_file(url: str, filename: str, location: str) -> None:
    """
    Downloads a .yml file from a specified URL and saves it locally.

    Args:
        url (str): The URL of the .yml file to download.
        save_path (str): The local path where the .yml file should be saved.

    Raises:
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

