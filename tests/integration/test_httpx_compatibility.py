"""Integration tests for httpx library compatibility."""

from typing import cast

import pytest
from httpx import AsyncClient, Request, Response

from apiconfig.exceptions import (
    ApiClientError,
    ApiClientForbiddenError,
    ApiClientRateLimitError,
    create_api_client_error,
)
from apiconfig.exceptions.auth import ExpiredTokenError
from apiconfig.types import HttpResponseProtocol

# Only run if httpx is available
httpx_lib = pytest.importorskip("httpx")


class TestHttpxResponseObjects:
    """Test with actual httpx.Response objects."""

    def test_with_real_httpx_response(self) -> None:
        """Test with actual httpx.Response object."""
        # Create a mock httpx response
        request: Request = httpx_lib.Request("GET", "https://api.example.com/data")
        response: Response = httpx_lib.Response(
            status_code=404,
            headers={"content-type": "application/json"},
            content=b'{"error": "Not found"}',
            request=request,
        )

        exc = ApiClientError("Not found", response=cast(HttpResponseProtocol, response))

        assert cast(Response, exc.response) is response
        assert cast(Request, exc.request) is request
        assert exc.status_code == 404
        assert exc.method == "GET"
        assert exc.url == "https://api.example.com/data"
        # httpx doesn't always have reason
        assert str(exc) == "Not found (HTTP 404, GET https://api.example.com/data)"

    def test_httpx_sync_client_response(self) -> None:
        """Test with httpx sync client response."""
        request: Request = httpx_lib.Request("DELETE", "https://api.example.com/resource/123")
        response: Response = httpx_lib.Response(
            status_code=403,
            request=request,
            content=b"Forbidden",
        )

        exc = create_api_client_error(
            403,
            "Access denied",
            response=cast(HttpResponseProtocol, response),
        )

        assert isinstance(exc, ApiClientForbiddenError)
        assert exc.method == "DELETE"
        assert exc.url == "https://api.example.com/resource/123"

    @pytest.mark.asyncio
    async def test_httpx_async_client_response(self) -> None:
        """Test with httpx async client response."""
        async with AsyncClient() as client:
            request: Request = client.build_request("POST", "https://api.example.com/async/data")
        response: Response = httpx_lib.Response(
            status_code=429,
            headers={"Retry-After": "60"},
            request=request,
            content=b"Rate limit exceeded",
        )

        exc = ApiClientRateLimitError("Too many requests", response=cast(HttpResponseProtocol, response))

        assert exc.status_code == 429
        assert exc.method == "POST"
        assert exc.url == "https://api.example.com/async/data"
        # Can access headers through original response
        assert exc.response is not None
        assert exc.response.headers["Retry-After"] == "60"

    def test_httpx_with_json_response(self) -> None:
        """Test with httpx response containing JSON data."""
        request: Request = httpx_lib.Request("PUT", "https://api.example.com/user/456")
        response: Response = httpx_lib.Response(
            status_code=422,
            headers={"content-type": "application/json"},
            content=b'{"errors": [{"field": "email", "message": "Invalid format"}]}',
            request=request,
        )

        exc = create_api_client_error(422, "Validation failed", response=cast(HttpResponseProtocol, response))

        # Can access JSON through original response
        assert exc.response is not None
        assert exc.response.json() == {"errors": [{"field": "email", "message": "Invalid format"}]}  # type: ignore[attr-defined]

    def test_httpx_auth_error(self) -> None:
        """Test authentication error with httpx."""
        request: Request = httpx_lib.Request("GET", "https://api.example.com/protected", headers={"Authorization": "Bearer expired_token"})
        response: Response = httpx_lib.Response(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer realm='api'"},
            request=request,
            content=b"Token expired",
        )

        exc = ExpiredTokenError("Access token expired", response=cast(HttpResponseProtocol, response))

        assert exc.status_code == 401
        assert exc.method == "GET"
        assert exc.url == "https://api.example.com/protected"


class TestHttpxStreamingResponses:
    """Test with httpx streaming responses."""

    def test_stream_response(self) -> None:
        """Test with httpx stream response."""
        request: Request = httpx_lib.Request("GET", "https://api.example.com/stream")

        # Create a response with streaming content
        response: Response = httpx_lib.Response(
            status_code=200,
            request=request,
            # httpx supports various content types
            content=b"Streaming content",
        )

        # Should work even with streaming responses
        exc = ApiClientError("Stream processing failed", response=cast(HttpResponseProtocol, response))

        assert exc.status_code == 200
        assert exc.method == "GET"


class TestHttpxEdgeCases:
    """Test edge cases specific to httpx."""

    def test_httpx_response_without_request(self) -> None:
        """Test httpx response created without request.

        httpx has a design choice where Response.request raises RuntimeError
        instead of returning None when no request is associated. Our code
        handles this specific case gracefully.
        """
        # httpx allows creating responses without requests
        response: Response = httpx_lib.Response(
            status_code=500,
            content=b"Internal error",
        )

        # Verify httpx behavior - it raises RuntimeError
        with pytest.raises(RuntimeError, match="request instance has not been set"):
            _ = response.request

        # Our exception handles this gracefully
        exc = ApiClientError("Server error", response=cast(HttpResponseProtocol, response))

        assert exc.status_code == 500
        assert exc.request is None
        assert exc.method is None
        assert exc.url is None
        assert str(exc) == "Server error (HTTP 500)"

    def test_httpx_with_custom_transport(self) -> None:
        """Test with httpx response from custom transport."""
        # Simulate a response from a custom transport
        request: Request = httpx_lib.Request("PATCH", "https://custom.transport/api")
        response: Response = httpx_lib.Response(
            status_code=400,
            request=request,
            content=b"Bad request from custom transport",
            extensions={"custom": "transport_data"},
        )

        exc = ApiClientError("Custom transport error", response=cast(HttpResponseProtocol, response))

        assert exc.method == "PATCH"
        assert exc.url == "https://custom.transport/api"
        # Can access extensions through original response
        assert exc.response is not None
        assert exc.response.extensions["custom"] == "transport_data"  # type: ignore[attr-defined]
