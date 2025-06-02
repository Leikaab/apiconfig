apiconfig.auth
==============

.. automodule:: apiconfig.auth
   :members:
   :undoc-members:
   :show-inheritance:

Auth Strategy Refresh Interface
==============================

The enhanced AuthStrategy base class now supports refresh capabilities for handling token expiration and re-authentication scenarios.

.. automethod:: apiconfig.auth.base.AuthStrategy.can_refresh
.. automethod:: apiconfig.auth.base.AuthStrategy.refresh
.. automethod:: apiconfig.auth.base.AuthStrategy.is_expired
.. automethod:: apiconfig.auth.base.AuthStrategy.get_refresh_callback

Refresh Callback Integration
----------------------------

The refresh callback interface is designed for integration with HTTP client retry logic:

.. code-block:: python

    # Get refresh callback for integration with retry logic
    auth_strategy = BearerAuth(token="your_token", refresh_token="refresh_token")
    refresh_callback = auth_strategy.get_refresh_callback()

    if refresh_callback:
        # Use with crudclient or similar retry mechanisms
        client.request_with_retry(url, setup_auth_func=refresh_callback)