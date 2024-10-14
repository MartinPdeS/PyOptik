PyOptik
=======

PyOptik is a powerful Python tool designed to import refractive indexes and extinction coefficients for various materials across different wavelengths. The data provided by PyOptik can be used in numerous applications, including simulating light interactions with particles. All data is sourced from the reputable RefractiveIndex.INFO database.

|Logo|

.. list-table::
   :widths: 10 25 25 25
   :header-rows: 1

   * - Testing
     - |ci/cd|
     - |coverage|
     -
   * - Package
     - |PyPi|
     - |PyPi_download|
     - |anaconda|
   * - Meta
     - |python|
     - |docs|
     -

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

   pip install PyOptik
   conda install --channels martinpdes pyoptik

Simple Usage
************

After installing PyOptik, you can easily access material properties:

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


You can also add a custom element to your library providing a URL from `refractiveindex.info <https://refractiveindex.info>`_ website.

.. code:: python

   from PyOptik.utils import download_yml_file
   from PyOptik.directories import sellmeier_data_path  # or tabulated_data_path for tabulated elements

   download_yml_file(
      filename='test',
      url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml',
      location=tabulated_data_path
   )

Evidently, you can also remove element from the library using as follows:


.. code:: python

   from PyOptik.utils import remove_element

   remove_element(filename='test', location='any')  # location can be "any", "sellmeier" or "tabulated"

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
   :target: https://www.python.org/

.. |Logo| image:: https://github.com/MartinPdeS/PyOptik/raw/master/docs/images/logo.png

.. |example_bk7| image:: https://github.com/MartinPdeS/PyOptik/raw/master/docs/images/example_bk7.png
   :target: https://github.com/MartinPdeS/PyOptik/blob/master/docs/images/example_bk7.png

.. |docs| image:: https://github.com/martinpdes/pyoptik/actions/workflows/deploy_documentation.yml/badge.svg
   :target: https://martinpdes.github.io/PyOptik/
   :alt: Documentation Status

.. |ci/cd| image:: https://github.com/martinpdes/pyoptik/actions/workflows/deploy_coverage.yml/badge.svg
   :target: https://martinpdes.github.io/PyOptik/actions
   :alt: Unittest Status

.. |PyPi| image:: https://badge.fury.io/py/pyoptik.svg
   :target: https://badge.fury.io/py/pyoptik

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/pyoptik.svg
   :target: https://pypistats.org/packages/pyoptik

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/PyOptik/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |anaconda| image:: https://anaconda.org/martinpdes/pyoptik/badges/version.svg
   :target: https://anaconda.org/martinpdes/pyoptik