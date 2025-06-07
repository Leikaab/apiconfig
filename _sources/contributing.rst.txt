Contributing
===========

Thank you for your interest in contributing to ``apiconfig``! This guide will help you get started with contributing to the project.

Setting Up the Development Environment
------------------------------------

Prerequisites
~~~~~~~~~~~

- Python 3.11 or higher
- Poetry (for dependency management)
- Docker (for Dev Containers, recommended)
- Visual Studio Code (for Dev Containers, recommended)

Clone the Repository
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/Leikaab/apiconfig.git
   cd apiconfig

Using Dev Containers (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project includes a Dev Container configuration that provides a pre-configured Docker container as a fully-featured development environment:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. Wait for the container to build (first time only)
4. Develop inside the container

Manual Setup
~~~~~~~~~~

If you prefer not to use Dev Containers:

.. code-block:: bash

   # Install dependencies
   poetry install --with dev,docs

   # Activate the virtual environment
   poetry shell

   # Install pre-commit hooks
   pre-commit install
   pre-commit install --hook-type pre-push

Running Tests
-----------

Unit Tests
~~~~~~~~~

.. code-block:: bash

   pytest tests/unit

Integration Tests
~~~~~~~~~~~~~~

Integration tests require API credentials. Copy ``.env.example`` to ``.env`` and fill in your secrets:

.. code-block:: bash

   pytest tests/integration

Coverage
~~~~~~~

.. code-block:: bash

   # Generate coverage report
   pytest tests/unit/ --cov=apiconfig --cov-report=html

   # Open the report
   open htmlcov/index.html

Code Style and Quality
--------------------

The project uses several tools to maintain code quality:

- **Black:** Code formatting
- **isort:** Import sorting
- **Flake8:** Linting
- **Mypy:** Static type checking

These are all run automatically via pre-commit hooks.

Branching Strategy
---------------

We follow the Gitflow branching model:

- **main:** Latest stable release (protected)
- **develop:** Latest development changes (protected)
- **feature/*:** New features/fixes (branch from ``develop``)
- **release/*:** Release preparation (branch from ``develop``)
- **hotfix/*:** Critical production fixes (branch from ``main``)

For most contributions, create a ``feature/*`` branch from ``develop``.

Commit Message Guidelines
----------------------

Follow the `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_ specification:

.. code-block:: text

   feat: add environment variable configuration provider
   fix: handle missing keys gracefully in dict provider
   docs: update CONTRIBUTING.md with Gitflow model
   refactor: simplify ClientConfig merging logic
   test: add unit tests for custom AuthStrategy
   chore: update pre-commit hook versions

Pull Request Process
-----------------

1. Ensure all pre-commit and pre-push checks pass
2. Push your ``feature/*`` branch to your fork
3. Create a PR targeting ``develop``
4. Provide a clear description and link relevant issues
5. Pass all CI checks
6. Address code review feedback

Documentation
-----------

When contributing new features or changes, please update the documentation:

1. Update docstrings in the code
2. Add or update relevant sections in the documentation
3. Add examples if applicable

Building the Documentation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Navigate to the docs directory
   cd docs

   # Build the documentation
   make html

   # Open the documentation
   open build/html/index.html

Release Process
------------

Releases are managed via GitHub Actions:

- Merging to ``develop`` triggers a pre-release to PyPI
- Merging to ``main`` triggers a stable release to PyPI (if version is bumped in ``pyproject.toml``)

For more details, see the `CONTRIBUTING.md <https://github.com/Leikaab/apiconfig/blob/main/CONTRIBUTING.md>`_ file in the repository.