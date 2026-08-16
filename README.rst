|logo|

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Badge
     - Status
   * - Python versions
     - |python|
   * - Documentation
     - |docs|
   * - Continuous integration
     - |ci/cd|
   * - Test coverage
     - |coverage|
   * - PyPI package
     - |PyPi|
   * - PyPI downloads
     - |PyPi_download|
   * - Anaconda package
     - |anaconda|
   * - Anaconda downloads
     - |anaconda_download|

PyOptik
=======

**PyOptik** is a Python library for evaluating optical material properties.
It provides unit-aware refractive-index calculations, dispersion models,
tabulated optical constants, group-delay properties, plotting helpers, and a
catalog interface for the hierarchical `RefractiveIndex.INFO
<https://refractiveindex.info>`_ database.

The library is designed for optical design, photonics simulations,
electromagnetic modeling, and experimental data analysis.

Features
--------

* Sellmeier and other dispersion-formula models.
* Tabulated complex refractive index data, ``n + i k``.
* Unit-aware wavelength calculations through ``TypedUnit`` and Pint.
* Group index, group velocity, group delay, and group-delay dispersion.
* NumPy-compatible scalar and array evaluation.
* Plotting helpers for dispersion and absorption data.
* Hierarchical catalog access using upstream ``shelf / book / page`` identity.
* Curated material aliases such as ``MaterialBank.BK7`` for quick workflows.
* Downloadable custom and upstream material data with local caching.

Installation
------------

Install the latest release from PyPI:

.. code-block:: bash

   python -m pip install PyOptik

The package is also available through Anaconda:

.. code-block:: bash

   conda install -c martinpdes pyoptik

Verify the installation with the same interpreter that will run your code:

.. code-block:: bash

   python -c "import PyOptik; print(PyOptik.__version__)"

First calculation
-----------------

Wavelengths should carry units. This avoids ambiguity between metres,
micrometres, and nanometres.

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import MaterialBank

   bk7 = MaterialBank.BK7
   index = bk7.compute_refractive_index(550 * ureg.nanometer)

   print(index)

For backward compatibility, bare numeric wavelengths are interpreted as
metres. Unit-bearing quantities are recommended for new code.

Material models
---------------

Sellmeier materials evaluate a dispersion formula:

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import MaterialBank

   silica = MaterialBank.fused_silica
   wavelengths = [800, 1310, 1550] * ureg.nanometer
   index = silica.compute_refractive_index(wavelengths)

Tabulated materials interpolate complex optical constants:

.. code-block:: python

   silicon = MaterialBank.silicon
   index = silicon.compute_refractive_index(1.55 * ureg.micrometer)

The real part is the refractive index ``n`` and the imaginary part is the
extinction coefficient ``k``.

Validity ranges
~~~~~~~~~~~~~~~

Material data is only valid over the wavelength range supplied by its source.
Out-of-range behavior can be selected explicitly:

.. code-block:: python

   wavelength = 300 * ureg.nanometer

   # Default: issue a warning and evaluate.
   index = bk7.compute_refractive_index(wavelength, out_of_range="warn")

   # Fail fast for production calculations.
   index = bk7.compute_refractive_index(wavelength, out_of_range="raise")

   # Evaluate at the nearest validity boundary.
   index = bk7.compute_refractive_index(wavelength, out_of_range="clip")

Group and pulse properties
--------------------------

Every material model provides group-related quantities:

.. code-block:: python

   wavelength = 1550 * ureg.nanometer

   group_index = silica.compute_group_index(wavelength)
   group_velocity = silica.compute_group_velocity(wavelength)
   group_delay = silica.compute_group_delay(
       wavelength,
       length=10 * ureg.centimeter,
   )
   group_delay_dispersion = silica.compute_group_delay_dispersion(wavelength)

These methods accept scalar or array wavelengths and return unit-aware values.

Plotting
--------

Material models include simple dispersion plots:

.. code-block:: python

   from PyOptik import MaterialBank

   MaterialBank.BK7.plot()
   MaterialBank.gold.plot()

For non-interactive environments such as CI or servers, select a headless
Matplotlib backend before importing plotting code:

.. code-block:: python

   import matplotlib
   matplotlib.use("Agg")

Hierarchical material catalog
-----------------------------

RefractiveIndex.INFO organizes data by **shelf**, **book**, and **page**.
PyOptik preserves this identity so that materials from different sources do
not collide simply because they share a short name.

Load the upstream catalog index:

.. code-block:: python

   from PyOptik import MaterialCatalog

   catalog = MaterialCatalog.from_upstream()

   print(catalog.shelves())
   print(catalog.books(shelf="specs"))

Download a complete source collection, such as an optical-glass book:

.. code-block:: python

   catalog.download(
       shelf="specs",
       book="SCHOTT-optical",
   )

Access a page by its canonical identifier and load its material model:

.. code-block:: python

   page = catalog.get("specs/SCHOTT-optical/N-BK7")
   bk7 = page.load()

The shorter compatibility interface remains available:

.. code-block:: python

   from PyOptik import MaterialBank

   catalog = MaterialBank.update_catalog()
   page = MaterialBank.get_page("specs/SCHOTT-optical/N-BK7")

Material data is cached in a user data directory. Set
``PYOPTIK_DATA_DIR`` to choose a different location.

Curated libraries and aliases
-----------------------------

For quick workflows, ``MaterialBank`` provides aliases and curated download
collections:

.. code-block:: python

   from PyOptik import MaterialBank

   MaterialBank.build_library("classics")
   MaterialBank.print_available()

   MaterialBank.build_library("metals")
   gold = MaterialBank.get("gold", kind="tabulated")

Available collections can be listed with:

.. code-block:: python

   print(MaterialBank.list_available_libraries())

The command-line interface provides the same collection download workflow:

.. code-block:: bash

   python -m PyOptik --list-libraries
   python -m PyOptik classics
   python -m PyOptik metals --verbose

Custom materials
----------------

Add a source YAML file from a URL:

.. code-block:: python

   from PyOptik import MaterialBank, MaterialType

   MaterialBank.add_material_to_bank(
       filename="water_19C",
       material_type=MaterialType.SELLMEIER,
       url="https://refractiveindex.info/database/data/main/H2O/nk/Daimon-19.0C.yml",
   )

Create a custom Sellmeier file:

.. code-block:: python

   MaterialBank.create_sellmeier_file(
       filename="my_glass",
       formula_type=2,
       coefficients=[0, 1.0, 0.01, 0.5, 0.1],
       wavelength_range=(0.4, 2.0),
       reference="Internal measurement",
   )

Create a custom tabulated ``n,k`` file:

.. code-block:: python

   MaterialBank.create_tabulated_file(
       filename="my_metal",
       data=[
           (0.50, 0.95, 1.80),
           (0.60, 0.90, 2.10),
           (0.70, 0.85, 2.40),
       ],
       reference="Internal measurement",
   )

Remove user-installed data with:

.. code-block:: python

   MaterialBank.remove_item("water_19C")

Common issues
-------------

* Attach units to wavelengths whenever possible.
* Use ``out_of_range="raise"`` when extrapolation would invalidate a result.
* Use the canonical catalog identifier when provenance or source selection
  matters.
* Use ``MPLBACKEND=Agg`` for documentation builds, CI, and remote servers.
* If a material cannot be found, build the required curated library or load
  the upstream catalog with ``MaterialCatalog.from_upstream()``.

Development and testing
-----------------------

Clone the repository and install development dependencies:

.. code-block:: bash

   git clone https://github.com/MartinPdeS/PyOptik.git
   cd PyOptik
   python -m pip install -e ".[testing,documentation,dev]"

Run the offline test suite:

.. code-block:: bash

   MPLBACKEND=Agg pytest -m "not network"

Build the documentation:

.. code-block:: bash

   MPLBACKEND=Agg sphinx-build -b html -W docs/source docs/build/html

Network-dependent tests are marked with ``network`` and are excluded from
normal CI runs.

Documentation and references
----------------------------

* `Online documentation <https://martinpdes.github.io/PyOptik/>`_
* `RefractiveIndex.INFO database <https://github.com/polyanskiy/refractiveindex.info-database>`_
* `PyOptik source repository <https://github.com/MartinPdeS/PyOptik>`_

The material data is sourced from RefractiveIndex.INFO. Refer to each
material page for its original scientific or manufacturer reference.

.. |python| image:: https://img.shields.io/pypi/pyversions/pyoptik.svg
   :alt: Supported Python versions
   :target: https://pypi.org/project/pyoptik/

.. |logo| image:: https://github.com/MartinPdeS/PyOptik/raw/master/docs/images/logo.png
   :alt: PyOptik logo

.. |docs| image:: https://github.com/martinpdes/pyoptik/actions/workflows/deploy_documentation.yml/badge.svg
   :target: https://martinpdes.github.io/PyOptik/
   :alt: Documentation status

.. |ci/cd| image:: https://github.com/martinpdes/pyoptik/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/MartinPdeS/PyOptik/actions/workflows/tests.yml
   :alt: Continuous integration status

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/PyOptik/python-coverage-comment-action-data/badge.svg
   :alt: Test coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |PyPi| image:: https://badge.fury.io/py/pyoptik.svg
   :alt: PyPI version
   :target: https://pypi.org/project/pyoptik/

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/pyoptik.svg
   :alt: PyPI downloads
   :target: https://pypistats.org/packages/pyoptik

.. |anaconda| image:: https://anaconda.org/martinpdes/pyoptik/badges/version.svg
   :alt: Anaconda version
   :target: https://anaconda.org/martinpdes/pyoptik

.. |anaconda_download| image:: https://anaconda.org/martinpdes/pyoptik/badges/downloads.svg
   :alt: Anaconda downloads
   :target: https://anaconda.org/martinpdes/pyoptik
