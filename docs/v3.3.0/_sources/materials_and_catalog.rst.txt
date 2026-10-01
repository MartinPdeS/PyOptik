Materials and catalog
=====================

Material models
---------------

PyOptik exposes one calculation interface for two source representations:

``SellmeierMaterial``
   Evaluates RefractiveIndex.INFO formula types 1 through 9. Formula datasets
   are compact and provide smooth dispersion within their stated range.

``TabulatedMaterial``
   Interpolates measured real index ``n``, extinction coefficient ``k``, or
   combined ``nk`` tables. Linear interpolation is the default; monotonic PCHIP
   is available with ``interpolation="pchip"``.

Both support scalar and array wavelengths, provenance, validity policies,
derived optical quantities, and plotting.

Find a material by name
-----------------------

The ``material(...)`` shortcut accepts common names, chemical formulas, and
canonical IDs. Use it with familiar terms while retaining dataset provenance:

.. code-block:: python

   from PyOptik import material, find_materials
   from TypedUnit import ureg

   glass = material("BK7")
   gold = material("gold")
   silica = material("SiO2")
   water = material("water")
   print(gold.nk(633 * ureg.nm))
   print(gold.provenance)

Supported family aliases include gold/Au, silver/Ag, silicon/Si,
silica/fused silica/SiO2, and water/H2O. Case, accents, spaces, and
punctuation are normalized for alias and exact source matching. ``BK7``
and ``N-BK7`` explicitly refer to ``specs/SCHOTT-optical/N-BK7``; this is
a naming convention, not a claim that every BK7-type glass is identical.
Common names use these fixed source choices. They are convenience defaults,
not a ranking of measurement quality:

.. list-table:: Documented default datasets
   :header-rows: 1
   :widths: 30 45 25

   * - Names
     - Canonical dataset
     - Source
   * - silica, fused silica, SiO2
     - ``main/SiO2/Malitson``
     - Malitson (1965)
   * - gold, Au
     - ``main/Au/Johnson``
     - Johnson and Christy (1972)
   * - silver, Ag
     - ``main/Ag/Johnson``
     - Johnson and Christy (1972)
   * - water, H2O
     - ``main/H2O/Hale``
     - Hale and Querry (1973)
   * - BK7, N-BK7
     - ``specs/SCHOTT-optical/N-BK7``
     - SCHOTT

``catalog_id`` and ``provenance`` expose the resolved source on every loaded
model. For reproducible work, record that identity, the source reference,
and the snapshot version/checksum. Pass a canonical ID to pin the page.
If a documented default is missing from a custom catalog, the lookup raises
an error; it never substitutes another measurement. Silicon/Si has no
convenience default and requires a source when its family is ambiguous.

Other queries first match an exact catalog book or page name, then use
case-insensitive catalog text search. Spelling suggestions are offered for
unknown names; they are never loaded automatically.

Choose a scientific source
~~~~~~~~~~~~~~~~~~~~~~~~~~

Different measurements of the same material can have different wavelength
ranges, temperatures, phases, or fabrication conditions. A supplied ``source``
always overrides the convenience default. ``find_materials`` always lists all
matching datasets, even for a name with a default:


.. code-block:: python

   for page in find_materials("Au"):
       print(page.id.key, page.description)

   # An exact page ID takes precedence over partial source matches.
   gold = material("Au", source="Johnson")
   same_gold = material("main/Au/Johnson")

Pass ``use_default=False`` to require a source when several datasets match:

.. code-block:: python

   from PyOptik import AmbiguousMaterialError

   try:
       gold = material("Au", use_default=False)
   except AmbiguousMaterialError as error:
       print(error)  # Lists dataset descriptions, canonical IDs, and selection syntax.

Names without a documented default also raise this error when ambiguous.
``source`` accepts an exact page ID, canonical ID, or text from the catalog
source description. If the text still matches several pages (for example,
several temperatures from the same author), the lookup remains ambiguous.
Use the complete page ID or canonical path to select a specific measurement.
``find_materials`` returns pages without loading models; ambiguity exceptions
also expose these pages in their ``candidates`` attribute.

An existing local catalog is read without a network request. If no index
exists, the first lookup downloads the upstream snapshot. Missing selected
page data raises the existing setup error. Specify ``data_root`` for a custom
cache or ``catalog`` for an existing, fully offline catalog:

.. code-block:: python

   from PyOptik import MaterialCatalog

   catalog = MaterialCatalog.from_snapshot(data_root="./optical-data")
   gold = material("Au", source="Johnson", catalog=catalog, interpolation="pchip")

``load_material(...)`` is equivalent to ``material(...)``. The existing
``PyOptik.material`` package remains importable for code using material classes
or submodules.

Catalog organization
--------------------

RefractiveIndex.INFO organizes pages as ``shelf / book / page``. PyOptik keeps
that complete identity to prevent short-name collisions:

.. code-block:: python

   from PyOptik import MaterialCatalog

   catalog = MaterialCatalog.from_snapshot()
   page = catalog.get("main/Si/Aspnes")
   silicon = page.load(interpolation="pchip")

Search and selection
--------------------

Search matches canonical IDs, names, descriptions, and source URLs. Filters
can narrow results by shelf, book, reference text, or local availability:

.. code-block:: python

   matches = catalog.search("BK7", shelf="specs", available=True)
   for page in matches:
       print(page.id, page.description)

Use :doc:`catalog_browser` for the same workflow in an interactive terminal.

Provenance and integrity
------------------------

Catalog pages and loaded materials retain complementary provenance records:

.. code-block:: python

   page_record = page.provenance()
   material_record = page.load().provenance
   integrity = catalog.verify_integrity()

These records include canonical identity, source URL, local path, scientific
reference, experimental conditions, comments, and validity range where
available. Set ``PYOPTIK_DATA_DIR`` or pass ``data_root=...`` for a custom
snapshot location.

