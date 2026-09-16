Custom materials
================

PyOptik can construct optical materials directly from measured arrays, CSV
files, or dispersion coefficients. Custom materials support the same unit-aware
calculations, interpolation policies, provenance fields, and YAML format as
catalog materials.

Tabulated data from arrays
--------------------------

Attach units to the wavelength axis and provide at least one of ``n`` or ``k``.
The arrays must be one-dimensional, finite, equal in length, and strictly
increasing in wavelength.

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import TabulatedMaterial

   sample = TabulatedMaterial.from_arrays(
       "measured-sample",
       [400, 500, 600] * ureg.nanometer,
       n=[1.40, 1.45, 1.50],
       k=[0.01, 0.02, 0.04],
       reference="Laboratory measurement",
       conditions={"temperature": "293 K"},
       comments="Uncoated sample",
       interpolation="pchip",
   )

   index = sample.compute_refractive_index(550 * ureg.nanometer)
   sample.to_yaml("measured-sample.yml")

When wavelengths do not carry units, they are interpreted as micrometres by
``from_arrays``. Unit-bearing values are recommended.

CSV import
----------

``from_csv`` expects a header row and uses the columns ``wavelength``, ``n``,
and ``k`` by default. Either optical-constant column may be omitted.

.. code-block:: text

   wavelength,n,k
   400,1.40,0.01
   500,1.45,0.02
   600,1.50,0.04

.. code-block:: python

   sample = TabulatedMaterial.from_csv(
       "measurement.csv",
       wavelength_unit=ureg.nanometer,
       reference="Laboratory measurement",
   )

Use ``wavelength_column``, ``n_column``, and ``k_column`` when a file uses
different headers.

Formula materials
-----------------

Formula types 1 through 9 follow the RefractiveIndex.INFO definitions.
Coefficient order therefore follows the selected upstream formula type.

.. code-block:: python

   from PyOptik import SellmeierMaterial

   glass = SellmeierMaterial.from_coefficients(
       "fitted-glass",
       [0.1, 0.2, 0.3],
       formula_type=1,
       wavelength_range=[400, 900] * ureg.nanometer,
       reference="Internal fit",
   )
   glass.to_yaml("fitted-glass.yml")

Typed documents and validation
------------------------------

The lower-level parser returns an immutable ``MaterialDocument`` containing
typed formula or tabulated datasets and shared metadata. It is useful for
validation, inspection, and tools that do not need to evaluate a material.

.. code-block:: python

   from PyOptik import parse_material

   document = parse_material("measured-sample.yml")
   print(document.metadata.reference)
   print(document.tabulated_datasets)

   document.to_yaml("validated-copy.yml")

Malformed coefficient sets, invalid table shapes, non-finite values, unsorted
wavelengths, unsupported formula types, and malformed metadata raise
``ValueError`` with source context. YAML export writes through a temporary file
and atomically replaces the destination after successful serialization.
