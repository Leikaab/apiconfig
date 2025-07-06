"""Integration tests for requests library compatibility."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from apiconfig.exceptions import (
    ApiClientBadRequestError,
    ApiClientError,
    ApiClientNotFoundError,
    create_api_client_error,
)
from apiconfig.exceptions.auth import AuthenticationError, TokenRefreshError
from apiconfig.types import HttpResponseProtocol

# Only run if requests is available
requests_lib = pytest.importorskip("requests")

if TYPE_CHECKING:  # pragma: no cover - used for type checking only
    from requests import PreparedRequest, Request, Response, Session


class TestRequestsResponseObjects:
    """Test with actual requests.Response objects."""

    def test_with_real_requests_response(self) -> None:
        """Test with actual requests.Response object."""
        # Create a mock requests response
        response: Response = requests_lib.Response()
        response.status_code = 400
        response.reason = "Bad Request"
        response.url = "https://api.example.com/test"
        response.request = requests_lib.Request(method="POST", url=response.url).prepare()
        response._content = b'{"error": "Invalid data"}'

        http_response = cast(HttpResponseProtocol, response)
        exc = ApiClientBadRequestError("Request failed", response=http_response)

        assert exc.response is http_response
        assert exc.request is http_response.request
        assert exc.status_code == 400
        assert exc.method == "POST"
        assert exc.url == "https://api.example.com/test"
        assert exc.reason == "Bad Request"
        assert str(exc) == "Request failed (HTTP 400, POST https://api.example.com/test)"

    def test_requests_error_chaining(self) -> None:
        """Test exception chaining from requests.HTTPError."""
        response: Response = requests_lib.Response()
        response.status_code = 404
        response.reason = "Not Found"
        response.url = "https://api.example.com/missing"
        response.request = requests_lib.Request(method="GET", url=response.url).prepare()

        try:
            response.raise_for_status()
        except requests_lib.HTTPError as e:
            exc = ApiClientNotFoundError(
                "Resource not found",
                response=cast(HttpResponseProtocol, e.response),
            )
            assert exc.status_code == 404
            assert exc.method == "GET"
            assert exc.url == "https://api.example.com/missing"

    def test_requests_with_factory_function(self) -> None:
        """Test factory function with requests objects."""
        response: Response = requests_lib.Response()
        response.status_code = 422
        response.reason = "Unprocessable Entity"
        response.url = "https://api.example.com/validate"
        response.request = requests_lib.Request(method="PUT", url=response.url).prepare()
        response._content = b'{"errors": ["field1 is required"]}'

        exc = create_api_client_error(422, "Validation failed", response=cast(HttpResponseProtocol, response))

        assert exc.__class__.__name__ == "ApiClientUnprocessableEntityError"
        assert exc.status_code == 422
        assert exc.method == "PUT"
        assert exc.url == "https://api.example.com/validate"

    def test_requests_session_response(self) -> None:
        """Test with response from requests.Session."""
        # Create a session and prepare a request
        session: Session = requests_lib.Session()
        request: Request = requests_lib.Request(method="DELETE", url="https://api.example.com/item/123", headers={"Authorization": "Bearer token123"})
        prepared = session.prepare_request(request)

        # Create a response
        response: Response = requests_lib.Response()
        response.status_code = 401
        response.reason = "Unauthorized"
        response.url = cast(str, prepared.url)
        response.request = prepared
        response.headers["WWW-Authenticate"] = "Bearer"

        exc = AuthenticationError("Invalid token", response=cast(HttpResponseProtocol, response))

        assert exc.status_code == 401
        assert exc.method == "DELETE"
        assert exc.url == "https://api.example.com/item/123"
        assert str(exc) == "Invalid token (Request: DELETE https://api.example.com/item/123, Response: 401 Unauthorized)"

    def test_requests_with_json_response(self) -> None:
        """Test with requests response containing JSON data."""
        response: Response = requests_lib.Response()
        response.status_code = 400
        response.reason = "Bad Request"
        response.url = "https://api.example.com/data"
        response.request = requests_lib.Request(method="POST", url=response.url).prepare()
        response._content = b'{"error": "Invalid input", "code": "VALIDATION_ERROR"}'
        response.headers["Content-Type"] = "application/json"

        http_response = cast(HttpResponseProtocol, response)
        exc = ApiClientBadRequestError("Validation error", response=http_response)

        # Can access original response for JSON data
        assert exc.response is http_response
        assert response.json() == {"error": "Invalid input", "code": "VALIDATION_ERROR"}

    def test_requests_token_refresh_scenario(self) -> None:
        """Test token refresh error with requests."""
        # Simulate a token refresh request
        refresh_request: PreparedRequest = requests_lib.Request(
            method="POST", url="https://auth.example.com/oauth/token", data={"grant_type": "refresh_token", "refresh_token": "expired_token"}
        ).prepare()

        response: Response = requests_lib.Response()
        response.status_code = 400
        response.reason = "Bad Request"
        response.url = cast(str, refresh_request.url)
        response.request = refresh_request
        response._content = b'{"error": "invalid_grant", "error_description": "Refresh token expired"}'
        http_response = cast(HttpResponseProtocol, response)

        exc = TokenRefreshError("Failed to refresh token", response=http_response)

        assert exc.status_code == 400
        assert exc.method == "POST"
        assert exc.url == "https://auth.example.com/oauth/token"


class TestRequestsEdgeCases:
    """Test edge cases specific to requests library."""

    def test_response_without_prepared_request(self) -> None:
        """Test response that has unprepared request."""
        response: Response = requests_lib.Response()
        response.status_code = 500
        response.reason = "Internal Server Error"
        response.url = "https://api.example.com/error"
        # Create unprepared request
        response.request = requests_lib.Request(method="GET", url=response.url)

        exc = ApiClientError("Server error", response=cast(HttpResponseProtocol, response))

        assert exc.status_code == 500
        # Should still extract from unprepared request
        assert exc.method == "GET"
        assert exc.url == "https://api.example.com/error"

    def test_response_with_redirect_history(self) -> None:
        """Test response that went through redirects."""
        # Create the final response
        response: Response = requests_lib.Response()
        response.status_code = 404
        response.reason = "Not Found"
        response.url = "https://api.example.com/final/location"
        response.request = requests_lib.Request(method="GET", url="https://api.example.com/final/location").prepare()

        # Add redirect history
        redirect1: Response = requests_lib.Response()
        redirect1.status_code = 301
        redirect1.url = "https://api.example.com/original"

        redirect2: Response = requests_lib.Response()
        redirect2.status_code = 302
        redirect2.url = "https://api.example.com/intermediate"

        response.history = [redirect1, redirect2]

        exc = ApiClientNotFoundError(
            "Resource not found after redirects",
            response=cast(HttpResponseProtocol, response),
        )

        # Should use final URL
        assert exc.url == "https://api.example.com/final/location"
        assert exc.status_code == 404

        # Can access history through original response
        assert exc.response is not None and hasattr(exc.response, "history")
        assert exc.response.history is not None  # Type guard for pyright
        assert len(exc.response.history) == 2
