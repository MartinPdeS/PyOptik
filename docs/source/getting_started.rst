Getting started
===============

Installation
------------

Install PyOptik and download the independently maintained material snapshot:

.. code-block:: bash

   python -m pip install PyOptik
   pyoptik setup

Install the optional terminal browser with ``python -m pip install
"PyOptik[ui]"``.

Your first calculation
----------------------

Load a page by its canonical ``shelf/book/page`` identifier and attach units
to every wavelength:

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import MaterialCatalog

   catalog = MaterialCatalog.from_snapshot()
   glass = catalog.get("specs/SCHOTT-optical/N-BK7").load()

   wavelength = 550 * ureg.nanometer
   index = glass.compute_refractive_index(wavelength)
   print(index)

Arrays use the same API:

.. code-block:: python

   wavelengths = [486.1, 587.6, 656.3] * ureg.nanometer
   indices = glass.compute_refractive_index(wavelengths)

Common properties
-----------------

Every material provides a consistent set of derived quantities:

.. code-block:: python

   n = glass.n(wavelength)
   k = glass.k(wavelength)
   epsilon_r = glass.relative_permittivity(wavelength)
   alpha = glass.absorption_coefficient(wavelength)
   group_index = glass.compute_group_index(wavelength)

Use ``out_of_range="raise"`` when calculations must stay inside the source
validity interval.

Next steps
----------

* :doc:`materials_and_catalog` explains model types, search, and provenance.
* :doc:`custom_materials` covers arrays, CSV import, coefficients, and export.
* :doc:`thin_films` covers interfaces and multilayer coatings.
* :doc:`examples` contains complete executable workflows.
* :doc:`conventions` records physical and numerical conventions.

