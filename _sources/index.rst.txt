Welcome to apiconfig's documentation!
=====================================

.. note::

   The latest documentation is always available at https://leikaab.github.io/apiconfig/


**apiconfig** is a standalone Python library for managing API client configuration and authentication. It provides a robust, extensible foundation for building API clients, handling configuration (base URLs, timeouts, retries, headers) and supporting multiple authentication strategies (API key, Basic, Bearer, custom).

.. image:: https://img.shields.io/pypi/pyversions/apiconfig
   :target: https://pypi.org/project/apiconfig/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/v/apiconfig
   :target: https://pypi.org/project/apiconfig/
   :alt: PyPI - Version

.. image:: https://github.com/Leikaab/apiconfig/actions/workflows/tests.yaml/badge.svg
   :target: https://github.com/Leikaab/apiconfig/actions/workflows/tests.yaml
   :alt: Test Status

.. image:: https://github.com/Leikaab/apiconfig/actions/workflows/publish.yaml/badge.svg
   :target: https://github.com/Leikaab/apiconfig/actions/workflows/publish.yaml
   :alt: Publish to PyPI

Key Features
-----------

- **Unified API Client Configuration**: Manage base URLs, versions, headers, timeouts, retries, and more with a single, validated config object.
- **Authentication Strategies**: Built-in support for API Key, Basic, Bearer, and custom authentication via the Strategy Pattern.
- **Config Providers**: Load configuration from environment variables, files, or in-memory sources.
- **Extensible**: Easily add new authentication methods or config providers.
- **Robust Error Handling**: Clear, structured exception hierarchy for all config and auth errors.
- **Type Safety**: Strong type hints and type-checked public API.
- **Logging Integration**: Standard logging hooks for debugging and auditability.
- **100% Test Coverage**: Fully tested with unit and integration tests.

Quick Example
-----------

.. code-block:: python

   from apiconfig import ClientConfig, ApiKeyAuth
   import httpx

   # Set up authentication
   auth = ApiKeyAuth(api_key="my-secret-key", header_name="X-API-Key")

   # Create configuration
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       auth_strategy=auth,
       timeout=10.0,
   )

   # Use with any HTTP client
   headers = {}
   if config.auth_strategy:
       headers.update(config.auth_strategy.prepare_request_headers())

   with httpx.Client(timeout=config.timeout) as client:
       response = client.get(f"{config.base_url}/resource", headers=headers)
       data = response.json()

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   getting_started
   user_guide
   examples
   contributing

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
