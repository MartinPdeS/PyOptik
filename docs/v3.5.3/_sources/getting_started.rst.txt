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

Use a familiar glass name and attach units to every wavelength:

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import material

   glass = material("N-BK7")
   wavelength = 550 * ureg.nanometer
   print(glass.n(wavelength))
   print(glass.catalog_id)  # specs/SCHOTT-optical/N-BK7

``BK7`` and ``N-BK7`` select SCHOTT N-BK7. Common material names also have
documented sources, so a first calculation needs no catalog browsing:

.. code-block:: python

   silica = material("fused silica")  # main/SiO2/Malitson
   gold = material("gold")  # main/Au/Johnson
   print(gold.nk(633 * ureg.nm))

Pass ``source="Rakic-LD"`` to choose another gold dataset. Use
``material("Au", use_default=False)`` to require an explicit source; if
several datasets match it raises ``AmbiguousMaterialError`` with descriptions
and canonical IDs. Names without a documented default follow the same rule.
Defaults never depend on catalog ordering or cache availability. See
:doc:`materials_and_catalog` for the default-source table and discovery.

The shortcut downloads a snapshot if no local catalog exists. Subsequent
lookups use the local index. To repair an incomplete cache, run
``pyoptik setup`` again.

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

