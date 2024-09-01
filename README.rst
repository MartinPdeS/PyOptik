.. |python| image:: https://img.shields.io/pypi/pyversions/pyoptik.svg
   :target: https://www.python.org/

.. |Logo| image:: https://github.com/MartinPdeS/PyOptik/raw/master/docs/images/logo.png

.. |docs| image:: https://readthedocs.org/projects/pyoptik/badge/?version=latest
   :target: https://pyoptik.readthedocs.io/en/latest/

.. |PyPi| image:: https://badge.fury.io/py/pyoptik.svg
   :target: https://badge.fury.io/py/pyoptik

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/pyoptik.svg
   :target: https://pypistats.org/packages/pyoptik

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/PyOptik/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html

PyOptik
=======

PyOptik is a powerful Python tool designed to import refractive indexes and extinction coefficients for various materials across different wavelengths. The data provided by PyOptik can be used in numerous applications, including simulating light interactions with particles. All data is sourced from the reputable RefractiveIndex.INFO database.

|Logo|

|python| |docs| |PyPi| |PyPi_download| |coverage|

Features
********
- **Comprehensive Database Access**: Seamlessly import refractive index and extinction coefficient data for a wide range of materials.
- **Simulation Ready**: Ideal for light-matter interaction simulations, particularly in optics and photonics.
- **Simple API**: Easy-to-use API that integrates well with other Python libraries.
- **Open Source**: Fully open-source.

Installation
************

To install PyOptik, simply use pip:

.. code:: bash

   pip install pyoptik

Usage
*****

After installing PyOptik, you can easily access material properties:

.. code:: python

   from PyOptik import UsualMaterial

   # Access the refractive index of BK7 glass
   bk7 = UsualMaterial.BK7
   n = bk7.compute_refractive_index(0.55e-6)
   print(f"Refractive index at 0.55 µm: {n}")

   # Accessing and plotting material properties
   bk7.plot(wavelength_range=[0.3e-6, 2.5e-6])

Example
*******

Here’s a quick example demonstrating how to use PyOptik to retrieve and plot the refractive index of a material:

.. code:: python

   import numpy as np
   from PyOptik import UsualMaterial

   # Define wavelength range
   wavelengths = np.linspace(0.3e-6, 2.5e-6, 100)

   # Retrieve refractive index for BK7 glass
   bk7 = UsualMaterial.BK7
   n_values = bk7.compute_refractive_index(wavelengths)

   # Plot the results
   bk7.plot(wavelength_range=wavelengths)

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



