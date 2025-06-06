Installation
===========

This guide will help you install the ``apiconfig`` package and its dependencies.

Requirements
-----------

- Python 3.11 or higher
- pip or Poetry (recommended)

Installing with pip
------------------

You can install ``apiconfig`` directly from PyPI:

.. code-block:: bash

   pip install apiconfig

Installing with Poetry
---------------------

If you're using Poetry for dependency management (recommended), you can add ``apiconfig`` to your project:

.. code-block:: bash

   poetry add apiconfig

Development Installation
-----------------------

For development or contributing to the project, clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/Leikaab/apiconfig.git
   cd apiconfig
   poetry install --with dev,docs

Verifying Installation
---------------------

You can verify that ``apiconfig`` is installed correctly by importing it in Python:

.. code-block:: python

   import apiconfig
   print(apiconfig.__version__)

Next Steps
---------

Once you have installed ``apiconfig``, check out the :doc:`getting_started` guide to learn how to use it.