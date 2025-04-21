"""Tests for the BearerAuth strategy."""

import pytest

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.exceptions.auth import AuthStrategyError


class TestBearerAuth:
    """Tests for the BearerAuth strategy."""

    def test_init_with_valid_token(self) -> None:
        """Test initialization with a valid token."""
        auth = BearerAuth(token="valid_token")
        assert auth.token == "valid_token"

    def test_init_rejects_empty_token(self) -> None:
        """Test that BearerAuth rejects empty tokens."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="Bearer token cannot be empty or whitespace"):
            BearerAuth(token="")

        # Whitespace only
        with pytest.raises(AuthStrategyError, match="Bearer token cannot be empty or whitespace"):
            BearerAuth(token="   ")

    def test_prepare_request_headers(self) -> None:
        """Test prepare_request_headers generates the correct Authorization header."""
        auth = BearerAuth(token="test_token")
        headers = auth.prepare_request_headers()
        assert headers == {"Authorization": "Bearer test_token"}

    def test_prepare_request_params(self) -> None:
        """Test prepare_request_params returns an empty dictionary."""
        auth = BearerAuth(token="test_token")
        params = auth.prepare_request_params()
        assert params == {}
