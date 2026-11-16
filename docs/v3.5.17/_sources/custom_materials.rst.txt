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
increasing in strictly positive wavelength. Negative optical constants remain
representable; the configurable evaluation policy below controls diagnostics.

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

Exporting numerical arrays
--------------------------

``wavelength, n, k = sample.to_arrays()`` returns independent arrays suitable
for numerical tools. Wavelengths carry micrometre units. Separate n and k grids
are combined within their overlapping range, including both bounds. Missing n
is represented by 1 and missing k by 0. Linear interpolation of these arrays
preserves the source curves inside the exported range. For pchip materials,
these are samples; linear interpolation does not preserve the cubic curve.

CSV columns may be absent, but empty cells in present columns raise
``ValueError`` with their line number. Use ``missing_k=0.0`` in ``from_csv``
when empty extinction cells explicitly mean zero. Empty n cells always raise;
a missing first value never causes the remaining column to be discarded.
Formula wavelength bounds must also be strictly positive.

Physical validation policies
----------------------------

Material evaluation and ``to_arrays`` default to ``validation="warn"``.
A ``MaterialValidationWarning`` reports nonpositive real refractive index or
negative extinction coefficient. With PyOptik's ``n + i*k`` convention, positive
k describes absorption and negative k describes gain. Negative-index and active
materials remain supported through explicit allowances:

.. code-block:: python

   index = sample.compute_refractive_index(
       wavelength=450 * ureg.nanometer,
       validation="raise",
       allow_negative_index=True,
       allow_gain=True,
   )

``validation="ignore"`` suppresses these physical-assumption diagnostics;
``"raise"`` turns them into ``ValueError``. These options are also forwarded by
``nk``, ``n``, ``k`` and the other evaluation helpers. Diagnostics occur when
values are evaluated or exported, not merely when data is loaded. Checks cover
only those samples; they do not prove causality or validity at every wavelength.
Nonempty, finite results and positive, finite wavelengths are required under
all policies, including ``"ignore"``. Dataset construction also rejects
nonfinite values and nonpositive wavelengths.

Standalone arrays can use the same implementation:

.. code-block:: python

   from PyOptik import validate_refractive_indices, validate_wavelengths

   indices = validate_refractive_indices(
       values=[1.45 + 0.01j, 1.50 + 0.02j],
       policy="raise",
   )
   validate_wavelengths(wavelength=[400, 500] * ureg.nanometer)

``validate_refractive_indices`` returns a complex NumPy array with the input
shape. Its default tolerance of ``1e-12`` applies only to tiny negative
extinction coefficients, and can be overridden with ``tolerance``. Negative
real indices are never silently clamped. ``allow_negative_index=True`` also
permits zero real index, including purely imaginary indices. Empty samples,
nonfinite samples, invalid policies, and invalid tolerances always raise.
