

.. _source_code:

Source Code
===========

Welcome to the PyOptik Source Code Documentation. This section provides a comprehensive overview of the key classes, functions, and utilities available within the `PyOptik` library. Each component is documented in detail, with information on its members, inherited properties, and direct links to the source code.

Class Documentation
===================

Below, you will find detailed, automatically generated documentation for significant classes and functions in the `PyOptik` library. These descriptions are intended to help you understand how each class and function fits into the overall framework, and how to utilize them effectively in your projects.


Catalog and Upstream Hierarchy
------------------------------

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


Material Models
---------------


SellmeierMaterial
-----------------

The `SellmeierMaterial` class extends the `Material` base class to handle materials defined by the Sellmeier equation. It allows for precise modeling of refractive indices using parameters from the Sellmeier formula, which is essential for optical design and simulation.

.. autoclass:: PyOptik.SellmeierMaterial
    :members:
    :member-order: bysource
    :show-inheritance:
    :undoc-members:



TabulatedMaterial
-----------------

The `TabulatedMaterial` class extends the `Material` base class to handle materials characterized by tabulated refractive index and absorption values. This class is particularly useful when working with empirical data from experiments or literature.

.. autoclass:: PyOptik.TabulatedMaterial
    :members:
    :member-order: bysource
    :show-inheritance:
    :undoc-members:


Base Utilities
--------------

.. autoclass:: PyOptik.material.base_class.BaseMaterial
    :members:
    :member-order: bysource
    :show-inheritance:


Enumerations
------------

.. autoclass:: PyOptik.MaterialType
    :members:

Directives for Sphinx Gallery
=============================

To further enhance your understanding of `PyOptik`, we have integrated practical examples throughout the documentation using Sphinx Gallery. These examples demonstrate how to use the library's classes and functions in realistic scenarios.

.. note::
    You can find example usage of the `SellmeierMaterial` and `TabulatedMaterial` classes in the "Examples" section. These examples are automatically generated from the source code and provide hands-on insight into practical applications of the library.
