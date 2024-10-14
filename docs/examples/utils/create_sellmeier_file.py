"""
Example: Create a Custom Sellmeier YAML File
============================================

This example demonstrates how to create a custom Sellmeier YAML file using the
`create_sellmeier_file` function from the `PyOptik.utils` module.
"""

from PyOptik.utils import create_sellmeier_file
from PyOptik.directories import sellmeier_data_path
from PyOptik import SellmeierMaterial

# Define the file properties
filename = 'example_sellmeier'
coefficients = [1.86e-06, 1.31e-08, -1.37e-11, 4.34e-07, 6.27e-10, 0.17]
formula_type = 1

# Call the function to create the file
create_sellmeier_file(
    filename=filename,
    coefficients=coefficients,
    formula_type=formula_type,
    wavelength_range=(0.2, 2.0),
    reference="Sample Reference",
    comments="This is a sample Sellmeier file created for demonstration purposes. "
)

print(f"Sellmeier YAML file {filename}.yml has been created in {sellmeier_data_path}")

m = SellmeierMaterial(filename)

m.plot()