CrudClient Integration Guide
============================

This guide shows how to integrate apiconfig authentication strategies with
crudclient's retry mechanisms for robust API client implementations.

Basic Integration
-----------------

.. code-block:: python

    from apiconfig.auth.strategies import BearerAuth
    from crudclient import CrudClient

    # Set up auth strategy with refresh capabilities
    def make_http_request(method, url, headers=None, data=None):
        import requests
        return requests.request(method, url, headers=headers, json=data)

    auth_strategy = BearerAuth(
        token="your_access_token",
        refresh_token="your_refresh_token",
        token_url="https://api.example.com/oauth/token",
        http_request_callable=make_http_request
    )

    # Create crudclient with auth refresh integration
    client = CrudClient(base_url="https://api.example.com")

    # Get refresh callback for retry integration
    refresh_callback = auth_strategy.get_refresh_callback()

    # Make requests with automatic auth refresh on 401 errors
    response = client.request_with_retry(
        "GET", "/protected-endpoint",
        headers=auth_strategy.prepare_request_headers(),
        setup_auth_func=refresh_callback
    )

Advanced Integration with Custom Configuration
-----------------------------------------------

.. code-block:: python

    from apiconfig.config import ConfigManager
    from apiconfig.config.providers import EnvConfigProvider
    from apiconfig.auth.strategies import BearerAuth

    # Load configuration
    config_manager = ConfigManager()
    config_manager.add_provider(EnvConfigProvider())
    config = config_manager.get_config()

    # Set up auth with configuration
    auth_strategy = BearerAuth(
        token=config["access_token"],
        refresh_token=config["refresh_token"],
        token_url=config["token_url"],
        http_request_callable=make_http_request
    )

    # Use with crudclient
    client = CrudClient(
        base_url=config["api_base_url"],
        default_headers=auth_strategy.prepare_request_headers()
    )

Tripletex Example
-----------------

.. code-block:: python

    from helpers_for_tests.tripletex import TripletexSessionAuth
    from crudclient import CrudClient

    # Set up Tripletex session auth with refresh
    auth_strategy = TripletexSessionAuth(
        consumer_token="your_consumer_token",
        employee_token="your_employee_token",
        company_id="your_company_id",
        session_token_hostname="tripletex.no",
        http_request_callable=make_http_request
    )

    # Create client with Tripletex auth
    client = CrudClient(base_url="https://tripletex.no/v2")

    # Make authenticated requests with auto-refresh
    countries = client.get(
        "/country",
        headers=auth_strategy.prepare_request_headers(),
        setup_auth_func=auth_strategy.get_refresh_callback()
    )