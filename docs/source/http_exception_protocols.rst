HTTP Exception Protocol Enhancement
===================================

The apiconfig library now supports seamless integration with popular HTTP libraries like ``requests`` and ``httpx`` through Protocol types. This allows you to pass response objects directly to exceptions without manual conversion.

Quick Start
-----------

Instead of manually extracting context:

.. code-block:: python

    # Old approach (no longer supported)
    request_context = {"method": "GET", "url": "https://api.example.com"}
    response_context = {"status_code": 404, "reason": "Not Found"}
    raise ApiClientNotFoundError("Resource not found",
                                request_context=request_context,
                                response_context=response_context)

You can now pass HTTP library objects directly:

.. code-block:: python

    # New approach with requests
    import requests
    from apiconfig.exceptions import ApiClientNotFoundError

    try:
        response = requests.get("https://api.example.com/users/123")
        response.raise_for_status()
    except requests.HTTPError as e:
        raise ApiClientNotFoundError("User not found", response=e.response)

    # New approach with httpx
    import httpx
    from apiconfig.exceptions import create_api_client_error

    response = httpx.get("https://api.example.com/data")
    if response.status_code >= 400:
        raise create_api_client_error(
            response.status_code,
            "Request failed",
            response=response
        )

Protocol Support
----------------

The library uses Protocol types to define the expected interface:

.. code-block:: python

    from typing import Protocol, Optional, Any, runtime_checkable

    @runtime_checkable
    class HttpRequestProtocol(Protocol):
        """Protocol matching common HTTP request objects."""
        method: str
        url: str
        headers: Any

    @runtime_checkable
    class HttpResponseProtocol(Protocol):
        """Protocol matching common HTTP response objects."""
        status_code: int
        headers: Any
        text: str
        request: Optional[Any]
        reason: Optional[str]

Any object that has these attributes will work seamlessly with apiconfig exceptions.

Usage Examples
--------------

With requests Library
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import requests
    from apiconfig.exceptions import (
        ApiClientError,
        ApiClientBadRequestError,
        create_api_client_error
    )

    # Direct response passing
    response = requests.post("https://api.example.com/users", json={"name": "John"})
    if response.status_code == 400:
        raise ApiClientBadRequestError("Invalid user data", response=response)

    # Using the factory function
    if not response.ok:
        raise create_api_client_error(
            response.status_code,
            f"API request failed: {response.text}",
            response=response
        )

    # The exception captures all context
    # exception.status_code == 400
    # exception.method == "POST"
    # exception.url == "https://api.example.com/users"
    # exception.response (original requests.Response object)
    # exception.request (original requests.PreparedRequest object)

With httpx Library
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import httpx
    from apiconfig.exceptions import ApiClientError
    from apiconfig.exceptions.auth import AuthenticationError

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/protected")

        if response.status_code == 401:
            raise AuthenticationError("Invalid credentials", response=response)

        if response.is_error:
            raise ApiClientError(f"Request failed: {response.text}", response=response)

Authentication Exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from apiconfig.exceptions.auth import (
        TokenRefreshError,
        ExpiredTokenError,
        InvalidCredentialsError
    )

    # Token refresh scenario
    refresh_response = requests.post(
        "https://auth.example.com/token/refresh",
        data={"refresh_token": refresh_token}
    )

    if refresh_response.status_code == 400:
        raise TokenRefreshError(
            "Failed to refresh access token",
            response=refresh_response
        )

    # All authentication exceptions support the same pattern
    if response.status_code == 401:
        error_data = response.json()
        if error_data.get("error") == "token_expired":
            raise ExpiredTokenError("Access token has expired", response=response)
        else:
            raise InvalidCredentialsError("Invalid credentials", response=response)

Accessing Original Objects
--------------------------

The original request and response objects are always accessible:

.. code-block:: python

    try:
        response = requests.get("https://api.example.com/data")
        response.raise_for_status()
    except requests.HTTPError as e:
        exc = ApiClientError("Request failed", response=e.response)

        # Access original objects
        original_response = exc.response  # requests.Response
        original_request = exc.request    # requests.PreparedRequest

        # Access extracted attributes
        print(f"Method: {exc.method}")
        print(f"URL: {exc.url}")
        print(f"Status: {exc.status_code}")
        print(f"Reason: {exc.reason}")

        # Access response data through original object
        if original_response.headers.get("content-type") == "application/json":
            error_details = original_response.json()

Custom HTTP Clients
-------------------

Any HTTP client that provides objects with the required attributes will work:

.. code-block:: python

    class CustomHttpResponse:
        def __init__(self, status_code, method, url):
            self.status_code = status_code
            self.headers = {}
            self.text = ""
            self.reason = "Custom Reason"
            self.request = type('Request', (), {
                'method': method,
                'url': url,
                'headers': {}
            })()

    # Works seamlessly
    custom_response = CustomHttpResponse(500, "GET", "https://api.example.com")
    raise ApiClientError("Custom client error", response=custom_response)

Best Practices
--------------

1. **Always pass the response object** when available - it provides the most context
2. **Use the factory function** ``create_api_client_error()`` for dynamic error creation
3. **Access original objects** when you need additional data (headers, JSON body, etc.)
4. **Let the library extract context** - don't manually extract unless necessary

Migration Guide
---------------

If you're migrating from the old TypedDict-based API:

.. code-block:: python

    # Old code
    from apiconfig.types import HttpRequestContext, HttpResponseContext

    request_context: HttpRequestContext = {
        "method": "POST",
        "url": "https://api.example.com/data"
    }
    response_context: HttpResponseContext = {
        "status_code": 400,
        "reason": "Bad Request"
    }
    raise ApiClientError("Failed",
                        request_context=request_context,
                        response_context=response_context)

    # New code - just pass the response object!
    raise ApiClientError("Failed", response=response)

The new API is simpler, more powerful, and works seamlessly with your existing HTTP client code.