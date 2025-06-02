# -*- coding: utf-8 -*-
# File: tests/unit/testing/test_auth_verification.py
"""Unit tests for auth verification utilities."""

import base64
import json

import pytest

from apiconfig.exceptions.auth import AuthenticationError
from apiconfig.testing.auth_verification import (
    AdvancedAuthVerification,
    AuthHeaderVerification,
    AuthTestHelpers,
)


class TestAuthHeaderVerification:
    """Test cases for AuthHeaderVerification class."""

    def test_verify_basic_auth_header_valid(self) -> None:
        """Test valid basic auth header verification."""
        # Create valid basic auth header
        credentials = base64.b64encode(b"testuser:testpass").decode()
        header = f"Basic {credentials}"

        result = AuthHeaderVerification.verify_basic_auth_header(header)
        assert result is True

    def test_verify_basic_auth_header_with_expected_credentials(self) -> None:
        """Test basic auth header with expected credentials."""
        credentials = base64.b64encode(b"testuser:testpass").decode()
        header = f"Basic {credentials}"

        result = AuthHeaderVerification.verify_basic_auth_header(header, expected_username="testuser", expected_password="testpass")
        assert result is True

    def test_verify_basic_auth_header_invalid_prefix(self) -> None:
        """Test basic auth header with invalid prefix."""
        with pytest.raises(AuthenticationError, match="Basic auth header must start with 'Basic '"):
            AuthHeaderVerification.verify_basic_auth_header("Bearer token123")

    def test_verify_basic_auth_header_invalid_encoding(self) -> None:
        """Test basic auth header with invalid base64 encoding."""
        with pytest.raises(AuthenticationError, match="Invalid Basic auth encoding"):
            AuthHeaderVerification.verify_basic_auth_header("Basic invalid_base64!")

    def test_verify_basic_auth_header_missing_colon(self) -> None:
        """Test basic auth header without colon separator."""
        credentials = base64.b64encode(b"testusernocolon").decode()
        header = f"Basic {credentials}"

        with pytest.raises(AuthenticationError, match="Basic auth credentials must contain ':'"):
            AuthHeaderVerification.verify_basic_auth_header(header)

    def test_verify_basic_auth_header_wrong_username(self) -> None:
        """Test basic auth header with wrong username."""
        credentials = base64.b64encode(b"wronguser:testpass").decode()
        header = f"Basic {credentials}"

        with pytest.raises(AuthenticationError, match="Expected username 'testuser', got 'wronguser'"):
            AuthHeaderVerification.verify_basic_auth_header(header, expected_username="testuser")

    def test_verify_basic_auth_header_wrong_password(self) -> None:
        """Test basic auth header with wrong password."""
        credentials = base64.b64encode(b"testuser:wrongpass").decode()
        header = f"Basic {credentials}"

        with pytest.raises(AuthenticationError, match="Password does not match expected value"):
            AuthHeaderVerification.verify_basic_auth_header(header, expected_password="testpass")

    def test_verify_bearer_auth_header_valid(self) -> None:
        """Test valid bearer auth header verification."""
        result = AuthHeaderVerification.verify_bearer_auth_header("Bearer token123")
        assert result is True

    def test_verify_bearer_auth_header_with_expected_token(self) -> None:
        """Test bearer auth header with expected token."""
        result = AuthHeaderVerification.verify_bearer_auth_header("Bearer token123", expected_token="token123")
        assert result is True

    def test_verify_bearer_auth_header_with_pattern(self) -> None:
        """Test bearer auth header with regex pattern."""
        result = AuthHeaderVerification.verify_bearer_auth_header("Bearer abc123", token_pattern=r"^[a-z]+\d+$")
        assert result is True

    def test_verify_bearer_auth_header_invalid_prefix(self) -> None:
        """Test bearer auth header with invalid prefix."""
        with pytest.raises(AuthenticationError, match="Bearer auth header must start with 'Bearer '"):
            AuthHeaderVerification.verify_bearer_auth_header("Basic token123")

    def test_verify_bearer_auth_header_empty_token(self) -> None:
        """Test bearer auth header with empty token."""
        with pytest.raises(AuthenticationError, match="Bearer token cannot be empty"):
            AuthHeaderVerification.verify_bearer_auth_header("Bearer ")

    def test_verify_bearer_auth_header_wrong_token(self) -> None:
        """Test bearer auth header with wrong token."""
        with pytest.raises(AuthenticationError, match="Expected token 'expected', got 'actual'"):
            AuthHeaderVerification.verify_bearer_auth_header("Bearer actual", expected_token="expected")

    def test_verify_bearer_auth_header_pattern_mismatch(self) -> None:
        """Test bearer auth header with pattern mismatch."""
        with pytest.raises(AuthenticationError, match="Token does not match pattern"):
            AuthHeaderVerification.verify_bearer_auth_header("Bearer 123abc", token_pattern=r"^[a-z]+\d+$")

    def test_verify_api_key_header_valid(self) -> None:
        """Test valid API key header verification."""
        result = AuthHeaderVerification.verify_api_key_header("sk-123abc")
        assert result is True

    def test_verify_api_key_header_with_expected_key(self) -> None:
        """Test API key header with expected key."""
        result = AuthHeaderVerification.verify_api_key_header("sk-123abc", expected_key="sk-123abc")
        assert result is True

    def test_verify_api_key_header_with_pattern(self) -> None:
        """Test API key header with regex pattern."""
        result = AuthHeaderVerification.verify_api_key_header("sk-123abc", key_pattern=r"^sk-[a-z0-9]+$")
        assert result is True

    def test_verify_api_key_header_empty(self) -> None:
        """Test empty API key header."""
        with pytest.raises(AuthenticationError, match="API key header cannot be empty"):
            AuthHeaderVerification.verify_api_key_header("")

    def test_verify_api_key_header_wrong_key(self) -> None:
        """Test API key header with wrong key."""
        with pytest.raises(AuthenticationError, match="Expected key 'expected', got 'actual'"):
            AuthHeaderVerification.verify_api_key_header("actual", expected_key="expected")

    def test_verify_api_key_header_pattern_mismatch(self) -> None:
        """Test API key header with pattern mismatch."""
        with pytest.raises(AuthenticationError, match="API key does not match pattern"):
            AuthHeaderVerification.verify_api_key_header("invalid-key", key_pattern=r"^sk-[a-z0-9]+$")

    def test_verify_auth_header_format_basic(self) -> None:
        """Test auth header format verification for basic auth."""
        headers = {"Authorization": "Basic " + base64.b64encode(b"user:pass").decode()}
        AuthHeaderVerification.verify_auth_header_format(headers, "basic")

    def test_verify_auth_header_format_bearer(self) -> None:
        """Test auth header format verification for bearer auth."""
        headers = {"Authorization": "Bearer token123"}
        AuthHeaderVerification.verify_auth_header_format(headers, "bearer")

    def test_verify_auth_header_format_api_key(self) -> None:
        """Test auth header format verification for API key."""
        headers = {"X-API-Key": "sk-123abc"}
        AuthHeaderVerification.verify_auth_header_format(headers, "api_key", header_name="X-API-Key")

    def test_verify_auth_header_format_missing_header(self) -> None:
        """Test auth header format verification with missing header."""
        headers: dict[str, str] = {}
        with pytest.raises(AuthenticationError, match="Missing Authorization header"):
            AuthHeaderVerification.verify_auth_header_format(headers, "bearer")

    def test_verify_auth_header_format_unsupported_type(self) -> None:
        """Test auth header format verification with unsupported type."""
        headers = {"Authorization": "Custom token123"}
        with pytest.raises(AuthenticationError, match="Unsupported auth type: custom"):
            AuthHeaderVerification.verify_auth_header_format(headers, "custom")

    def test_verify_multiple_auth_headers(self) -> None:
        """Test verification of multiple auth headers."""
        headers = {"Authorization": "Bearer token123", "X-API-Key": "sk-123abc"}
        auth_configs: list[dict[str, str]] = [
            {"auth_type": "bearer", "header_name": "Authorization"},
            {"auth_type": "api_key", "header_name": "X-API-Key", "expected_key": "sk-123abc"},
        ]
        AuthHeaderVerification.verify_multiple_auth_headers(headers, auth_configs)

    def test_verify_multiple_auth_headers_failure(self) -> None:
        """Test verification of multiple auth headers with failure."""
        headers = {"Authorization": "Bearer token123", "X-API-Key": "wrong-key"}
        auth_configs: list[dict[str, str]] = [
            {"auth_type": "bearer", "header_name": "Authorization"},
            {"auth_type": "api_key", "header_name": "X-API-Key", "expected_key": "sk-123abc"},
        ]
        with pytest.raises(AuthenticationError, match="Expected key"):
            AuthHeaderVerification.verify_multiple_auth_headers(headers, auth_configs)

    def test_verify_no_auth_headers_success(self) -> None:
        """Test verification that no auth headers are present."""
        headers = {"Content-Type": "application/json"}
        AuthHeaderVerification.verify_no_auth_headers(headers)

    def test_verify_no_auth_headers_failure(self) -> None:
        """Test verification that no auth headers are present with failure."""
        headers = {"Authorization": "Bearer token123"}
        with pytest.raises(AuthenticationError, match="Unexpected auth headers found"):
            AuthHeaderVerification.verify_no_auth_headers(headers)

    def test_verify_no_auth_headers_custom_list(self) -> None:
        """Test verification with custom auth header list."""
        headers = {"X-Custom-Auth": "token123"}
        AuthHeaderVerification.verify_no_auth_headers(headers, auth_header_names=["Authorization", "X-API-Key"])


class TestAdvancedAuthVerification:
    """Test cases for AdvancedAuthVerification class."""

    def test_verify_jwt_structure_valid(self) -> None:
        """Test valid JWT structure verification."""
        # Create a simple JWT for testing
        header = {"typ": "JWT", "alg": "HS256"}
        payload = {"sub": "1234567890", "name": "John Doe", "admin": True}

        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature_b64 = "signature"

        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        result = AdvancedAuthVerification.verify_jwt_structure(jwt_token)
        assert "header" in result
        assert "payload" in result
        assert result["header"]["typ"] == "JWT"
        assert result["header"]["alg"] == "HS256"

    def test_verify_jwt_structure_invalid_parts(self) -> None:
        """Test JWT structure verification with invalid number of parts."""
        with pytest.raises(AuthenticationError, match="JWT must have exactly 3 parts"):
            AdvancedAuthVerification.verify_jwt_structure("invalid.jwt")

    def test_verify_jwt_structure_missing_alg(self) -> None:
        """Test JWT structure verification with missing alg field."""
        header = {"typ": "JWT"}  # Missing alg
        payload = {"sub": "1234567890"}

        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature_b64 = "signature"

        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        with pytest.raises(AuthenticationError, match="JWT header missing 'alg' field"):
            AdvancedAuthVerification.verify_jwt_structure(jwt_token)

    def test_verify_jwt_structure_invalid_typ(self) -> None:
        """Test JWT structure verification with invalid typ field."""
        header = {"typ": "INVALID", "alg": "HS256"}
        payload = {"sub": "1234567890"}

        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature_b64 = "signature"

        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        with pytest.raises(AuthenticationError, match="JWT header 'typ' must be 'JWT'"):
            AdvancedAuthVerification.verify_jwt_structure(jwt_token)

    def test_verify_jwt_structure_invalid_json(self) -> None:
        """Test JWT structure verification with invalid JSON."""
        with pytest.raises(AuthenticationError, match="Invalid JWT structure"):
            AdvancedAuthVerification.verify_jwt_structure("invalid.invalid.signature")

    def test_verify_oauth2_token_format_valid(self) -> None:
        """Test valid OAuth2 token format verification."""
        result = AdvancedAuthVerification.verify_oauth2_token_format("valid_oauth2_token_123")
        assert result is True

    def test_verify_oauth2_token_format_empty(self) -> None:
        """Test OAuth2 token format verification with empty token."""
        with pytest.raises(AuthenticationError, match="OAuth2 token cannot be empty"):
            AdvancedAuthVerification.verify_oauth2_token_format("")

    def test_verify_oauth2_token_format_too_short(self) -> None:
        """Test OAuth2 token format verification with too short token."""
        with pytest.raises(AuthenticationError, match="Bearer token appears too short"):
            AdvancedAuthVerification.verify_oauth2_token_format("short")

    def test_verify_oauth2_token_format_jwt(self) -> None:
        """Test OAuth2 token format verification with JWT token."""
        # Create a simple JWT for testing
        header = {"typ": "JWT", "alg": "HS256"}
        payload = {"sub": "1234567890"}

        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature_b64 = "signature"

        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        result = AdvancedAuthVerification.verify_oauth2_token_format(jwt_token)
        assert result is True

    def test_verify_oauth2_token_format_non_bearer(self) -> None:
        """Test OAuth2 token format verification with non-bearer token type."""
        result = AdvancedAuthVerification.verify_oauth2_token_format("valid_token_123", token_type="access")
        assert result is True

    def test_verify_session_token_format_valid(self) -> None:
        """Test valid session token format verification."""
        result = AdvancedAuthVerification.verify_session_token_format("session_token_123")
        assert result is True

    def test_verify_session_token_format_with_prefix(self) -> None:
        """Test session token format verification with expected prefix."""
        result = AdvancedAuthVerification.verify_session_token_format("sess_token_123", expected_prefix="sess_")
        assert result is True

    def test_verify_session_token_format_empty(self) -> None:
        """Test session token format verification with empty token."""
        with pytest.raises(AuthenticationError, match="Session token cannot be empty"):
            AdvancedAuthVerification.verify_session_token_format("")

    def test_verify_session_token_format_wrong_prefix(self) -> None:
        """Test session token format verification with wrong prefix."""
        with pytest.raises(AuthenticationError, match="Session token must start with 'sess_'"):
            AdvancedAuthVerification.verify_session_token_format("wrong_token_123", expected_prefix="sess_")

    def test_verify_session_token_format_too_short(self) -> None:
        """Test session token format verification with too short token."""
        with pytest.raises(AuthenticationError, match="Session token appears too short"):
            AdvancedAuthVerification.verify_session_token_format("short")


class TestAuthTestHelpers:
    """Test cases for AuthTestHelpers class."""

    def test_assert_auth_applied_success(self) -> None:
        """Test successful auth application assertion."""
        headers = {"Authorization": "Bearer token123"}
        AuthTestHelpers.assert_auth_applied(headers, "bearer")

    def test_assert_auth_applied_failure(self) -> None:
        """Test failed auth application assertion."""
        headers: dict[str, str] = {}
        with pytest.raises(AssertionError, match="Authentication not properly applied"):
            AuthTestHelpers.assert_auth_applied(headers, "bearer")

    def test_assert_no_auth_applied_success(self) -> None:
        """Test successful no auth assertion."""
        headers = {"Content-Type": "application/json"}
        AuthTestHelpers.assert_no_auth_applied(headers)

    def test_assert_no_auth_applied_failure(self) -> None:
        """Test failed no auth assertion."""
        headers = {"Authorization": "Bearer token123"}
        with pytest.raises(AssertionError, match="Unexpected authentication found"):
            AuthTestHelpers.assert_no_auth_applied(headers)

    def test_create_test_auth_headers_basic(self) -> None:
        """Test creation of basic auth test headers."""
        headers = AuthTestHelpers.create_test_auth_headers("basic")
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

        # Verify the default credentials
        encoded = headers["Authorization"][6:]  # Remove "Basic "
        decoded = base64.b64decode(encoded).decode()
        assert decoded == "testuser:testpass"

    def test_create_test_auth_headers_basic_custom(self) -> None:
        """Test creation of basic auth test headers with custom credentials."""
        headers = AuthTestHelpers.create_test_auth_headers("basic", username="custom", password="secret")
        assert "Authorization" in headers

        # Verify the custom credentials
        encoded = headers["Authorization"][6:]  # Remove "Basic "
        decoded = base64.b64decode(encoded).decode()
        assert decoded == "custom:secret"

    def test_create_test_auth_headers_bearer(self) -> None:
        """Test creation of bearer auth test headers."""
        headers = AuthTestHelpers.create_test_auth_headers("bearer")
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_bearer_token"

    def test_create_test_auth_headers_bearer_custom(self) -> None:
        """Test creation of bearer auth test headers with custom token."""
        headers = AuthTestHelpers.create_test_auth_headers("bearer", token="custom_token")
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer custom_token"

    def test_create_test_auth_headers_api_key(self) -> None:
        """Test creation of API key test headers."""
        headers = AuthTestHelpers.create_test_auth_headers("api_key")
        assert "X-API-Key" in headers
        assert headers["X-API-Key"] == "test_api_key"

    def test_create_test_auth_headers_api_key_custom(self) -> None:
        """Test creation of API key test headers with custom values."""
        headers = AuthTestHelpers.create_test_auth_headers("api_key", key="custom_key", header_name="X-Custom-Key")
        assert "X-Custom-Key" in headers
        assert headers["X-Custom-Key"] == "custom_key"

    def test_create_test_auth_headers_unknown_type(self) -> None:
        """Test creation of test headers with unknown auth type."""
        headers = AuthTestHelpers.create_test_auth_headers("unknown")
        assert headers == {}


class TestIntegrationScenarios:
    """Test cases for integration scenarios."""

    def test_complete_auth_verification_workflow(self) -> None:
        """Test complete auth verification workflow."""
        # Create test headers
        headers = AuthTestHelpers.create_test_auth_headers("bearer", token="test123")

        # Verify auth was applied
        AuthTestHelpers.assert_auth_applied(headers, "bearer", expected_token="test123")

        # Verify specific header format
        AuthHeaderVerification.verify_auth_header_format(headers, "bearer", expected_token="test123")

    def test_multiple_auth_types_workflow(self) -> None:
        """Test workflow with multiple auth types."""
        # Create headers with multiple auth types
        basic_headers = AuthTestHelpers.create_test_auth_headers("basic")
        api_key_headers = AuthTestHelpers.create_test_auth_headers("api_key", header_name="X-API-Key")

        # Combine headers
        combined_headers = {**basic_headers, **api_key_headers}

        # Verify multiple auth headers
        auth_configs: list[dict[str, str]] = [
            {"auth_type": "basic", "header_name": "Authorization"},
            {"auth_type": "api_key", "header_name": "X-API-Key"},
        ]
        AuthHeaderVerification.verify_multiple_auth_headers(combined_headers, auth_configs)

    def test_jwt_oauth2_integration(self) -> None:
        """Test JWT and OAuth2 integration scenario."""
        # Create a JWT token
        header = {"typ": "JWT", "alg": "HS256"}
        payload = {"sub": "1234567890", "name": "John Doe"}

        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature_b64 = "signature"

        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        # Verify JWT structure
        result = AdvancedAuthVerification.verify_jwt_structure(jwt_token)
        assert result["payload"]["name"] == "John Doe"

        # Verify as OAuth2 token
        AdvancedAuthVerification.verify_oauth2_token_format(jwt_token)

        # Verify in bearer header
        headers = {"Authorization": f"Bearer {jwt_token}"}
        AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])
