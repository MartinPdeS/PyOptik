"""
========================================
Building database and Printing Materials
========================================

This example demonstrates how to build a material library using the `build_library` function
from the PyOptik package and how to print out the available materials using the `MaterialBank` class.

We will first build the `others` material library, removing any previously downloaded files,
and then print out all the available materials in the `MaterialBank`.

The available libraries are:
- 'classics'
- 'glasses'
- 'metals'
- 'organics'
- 'others'
- 'all' (to download all libraries)

"""

# %%
# Import necessary modules
from PyOptik import MaterialBank

# Build the 'classics' material library and remove previously downloaded files
MaterialBank.build_library('all', remove_previous=False)

# Print all the available materials (Sellmeier and Tabulated)
MaterialBank.print_available()
