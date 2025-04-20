"""Tests for the ApiKeyAuth strategy."""

import pytest

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.exceptions.auth import AuthStrategyError


class TestApiKeyAuth:
    """Tests for the ApiKeyAuth strategy."""

    def test_init_requires_one_of_header_or_param_name(self) -> None:
        """Test that ApiKeyAuth requires one of header_name or param_name."""
        # Should raise when both are None
        with pytest.raises(AuthStrategyError, match="One of header_name or param_name must be provided"):
            ApiKeyAuth(api_key="test_key")

        # Should not raise when header_name is provided
        ApiKeyAuth(api_key="test_key", header_name="X-API-Key")

        # Should not raise when param_name is provided
        ApiKeyAuth(api_key="test_key", param_name="api_key")

    def test_init_rejects_both_header_and_param_name(self) -> None:
        """Test that ApiKeyAuth rejects when both header_name and param_name are provided."""
        with pytest.raises(AuthStrategyError, match="Only one of header_name or param_name should be provided"):
            ApiKeyAuth(
                api_key="test_key",
                header_name="X-API-Key",
                param_name="api_key"
            )

    def test_init_rejects_empty_api_key(self) -> None:
        """Test that ApiKeyAuth rejects empty API keys."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="API key cannot be empty or whitespace"):
            ApiKeyAuth(api_key="", header_name="X-API-Key")

        # Whitespace only
        with pytest.raises(AuthStrategyError, match="API key cannot be empty or whitespace"):
            ApiKeyAuth(api_key="   ", header_name="X-API-Key")

    def test_init_rejects_empty_header_name(self) -> None:
        """Test that ApiKeyAuth rejects empty header names."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="Header name cannot be empty or whitespace"):
            ApiKeyAuth(api_key="test_key", header_name="")

        # Whitespace only
        with pytest.raises(AuthStrategyError, match="Header name cannot be empty or whitespace"):
            ApiKeyAuth(api_key="test_key", header_name="   ")

    def test_init_rejects_empty_param_name(self) -> None:
        """Test that ApiKeyAuth rejects empty parameter names."""
        # Empty string
        with pytest.raises(AuthStrategyError, match="Parameter name cannot be empty or whitespace"):
            ApiKeyAuth(api_key="test_key", param_name="")

        # Whitespace only
        with pytest.raises(AuthStrategyError, match="Parameter name cannot be empty or whitespace"):
            ApiKeyAuth(api_key="test_key", param_name="   ")

    def test_prepare_request_headers_with_header_name(self) -> None:
        """Test prepare_request_headers with header_name."""
        auth = ApiKeyAuth(api_key="test_key", header_name="X-API-Key")
        headers = auth.prepare_request_headers()
        assert headers == {"X-API-Key": "test_key"}

    def test_prepare_request_headers_without_header_name(self) -> None:
        """Test prepare_request_headers without header_name."""
        auth = ApiKeyAuth(api_key="test_key", param_name="api_key")
        headers = auth.prepare_request_headers()
        assert headers == {}

    def test_prepare_request_params_with_param_name(self) -> None:
        """Test prepare_request_params with param_name."""
        auth = ApiKeyAuth(api_key="test_key", param_name="api_key")
        params = auth.prepare_request_params()
        assert params == {"api_key": "test_key"}

    def test_prepare_request_params_without_param_name(self) -> None:
        """Test prepare_request_params without param_name."""
        auth = ApiKeyAuth(api_key="test_key", header_name="X-API-Key")
        params = auth.prepare_request_params()
        assert params == {}
