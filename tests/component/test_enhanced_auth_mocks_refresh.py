"""Component tests for enhanced auth mocks refresh scenarios."""

import threading
import time
from typing import Dict

import pytest

from apiconfig.exceptions.auth import TokenRefreshError
from apiconfig.testing.unit.mocks.auth import (
    AuthTestScenarioBuilder,
    MockApiKeyAuthWithRefresh,
    MockAuthErrorInjector,
    MockBearerAuthWithRefresh,
    MockCustomAuthWithRefresh,
    MockHttpRequestCallable,
    MockRefreshableAuthStrategy,
)
from apiconfig.types import TokenRefreshResult


class TestEnhancedAuthMocksRefresh:
    """Test enhanced auth mocks support refresh scenarios in component tests."""

    def test_mock_refreshable_auth_strategy_basic_refresh(self) -> None:
        """Test basic refresh functionality of MockRefreshableAuthStrategy."""
        # Create mock auth strategy with refresh capabilities
        mock_auth = MockRefreshableAuthStrategy(initial_token="initial_token", can_refresh=True, refresh_success=True)

        # Test initial state
        assert mock_auth.can_refresh()
        assert not mock_auth.is_expired()
        assert mock_auth.current_token == "initial_token"

        # Test refresh
        result = mock_auth.refresh()
        assert result is not None
        assert "token_data" in result
        token_data = result.get("token_data")
        assert token_data is not None
        assert "access_token" in token_data
        assert token_data.get("access_token") == "initial_token_refreshed_1"
        assert mock_auth.current_token == "initial_token_refreshed_1"

    def test_mock_refreshable_auth_strategy_refresh_failure(self) -> None:
        """Test refresh failure scenarios with mock injection."""
        # Create mock auth strategy configured to fail refresh
        mock_auth = MockRefreshableAuthStrategy(can_refresh=True, refresh_success=False)

        # Test that refresh raises error
        with pytest.raises(TokenRefreshError, match="Mock refresh failure"):
            mock_auth.refresh()

    def test_mock_refreshable_auth_strategy_refresh_callback(self) -> None:
        """Test refresh callback integration."""
        mock_auth = MockRefreshableAuthStrategy(initial_token="callback_token", can_refresh=True, refresh_success=True)

        # Get refresh callback
        callback = mock_auth.get_refresh_callback()
        assert callback is not None
        assert callable(callback)

        # Test callback execution
        old_token = mock_auth.current_token
        callback()  # Should refresh without error
        assert mock_auth.current_token != old_token

    def test_mock_refreshable_auth_strategy_no_refresh_capability(self) -> None:
        """Test strategy with no refresh capability."""
        mock_auth = MockRefreshableAuthStrategy(can_refresh=False)

        assert not mock_auth.can_refresh()
        callback = mock_auth.get_refresh_callback()
        assert callback is None

    def test_mock_bearer_auth_with_refresh(self) -> None:
        """Test MockBearerAuthWithRefresh functionality."""
        mock_auth = MockBearerAuthWithRefresh(initial_token="bearer_token_123", can_refresh=True, refresh_success=True)

        # Test apply_auth
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)
        assert headers["Authorization"] == "Bearer bearer_token_123"

        # Test refresh
        result = mock_auth.refresh()
        assert result is not None

        # Test new headers after refresh
        new_headers: Dict[str, str] = {}
        mock_auth.apply_auth(new_headers)
        assert new_headers["Authorization"] != headers["Authorization"]
        assert new_headers["Authorization"].startswith("Bearer ")

    def test_mock_api_key_auth_with_refresh(self) -> None:
        """Test MockApiKeyAuthWithRefresh functionality."""
        mock_auth = MockApiKeyAuthWithRefresh(header_name="X-Custom-Key", initial_token="api_key_456", can_refresh=True, refresh_success=True)

        # Test apply_auth
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)
        assert headers["X-Custom-Key"] == "api_key_456"

        # Test refresh
        result = mock_auth.refresh()
        assert result is not None

        # Test new headers after refresh
        new_headers: Dict[str, str] = {}
        mock_auth.apply_auth(new_headers)
        assert new_headers["X-Custom-Key"] != headers["X-Custom-Key"]

    def test_mock_custom_auth_with_refresh(self) -> None:
        """Test MockCustomAuthWithRefresh functionality."""
        mock_auth = MockCustomAuthWithRefresh(
            auth_header_format="Custom-Auth {token}", initial_token="custom_token_789", can_refresh=True, refresh_success=True
        )

        # Test apply_auth
        headers: Dict[str, str] = {}
        mock_auth.apply_auth(headers)
        assert headers["Authorization"] == "Custom-Auth custom_token_789"

        # Test refresh
        result = mock_auth.refresh()
        assert result is not None

        # Test new headers after refresh
        new_headers: Dict[str, str] = {}
        mock_auth.apply_auth(new_headers)
        assert new_headers["Authorization"] != headers["Authorization"]
        assert new_headers["Authorization"].startswith("Custom-Auth ")

    def test_mock_auth_error_injector_failing_refresh(self) -> None:
        """Test MockAuthErrorInjector for failing refresh scenarios."""
        # Test network failure
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="network", failure_after_attempts=1)

        # First refresh should succeed
        result = strategy.refresh()
        assert result is not None

        # Second refresh should fail with network error
        with pytest.raises(ConnectionError, match="Mock network failure"):
            strategy.refresh()

    def test_mock_auth_error_injector_auth_failure(self) -> None:
        """Test MockAuthErrorInjector for auth failure scenarios."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="auth", failure_after_attempts=0)

        # Should fail immediately with auth error
        with pytest.raises(TokenRefreshError, match="Mock authentication failure"):
            strategy.refresh()

    def test_mock_auth_error_injector_timeout_failure(self) -> None:
        """Test MockAuthErrorInjector for timeout failure scenarios."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="timeout", failure_after_attempts=0)

        # Should fail immediately with timeout error
        with pytest.raises(TimeoutError, match="Mock timeout failure"):
            strategy.refresh()

    def test_mock_auth_error_injector_intermittent_failure(self) -> None:
        """Test MockAuthErrorInjector for intermittent failure scenarios."""
        # Use high failure probability to ensure we get failures
        strategy = MockAuthErrorInjector.create_intermittent_failure_strategy(failure_probability=1.0)  # Always fail

        # Should always fail with intermittent error
        with pytest.raises(TokenRefreshError, match="Mock intermittent failure"):
            strategy.refresh()

        # Test with low failure probability
        strategy_low_fail = MockAuthErrorInjector.create_intermittent_failure_strategy(failure_probability=0.0)  # Never fail

        # Should always succeed
        result = strategy_low_fail.refresh()
        assert result is not None

    def test_auth_test_scenario_builder_token_expiry(self) -> None:
        """Test AuthTestScenarioBuilder token expiry scenario."""
        strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(
            initial_token="expiring_token", expires_after_seconds=0.1  # Very short expiry for testing
        )

        # Initially not expired
        assert not strategy.is_expired()

        # Wait for expiry
        time.sleep(0.2)

        # Should now be expired
        assert strategy.is_expired()

    def test_auth_test_scenario_builder_concurrent_refresh(self) -> None:
        """Test AuthTestScenarioBuilder concurrent refresh scenario."""
        strategy = AuthTestScenarioBuilder.create_concurrent_refresh_scenario(num_concurrent_refreshes=3)

        # Test that strategy has thread safety attributes
        assert hasattr(strategy, "_refresh_lock")

        # Test concurrent refresh operations
        results: list[TokenRefreshResult] = []
        errors: list[Exception] = []

        def refresh_worker() -> None:
            try:
                result = strategy.refresh()
                if result is not None:
                    results.append(result)
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads: list[threading.Thread] = []
        for _ in range(3):
            thread = threading.Thread(target=refresh_worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        assert len(results) == 3
        assert len(errors) == 0
        assert strategy.max_concurrent_refreshes >= 1

    def test_auth_test_scenario_builder_crudclient_integration(self) -> None:
        """Test AuthTestScenarioBuilder crudclient integration scenario."""
        strategy = AuthTestScenarioBuilder.create_crudclient_integration_scenario()

        # Test that strategy has callback tracking attributes
        assert hasattr(strategy, "_callback_calls")
        assert hasattr(strategy, "_callback_errors")

        # Get and use callback
        callback = strategy.get_refresh_callback()
        assert callback is not None

        # Call callback multiple times
        callback()
        callback()

        # Check tracking
        assert strategy._callback_calls == 2  # pyright: ignore[reportPrivateUsage]
        assert len(strategy._callback_errors) == 0  # pyright: ignore[reportPrivateUsage]

    def test_mock_http_request_callable(self) -> None:
        """Test MockHttpRequestCallable functionality."""
        # Create mock HTTP callable with custom responses
        responses = {
            "POST:/token": {
                "access_token": "custom_access_token",
                "refresh_token": "custom_refresh_token",
                "expires_in": 7200,
                "token_type": "Bearer",
            }
        }

        mock_http = MockHttpRequestCallable(responses=responses, delay=0.0, failure_rate=0.0)

        # Test request
        response = mock_http("POST", "/token", data={"grant_type": "refresh_token"})
        assert response.status_code == 200
        assert response.json()["access_token"] == "custom_access_token"

        # Check call tracking
        assert mock_http.call_count == 1
        assert len(mock_http.call_history) == 1
        assert mock_http.call_history[0]["method"] == "POST"
        assert mock_http.call_history[0]["url"] == "/token"

    def test_mock_http_request_callable_with_failures(self) -> None:
        """Test MockHttpRequestCallable with failure scenarios."""
        mock_http = MockHttpRequestCallable(failure_rate=1.0)  # Always fail

        # Should always raise ConnectionError
        with pytest.raises(ConnectionError, match="Mock HTTP failure"):
            mock_http("GET", "/test")

    def test_mock_http_request_callable_with_delay(self) -> None:
        """Test MockHttpRequestCallable with delay."""
        mock_http = MockHttpRequestCallable(delay=0.1)

        start_time = time.time()
        response = mock_http("GET", "/test")
        end_time = time.time()

        # Should have taken at least 0.1 seconds
        assert end_time - start_time >= 0.1
        assert response.status_code == 200

    def test_refresh_attempts_limit(self) -> None:
        """Test that refresh attempts are limited correctly."""
        mock_auth = MockRefreshableAuthStrategy(max_refresh_attempts=2, can_refresh=True, refresh_success=True)

        # First two refreshes should succeed
        result1 = mock_auth.refresh()
        assert result1 is not None

        result2 = mock_auth.refresh()
        assert result2 is not None

        # Third refresh should fail due to attempt limit
        assert not mock_auth.can_refresh()
        with pytest.raises(TokenRefreshError, match="Mock refresh not available"):
            mock_auth.refresh()

    def test_token_expiration_state_management(self) -> None:
        """Test token expiration state management."""
        mock_auth = MockRefreshableAuthStrategy()

        # Initially not expired
        assert not mock_auth.is_expired()

        # Set expired
        mock_auth.set_expired(True)
        assert mock_auth.is_expired()

        # Refresh should clear expired state
        if mock_auth.can_refresh():
            result = mock_auth.refresh()
            assert result is not None
            assert not mock_auth.is_expired()
