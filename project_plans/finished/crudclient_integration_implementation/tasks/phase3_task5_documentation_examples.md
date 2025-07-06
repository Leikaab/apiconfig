# Phase 3, Task 5: Documentation and Examples

## Overview
Update documentation with crudclient integration examples, create user guides for auth refresh patterns, add API documentation for new interfaces, and create migration guide for existing crudclient users.

## Objective
Provide comprehensive documentation that enables users to understand and implement the new auth refresh functionality, with specific focus on crudclient integration patterns and migration guidance.

## Requirements

### 1. API Documentation Updates
Update existing API documentation to include new interfaces:

#### 1.1 Auth Strategy Documentation
Update `docs/source/api/auth.rst` to include:

```rst
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
```

#### 1.2 Type Definitions Documentation
Update `docs/source/api/types.rst` to include:

```rst
Auth Refresh Types
==================

.. autoclass:: apiconfig.types.RefreshedTokenData
.. autoclass:: apiconfig.types.TokenRefreshResult
.. autoclass:: apiconfig.types.HttpRequestContext
.. autoclass:: apiconfig.types.HttpResponseContext

Type Aliases
------------

.. autodata:: apiconfig.types.HttpRequestCallable
.. autodata:: apiconfig.types.AuthRefreshCallback
.. autodata:: apiconfig.types.ResponseBodyType
```

### 2. User Guide for Auth Refresh Patterns
Create new user guide `docs/source/auth_refresh_guide.rst`:

```rst
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
        token="current_access_token",
        refresh_token="current_refresh_token",
        token_url="https://api.example.com/oauth/token",
        http_request_callable=http_request_func
    )

    # Check if refresh is supported
    if auth_strategy.can_refresh():
        print("Auth strategy supports refresh")

    # Manually refresh if needed
    if auth_strategy.is_expired():
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
    import apiconfig.types as api_types

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
```

### 3. CrudClient Integration Examples
Create `docs/source/crudclient_integration.rst`:

```rst
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
    from apiconfig.config.providers import EnvProvider
    from apiconfig.auth.strategies import BearerAuth

    # Load configuration
    config_manager = ConfigManager()
    config_manager.add_provider(EnvProvider())
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
```


## Implementation Steps

1. **Update API documentation** in `docs/source/api/` files
2. **Create new user guides** for auth refresh patterns
3. **Create CrudClient integration guide** with practical examples
4. **Update main documentation index** to include new guides
5. **Add code examples** that can be tested and validated
6. **Review and validate** all documentation for accuracy

## Files to Create/Modify
- `docs/source/api/auth.rst` (update)
- `docs/source/api/types.rst` (update)
- `docs/source/auth_refresh_guide.rst` (new)
- `docs/source/crudclient_integration.rst` (new)
- `docs/source/index.rst` (update to include new guides)

## Dependencies
- All Phase 3 tasks completion
- Working implementation of all auth refresh functionality
- Validated real integration test examples (from Phase 3)

## Quality Gates

### Documentation Quality
- [ ] All new interfaces properly documented
- [ ] Code examples are tested and working
- [ ] Clear, comprehensive user guides
- [ ] Migration path clearly explained

### Completeness
- [ ] All new functionality covered in documentation
- [ ] Integration patterns clearly demonstrated
- [ ] Error handling and edge cases documented
- [ ] Performance considerations mentioned

### Usability
- [ ] Documentation is easy to follow
- [ ] Examples are practical and realistic
- [ ] Migration guide addresses common scenarios
- [ ] Clear separation between basic and advanced usage

## Success Criteria
- [ ] Comprehensive API documentation for all new interfaces
- [ ] Clear user guides for auth refresh patterns
- [ ] Practical CrudClient integration examples
- [ ] All code examples tested and validated
- [ ] Documentation builds successfully

## Notes
- Focus on practical, real-world examples
- Ensure all code examples are tested and working
- Consider different user skill levels (basic to advanced)
- Include troubleshooting and common issues sections

## Estimated Effort
4-6 hours

## Next Task
[Phase 3 Final Validation](phase3_final_validation.md)