

.. _source_code:

API reference
=============

This page documents the public classes and functions. For task-oriented
introductions, begin with :doc:`getting_started` or :doc:`examples`.

Public API
----------

Below, you will find detailed, automatically generated documentation for significant classes and functions in the `PyOptik` library. These descriptions are intended to help you understand how each class and function fits into the overall framework, and how to utilize them effectively in your projects.


Catalog
~~~~~~~

PyOptik preserves the upstream ``shelf / book / page`` organization used by
RefractiveIndex.INFO. The catalog API is useful when source provenance matters
or when downloading a complete material collection.

.. autoclass:: PyOptik.MaterialId
    :members:

.. autoclass:: PyOptik.MaterialPage
    :members:

.. autoclass:: PyOptik.MaterialCatalog
    :members:

.. autofunction:: PyOptik.download_snapshot


Material models
~~~~~~~~~~~~~~~


Sellmeier material
^^^^^^^^^^^^^^^^^^

The `SellmeierMaterial` class extends the `Material` base class to handle materials defined by the Sellmeier equation. It allows for precise modeling of refractive indices using parameters from the Sellmeier formula, which is essential for optical design and simulation.

.. autoclass:: PyOptik.SellmeierMaterial
    :members:
    :member-order: bysource
    :show-inheritance:
    :undoc-members:



Tabulated material
^^^^^^^^^^^^^^^^^^

The `TabulatedMaterial` class extends the `Material` base class to handle materials characterized by tabulated refractive index and absorption values. This class is particularly useful when working with empirical data from experiments or literature.

.. autoclass:: PyOptik.TabulatedMaterial
    :members:
    :member-order: bysource
    :show-inheritance:
    :undoc-members:


Base material
^^^^^^^^^^^^^

.. autoclass:: PyOptik.material.base_class.BaseMaterial
    :members:
    :member-order: bysource
    :show-inheritance:


Typed material documents
~~~~~~~~~~~~~~~~~~~~~~~~

These immutable data objects provide the validated representation shared by
catalog loading, user-defined material construction, and YAML export.

.. autoclass:: PyOptik.MaterialMetadata
    :members:

.. autoclass:: PyOptik.FormulaDataset
    :members:

.. autoclass:: PyOptik.TabulatedDataset
    :members:

.. autoclass:: PyOptik.MaterialDocument
    :members:

.. autofunction:: PyOptik.parse_material


Interface and thin-film optics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PyOptik.FresnelResult
    :members:

.. autoclass:: PyOptik.ThinFilmLayer
    :members:

.. autoclass:: PyOptik.ThinFilmResult
    :members:

.. autofunction:: PyOptik.fresnel_coefficients

.. autofunction:: PyOptik.brewster_angle

.. autofunction:: PyOptik.critical_angle

.. autofunction:: PyOptik.thin_film_stack


Enumerations
~~~~~~~~~~~~

.. autoclass:: PyOptik.MaterialType
    :members:
