PyOptik documentation
=====================

**PyOptik** is a unit-aware Python toolkit for optical material data,
dispersion, Fresnel interfaces, and coherent thin-film stacks. It combines a
searchable RefractiveIndex.INFO catalog with APIs for measured and fitted
materials.

Start with a plot
-----------------

* :doc:`Calculate silica group index and dispersion <tutorials/silica_dispersion>`.
* :doc:`Plot gold's refractive index and extinction coefficient <tutorials/gold_optical_constants>`.
* :doc:`Design an antireflection coating <tutorials/antireflection_coating>`.

Each tutorial includes a complete script and an **Open in Colab** notebook.

.. list-table::
   :widths: 28 72

   * - :doc:`Getting started <getting_started>`
     - Install the package, download the catalog, and calculate refractive
       index with explicit wavelength units.
   * - :doc:`Example gallery <examples>`
     - Follow executable examples for dispersion, custom data, interfaces,
       coatings, pulse properties, and catalog search.
   * - :doc:`Interfaces and thin films <thin_films>`
     - Calculate Fresnel coefficients and coherent multilayer spectra for s and
       p polarization.
   * - :doc:`Custom materials <custom_materials>`
     - Construct materials from arrays, CSV files, or formula coefficients and
       export validated YAML.

Quick example
-------------

.. code-block:: python

   from TypedUnit import ureg
   from PyOptik import material, fresnel_coefficients

   glass = material("N-BK7")

   wavelength = 550 * ureg.nanometer
   index = glass.compute_refractive_index(wavelength)
   interface = fresnel_coefficients(1.0, glass, wavelength=wavelength)

   print(index)
   print(interface.reflectance)

.. toctree::
   :maxdepth: 2

   getting_started
   tutorials
   user_guide
   examples
   code
   references
