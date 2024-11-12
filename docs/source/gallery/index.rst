:orphan:

.. _examples_gallery:

Examples Gallery
================

Welcome to the PyOptik Examples Gallery. Here you will find a collection of examples that demonstrate the versatility and power of PyOptik.
These examples range from simple introductory use cases to more advanced, application-specific tutorials.

The gallery includes:

- **Basic API Usage**: Learn how to get started with PyOptik, covering fundamental operations and core functionalities of the library.

- **Application Tutorials**: Follow step-by-step guides that show how PyOptik can be used in practical, real-world scenarios, such as:

  - **Simulating Optical Properties**: Understand how to simulate the optical properties of various materials, including refractive index and absorption characteristics.

  - **Fiber Optic Analysis**: See how PyOptik can be utilized for fiber optics simulations, providing insights into light propagation and mode analysis.

  - **Biomedical Imaging Applications**: Discover how PyOptik can be leveraged for imaging purposes, including applications in biomedical optics.

These examples are designed to help users at all levels, whether you are a beginner learning how to use the basic API or an experienced user looking for guidance on more advanced use cases.

Explore the gallery and unlock the potential of PyOptik for your optical simulations and research!


.. toctree::
    :maxdepth: 2
    :hidden:

    sellmeier/index.rst
    tabulated/index.rst
    utils/index.rst




.. raw:: html

    <div class="sphx-glr-thumbnails">


.. raw:: html

    </div>

Examples: Sellmeier Material
============================

This folder contains examples that demonstrate how to use the `SellmeierMaterial` class from the PyOptik library. These examples illustrate the practical applications of modeling materials using the Sellmeier equation, which is commonly used in optical design to determine the refractive index of various materials.

Contents
--------

- **Basic Sellmeier Calculation**: Shows how to instantiate the `SellmeierMaterial` class and calculate the refractive index for different wavelengths.
- **Plotting Refractive Index**: Demonstrates how to visualize the refractive index as a function of wavelength using the `plot` method.
- **Application Example**: Provides an example of how to use the Sellmeier model in a more advanced optical simulation or analysis.

Usage
-----

To run these examples, make sure you have installed all required dependencies as outlined in the main `PyOptik` README. Navigate to this folder and execute the Python scripts as follows:



.. raw:: html

    <div class="sphx-glr-thumbnails">


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates the usage of the PyOptik library to calculate and plot the refractive ...">

.. only:: html

  .. image:: /gallery/sellmeier/images/thumb/sphx_glr_plot_bk7_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_sellmeier_plot_bk7.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot the Refractive Index of Optical Material: BK7</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates the usage of the PyOptik library to calculate and plot the refractive ...">

.. only:: html

  .. image:: /gallery/sellmeier/images/thumb/sphx_glr_plot_silica_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_sellmeier_plot_silica.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot the Refractive Index of Optical Material: Silica</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates the usage of the PyOptik library to calculate and plot the refractive ...">

.. only:: html

  .. image:: /gallery/sellmeier/images/thumb/sphx_glr_plot_water_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_sellmeier_plot_water.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot the Refractive Index of Optical Material: Water</div>
    </div>


.. raw:: html

    </div>

Examples: Tabulated Material
============================

This folder contains examples demonstrating how to use the `TabulatedMaterial` class from the PyOptik library.
These examples illustrate the practical applications of working with tabulated refractive index and absorption data, which is useful for analyzing materials based on empirical measurements.

Contents
--------

- **Basic Tabulated Material Usage**: Shows how to create an instance of the `TabulatedMaterial` class and access the refractive index and absorption values.
- **Interpolating Refractive Index**: Demonstrates how to interpolate the refractive index and absorption values for a given range of wavelengths.
- **Visualization Example**: Provides an example of plotting the refractive index and absorption over a range of wavelengths using the `plot` method.




.. raw:: html

    <div class="sphx-glr-thumbnails">


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates the usage of the PyOptik library to calculate and plot the refractive ...">

.. only:: html

  .. image:: /gallery/tabulated/images/thumb/sphx_glr_plot_sf5_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_tabulated_plot_sf5.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot the Refractive Index of Optical Material: SF5</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates the usage of the PyOptik library to calculate and plot the refractive ...">

.. only:: html

  .. image:: /gallery/tabulated/images/thumb/sphx_glr_plot_silver_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_tabulated_plot_silver.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot the Refractive Index of Optical Material: Silver</div>
    </div>


.. raw:: html

    </div>

Examples: Utility Functions
===========================

This folder contains examples demonstrating the various utility functions provided by the `PyOptik.utils` module.
These utilities are designed to facilitate common tasks such as managing directories, downloading necessary data, and creating custom material definitions.
The examples provided here aim to help you leverage these utilities effectively in your workflows.



.. raw:: html

    <div class="sphx-glr-thumbnails">


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to build a material library using the build_library function from...">

.. only:: html

  .. image:: /gallery/utils/images/thumb/sphx_glr_build_library_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_utils_build_library.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Building database and Printing Materials</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to create a custom Sellmeier YAML file using the create_sellmeier...">

.. only:: html

  .. image:: /gallery/utils/images/thumb/sphx_glr_create_sellmeier_file_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_utils_create_sellmeier_file.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example: Create a Custom Sellmeier YAML File</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to create a custom YAML file containing tabulated nk data using t...">

.. only:: html

  .. image:: /gallery/utils/images/thumb/sphx_glr_create_tabulated_file_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_utils_create_tabulated_file.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example: Create a Custom Tabulated Data YAML File</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to download a YAML file from a URL using the download_yml_file fu...">

.. only:: html

  .. image:: /gallery/utils/images/thumb/sphx_glr_download_yml_file_thumb.png
    :alt:

  :ref:`sphx_glr_gallery_utils_download_yml_file.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example: Download a YAML file</div>
    </div>


.. raw:: html

    </div>


.. toctree::
   :hidden:
   :includehidden:


   /gallery/sellmeier/index.rst
   /gallery/tabulated/index.rst
   /gallery/utils/index.rst



.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
