"""
Example: Download a YAML file
=============================

This example demonstrates how to download a YAML file from a URL using the
`download_yml_file` function from the `PyOptik.utils` module.
"""

# %%
from PyOptik.utils import download_yml_file
from PyOptik import MaterialBank, MaterialType

# Define the URL of the YAML file and the destination
url = 'https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml'
filename = 'example_download'

# Call the function to download the file
download_yml_file(filename=filename, url=url, location=MaterialType.SELLMEIER)

MaterialBank.print_available()

m = MaterialBank.get('example_download')

m.plot()
