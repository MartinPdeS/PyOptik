
|logo|

.. list-table::
   :widths: 10 25 25
   :header-rows: 0

   * - Meta
     - |python|
     - |docs|
   * - Testing
     - |ci/cd|
     - |coverage|
   * - PyPi
     - |PyPi|
     - |PyPi_download|
   * - Anaconda
     - |anaconda|
     - |anaconda_download|


PyOptik
=======

PyOptik is a Python tool designed to import refractive indexes and extinction coefficients for various materials across different wavelengths. The data provided by PyOptik can be used in numerous applications, including simulating light interactions with particles. All data is sourced from the reputable RefractiveIndex.INFO database.



Features
********

- **Comprehensive Database Access**: Seamlessly import refractive index and extinction coefficient data for a wide range of materials.
- **Simulation Ready**: Ideal for light-matter interaction simulations, particularly in optics and photonics.
- **Simple API**: Easy-to-use API that integrates well with other Python libraries.
- **Open Source**: Fully open-source.

Installation
************

To install PyOptik, simply use `pip` or `conda`:

.. code:: bash

   pip install PyOptik                               (using PyPi package manager)

   conda install --channels martinpdes pyoptik       (using anaconda environment manager)

Building the Material Library
*****************************

PyOptik allows you to build and customize a local material library, importing material data from various categories. You can download the following categories of materials from the RefractiveIndex.INFO database:

- `classics`: Commonly used optical materials.
- `glasses`: Various types of glass materials.
- `metals`: Different metal materials for optical simulations.
- `organics`: Organic materials with optical properties.
- `others`: Other optical materials.
- `all`: Download all available categories at once.

To build a material library, use the `build_library` function. This will download and save the material data to your local machine.

**Example: Building the Material Library:**

In this example, we will download the `others` category of materials and remove any previously existing data in that category:

.. code:: python

   from PyOptik import MaterialBank

   # Download the 'classics' category and remove previous files
   MaterialBank.build_library('classics', remove_previous=True)

**Available Categories:**

To download materials from another category, simply pass the category name as an argument to `build_library`. For example:

.. code:: python

   # Download materials from the 'glasses' category
   MaterialBank.build_library('glasses')

To download all material categories at once:

.. code:: python

   # Download all available material categories
   MaterialBank.build_library('all')

You can also set the `remove_previous` parameter to `True` to remove old data before downloading new material data.

Viewing Available Materials
***************************

Once you have built the material library, you can view all the available materials using the `MaterialBank` class. This will print a list of materials stored in your local library.

**Example:**

.. code:: python

   from PyOptik import MaterialBank

   # Print the available materials in a tabulated format
   MaterialBank.print_materials()

Simple Usage
************

After installing PyOptik and building the material library, you can easily access material properties:

.. code:: python

   from PyOptik import MaterialBank

   # Access the refractive index of BK7 glass
   bk7 = MaterialBank.BK7
   n = bk7.compute_refractive_index(0.55e-6)
   print(f"Refractive index at 0.55 µm: {n}")

Example
*******

Here is a quick example demonstrating how to use PyOptik to retrieve and plot the refractive index of a material:

.. code:: python

   import numpy as np
   from PyOptik import MaterialBank

   # Define wavelength range
   wavelengths = np.linspace(0.3e-6, 2.5e-6, 100)

   # Retrieve refractive index for BK7 glass
   bk7 = MaterialBank.BK7
   n_values = bk7.compute_refractive_index(wavelengths)

   # Plot the results
   bk7.plot()

This code produces the following figure: |example_bk7|

Adding and Removing Custom Materials
************************************

You can add a custom material to your library by providing a URL from `refractiveindex.info <https://refractiveindex.info>`_.

**Adding a Custom Material:**

.. code:: python

   from PyOptik import MaterialBank, MaterialType

   # Define the URL of the YAML file and the destination
   # Call the function to download the file
   MaterialBank.add_material_to_bank(
      filename='example_download',
      material_type=MaterialType.SELLMEIER,
      url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml'
   )

   MaterialBank.print_available()

**Removing a Material:**

You can also remove a material from the library as follows:

.. code:: python

   from PyOptik.utils import remove_element

   MaterialBank.remove_item(filename='example_download')

Testing
*******

To test locally after cloning the GitHub repository, install the dependencies and run the tests:

.. code:: bash

   git clone https://github.com/MartinPdeS/PyOptik.git
   cd PyOptik
   pip install .
   pytest

Contributing
************

PyOptik is open to contributions. Whether you're fixing bugs, adding new features, or improving documentation, your help is welcome! Please feel free to fork the repository and submit pull requests.

Contact Information
*******************

As of 2024, PyOptik is still under development. If you would like to collaborate, it would be a pleasure to hear from you. Contact me at:

**Author**: `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_

**Email**: `martin.poinsinet.de.sivry@gmail.com <mailto:martin.poinsinet.de.sivry@gmail.com?subject=PyOptik>`_

.. |python| image:: https://img.shields.io/pypi/pyversions/pyoptik.svg
   :alt: Python
   :target: https://www.python.org/

.. |logo| image:: https://github.com/MartinPdeS/PyOptik/raw/master/docs/images/logo.png
   :alt: PyOptik logo

.. |example_bk7| image:: https://github.com/MartinPdeS/PyOptik/raw/master/docs/images/example_bk7.png
   :alt: PyOptik example: BK7
   :target: https://github.com/MartinPdeS/PyOptik/blob/master/docs/images/example_bk7.png

.. |docs| image:: https://github.com/martinpdes/pyoptik/actions/workflows/deploy_documentation.yml/badge.svg
   :target: https://martinpdes.github.io/PyOptik/
   :alt: Documentation Status

.. |ci/cd| image:: https://github.com/martinpdes/pyoptik/actions/workflows/deploy_coverage.yml/badge.svg
   :target: https://martinpdes.github.io/PyOptik/actions
   :alt: Unittest Status

.. |PyPi| image:: https://badge.fury.io/py/pyoptik.svg
   :alt: PyPi version
   :target: https://badge.fury.io/py/pyoptik

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/pyoptik.svg
   :alt: PyPi version
   :target: https://pypistats.org/packages/pyoptik

.. |anaconda_download| image:: https://anaconda.org/martinpdes/pyoptik/badges/downloads.svg
   :alt: Anaconda downloads
   :target: https://anaconda.org/martinpdes/pyoptik

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/PyOptik/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |anaconda| image:: https://anaconda.org/martinpdes/pyoptik/badges/version.svg
   :alt: Anaconda version
   :target: https://anaconda.org/martinpdes/pyoptik
