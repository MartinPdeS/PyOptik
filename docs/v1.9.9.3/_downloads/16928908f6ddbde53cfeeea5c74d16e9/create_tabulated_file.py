"""
Example: Create a Custom Tabulated Data YAML File
=================================================

This example demonstrates how to create a custom YAML file containing tabulated
`nk` data using the `create_tabulated_file` function from the `PyOptik.utils` module.
"""

# %%
from PyOptik import MaterialBank


# Define the tabulated data (wavelength in micrometers, n, k)
tabulated_data = [
    (0.1879, 0.94, 1.337),
    (0.1916, 0.95, 1.388),
    (0.1953, 0.97, 1.440),
    (0.1993, 0.98, 1.493),
    (0.2033, 0.99, 1.550),
]

# Define the file properties
filename = 'example_tabulated'
reference = "Example Reference for Tabulated Data"
comments = "This file contains sample tabulated data for demonstration purposes. "

# Call the function to create the file
MaterialBank.create_tabulated_file(
    filename=filename,
    data=tabulated_data,
    reference=reference,
    comments=comments
)

m = MaterialBank.get(filename)

m.plot()
