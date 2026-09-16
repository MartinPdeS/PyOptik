Terminal catalog browser
========================

PyOptik includes an optional full-screen terminal interface for exploring a
downloaded RefractiveIndex.INFO snapshot. It uses Textual and is installed
separately so calculation-only environments do not need terminal UI packages.

Installation and startup
------------------------

.. code-block:: bash

   python -m pip install "PyOptik[ui]"
   pyoptik setup
   pyoptik browse

The browser reads the local snapshot and does not access the network. To open
a snapshot stored elsewhere, pass its data root:

.. code-block:: bash

   pyoptik browse --data-root ./refractiveindex-data

Navigation
----------

The left pane contains a live search field and the matching material pages.
Search covers canonical ``shelf/book/page`` identifiers, names, descriptions,
and source URLs. The right pane displays:

* canonical material identity;
* description and local-cache status;
* local path and upstream source URL;
* the source's scientific or manufacturer reference.

Use the arrow keys or mouse to select a row. Press ``/`` to return to the search
field and ``q`` to quit.

If no snapshot exists, the command reports its expected location and asks you
to run ``pyoptik setup``. The browser never silently downloads or modifies
catalog data.

