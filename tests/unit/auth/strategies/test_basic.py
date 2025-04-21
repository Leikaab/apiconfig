"""Tests for the BasicAuth strategy."""

import base64

import pytest

from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.exceptions.auth import AuthStrategyError


class TestBasicAuth:
    """Tests for the BasicAuth strategy."""

    def test_init_with_valid_credentials(self) -> None:
        """Test initialization with valid credentials."""
        auth = BasicAuth(username="test_user", password="test_pass")
        assert auth.username == "test_user"
        assert auth.password == "test_pass"

    def test_init_rejects_empty_username(self) -> None:
        """Test that BasicAuth rejects empty usernames."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="Username cannot be empty or whitespace"):
            BasicAuth(username="", password="test_pass")

        # Whitespace only
        with pytest.raises(AuthStrategyError, match="Username cannot be empty or whitespace"):
            BasicAuth(username="   ", password="test_pass")

    def test_init_rejects_empty_password(self) -> None:
        """Test that BasicAuth rejects empty passwords."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="Password cannot be empty"):
            BasicAuth(username="test_user", password="")

        # Note: We don't strip whitespace for passwords, as they might legitimately contain only spaces
        # So this should NOT raise an error
        auth = BasicAuth(username="test_user", password="   ")
        assert auth.password == "   "

    def test_prepare_request_headers(self) -> None:
        """Test prepare_request_headers generates the correct Authorization header."""
        auth = BasicAuth(username="test_user", password="test_pass")
        headers = auth.prepare_request_headers()

        # Manually create the expected header value
        auth_string = "test_user:test_pass"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        expected_header = f"Basic {encoded_auth}"

        assert headers == {"Authorization": expected_header}

    def test_prepare_request_params(self) -> None:
        """Test prepare_request_params returns an empty dictionary."""
        auth = BasicAuth(username="test_user", password="test_pass")
        params = auth.prepare_request_params()
        assert params == {}
