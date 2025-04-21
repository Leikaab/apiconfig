import json
from unittest.mock import MagicMock

import pytest

from apiconfig.auth.token.refresh import refresh_oauth2_token
from apiconfig.config.base import ClientConfig
from apiconfig.exceptions.auth import (
    TokenRefreshError,
    TokenRefreshJsonError,
    TokenRefreshNetworkError,
    TokenRefreshTimeoutError,
)


class TestRefreshOAuth2Token:
    """Tests for the refresh_oauth2_token function."""

    @pytest.fixture
    def mock_response(self) -> MagicMock:
        """Create a mock HTTP response."""
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer",
        }
        return mock

    @pytest.fixture
    def mock_http_client(self, mock_response: MagicMock) -> MagicMock:
        """Create a mock HTTP client."""
        mock_client = MagicMock()
        mock_client.post.return_value = mock_response
        return mock_client

    def test_refresh_oauth2_token_requires_http_client(self) -> None:
        """Test that refresh_oauth2_token requires an HTTP client."""
        with pytest.raises(TokenRefreshError, match="HTTP client"):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
            )

    def test_refresh_oauth2_token_success(
        self, mock_http_client: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test successful token refresh."""
        # Call the function
        result = refresh_oauth2_token(
            refresh_token="test_refresh_token",
            token_url="https://example.com/token",
            http_client=mock_http_client,
        )

        # Verify the result
        assert result == mock_response.json.return_value
        assert "access_token" in result
        assert result["access_token"] == "new_access_token"

        # Verify the request was made correctly
        mock_http_client.post.assert_called_once()
        args, kwargs = mock_http_client.post.call_args
        assert args[0] == "https://example.com/token"
        assert kwargs["data"]["grant_type"] == "refresh_token"
        assert kwargs["data"]["refresh_token"] == "test_refresh_token"
        assert kwargs["timeout"] == 10.0  # Default timeout

    def test_refresh_oauth2_token_with_client_config(
        self, mock_http_client: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test token refresh with ClientConfig for timeout and retries."""
        # Create a client config with custom timeout and retries
        client_config = ClientConfig(timeout=5.0, retries=2)

        # Call the function
        result = refresh_oauth2_token(
            refresh_token="test_refresh_token",
            token_url="https://example.com/token",
            client_config=client_config,
            http_client=mock_http_client,
        )

        # Verify the result
        assert result == mock_response.json.return_value

        # Verify the request was made with the correct timeout
        mock_http_client.post.assert_called_once()
        args, kwargs = mock_http_client.post.call_args
        assert kwargs["timeout"] == 5.0  # Custom timeout from client_config

    def test_refresh_oauth2_token_with_explicit_params(
        self, mock_http_client: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test token refresh with explicit timeout and retries."""
        # Call the function with explicit parameters
        result = refresh_oauth2_token(
            refresh_token="test_refresh_token",
            token_url="https://example.com/token",
            timeout=3.0,
            max_retries=1,
            http_client=mock_http_client,
        )

        # Verify the result
        assert result == mock_response.json.return_value

        # Verify the request was made with the correct timeout
        mock_http_client.post.assert_called_once()
        args, kwargs = mock_http_client.post.call_args
        assert kwargs["timeout"] == 3.0  # Explicit timeout

    def test_refresh_oauth2_token_with_auth_credentials(
        self, mock_http_client: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test token refresh with client credentials."""
        # Setup BasicAuth for the mock client
        mock_http_client.BasicAuth = MagicMock(return_value="basic_auth")

        # Call the function with client credentials
        result = refresh_oauth2_token(
            refresh_token="test_refresh_token",
            token_url="https://example.com/token",
            client_id="test_client_id",
            client_secret="test_client_secret",
            http_client=mock_http_client,
        )

        # Verify the result
        assert result == mock_response.json.return_value

        # Verify the request was made with Basic Auth
        mock_http_client.post.assert_called_once()
        args, kwargs = mock_http_client.post.call_args
        assert "auth" in kwargs
        assert kwargs["auth"] == "basic_auth"
        mock_http_client.BasicAuth.assert_called_once_with(
            username="test_client_id", password="test_client_secret"
        )

    def test_refresh_oauth2_token_with_extra_params(
        self, mock_http_client: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test token refresh with extra parameters."""
        # Call the function with extra parameters
        result = refresh_oauth2_token(
            refresh_token="test_refresh_token",
            token_url="https://example.com/token",
            extra_params={"scope": "read write", "audience": "api://default"},
            http_client=mock_http_client,
        )

        # Verify the result
        assert result == mock_response.json.return_value

        # Verify the request was made with the extra parameters
        mock_http_client.post.assert_called_once()
        args, kwargs = mock_http_client.post.call_args
        assert kwargs["data"]["scope"] == "read write"
        assert kwargs["data"]["audience"] == "api://default"

    def test_refresh_oauth2_token_timeout_error(
        self, mock_http_client: MagicMock
    ) -> None:
        """Test token refresh with timeout error."""

        # Setup the mock client to raise a timeout error
        class TimeoutException(Exception):
            pass

        mock_http_client.post.side_effect = TimeoutException("Request timed out")

        # Call the function and expect a TokenRefreshTimeoutError
        with pytest.raises(TokenRefreshTimeoutError, match="timed out"):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
                max_retries=1,  # Reduce retries for faster test
                http_client=mock_http_client,
            )

    def test_refresh_oauth2_token_network_error(
        self, mock_http_client: MagicMock
    ) -> None:
        """Test token refresh with network error."""

        # Setup the mock client to raise a network error
        class ConnectError(Exception):
            pass

        mock_http_client.post.side_effect = ConnectError("Connection failed")

        # Call the function and expect a TokenRefreshNetworkError after retries
        with pytest.raises(TokenRefreshNetworkError, match="Network error"):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
                max_retries=1,  # Reduce retries for faster test
                http_client=mock_http_client,
            )

    def test_refresh_oauth2_token_json_error(self, mock_http_client: MagicMock) -> None:
        """Test token refresh with JSON decoding error."""
        # Setup a mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Set up the json method to raise JSONDecodeError
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        # Ensure text and content attributes are not available to force using json()
        type(mock_response).text = property(lambda self: None)
        type(mock_response).content = property(lambda self: None)
        mock_http_client.post.return_value = mock_response

        # Call the function and expect a TokenRefreshJsonError
        with pytest.raises(TokenRefreshJsonError, match="Failed to decode"):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
                http_client=mock_http_client,
            )

    def test_refresh_oauth2_token_missing_access_token(
        self, mock_http_client: MagicMock
    ) -> None:
        """Test token refresh with missing access_token in response."""
        # Setup a mock response with missing access_token
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "expires_in": 3600,
            "token_type": "Bearer",
            # No access_token
        }
        mock_http_client.post.return_value = mock_response

        # Call the function and expect a TokenRefreshError
        with pytest.raises(TokenRefreshError, match="missing 'access_token'"):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
                http_client=mock_http_client,
            )

    def test_refresh_oauth2_token_http_error(self, mock_http_client: MagicMock) -> None:
        """Test token refresh with HTTP error."""
        # Setup a mock response with HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        mock_http_client.post.return_value = mock_response

        # Call the function and expect a TokenRefreshError
        with pytest.raises(TokenRefreshError):
            refresh_oauth2_token(
                refresh_token="test_refresh_token",
                token_url="https://example.com/token",
                http_client=mock_http_client,
            )

    def test_refresh_oauth2_token_retry_success(
        self, mock_http_client: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test token refresh with successful retry after network error."""

        # Create a custom exception class for network errors
        class ConnectError(Exception):
            pass

        # Setup the mock client to fail once then succeed
        mock_http_client.post.side_effect = [
            ConnectError("Connection failed"),  # First call fails
            mock_response,  # Second call succeeds
        ]

        # Call the function
        result = refresh_oauth2_token(
            refresh_token="test_refresh_token",
            token_url="https://example.com/token",
            max_retries=2,
            http_client=mock_http_client,
        )

        # Verify the result
        assert result == mock_response.json.return_value

        # Verify the client was called twice
        assert mock_http_client.post.call_count == 2
