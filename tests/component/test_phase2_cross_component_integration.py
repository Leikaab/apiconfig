"""Component tests for Phase 2 cross-component integration."""

import base64
import time
from typing import Dict, List

import pytest

from apiconfig.exceptions.auth import AuthenticationError, TokenRefreshError
from apiconfig.testing.auth_verification import (
    AdvancedAuthVerification,
    AuthHeaderVerification,
    AuthTestHelpers,
)
from apiconfig.testing.unit.mocks.auth import (
    AuthTestScenarioBuilder,
    MockApiKeyAuthWithRefresh,
    MockAuthErrorInjector,
    MockBearerAuthWithRefresh,
    MockCustomAuthWithRefresh,
    MockHttpRequestCallable,
)


class TestPhase2CrossComponentIntegration:
    """Test that verification and mocking work together in component tests."""

    def test_verification_and_mocking_integration(self) -> None:
        """Test that verification and mocking work together in component tests."""
        # Create a mock auth strategy with realistic behavior
        mock_auth = MockBearerAuthWithRefresh(initial_token="mock_token_12345", can_refresh=True, refresh_success=True)

        # Get headers from mock
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)

        # Verify headers using verification utilities
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"], expected_token="mock_token_12345")

        # Test refresh flow integration
        if mock_auth.can_refresh():
            old_token = mock_auth.current_token
            result = mock_auth.refresh()

            # Verify refresh result structure
            assert result is not None
            assert "token_data" in result
            token_data = result.get("token_data")
            assert token_data is not None
            assert "access_token" in token_data

            # Get new headers and verify they're different
            new_headers: Dict[str, str] = {}
            mock_auth.apply_auth(new_headers)
            new_token = new_headers["Authorization"][7:]  # Remove "Bearer " prefix
            assert new_token != old_token

            # Verify new headers
            assert AuthHeaderVerification.verify_bearer_auth_header(new_headers["Authorization"])

    def test_auth_test_helpers_with_enhanced_mocks(self) -> None:
        """Test AuthTestHelpers integration with enhanced mocks."""
        # Create test headers using helpers
        test_headers = AuthTestHelpers.create_test_auth_headers("bearer", token="helper_created_token")

        # Verify using verification utilities
        AuthTestHelpers.assert_auth_applied(test_headers, "bearer", expected_token="helper_created_token")

        # Create mock strategy and compare
        mock_auth = MockBearerAuthWithRefresh(initial_token="helper_created_token")
        mock_headers: Dict[str, str] = {}
        mock_auth.apply_auth(mock_headers)

        # Both should produce equivalent results
        assert test_headers["Authorization"] == mock_headers["Authorization"]

    def test_advanced_verification_with_mock_jwt(self) -> None:
        """Test advanced verification with mock JWT tokens."""
        # Create a mock JWT token for testing
        header = {"typ": "JWT", "alg": "HS256"}
        payload = {"sub": "1234567890", "name": "Test User", "exp": 1234567890}

        import json

        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature_b64 = "mock_signature"

        jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

        # Create mock auth with JWT token
        mock_auth = MockBearerAuthWithRefresh(initial_token=jwt_token)
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)

        # Verify JWT structure using advanced verification
        token_from_header = headers["Authorization"][7:]  # Remove "Bearer " prefix
        result = AdvancedAuthVerification.verify_jwt_structure(token_from_header)

        assert "header" in result
        assert "payload" in result
        assert result["header"]["typ"] == "JWT"
        assert result["payload"]["name"] == "Test User"

        # Verify as OAuth2 token
        assert AdvancedAuthVerification.verify_oauth2_token_format(token_from_header)

    def test_error_injection_with_verification(self) -> None:
        """Test error injection integration with verification utilities."""
        # Create failing strategy
        failing_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(
            failure_type="auth", failure_after_attempts=1, initial_token="failing_token"
        )

        # Initial auth should work
        headers: Dict[str, str] = {}
        failing_strategy.apply_auth(headers)
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

        # First refresh should succeed
        result = failing_strategy.refresh()
        assert result is not None

        # Second refresh should fail
        with pytest.raises(TokenRefreshError, match="Mock authentication failure"):
            failing_strategy.refresh()

        # Headers should still be verifiable with the last successful token
        new_headers: Dict[str, str] = {}
        failing_strategy.apply_auth(new_headers)
        assert AuthHeaderVerification.verify_bearer_auth_header(new_headers["Authorization"])

    def test_scenario_builder_with_verification(self) -> None:
        """Test scenario builder integration with verification utilities."""
        # Create token expiry scenario
        expiry_strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token="expiring_token_123", expires_after_seconds=0.1)

        # Initial verification should work
        headers: Dict[str, str] = {}
        expiry_strategy.apply_auth(headers)
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

        # Wait for expiry
        time.sleep(0.2)
        assert expiry_strategy.is_expired()

        # Headers should still be verifiable (token doesn't change until refresh)
        current_headers: Dict[str, str] = {}
        expiry_strategy.apply_auth(current_headers)
        assert AuthHeaderVerification.verify_bearer_auth_header(current_headers["Authorization"])

    def test_concurrent_refresh_with_verification(self) -> None:
        """Test concurrent refresh scenario with verification."""
        import threading

        concurrent_strategy = AuthTestScenarioBuilder.create_concurrent_refresh_scenario(num_concurrent_refreshes=3)

        # Track verification results from multiple threads
        verification_results: List[bool] = []
        verification_errors: List[Exception] = []

        def verify_worker() -> None:
            try:
                # Refresh and verify
                result = concurrent_strategy.refresh()
                if result is not None:
                    headers: Dict[str, str] = {}
                    concurrent_strategy.apply_auth(headers)
                    is_valid = AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])
                    verification_results.append(is_valid)
            except Exception as e:
                verification_errors.append(e)

        # Start multiple verification threads
        threads: list[threading.Thread] = []
        for _ in range(3):
            thread = threading.Thread(target=verify_worker)
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # All verifications should succeed
        assert len(verification_results) == 3
        assert all(verification_results)
        assert len(verification_errors) == 0

    def test_crudclient_integration_scenario_with_verification(self) -> None:
        """Test crudclient integration scenario with verification."""
        crudclient_strategy = AuthTestScenarioBuilder.create_crudclient_integration_scenario()

        # Test callback integration
        callback = crudclient_strategy.get_refresh_callback()
        assert callback is not None

        # Execute callback and verify results
        old_token = crudclient_strategy.current_token
        callback()

        # Verify callback was tracked
        assert crudclient_strategy._callback_calls == 1  # pyright: ignore[reportPrivateUsage]

        # Verify new token
        headers: Dict[str, str] = {}
        crudclient_strategy.apply_auth(headers)
        new_token = headers["Authorization"][5:]  # Remove "Mock " prefix
        assert new_token != old_token

        # Verify headers are still valid
        assert headers["Authorization"].startswith("Mock ")

    def test_http_mock_with_auth_verification(self) -> None:
        """Test HTTP mock integration with auth verification."""
        # Create HTTP mock with custom token response
        http_mock = MockHttpRequestCallable(
            responses={
                "POST:/oauth/token": {
                    "access_token": "http_mock_token_456",
                    "refresh_token": "http_mock_refresh_456",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                }
            }
        )

        # Simulate token refresh request
        response = http_mock("POST", "/oauth/token", data={"grant_type": "refresh_token"})
        token_data = response.json()

        # Create mock auth with the received token
        assert "access_token" in token_data
        mock_auth = MockBearerAuthWithRefresh(initial_token=token_data["access_token"])
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)

        # Verify the token
        assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"], expected_token="http_mock_token_456")

    def test_multiple_auth_types_cross_component(self) -> None:
        """Test multiple auth types working together across components."""
        # Create different mock auth strategies
        bearer_mock = MockBearerAuthWithRefresh(initial_token="bearer_123")
        api_key_mock = MockApiKeyAuthWithRefresh(header_name="X-API-Key", initial_token="api_key_456")
        custom_mock = MockCustomAuthWithRefresh(auth_header_format="Custom-Token {token}", initial_token="custom_789")

        # Test each auth type separately to avoid header conflicts
        bearer_headers: Dict[str, str] = {}
        bearer_mock.apply_auth(bearer_headers)
        assert AuthHeaderVerification.verify_bearer_auth_header(bearer_headers["Authorization"], expected_token="bearer_123")

        api_key_headers: Dict[str, str] = {}
        api_key_mock.apply_auth(api_key_headers)
        assert AuthHeaderVerification.verify_api_key_header(api_key_headers["X-API-Key"], expected_key="api_key_456")

        custom_headers: Dict[str, str] = {}
        custom_mock.apply_auth(custom_headers)
        assert custom_headers["Authorization"] == "Custom-Token custom_789"

        # Test combined headers (API key + custom auth, since both can coexist)
        combined_headers: Dict[str, str] = {}
        api_key_mock.apply_auth(combined_headers)
        custom_mock.apply_auth(combined_headers)  # This overwrites Authorization but keeps X-API-Key

        assert AuthHeaderVerification.verify_api_key_header(combined_headers["X-API-Key"], expected_key="api_key_456")
        assert combined_headers["Authorization"] == "Custom-Token custom_789"

    def test_error_scenarios_cross_component(self) -> None:
        """Test error scenarios across all Phase 2 components."""
        # Test verification errors with mock data
        mock_auth = MockBearerAuthWithRefresh(initial_token="valid_token")
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)

        # Corrupt the header and test verification failure
        headers["Authorization"] = "Invalid Bearer Token"
        with pytest.raises(AuthenticationError):
            AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

        # Test mock error injection
        error_strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="network", failure_after_attempts=0)

        with pytest.raises(ConnectionError, match="Mock network failure"):
            error_strategy.refresh()

        # Test assertion helpers with invalid data
        invalid_headers: Dict[str, str] = {"Authorization": "Malformed"}
        with pytest.raises(AssertionError, match="Authentication not properly applied"):
            AuthTestHelpers.assert_auth_applied(invalid_headers, "bearer")

    def test_performance_cross_component(self) -> None:
        """Test performance of cross-component operations."""
        # Create multiple mock strategies
        strategies: List[MockBearerAuthWithRefresh] = []
        for i in range(10):
            strategy = MockBearerAuthWithRefresh(initial_token=f"perf_token_{i}", refresh_delay=0.0)  # No artificial delay
            strategies.append(strategy)

        # Measure time for auth application and verification
        start_time = time.time()

        for strategy in strategies:
            headers: Dict[str, str] = {}
            strategy.apply_auth(headers)
            AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

            if strategy.can_refresh():
                result = strategy.refresh()
                assert result is not None

                new_headers: Dict[str, str] = {}
                strategy.apply_auth(new_headers)
                AuthHeaderVerification.verify_bearer_auth_header(new_headers["Authorization"])

        end_time = time.time()

        # Should complete quickly (less than 1 second for 10 strategies)
        assert end_time - start_time < 1.0

    def test_comprehensive_workflow_integration(self) -> None:
        """Test comprehensive workflow integrating all Phase 2 components."""
        # Step 1: Create test headers using helpers
        initial_headers = AuthTestHelpers.create_test_auth_headers("bearer", token="workflow_token_initial")

        # Step 2: Verify initial headers
        AuthTestHelpers.assert_auth_applied(initial_headers, "bearer", expected_token="workflow_token_initial")

        # Step 3: Create enhanced mock with same token
        mock_auth = MockBearerAuthWithRefresh(initial_token="workflow_token_initial", can_refresh=True, refresh_success=True)

        # Step 4: Verify mock produces same headers
        mock_headers: Dict[str, str] = {}
        mock_auth.apply_auth(mock_headers)
        assert mock_headers == initial_headers

        # Step 5: Test refresh workflow
        refresh_result = mock_auth.refresh()
        assert refresh_result is not None

        # Step 6: Verify refreshed headers
        refreshed_headers: Dict[str, str] = {}
        mock_auth.apply_auth(refreshed_headers)
        assert refreshed_headers != initial_headers

        AuthHeaderVerification.verify_bearer_auth_header(refreshed_headers["Authorization"])

        # Step 7: Test callback integration
        callback = mock_auth.get_refresh_callback()
        assert callback is not None

        old_token = mock_auth.current_token
        callback()
        assert mock_auth.current_token != old_token

        # Step 8: Final verification
        final_headers: Dict[str, str] = {}
        mock_auth.apply_auth(final_headers)
        AuthTestHelpers.assert_auth_applied(final_headers, "bearer")
