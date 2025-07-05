"""Component tests for Phase 2 error scenarios."""

import base64
import json
from typing import Dict
from unittest.mock import Mock as MockClass

import pytest

from apiconfig.exceptions.auth import AuthenticationError, TokenRefreshError
from apiconfig.testing.auth_verification import (
    AdvancedAuthVerification,
    AuthHeaderVerification,
    AuthTestHelpers,
)
from apiconfig.testing.unit.mocks.auth import (
    MockAuthErrorInjector,
    MockBearerAuthWithRefresh,
    MockHttpRequestCallable,
    MockRefreshableAuthStrategy,
)
from apiconfig.types import TokenRefreshResult


class TestPhase2ErrorScenarios:
    """Test error handling across Phase 2 components in component test scenarios."""

    def test_auth_header_verification_errors(self) -> None:
        """Test verification errors with invalid headers."""
        # Test invalid Bearer header prefix
        with pytest.raises(AuthenticationError, match="Bearer auth header must start with 'Bearer '"):
            AuthHeaderVerification.verify_bearer_auth_header("Invalid Bearer")

        # Test empty Bearer token
        with pytest.raises(AuthenticationError, match="Bearer token cannot be empty"):
            AuthHeaderVerification.verify_bearer_auth_header("Bearer ")

        # Test invalid Basic auth prefix
        with pytest.raises(AuthenticationError, match="Basic auth header must start with 'Basic '"):
            AuthHeaderVerification.verify_basic_auth_header("Invalid Basic")

        # Test malformed Basic auth encoding
        with pytest.raises(AuthenticationError, match="Invalid Basic auth encoding"):
            AuthHeaderVerification.verify_basic_auth_header("Basic invalid_base64!")

        # Test Basic auth without colon
        credentials_no_colon = base64.b64encode(b"usernocolon").decode()
        with pytest.raises(AuthenticationError, match="Basic auth credentials must contain ':'"):
            AuthHeaderVerification.verify_basic_auth_header(f"Basic {credentials_no_colon}")

        # Test empty API key
        with pytest.raises(AuthenticationError, match="API key header cannot be empty"):
            AuthHeaderVerification.verify_api_key_header("")

    def test_auth_header_verification_mismatch_errors(self) -> None:
        """Test verification errors with mismatched credentials."""
        # Test Bearer token mismatch
        with pytest.raises(AuthenticationError, match="Expected token 'expected', got 'actual'"):
            AuthHeaderVerification.verify_bearer_auth_header("Bearer actual", expected_token="expected")

        # Test Bearer token pattern mismatch
        with pytest.raises(AuthenticationError, match="Token does not match pattern"):
            AuthHeaderVerification.verify_bearer_auth_header("Bearer 123abc", token_pattern=r"^[a-z]+\d+$")

        # Test Basic auth username mismatch
        credentials = base64.b64encode(b"wronguser:pass").decode()
        with pytest.raises(AuthenticationError, match="Expected username 'testuser', got 'wronguser'"):
            AuthHeaderVerification.verify_basic_auth_header(f"Basic {credentials}", expected_username="testuser")

        # Test Basic auth password mismatch
        credentials = base64.b64encode(b"user:wrongpass").decode()
        with pytest.raises(AuthenticationError, match="Password does not match expected value"):
            AuthHeaderVerification.verify_basic_auth_header(f"Basic {credentials}", expected_password="testpass")

        # Test API key mismatch
        with pytest.raises(AuthenticationError, match="Expected key 'expected', got 'actual'"):
            AuthHeaderVerification.verify_api_key_header("actual", expected_key="expected")

        # Test API key pattern mismatch
        with pytest.raises(AuthenticationError, match="API key does not match pattern"):
            AuthHeaderVerification.verify_api_key_header("invalid-key", key_pattern=r"^sk-[a-z0-9]+$")

    def test_auth_header_format_verification_errors(self) -> None:
        """Test auth header format verification errors."""
        # Test missing header
        empty_headers: Dict[str, str] = {}
        with pytest.raises(AuthenticationError, match="Missing Authorization header"):
            AuthHeaderVerification.verify_auth_header_format(empty_headers, "bearer")

        # Test missing custom header
        with pytest.raises(AuthenticationError, match="Missing X-API-Key header"):
            AuthHeaderVerification.verify_auth_header_format(empty_headers, "api_key", header_name="X-API-Key")

        # Test unsupported auth type
        headers = {"Authorization": "Custom token123"}
        with pytest.raises(AuthenticationError, match="Unsupported auth type: custom"):
            AuthHeaderVerification.verify_auth_header_format(headers, "custom")

    def test_multiple_auth_headers_verification_errors(self) -> None:
        """Test multiple auth headers verification errors."""
        headers = {"Authorization": "Bearer token123", "X-API-Key": "wrong-key"}
        auth_configs = [
            {"auth_type": "bearer", "header_name": "Authorization"},
            {"auth_type": "api_key", "header_name": "X-API-Key", "expected_key": "correct-key"},
        ]

        with pytest.raises(AuthenticationError, match="Expected key"):
            AuthHeaderVerification.verify_multiple_auth_headers(headers, auth_configs)

    def test_no_auth_headers_verification_errors(self) -> None:
        """Test no auth headers verification errors."""
        # Test with auth headers present
        headers_with_auth = {"Authorization": "Bearer token123"}
        with pytest.raises(AuthenticationError, match="Unexpected auth headers found"):
            AuthHeaderVerification.verify_no_auth_headers(headers_with_auth)

        # Test with multiple auth headers
        headers_multiple_auth = {"Authorization": "Bearer token123", "X-API-Key": "key123", "X-Auth-Token": "token456"}
        with pytest.raises(AuthenticationError, match="Unexpected auth headers found"):
            AuthHeaderVerification.verify_no_auth_headers(headers_multiple_auth)

    def test_advanced_auth_verification_errors(self) -> None:
        """Test advanced auth verification errors."""
        # Test invalid JWT structure - wrong number of parts
        with pytest.raises(AuthenticationError, match="JWT must have exactly 3 parts"):
            AdvancedAuthVerification.verify_jwt_structure("invalid.jwt")

        # Test JWT with missing alg field
        header_no_alg = {"typ": "JWT"}
        payload = {"sub": "1234567890"}
        header_b64 = base64.b64encode(json.dumps(header_no_alg).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        jwt_no_alg = f"{header_b64}.{payload_b64}.signature"

        with pytest.raises(AuthenticationError, match="JWT header missing 'alg' field"):
            AdvancedAuthVerification.verify_jwt_structure(jwt_no_alg)

        # Test JWT with invalid typ field
        header_invalid_typ = {"typ": "INVALID", "alg": "HS256"}
        header_b64 = base64.b64encode(json.dumps(header_invalid_typ).encode()).decode().rstrip("=")
        jwt_invalid_typ = f"{header_b64}.{payload_b64}.signature"

        with pytest.raises(AuthenticationError, match="JWT header 'typ' must be 'JWT'"):
            AdvancedAuthVerification.verify_jwt_structure(jwt_invalid_typ)

        # Test JWT with invalid JSON
        with pytest.raises(AuthenticationError, match="Invalid JWT structure"):
            AdvancedAuthVerification.verify_jwt_structure("invalid.invalid.signature")

        # Test empty OAuth2 token
        with pytest.raises(AuthenticationError, match="OAuth2 token cannot be empty"):
            AdvancedAuthVerification.verify_oauth2_token_format("")

        # Test too short OAuth2 token
        with pytest.raises(AuthenticationError, match="Bearer token appears too short"):
            AdvancedAuthVerification.verify_oauth2_token_format("short")

        # Test empty session token
        with pytest.raises(AuthenticationError, match="Session token cannot be empty"):
            AdvancedAuthVerification.verify_session_token_format("")

        # Test session token with wrong prefix
        with pytest.raises(AuthenticationError, match="Session token must start with 'sess_'"):
            AdvancedAuthVerification.verify_session_token_format("wrong_token_123", expected_prefix="sess_")

        # Test too short session token
        with pytest.raises(AuthenticationError, match="Session token appears too short"):
            AdvancedAuthVerification.verify_session_token_format("short")

    def test_auth_test_helpers_assertion_errors(self) -> None:
        """Test AuthTestHelpers assertion errors."""
        # Test assert_auth_applied with invalid headers
        invalid_headers: Dict[str, str] = {}
        with pytest.raises(AssertionError, match="Authentication not properly applied"):
            AuthTestHelpers.assert_auth_applied(invalid_headers, "bearer")

        # Test assert_auth_applied with wrong token
        wrong_token_headers = {"Authorization": "Bearer wrong_token"}
        with pytest.raises(AssertionError, match="Authentication not properly applied"):
            AuthTestHelpers.assert_auth_applied(wrong_token_headers, "bearer", expected_token="correct_token")

        # Test assert_no_auth_applied with auth headers present
        auth_headers = {"Authorization": "Bearer token123"}
        with pytest.raises(AssertionError, match="Unexpected authentication found"):
            AuthTestHelpers.assert_no_auth_applied(auth_headers)

    def test_mock_refresh_strategy_errors(self) -> None:
        """Test mock refresh strategy error scenarios."""
        # Test refresh failure
        mock_auth = MockRefreshableAuthStrategy(can_refresh=True, refresh_success=False)

        with pytest.raises(TokenRefreshError, match="Mock refresh failure"):
            mock_auth.refresh()

        # Test refresh not available
        mock_auth_no_refresh = MockRefreshableAuthStrategy(can_refresh=False)
        assert mock_auth_no_refresh.get_refresh_callback() is None

        # Test max attempts exceeded
        mock_auth_limited = MockRefreshableAuthStrategy(max_refresh_attempts=1, can_refresh=True, refresh_success=True)

        # First refresh should succeed
        result = mock_auth_limited.refresh()
        assert result is not None

        # Second refresh should fail
        assert not mock_auth_limited.can_refresh()
        with pytest.raises(TokenRefreshError, match="Mock refresh not available"):
            mock_auth_limited.refresh()

    def test_mock_error_injector_scenarios(self) -> None:
        """Test mock error injection scenarios."""
        # Test network failure injection
        network_fail_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="network", failure_after_attempts=0)

        with pytest.raises(ConnectionError, match="Mock network failure"):
            network_fail_strategy.refresh()

        # Test auth failure injection
        auth_fail_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="auth", failure_after_attempts=0)

        with pytest.raises(TokenRefreshError, match="Mock authentication failure"):
            auth_fail_strategy.refresh()

        # Test timeout failure injection
        timeout_fail_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="timeout", failure_after_attempts=0)

        with pytest.raises(TimeoutError, match="Mock timeout failure"):
            timeout_fail_strategy.refresh()

        # Test custom failure injection
        custom_fail_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="custom", failure_after_attempts=0)

        with pytest.raises(Exception, match="Mock custom failure"):
            custom_fail_strategy.refresh()

        # Test intermittent failure with 100% failure rate
        intermittent_fail_strategy = MockAuthErrorInjector.create_intermittent_failure_strategy(failure_probability=1.0)

        with pytest.raises(TokenRefreshError, match="Mock intermittent failure"):
            intermittent_fail_strategy.refresh()

    def test_mock_http_request_callable_errors(self) -> None:
        """Test MockHttpRequestCallable error scenarios."""
        # Test with 100% failure rate
        failing_http = MockHttpRequestCallable(failure_rate=1.0)

        with pytest.raises(ConnectionError, match="Mock HTTP failure"):
            failing_http("GET", "/test")

        # Test call tracking even with failures
        try:
            failing_http("POST", "/fail")
        except ConnectionError:
            pass

        assert failing_http.call_count == 2  # Both calls should be tracked
        assert len(failing_http.call_history) == 2

    def test_cross_component_error_propagation(self) -> None:
        """Test error propagation across components."""
        # Create a failing mock strategy
        failing_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(
            failure_type="auth", failure_after_attempts=0, initial_token="failing_token"
        )

        # Apply auth (should work)
        headers: Dict[str, str] = {}
        failing_strategy.apply_auth(headers)

        # Verify headers (should work)
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

        # Try to refresh (should fail)
        with pytest.raises(TokenRefreshError, match="Mock authentication failure"):
            failing_strategy.refresh()

        # Get callback and test failure propagation
        callback = failing_strategy.get_refresh_callback()
        if callback is not None:
            with pytest.raises(TokenRefreshError):
                callback()

    def test_malformed_data_error_handling(self) -> None:
        """Test error handling with malformed data."""
        # Test with completely invalid auth header
        with pytest.raises(AuthenticationError):
            AuthHeaderVerification.verify_bearer_auth_header("Not an auth header at all")

        # Test with malformed Basic auth
        with pytest.raises(AuthenticationError, match="Invalid Basic auth encoding"):
            # Create invalid base64
            AuthHeaderVerification.verify_basic_auth_header("Basic !!invalid_base64!!")

        # Test verification with None values (should be handled gracefully)
        mock_strategy = MockClass()
        mock_strategy.prepare_request_headers.return_value = {"Authorization": None}

        headers = mock_strategy.prepare_request_headers()
        with pytest.raises((AuthenticationError, TypeError)):
            # This should fail gracefully, not crash
            AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

    def test_edge_case_error_scenarios(self) -> None:
        """Test edge case error scenarios."""
        # Test with very long tokens (should not cause issues)
        very_long_token = "a" * 10000
        mock_auth = MockBearerAuthWithRefresh(initial_token=very_long_token)
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)

        # Should still verify correctly
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"], expected_token=very_long_token)

        # Test with special characters in tokens
        special_token = "token_with_special_chars_!@#$%^&*()"
        mock_auth_special = MockBearerAuthWithRefresh(initial_token=special_token)
        headers_special: Dict[str, str] = {}
        mock_auth_special.apply_auth(headers_special)

        assert AuthHeaderVerification.verify_bearer_auth_header(headers_special["Authorization"], expected_token=special_token)

        # Test with unicode characters
        unicode_token = "token_with_unicode_ñáéíóú_测试"
        mock_auth_unicode = MockBearerAuthWithRefresh(initial_token=unicode_token)
        headers_unicode: Dict[str, str] = {}
        mock_auth_unicode.apply_auth(headers_unicode)

        assert AuthHeaderVerification.verify_bearer_auth_header(headers_unicode["Authorization"], expected_token=unicode_token)

    def test_concurrent_error_scenarios(self) -> None:
        """Test error scenarios in concurrent operations."""
        import threading

        # Create a strategy that fails after first attempt
        concurrent_fail_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="auth", failure_after_attempts=1)

        errors: list[Exception] = []
        successes: list[TokenRefreshResult | None] = []

        def concurrent_refresh() -> None:
            try:
                result = concurrent_fail_strategy.refresh()
                successes.append(result)
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads: list[threading.Thread] = []
        for _ in range(3):
            thread = threading.Thread(target=concurrent_refresh)
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Should have some successes and some failures
        assert len(successes) >= 1  # At least one should succeed
        assert len(errors) >= 1  # At least one should fail
        assert len(successes) + len(errors) == 3  # Total should be 3

        # All errors should be TokenRefreshError
        for error in errors:
            assert isinstance(error, TokenRefreshError)
