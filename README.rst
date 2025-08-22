
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


PyOptik: Optical Material Properties Made Simple
=================================================

**PyOptik** is a powerful Python library that provides seamless access to optical material properties from the comprehensive `RefractiveIndex.INFO <https://refractiveindex.info>`_ database. Whether you're simulating light-matter interactions, designing optical systems, or conducting photonics research, PyOptik delivers the refractive index and extinction coefficient data you need with a clean, intuitive API.

**Quick Start**: Get material properties in just 3 lines of code!

.. code:: python

   from TypedUnit import ureg
   from PyOptik import MaterialBank

   bk7 = MaterialBank.BK7
   n = bk7.compute_refractive_index(550 * ureg.nanometer)  # n ≈ 1.519

Key Features
************

**Comprehensive Material Database**
   Access thousands of materials from RefractiveIndex.INFO with automatic data management

**Multiple Data Formats**
   Support for both Sellmeier equation materials and tabulated wavelength data

**High-Performance Computing**
   Optimized calculations for group index, group velocity, and dispersion properties

**Simulation Ready**
   Perfect for optical design, photonics simulations, and electromagnetic modeling

**Developer Friendly**
   Clean API that integrates seamlessly with NumPy, Matplotlib, and scientific Python stack

**Advanced Analysis**
   Built-in plotting and visualization tools powered by MPSPlots

Installation
************

**Quick Install**

.. code:: bash

   pip install PyOptik

**Conda Install**

.. code:: bash

   conda install -c martinpdes pyoptik

**Development Install**

.. code:: bash

   git clone https://github.com/MartinPdeS/PyOptik.git
   cd PyOptik
   pip install -e .

Building Your Material Library
*******************************

PyOptik downloads material data from RefractiveIndex.INFO organized into categories. Choose what you need or download everything at once.

**Available Categories:**

``classics`` - Essential optical materials (BK7, fused silica, etc.)
``glasses`` - Various optical glasses
``metals`` - Metallic materials (gold, silver, aluminum, etc.)
``organics`` - Organic and polymer materials
``others`` - Specialized and exotic materials
``all`` - Everything (recommended for comprehensive access)

**Quick Setup - Download Essentials:**

.. code:: python

   from PyOptik import MaterialBank

   # Get the most commonly used materials
   MaterialBank.build_library('classics')

   # See what's available
   MaterialBank.print_materials()

**Complete Setup - Download Everything:**

.. code:: python

   # Download all materials (recommended)
   MaterialBank.build_library('all', remove_previous=True)

**Custom Selection:**

.. code:: python

   # Download specific categories
   MaterialBank.build_library('glasses')
   MaterialBank.build_library('metals')

   # Or chain them
   for category in ['classics', 'glasses', 'metals']:
       MaterialBank.build_library(category)

Quick Start Guide
*****************

**Basic Usage - Refractive Index**

.. code:: python

   from TypedUnit import ureg
   from PyOptik import MaterialBank
   import numpy as np

   # Access BK7 glass properties
   bk7 = MaterialBank.BK7

   # Single wavelength (550 nm)
   n = bk7.compute_refractive_index(550 * ureg.nanometer)
   print(f"BK7 refractive index at 550nm: {n:.4f}")

   # Multiple wavelengths
   wavelengths = np.linspace(400, 800, 100) * ureg.nanometer
   n_values = bk7.compute_refractive_index(wavelengths)

**Advanced Properties - Group Index & Velocity**

.. code:: python

   # Group index (important for pulse propagation)
   n_g = bk7.compute_group_index(550 * ureg.nanometer)

   # Group velocity (speed of pulse envelope)
   v_g = bk7.compute_group_velocity(550 * ureg.nanometer)

   print(f"Group index: {n_g:.4f}")
   print(f"Group velocity: {v_g:.2e} m/s")

**Visualization**

.. code:: python

   # Quick plot of material dispersion
   bk7.plot()

   # Custom wavelength range
   wavelengths = np.linspace(300, 2000, 500) * ureg.nanometer
   bk7.plot(wavelengths)

Detailed Example - Material Analysis
************************************

Here's a comprehensive example showing PyOptik's capabilities:

.. code:: python

   import numpy as np
   import matplotlib.pyplot as plt
   from PyOptik import MaterialBank

   # Define wavelength range (UV to Near-IR)
   wavelengths = np.linspace(200, 2500, 1000) * ureg.nanometer

   # Compare different materials
   materials = {
       'BK7 Glass': MaterialBank.BK7,
       'Fused Silica': MaterialBank.fused_silica,
       'Sapphire': MaterialBank.Al2O3
   }

   plt.figure(figsize=(12, 8))

   for name, material in materials.items():
       # Calculate refractive index across spectrum
       n_values = material.compute_refractive_index(wavelengths)

       # Plot dispersion curve
       plt.subplot(2, 2, 1)
       plt.plot(wavelengths*1e9, n_values, label=name, linewidth=2)

       # Group velocity dispersion
       group_indices = material.compute_group_index(wavelengths)
       plt.subplot(2, 2, 2)
       plt.plot(wavelengths*1e9, group_indices, label=name, linewidth=2)

   plt.subplot(2, 2, 1)
   plt.xlabel('Wavelength (nm)')
   plt.ylabel('Refractive Index')
   plt.title('Material Dispersion Comparison')
   plt.legend()
   plt.grid(True, alpha=0.3)

   plt.subplot(2, 2, 2)
   plt.xlabel('Wavelength (nm)')
   plt.ylabel('Group Index')
   plt.title('Group Index Comparison')
   plt.legend()
   plt.grid(True, alpha=0.3)

   plt.tight_layout()
   plt.show()

**Output:** |example_bk7|

This example demonstrates PyOptik's power for comparative material analysis and optical design.

Advanced Usage - Custom Materials
**********************************

**Adding Materials from RefractiveIndex.INFO**

Easily extend your library with materials from the web:

.. code:: python

   from PyOptik import MaterialBank, MaterialType

   # Add water at 19°C from RefractiveIndex.INFO
   MaterialBank.add_material_to_bank(
       filename='water_19C',
       material_type=MaterialType.SELLMEIER,
       url='https://refractiveindex.info/database/data-nk/main/H2O/Daimon-19.0C.yml'
   )

   # Now you can use it
   water = MaterialBank.water_19C
   n_water = water.compute_refractive_index(589e-9)  # Sodium D-line

**Managing Your Library**

.. code:: python

   # View all available materials
   MaterialBank.print_materials()

   # Remove unwanted materials
   MaterialBank.remove_item(filename='water_19C')

   # Check what's available after removal
   MaterialBank.print_available()

**Material Types**

PyOptik supports two material data formats:

**Sellmeier Materials**: Mathematical dispersion formulas (compact, smooth)
**Tabulated Materials**: Discrete wavelength-index pairs (experimental data)

Development & Testing
*********************

**Running Tests**

.. code:: bash

   # Clone and setup
   git clone https://github.com/MartinPdeS/PyOptik.git
   cd PyOptik
   pip install -e ".[testing]"

   # Run test suite
   pytest

   # Run with coverage
   pytest --cov=PyOptik --cov-report=html

**Code Quality**

.. code:: bash

   # Linting
   flake8 PyOptik/

   # Type checking (if using mypy)
   mypy PyOptik/

Contributing
************

We welcome contributions! PyOptik thrives on community input:

**Bug Reports**: Found an issue? Open an issue on GitHub
**Feature Requests**: Have ideas? We'd love to hear them
**Documentation**: Help improve our docs and examples
**Code**: Submit pull requests for fixes and enhancements

**Development Workflow:**

1. Fork the repository
2. Create a feature branch: ``git checkout -b feature-name``
3. Make your changes and add tests
4. Run the test suite: ``pytest``
5. Submit a pull request

Contact & Support
*****************

**Author**: `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_

**Email**: `martin.poinsinet.de.sivry@gmail.com <mailto:martin.poinsinet.de.sivry@gmail.com?subject=PyOptik>`_

**GitHub**: `PyOptik Repository <https://github.com/MartinPdeS/PyOptik>`_

**Documentation**: `Full Documentation <https://martinpdes.github.io/PyOptik/>`_

PyOptik is actively developed and maintained. We're always looking for collaborators interested in optical simulation and materials science!

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
