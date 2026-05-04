

.. _source_code:

Source Code
===========

Welcome to the PyOptik Source Code Documentation. This section provides a comprehensive overview of the key classes, functions, and utilities available within the `PyOptik` library. Each component is documented in detail, with information on its members, inherited properties, and direct links to the source code.

Class Documentation
===================

Below, you will find detailed, automatically generated documentation for significant classes and functions in the `PyOptik` library. These descriptions are intended to help you understand how each class and function fits into the overall framework, and how to utilize them effectively in your projects.


.. _material_bank:

MaterialBank
------------

The `MaterialBank` is the main interface for the user.

.. autoclass:: PyOptik.material_bank._MaterialBank
    :members:
    :member-order: bysource
    :show-inheritance:
    :undoc-members:


.. .. _sellmeier_material:


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

Utility Functions
-----------------

The `PyOptik.utils` module contains various utility functions that facilitate tasks like downloading data files, creating custom material definitions, and managing directories effectively.

.. autofunction:: PyOptik.utils.download_yml_file


Directives for Sphinx Gallery
=============================

To further enhance your understanding of `PyOptik`, we have integrated practical examples throughout the documentation using Sphinx Gallery. These examples demonstrate how to use the library's classes and functions in realistic scenarios.

.. note::
    You can find example usage of the `SellmeierMaterial` and `TabulatedMaterial` classes, as well as utility functions, in the "Examples" section of the documentation. These examples are automatically generated from the source code and provide hands-on insight into the practical applications of the library.

