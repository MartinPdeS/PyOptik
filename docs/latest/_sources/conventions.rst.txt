Physical conventions and data provenance
========================================

Wavelength and optical constants
--------------------------------

PyOptik accepts vacuum wavelength quantities. Always attach units—for example
``1550 * ureg.nanometer``—to avoid ambiguity. Bare numeric inputs are retained
for compatibility and interpreted as metres.

The complex refractive index uses the convention ``N = n + i k``: ``n`` is the
real refractive index and ``k`` is the non-negative extinction coefficient.
The convenience methods ``material.n(wavelength)``, ``material.k(wavelength)``,
``material.relative_permittivity(wavelength)``, and
``material.absorption_coefficient(wavelength)`` expose common derived values.
The relative permittivity is ``N²`` and the intensity absorption coefficient is
``α = 4πk / λ``.

Dispersion and group delay
--------------------------

``compute_group_delay_dispersion`` returns conventional frequency-domain GDD,
``dτ_g/dω = d²β/dω² × length``. Its units are time squared (typically fs²).
``compute_group_delay_wavelength_slope`` is deliberately separate because it
returns ``dτ_g/dλ``, a wavelength-space derivative with different units.

Interpolation and validity ranges
---------------------------------

Tabulated materials use linear interpolation by default. Pass
``interpolation="pchip"`` to ``MaterialPage.load`` or ``TabulatedMaterial`` for
monotonic piecewise-cubic interpolation without overshoot. Both methods use
linear endpoint extrapolation when ``out_of_range="warn"``; set
``out_of_range="raise"`` for strict validity enforcement, or
``out_of_range="clip"`` to evaluate at the nearest source boundary.

Provenance and conditions
-------------------------

Every loaded material provides ``material.provenance``. It contains the source
reference, upstream catalog ID and URL when available, source path, stated
wavelength range, and the upstream YAML ``CONDITIONS`` and ``COMMENTS`` fields.
Use it when recording simulation inputs or preparing results for publication.

.. code-block:: python

   page = catalog.get("specs/SCHOTT-optical/N-BK7")
   material = page.load()
   print(material.provenance)
