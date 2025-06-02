Getting Started
==============

This guide will help you get started with ``apiconfig`` quickly. We'll cover the basics of configuring an API client and using authentication strategies.

Basic Configuration
-----------------

The core of ``apiconfig`` is the ``ClientConfig`` class, which manages all configuration for your API client:

.. code-block:: python

   from apiconfig import ClientConfig

   # Create a basic configuration
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       headers={"X-My-Header": "value"},
       timeout=10.0,
       retries=3,
   )

   # Access the base URL
   print(config.base_url)  # https://api.example.com/v1

Authentication
-------------

``apiconfig`` supports multiple authentication strategies:

API Key Authentication
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apiconfig import ClientConfig, ApiKeyAuth

   # API Key in header
   auth = ApiKeyAuth(api_key="my-secret-key", header_name="X-API-Key")
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       auth_strategy=auth,
   )

   # API Key in query parameter
   auth = ApiKeyAuth(api_key="my-secret-key", param_name="api_key")

Basic Authentication
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apiconfig import ClientConfig, BasicAuth

   auth = BasicAuth(username="user", password="pass")
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       auth_strategy=auth,
   )

Bearer Token Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apiconfig import ClientConfig, BearerAuth

   auth = BearerAuth(token="my-jwt-token")
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       auth_strategy=auth,
   )

Custom Authentication
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apiconfig import ClientConfig, CustomAuth

   auth = CustomAuth(auth_callable=lambda: {"Authorization": "Custom xyz"})
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       auth_strategy=auth,
   )

Loading Configuration
-------------------

``apiconfig`` provides several ways to load configuration:

From Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apiconfig import EnvProvider, ClientConfig

   # Load from environment variables with prefix
   env = EnvProvider(prefix="MYAPI_")
   config_dict = env.load()

   # Create config from loaded values
   config = ClientConfig(**config_dict)

From a File
~~~~~~~~~~

.. code-block:: python

   from apiconfig import FileProvider, ClientConfig

   # Load from a JSON file
   file_provider = FileProvider(filepath="config.json")
   config_dict = file_provider.load()

   # Create config from loaded values
   config = ClientConfig(**config_dict)

Using with HTTP Clients
---------------------

``apiconfig`` works with any HTTP client. Here's an example with ``httpx``:

.. code-block:: python

   import httpx
   from apiconfig import ClientConfig, BearerAuth

   # Set up configuration
   auth = BearerAuth(token="my-jwt-token")
   config = ClientConfig(
       hostname="api.example.com",
       version="v1",
       auth_strategy=auth,
   )

   # Prepare request headers
   headers = {}
   if config.auth_strategy:
       headers.update(config.auth_strategy.prepare_request_headers())

   # Make a request
   with httpx.Client(timeout=config.timeout) as client:
       response = client.get(f"{config.base_url}/resource", headers=headers)
       data = response.json()

Next Steps
---------

Now that you understand the basics, check out the :doc:`user_guide` for more detailed information and advanced usage patterns.