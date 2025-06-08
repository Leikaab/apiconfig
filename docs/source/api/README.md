# API Reference

This folder contains the reStructuredText files that make up the
API reference section of the documentation. Each ``.rst`` file
corresponds to a module in ``apiconfig`` and is included by
``index.rst`` to build the full reference guide.

Files include:

- ``auth.rst`` – authentication strategies
- ``config.rst`` – configuration helpers
- ``exceptions.rst`` – error hierarchy
- ``testing.rst`` – utilities for writing tests
- ``utils.rst`` – small helper functions
- ``types.rst`` – typed definitions used across the library

When adding new modules, create a matching ``.rst`` file and list it
in ``index.rst`` so it appears in the generated documentation.
