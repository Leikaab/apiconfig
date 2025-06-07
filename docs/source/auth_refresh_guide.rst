Authentication Refresh Guide
============================

This guide explains how to use apiconfig's authentication refresh capabilities
to handle token expiration and re-authentication scenarios.

Overview
--------

Authentication refresh allows your application to automatically handle expired
tokens by refreshing them when needed, without manual intervention. This is
particularly useful for long-running applications and integration with HTTP
client retry mechanisms.

Basic Refresh Pattern
---------------------

.. code-block:: python

    from apiconfig.auth.strategies import BearerAuth
    from apiconfig.auth.token.storage import FileTokenStorage

    # Initialize auth strategy with refresh capabilities
    token_storage = FileTokenStorage("tokens.json")

    def http_request_func(method, url, headers=None, data=None):
        # Your HTTP request implementation
        return requests.request(method, url, headers=headers, data=data)

    auth_strategy = BearerAuth(
        access_token="current_access_token",
        http_request_callable=http_request_func,
    )

    # BearerAuth.refresh() must be implemented by a subclass
    # or by providing custom logic using the HTTP callback.

    # Check if refresh is supported
    if auth_strategy.can_refresh():
        print("Auth strategy supports refresh")

    # Manually refresh if your subclass implements it
    if auth_strategy.can_refresh() and auth_strategy.is_expired():
        result = auth_strategy.refresh()
        if result and result.get("token_data"):
            # Save new tokens
            token_storage.store_token(result["token_data"])

Integration with HTTP Clients
------------------------------

The refresh callback interface is designed for easy integration with HTTP client
retry mechanisms:

.. code-block:: python

    # Get refresh callback
    refresh_callback = auth_strategy.get_refresh_callback()

    # Use with crudclient
    from crudclient import CrudClient

    client = CrudClient(base_url="https://api.example.com")
    response = client.request_with_retry(
        "GET", "/protected-resource",
        setup_auth_func=refresh_callback
    )

Custom Auth Strategy with Refresh
----------------------------------

.. code-block:: python

    from apiconfig.auth.base import AuthStrategy
    from apiconfig.types import TokenRefreshResult, RefreshedTokenData

    class CustomSessionAuth(AuthStrategy):
        def __init__(self, session_token, refresh_endpoint, http_request_callable=None):
            super().__init__(http_request_callable)
            self.session_token = session_token
            self.refresh_endpoint = refresh_endpoint

        def can_refresh(self):
            return self.refresh_endpoint and self._http_request_callable

        def refresh(self):
            if not self.can_refresh():
                return None

            # Implement your refresh logic
            response = self._http_request_callable(
                "POST", self.refresh_endpoint,
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            new_token = response.json()["new_session_token"]
            self.session_token = new_token

            return {
                "token_data": {
                    "access_token": new_token,
                    "token_type": "session"
                },
                "config_updates": None
            }

        def prepare_request_headers(self):
            return {"Authorization": f"Session {self.session_token}"}

        def prepare_request_params(self):
            return {}

Error Handling
--------------

.. code-block:: python

    from apiconfig.exceptions.auth import TokenRefreshError

    try:
        result = auth_strategy.refresh()
    except TokenRefreshError as e:
        print(f"Token refresh failed: {e}")
        # Handle refresh failure (e.g., re-authenticate)