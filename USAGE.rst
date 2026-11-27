PyOptik usage guide
===================

First calculation
-----------------

Load a material by name and evaluate its refractive index at a wavelength with
units:

.. code-block:: python

   from PyOptik import material
   from TypedUnit import ureg

   bk7 = material("N-BK7")
   print(bk7.n(532 * ureg.nanometer))
   print(bk7.catalog_id)  # specs/SCHOTT-optical/N-BK7
   bk7.plot()

The first lookup needs an internet connection. The catalog preserves source
identity: use ``material("main/Au/Johnson")`` to select a specific dataset,
or ``find_materials("gold")`` to explore candidates. See the
`materials guide <https://martinpdes.github.io/PyOptik/docs/latest/materials_and_catalog.html>`_
for defaults, source selection, and provenance.

Interfaces and thin films
-------------------------

An ideal coating can also be calculated without downloading material data:

.. code-block:: python

   import numpy as np
   from PyOptik import ThinFilmLayer, thin_film_stack
   from TypedUnit import ureg

   wavelengths = np.linspace(350, 900, 600) * ureg.nanometer
   coating_index = np.sqrt(1.52)
   coating = ThinFilmLayer(coating_index, 550 * ureg.nanometer / (4 * coating_index))
   result = thin_film_stack(wavelengths, [coating], substrate_index=1.52)
   print(result.reflectance)

The stack model assumes coherent, isotropic layers; it does not model surface
roughness, anisotropy, or incoherent thick substrates. See the
`interfaces and thin films guide <https://martinpdes.github.io/PyOptik/docs/latest/thin_films.html>`_.

Citing PyOptik
--------------

If you use PyOptik in research, please cite the software using the metadata in
`CITATION.cff <https://github.com/MartinPdeS/PyOptik/blob/master/CITATION.cff>`_.
Also cite the RefractiveIndex.INFO database and the original sources for the
material datasets used in your work; source details are available through
``catalog_id`` and ``provenance``.
