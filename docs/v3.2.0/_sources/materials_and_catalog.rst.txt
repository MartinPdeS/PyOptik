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

