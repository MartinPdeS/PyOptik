Interfaces and thin films
=========================

PyOptik provides Fresnel interface calculations and a coherent characteristic-
matrix solver for isotropic multilayer coatings. Refractive indices may be
constant complex numbers or wavelength-dependent PyOptik material models.

Single interfaces
-----------------

``fresnel_coefficients`` returns electric-field amplitude coefficients and
power fractions for s or p polarization. Angles may be Pint/TypedUnit angle
quantities; bare angles are interpreted as radians.

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import fresnel_coefficients

   result = fresnel_coefficients(
       incident_index=1.0,
       transmitted_index=1.5,
       angle=45 * ureg.degree,
       polarization="p",
   )

   print(result.reflection_amplitude)
   print(result.transmission_amplitude)
   print(result.reflectance)
   print(result.transmittance)
   print(result.transmitted_angle.to(ureg.degree))

For a dispersive material, provide the evaluation wavelength:

.. code-block:: python

   glass = catalog.get("specs/SCHOTT-optical/N-BK7").load()
   result = fresnel_coefficients(
       1.0,
       glass,
       wavelength=550 * ureg.nanometer,
       polarization="s",
   )

Characteristic angles
---------------------

``brewster_angle`` returns the p-polarized zero-reflection angle, while
``critical_angle`` returns the onset of total internal reflection.

.. code-block:: python

   from PyOptik import brewster_angle, critical_angle

   brewster = brewster_angle(1.0, 1.5).to(ureg.degree)
   critical = critical_angle(1.5, 1.0).to(ureg.degree)

These helpers require positive, scalar, lossless indices. A critical angle
exists only when the incident index is greater than the transmitted index.

Coherent multilayers
--------------------

Use ``ThinFilmLayer`` for each film, ordered from the incident medium toward
the substrate. A ``(material, thickness)`` tuple is accepted as shorthand.

.. code-block:: python

   import numpy
   from PyOptik import ThinFilmLayer, thin_film_stack

   design_wavelength = 600 * ureg.nanometer
   substrate_index = 1.5
   coating_index = numpy.sqrt(substrate_index)

   coating = ThinFilmLayer(
       material=coating_index,
       thickness=design_wavelength / (4 * coating_index),
   )
   wavelengths = numpy.linspace(450, 750, 301) * ureg.nanometer
   result = thin_film_stack(
       wavelengths,
       [coating],
       incident_index=1.0,
       substrate_index=substrate_index,
       angle=0 * ureg.degree,
       polarization="s",
   )

   # Arrays aligned with ``wavelengths``.
   reflectance = result.reflectance
   transmittance = result.transmittance
   absorptance = result.absorptance

Materials in any layer or bounding medium are evaluated independently at every
wavelength. Positive extinction coefficient ``k`` follows PyOptik's ``n + i k``
convention and contributes positive absorptance.

Model limits
------------

The solver assumes plane waves, homogeneous isotropic non-magnetic layers,
parallel interfaces, and full coherence throughout the stack. It does not yet
include incoherent propagation through thick substrates, graded or anisotropic
layers, surface roughness, scattering, fluorescence, or partial coherence.
Power coefficients are evaluated from the normal optical flux. Numerical
round-off can produce absorptance extremely close to zero for lossless stacks.

