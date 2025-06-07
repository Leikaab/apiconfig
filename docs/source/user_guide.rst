User Guide
=========

This guide provides detailed information about using ``apiconfig`` for various scenarios and advanced use cases.

Configuration Management
----------------------

Merging Configurations
~~~~~~~~~~~~~~~~~~~~~

You can merge multiple configurations to combine settings from different sources:

.. code-block:: python

   from apiconfig import ClientConfig

   # Base configuration with defaults
   base_config = ClientConfig(
       hostname="api.example.com",
       timeout=30.0,
       retries=3,
   )

   # Override specific settings
   override_config = ClientConfig(
       timeout=10.0,
       headers={"X-Custom-Header": "value"},
   )

   # Merge configurations (override takes precedence)
   merged_config = base_config.merge(override_config)

   print(merged_config.hostname)  # api.example.com (from base)
   print(merged_config.timeout)   # 10.0 (from override)
   print(merged_config.retries)   # 3 (from base)

Configuration Providers
~~~~~~~~~~~~~~~~~~~~~

Environment Variables Provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Load configuration from environment variables:

.. code-block:: python

   from apiconfig import EnvProvider

   # With prefix (e.g., MYAPI_HOSTNAME, MYAPI_TIMEOUT)
   env = EnvProvider(prefix="MYAPI_")
   config_dict = env.load()

   # Without prefix (e.g., HOSTNAME, TIMEOUT)
   env = EnvProvider()
   config_dict = env.load()

File Provider
^^^^^^^^^^^

Load configuration from JSON or YAML files:

.. code-block:: python

   from apiconfig import FileProvider

   # JSON file
   json_provider = FileProvider(file_path="config.json")
   json_config = json_provider.load()

   # YAML file
   yaml_provider = FileProvider(file_path="config.yaml")
   yaml_config = yaml_provider.load()

Memory Provider
^^^^^^^^^^^^^

Use in-memory configuration:

.. code-block:: python

   from apiconfig import MemoryProvider

   # Hardcoded configuration
   data = {
       "hostname": "api.example.com",
       "version": "v2",
       "timeout": 15.0,
   }
   memory_provider = MemoryProvider(data=data)
   config_dict = memory_provider.load()

Authentication Strategies
-----------------------

API Key Authentication
~~~~~~~~~~~~~~~~~~~~

API keys can be sent in headers or query parameters:

.. code-block:: python

   from apiconfig import ApiKeyAuth

   # In header
   header_auth = ApiKeyAuth(
       api_key="my-secret-key",
       header_name="X-API-Key",
   )

   # In query parameter
   query_auth = ApiKeyAuth(
       api_key="my-secret-key",
       param_name="api_key",
   )

   # Get headers for a request
   headers = header_auth.prepare_request_headers()
   # {'X-API-Key': 'my-secret-key'}

   # Get query parameters for a request
   params = query_auth.prepare_request_params()
   # {'api_key': 'my-secret-key'}

Basic Authentication
~~~~~~~~~~~~~~~~~~

HTTP Basic Authentication with username and password:

.. code-block:: python

   from apiconfig import BasicAuth

   auth = BasicAuth(username="user", password="pass")

   # Get headers for a request
   headers = auth.prepare_request_headers()
   # {'Authorization': 'Basic dXNlcjpwYXNz'}

Bearer Authentication
~~~~~~~~~~~~~~~~~~~

JWT or OAuth token authentication:

.. code-block:: python

   from apiconfig import BearerAuth

   auth = BearerAuth(access_token="my-jwt-token")

   # Get headers for a request
   headers = auth.prepare_request_headers()
   # {'Authorization': 'Bearer my-jwt-token'}

Custom Authentication
~~~~~~~~~~~~~~~~~~~

For APIs with custom authentication schemes:

.. code-block:: python

   from apiconfig import CustomAuth

   # Using a callable
   def my_auth_function():
       # Complex logic to generate auth headers
       return {"Authorization": "Custom xyz123"}

   auth = CustomAuth(auth_callable=my_auth_function)

   # Get headers for a request
   headers = auth.prepare_request_headers()
   # {'Authorization': 'Custom xyz123'}

Token Management
--------------

Refresh Tokens
~~~~~~~~~~~~

For APIs that use refresh tokens:

.. code-block:: python

   from apiconfig.auth.token import RefreshTokenHandler

   # Define a refresh function
   def refresh_token(refresh_token):
       # Call API to get new tokens
       return {
           "access_token": "new-access-token",
           "refresh_token": "new-refresh-token",
           "expires_in": 3600
       }

   # Create a token handler
   token_handler = RefreshTokenHandler(
       refresh_function=refresh_token,
       initial_access_token="initial-access-token",
       initial_refresh_token="initial-refresh-token",
       expires_in=3600
   )

   # Get current access token
   access_token = token_handler.get_access_token()

   # Force refresh
   new_tokens = token_handler.refresh()

Token Storage
~~~~~~~~~~~

Store tokens securely:

.. code-block:: python

   from apiconfig.auth.token import FileTokenStorage

   # Store tokens in a file
   storage = FileTokenStorage(file_path=".tokens.json")

   # Save tokens
   storage.save({
       "access_token": "my-access-token",
       "refresh_token": "my-refresh-token",
       "expires_at": 1619712000
   })

   # Load tokens
   tokens = storage.load()

Error Handling
------------

``apiconfig`` provides specific exceptions for different error cases:

.. code-block:: python

   from apiconfig import ClientConfig
   from apiconfig.exceptions import (
       ConfigurationError,
       AuthenticationError,
       InvalidConfigError,
   )

   try:
       # This will raise an error if hostname is invalid
       config = ClientConfig(hostname="")
   except InvalidConfigError as e:
       print(f"Invalid configuration: {e}")

   try:
       # This will raise an error if auth strategy is invalid
       from apiconfig import ApiKeyAuth
       auth = ApiKeyAuth(api_key="")
   except AuthenticationError as e:
       print(f"Authentication error: {e}")

Logging
------

``apiconfig`` uses Python's standard logging module:

.. code-block:: python

   import logging
   from apiconfig.utils.logging import setup_logging

   # Basic logging setup
   logging.basicConfig(level=logging.INFO)

   # Or use the built-in helper
   setup_logging(level=logging.DEBUG)

   # Use the logger
   logger = logging.getLogger("apiconfig")
   logger.info("Configuring API client")
   logger.debug("Detailed debug information")

Best Practices
------------

1. **Use environment variables for secrets**:

   .. code-block:: python

      from apiconfig import EnvProvider, ClientConfig, ApiKeyAuth

      # Load API key from environment
      env = EnvProvider(prefix="MYAPI_")
      config_dict = env.load()

      # Create auth strategy with the API key
      auth = ApiKeyAuth(
          api_key=config_dict.get("API_KEY"),
          header_name="X-API-Key",
      )

2. **Separate configuration from client code**:

   .. code-block:: python

      # config.py
      from apiconfig import ClientConfig, BearerAuth, EnvProvider

      def get_config():
          env = EnvProvider(prefix="MYAPI_")
          config_dict = env.load()

        auth = BearerAuth(access_token=config_dict.get("TOKEN"))
          return ClientConfig(
              hostname=config_dict.get("HOSTNAME", "api.default.com"),
              version=config_dict.get("VERSION", "v1"),
              auth_strategy=auth,
          )

      # client.py
      import httpx
      from config import get_config

      def get_resource(resource_id):
          config = get_config()
          headers = {}
          if config.auth_strategy:
              headers.update(config.auth_strategy.prepare_request_headers())

          with httpx.Client(timeout=config.timeout) as client:
              return client.get(
                  f"{config.base_url}/resources/{resource_id}",
                  headers=headers,
              )

3. **Use immutable configurations**:

   Instead of modifying configurations, create new ones with updated values:

   .. code-block:: python

      # Instead of modifying
      config.timeout = 20.0  # Don't do this

      # Create a new config with the updated value
      new_config = ClientConfig(
          hostname=config.hostname,
          version=config.version,
          timeout=20.0,
          auth_strategy=config.auth_strategy,
      )

      # Or use merge
      override = ClientConfig(timeout=20.0)
      new_config = config.merge(override)