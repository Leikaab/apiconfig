"""Component tests for auth verification integration with mock strategies."""

import base64
from typing import Dict
from unittest.mock import Mock as MockClass

import pytest

from apiconfig.exceptions.auth import AuthenticationError
from apiconfig.testing.auth_verification import (
    AuthHeaderVerification,
    AuthTestHelpers,
)
from apiconfig.testing.unit.mocks.auth import (
    MockBearerAuthWithRefresh,
    MockRefreshableAuthStrategy,
)


class TestAuthVerificationIntegration:
    """Test auth verification utilities with mocked auth strategies."""

    def test_basic_auth_verification_with_mock_strategy(self) -> None:
        """Test Basic Auth verification with mocked strategy."""
        # Create mock basic auth strategy
        mock_basic_auth = MockClass()
        credentials = base64.b64encode(b"user:pass").decode()
        mock_basic_auth.prepare_request_headers.return_value = {"Authorization": f"Basic {credentials}"}

        # Get headers from mock
        headers = mock_basic_auth.prepare_request_headers()

        # Verify using auth verification utilities
        assert AuthHeaderVerification.verify_basic_auth_header(headers["Authorization"])

        # Verify with expected credentials
        assert AuthHeaderVerification.verify_basic_auth_header(headers["Authorization"], expected_username="user", expected_password="pass")

    def test_bearer_auth_verification_with_mock_strategy(self) -> None:
        """Test Bearer Auth verification with mocked strategy."""
        # Create mock bearer auth strategy
        mock_bearer_auth = MockClass()
        mock_bearer_auth.prepare_request_headers.return_value = {"Authorization": "Bearer test_token_12345"}

        # Get headers from mock
        headers = mock_bearer_auth.prepare_request_headers()

        # Verify using auth verification utilities
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

        # Verify with expected token
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"], expected_token="test_token_12345")

        # Verify with token pattern
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"], token_pattern=r"^test_token_\d+$")

    def test_api_key_verification_with_mock_strategy(self) -> None:
        """Test API Key verification with mocked strategy."""
        # Create mock API key auth strategy
        mock_api_key_auth = MockClass()
        mock_api_key_auth.prepare_request_headers.return_value = {"X-API-Key": "sk-test_key_123"}

        # Get headers from mock
        headers = mock_api_key_auth.prepare_request_headers()

        # Verify using auth verification utilities
        assert AuthHeaderVerification.verify_api_key_header(headers["X-API-Key"])

        # Verify with expected key
        assert AuthHeaderVerification.verify_api_key_header(headers["X-API-Key"], expected_key="sk-test_key_123")

        # Verify with key pattern
        assert AuthHeaderVerification.verify_api_key_header(headers["X-API-Key"], key_pattern=r"^sk-test_key_\d+$")

    def test_multiple_auth_headers_verification_with_mocks(self) -> None:
        """Test multiple auth headers verification with mocked strategies."""
        # Create mock strategies
        mock_bearer = MockClass()
        mock_bearer.prepare_request_headers.return_value = {"Authorization": "Bearer bearer_token_123"}

        mock_api_key = MockClass()
        mock_api_key.prepare_request_headers.return_value = {"X-API-Key": "api_key_456"}

        # Combine headers
        bearer_headers = mock_bearer.prepare_request_headers()
        api_key_headers = mock_api_key.prepare_request_headers()
        combined_headers = {**bearer_headers, **api_key_headers}

        # Verify multiple auth headers
        auth_configs = [
            {"auth_type": "bearer", "header_name": "Authorization"},
            {"auth_type": "api_key", "header_name": "X-API-Key", "expected_key": "api_key_456"},
        ]

        AuthHeaderVerification.verify_multiple_auth_headers(combined_headers, auth_configs)

    def test_auth_test_helpers_with_mock_strategies(self) -> None:
        """Test AuthTestHelpers with mock strategies."""
        # Test creating test headers
        bearer_headers = AuthTestHelpers.create_test_auth_headers("bearer", token="test_token")
        assert bearer_headers["Authorization"] == "Bearer test_token"

        # Test asserting auth applied
        AuthTestHelpers.assert_auth_applied(bearer_headers, "bearer", expected_token="test_token")

        # Test creating API key headers
        api_key_headers = AuthTestHelpers.create_test_auth_headers("api_key", key="custom_key", header_name="X-Custom-Key")
        assert api_key_headers["X-Custom-Key"] == "custom_key"

        # Test asserting auth applied for API key
        AuthTestHelpers.assert_auth_applied(api_key_headers, "api_key", header_name="X-Custom-Key", expected_key="custom_key")

    def test_verification_with_refreshable_mock_strategy(self) -> None:
        """Test verification utilities with refreshable mock strategies."""
        # Create refreshable mock strategy
        mock_auth = MockBearerAuthWithRefresh(initial_token="initial_bearer_token")

        # Apply auth to headers
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)

        # Verify the applied auth
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"], expected_token="initial_bearer_token")

        # Test refresh and verify new token
        if mock_auth.can_refresh():
            result = mock_auth.refresh()
            assert result is not None

            # Apply new auth
            new_headers: Dict[str, str] = {}
            mock_auth.apply_auth(new_headers)

            # Verify new token is different
            assert new_headers["Authorization"] != headers["Authorization"]
            assert AuthHeaderVerification.verify_bearer_auth_header(new_headers["Authorization"])

    def test_error_scenarios_with_mock_verification(self) -> None:
        """Test error scenarios with mock verification."""
        # Test invalid bearer header
        with pytest.raises(AuthenticationError, match="Bearer auth header must start with 'Bearer '"):
            AuthHeaderVerification.verify_bearer_auth_header("Invalid Bearer")

        # Test empty API key
        with pytest.raises(AuthenticationError, match="API key header cannot be empty"):
            AuthHeaderVerification.verify_api_key_header("")

        # Test missing header
        empty_headers: Dict[str, str] = {}
        with pytest.raises(AuthenticationError, match="Missing Authorization header"):
            AuthHeaderVerification.verify_auth_header_format(empty_headers, "bearer")

        # Test assertion failures
        invalid_headers = {"Authorization": "Invalid Token"}
        with pytest.raises(AssertionError, match="Authentication not properly applied"):
            AuthTestHelpers.assert_auth_applied(invalid_headers, "bearer")

    def test_no_auth_verification_with_mocks(self) -> None:
        """Test no auth verification with mock scenarios."""
        # Test headers without auth
        clean_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        AuthHeaderVerification.verify_no_auth_headers(clean_headers)
        AuthTestHelpers.assert_no_auth_applied(clean_headers)

        # Test headers with auth should fail
        auth_headers = {"Authorization": "Bearer token123"}
        with pytest.raises(AuthenticationError, match="Unexpected auth headers found"):
            AuthHeaderVerification.verify_no_auth_headers(auth_headers)

        with pytest.raises(AssertionError, match="Unexpected authentication found"):
            AuthTestHelpers.assert_no_auth_applied(auth_headers)

    def test_generic_mock_strategy_verification(self) -> None:
        """Test verification with generic mock strategy."""
        # Create generic mock strategy
        mock_strategy = MockRefreshableAuthStrategy(initial_token="generic_token_123")

        # Apply auth
        headers: Dict[str, str] = {}
        mock_strategy.apply_auth(headers)

        # Directly verify the "Mock {token}" format
        assert "Authorization" in headers
        auth_header = headers["Authorization"]
        assert auth_header.startswith("Mock ")  # Check for "Mock " prefix
        token_part = auth_header[5:]  # Extract token part after "Mock "
        assert token_part == "generic_token_123"  # Verify the token itself
