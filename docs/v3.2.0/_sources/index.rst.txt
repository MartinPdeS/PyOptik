PyOptik documentation
=====================

**PyOptik** is a unit-aware Python toolkit for optical material data,
dispersion, Fresnel interfaces, and coherent thin-film stacks. It combines a
searchable RefractiveIndex.INFO catalog with APIs for measured and fitted
materials.

.. list-table::
   :widths: 28 72

   * - :doc:`Getting started <getting_started>`
     - Install the package, download the catalog, and calculate refractive
       index with explicit wavelength units.
   * - :doc:`Example gallery <examples>`
     - Follow executable examples for dispersion, custom data, interfaces,
       coatings, pulse properties, and catalog search.
   * - :doc:`Interfaces and thin films <thin_films>`
     - Calculate Fresnel coefficients and coherent multilayer spectra for s and
       p polarization.
   * - :doc:`Custom materials <custom_materials>`
     - Construct materials from arrays, CSV files, or formula coefficients and
       export validated YAML.

Quick example
-------------

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import MaterialCatalog, fresnel_coefficients

   catalog = MaterialCatalog.from_snapshot()
   glass = catalog.get("specs/SCHOTT-optical/N-BK7").load()

   wavelength = 550 * ureg.nanometer
   index = glass.compute_refractive_index(wavelength)
   interface = fresnel_coefficients(1.0, glass, wavelength=wavelength)

   print(index)
   print(interface.reflectance)

.. toctree::
   :caption: Start here
   :maxdepth: 2

   getting_started

.. toctree::
   :caption: User guide
   :maxdepth: 2

   materials_and_catalog
   custom_materials
   thin_films
   catalog_browser

.. toctree::
   :caption: Learn by example
   :maxdepth: 2

   examples

.. toctree::
   :caption: Reference
   :maxdepth: 2

   conventions
   code
   references
