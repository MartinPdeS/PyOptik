"""
Example: Download a YAML file
=============================

This example demonstrates how to download a YAML file from a URL using the
`download_yml_file` function from the `PyOptik.utils` module.
"""

# %%
from PyOptik import MaterialBank, MaterialType

# Define the URL of the YAML file and the destination
# Call the function to download the file
MaterialBank.add_material_to_bank(
    filename='example_download',
    material_type=MaterialType.SELLMEIER,
    url='https://refractiveindex.info/database/data/main/H2O/nk/Daimon-19.0C.yml'
)

MaterialBank.print_available()

m = MaterialBank.get('example_download')

m.plot()

MaterialBank.remove_item(filename='example_download')

MaterialBank.print_available()
