# -*- coding: utf-8 -*-
"""Unit tests for enhanced auth mocks with refresh scenarios."""

import threading
import time
from typing import Any, Dict, Optional
from unittest.mock import patch

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


class TestMockRefreshableAuthStrategy:
    """Test cases for MockRefreshableAuthStrategy."""

    def test_init_default_values(self) -> None:
        """Test initialization with default values."""
        strategy = MockRefreshableAuthStrategy()

        assert strategy.initial_token == "mock_token"
        assert strategy.current_token == "mock_token"
        assert strategy.refresh_token == "mock_refresh"
        assert strategy._can_refresh is True  # pyright: ignore[reportPrivateUsage]
        assert strategy._refresh_success is True  # pyright: ignore[reportPrivateUsage]
        assert strategy._refresh_delay == 0.0  # pyright: ignore[reportPrivateUsage]
        assert strategy._max_refresh_attempts == 3  # pyright: ignore[reportPrivateUsage]
        assert strategy._refresh_attempts == 0  # pyright: ignore[reportPrivateUsage]
        assert strategy._is_expired is False  # pyright: ignore[reportPrivateUsage]

    def test_init_custom_values(self) -> None:
        """Test initialization with custom values."""
        strategy = MockRefreshableAuthStrategy(
            initial_token="custom_token",
            refresh_token="custom_refresh",
            can_refresh=False,
            refresh_success=False,
            refresh_delay=1.0,
            max_refresh_attempts=5,
        )

        assert strategy.initial_token == "custom_token"
        assert strategy.current_token == "custom_token"
        assert strategy.refresh_token == "custom_refresh"
        assert strategy._can_refresh is False  # pyright: ignore[reportPrivateUsage]
        assert strategy._refresh_success is False  # pyright: ignore[reportPrivateUsage]
        assert strategy._refresh_delay == 1.0  # pyright: ignore[reportPrivateUsage]
        assert strategy._max_refresh_attempts == 5  # pyright: ignore[reportPrivateUsage]

    def test_can_refresh_true_when_enabled_and_under_limit(self) -> None:
        """Test can_refresh returns True when enabled and under attempt limit."""
        strategy = MockRefreshableAuthStrategy(can_refresh=True, max_refresh_attempts=3)
        assert strategy.can_refresh() is True

    def test_can_refresh_false_when_disabled(self) -> None:
        """Test can_refresh returns False when disabled."""
        strategy = MockRefreshableAuthStrategy(can_refresh=False)
        assert strategy.can_refresh() is False

    def test_can_refresh_false_when_over_limit(self) -> None:
        """Test can_refresh returns False when over attempt limit."""
        strategy = MockRefreshableAuthStrategy(max_refresh_attempts=1)
        strategy._refresh_attempts = 1  # pyright: ignore[reportPrivateUsage]
        assert strategy.can_refresh() is False

    def test_is_expired_default_false(self) -> None:
        """Test is_expired returns False by default."""
        strategy = MockRefreshableAuthStrategy()
        assert strategy.is_expired() is False

    def test_set_expired_true(self) -> None:
        """Test set_expired sets expiration state to True."""
        strategy = MockRefreshableAuthStrategy()
        strategy.set_expired(True)
        assert strategy.is_expired() is True

    def test_set_expired_false(self) -> None:
        """Test set_expired sets expiration state to False."""
        strategy = MockRefreshableAuthStrategy()
        strategy.set_expired(True)
        strategy.set_expired(False)
        assert strategy.is_expired() is False

    def test_refresh_success(self) -> None:
        """Test successful refresh operation."""
        strategy = MockRefreshableAuthStrategy(initial_token="initial", refresh_token="refresh_token")

        result = strategy.refresh()

        assert result is not None
        token_data = result.get("token_data")
        assert token_data is not None
        assert token_data.get("access_token") == "initial_refreshed_1"
        assert token_data.get("refresh_token") == "refresh_token_new"
        assert token_data.get("expires_in") == 3600
        assert token_data.get("token_type") == "Bearer"
        assert result.get("config_updates") is None
        assert strategy.current_token == "initial_refreshed_1"
        assert strategy._refresh_attempts == 1  # pyright: ignore[reportPrivateUsage]
        assert strategy.is_expired() is False

    def test_refresh_with_delay(self) -> None:
        """Test refresh operation with delay."""
        strategy = MockRefreshableAuthStrategy(refresh_delay=0.1)

        start_time = time.time()
        strategy.refresh()
        end_time = time.time()

        assert end_time - start_time >= 0.1

    def test_refresh_failure_when_disabled(self) -> None:
        """Test refresh raises error when refresh_success is False."""
        strategy = MockRefreshableAuthStrategy(refresh_success=False)

        with pytest.raises(TokenRefreshError, match="Mock refresh failure"):
            strategy.refresh()

    def test_refresh_failure_when_cannot_refresh(self) -> None:
        """Test refresh raises error when can_refresh returns False."""
        strategy = MockRefreshableAuthStrategy(max_refresh_attempts=0)

        with pytest.raises(TokenRefreshError, match="Mock refresh not available"):
            strategy.refresh()

    def test_multiple_refresh_attempts(self) -> None:
        """Test multiple refresh attempts increment counter."""
        strategy = MockRefreshableAuthStrategy(max_refresh_attempts=3)

        result1 = strategy.refresh()
        result2 = strategy.refresh()

        assert strategy._refresh_attempts == 2  # pyright: ignore[reportPrivateUsage]
        assert result1 is not None
        token_data1 = result1.get("token_data")
        assert token_data1 is not None
        assert token_data1.get("access_token") == "mock_token_refreshed_1"
        assert result2 is not None
        token_data2 = result2.get("token_data")
        assert token_data2 is not None
        assert token_data2.get("access_token") == "mock_token_refreshed_2"

    def test_get_refresh_callback_when_can_refresh(self) -> None:
        """Test get_refresh_callback returns callback when refresh is possible."""
        strategy = MockRefreshableAuthStrategy()

        callback = strategy.get_refresh_callback()

        assert callback is not None
        assert callable(callback)

    def test_get_refresh_callback_when_cannot_refresh(self) -> None:
        """Test get_refresh_callback returns None when refresh is not possible."""
        strategy = MockRefreshableAuthStrategy(can_refresh=False)

        callback = strategy.get_refresh_callback()

        assert callback is None

    def test_refresh_callback_execution(self) -> None:
        """Test refresh callback executes refresh operation."""
        strategy = MockRefreshableAuthStrategy()
        callback = strategy.get_refresh_callback()

        assert callback is not None
        initial_token = strategy.current_token
        callback()

        assert strategy.current_token != initial_token
        assert strategy._refresh_attempts == 1  # pyright: ignore[reportPrivateUsage]

    def test_refresh_callback_raises_on_none_result(self) -> None:
        """Test refresh callback raises error when refresh returns None."""

        class RefreshReturnsNone(MockRefreshableAuthStrategy):
            def refresh(self) -> Optional[TokenRefreshResult]:
                return None

        strategy = RefreshReturnsNone()

        callback = strategy.get_refresh_callback()

        assert callback is not None
        with pytest.raises(TokenRefreshError, match="Mock callback: Refresh method returned None unexpectedly"):
            callback()

    def test_apply_auth_base_implementation(self) -> None:
        """Test apply_auth base implementation."""
        strategy = MockRefreshableAuthStrategy(initial_token="test_token")
        headers: Dict[str, str] = {}

        strategy.apply_auth(headers)

        assert headers["Authorization"] == "Mock test_token"


class TestMockBearerAuthWithRefresh:
    """Test cases for MockBearerAuthWithRefresh."""

    def test_apply_auth_bearer_format(self) -> None:
        """Test apply_auth uses Bearer format."""
        strategy = MockBearerAuthWithRefresh(initial_token="bearer_token")
        headers: Dict[str, str] = {}

        strategy.apply_auth(headers)

        assert headers["Authorization"] == "Bearer bearer_token"

    def test_refresh_updates_bearer_token(self) -> None:
        """Test refresh updates token used in Bearer auth."""
        strategy = MockBearerAuthWithRefresh(initial_token="initial_bearer")
        headers: Dict[str, str] = {}

        strategy.refresh()
        strategy.apply_auth(headers)

        assert headers["Authorization"] == "Bearer initial_bearer_refreshed_1"


class TestMockApiKeyAuthWithRefresh:
    """Test cases for MockApiKeyAuthWithRefresh."""

    def test_init_default_header_name(self) -> None:
        """Test initialization with default header name."""
        strategy = MockApiKeyAuthWithRefresh()
        assert strategy.header_name == "X-API-Key"

    def test_init_custom_header_name(self) -> None:
        """Test initialization with custom header name."""
        strategy = MockApiKeyAuthWithRefresh(header_name="X-Custom-Key")
        assert strategy.header_name == "X-Custom-Key"

    def test_apply_auth_api_key_format(self) -> None:
        """Test apply_auth uses API key format."""
        strategy = MockApiKeyAuthWithRefresh(initial_token="api_key_token", header_name="X-API-Key")
        headers: Dict[str, str] = {}

        strategy.apply_auth(headers)

        assert headers["X-API-Key"] == "api_key_token"

    def test_apply_auth_custom_header_name(self) -> None:
        """Test apply_auth uses custom header name."""
        strategy = MockApiKeyAuthWithRefresh(initial_token="custom_key", header_name="X-Custom-Auth")
        headers: Dict[str, str] = {}

        strategy.apply_auth(headers)

        assert headers["X-Custom-Auth"] == "custom_key"

    def test_refresh_updates_api_key(self) -> None:
        """Test refresh updates token used in API key auth."""
        strategy = MockApiKeyAuthWithRefresh(initial_token="initial_key")
        headers: Dict[str, str] = {}

        strategy.refresh()
        strategy.apply_auth(headers)

        assert headers["X-API-Key"] == "initial_key_refreshed_1"


class TestMockCustomAuthWithRefresh:
    """Test cases for MockCustomAuthWithRefresh."""

    def test_init_default_format(self) -> None:
        """Test initialization with default format."""
        strategy = MockCustomAuthWithRefresh()
        assert strategy.auth_header_format == "Custom {token}"

    def test_init_custom_format(self) -> None:
        """Test initialization with custom format."""
        strategy = MockCustomAuthWithRefresh(auth_header_format="Token {token}")
        assert strategy.auth_header_format == "Token {token}"

    def test_apply_auth_custom_format(self) -> None:
        """Test apply_auth uses custom format."""
        strategy = MockCustomAuthWithRefresh(initial_token="custom_token", auth_header_format="MyAuth {token}")
        headers: Dict[str, str] = {}

        strategy.apply_auth(headers)

        assert headers["Authorization"] == "MyAuth custom_token"

    def test_refresh_updates_custom_token(self) -> None:
        """Test refresh updates token used in custom auth."""
        strategy = MockCustomAuthWithRefresh(initial_token="initial_custom", auth_header_format="Custom {token}")
        headers: Dict[str, str] = {}

        strategy.refresh()
        strategy.apply_auth(headers)

        assert headers["Authorization"] == "Custom initial_custom_refreshed_1"


class TestMockAuthErrorInjector:
    """Test cases for MockAuthErrorInjector."""

    def test_create_failing_refresh_strategy_network_error(self) -> None:
        """Test creating strategy that fails with network error."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="network", failure_after_attempts=1)

        # First refresh should succeed
        result = strategy.refresh()
        assert result is not None

        # Second refresh should fail with network error
        with pytest.raises(ConnectionError, match="Mock network failure"):
            strategy.refresh()

    def test_create_failing_refresh_strategy_auth_error(self) -> None:
        """Test creating strategy that fails with auth error."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="auth", failure_after_attempts=0)

        # First refresh should fail with auth error
        with pytest.raises(TokenRefreshError, match="Mock authentication failure"):
            strategy.refresh()

    def test_create_failing_refresh_strategy_timeout_error(self) -> None:
        """Test creating strategy that fails with timeout error."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="timeout", failure_after_attempts=0)

        # First refresh should fail with timeout error
        with pytest.raises(TimeoutError, match="Mock timeout failure"):
            strategy.refresh()

    def test_create_failing_refresh_strategy_generic_error(self) -> None:
        """Test creating strategy that fails with generic error."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(failure_type="custom", failure_after_attempts=0)

        # First refresh should fail with generic error
        with pytest.raises(Exception, match="Mock custom failure"):
            strategy.refresh()

    def test_create_intermittent_failure_strategy_always_fail(self) -> None:
        """Test creating strategy with 100% failure rate."""
        strategy = MockAuthErrorInjector.create_intermittent_failure_strategy(failure_probability=1.0)

        with pytest.raises(TokenRefreshError, match="Mock intermittent failure"):
            strategy.refresh()

    def test_create_intermittent_failure_strategy_never_fail(self) -> None:
        """Test creating strategy with 0% failure rate."""
        strategy = MockAuthErrorInjector.create_intermittent_failure_strategy(failure_probability=0.0)

        result = strategy.refresh()
        assert result is not None

    @patch("random.random")
    def test_create_intermittent_failure_strategy_controlled(self, mock_random: Any) -> None:
        """Test creating strategy with controlled failure probability."""
        mock_random.return_value = 0.2  # Below 0.3 threshold

        strategy = MockAuthErrorInjector.create_intermittent_failure_strategy(failure_probability=0.3)

        with pytest.raises(TokenRefreshError, match="Mock intermittent failure"):
            strategy.refresh()


class TestAuthTestScenarioBuilder:
    """Test cases for AuthTestScenarioBuilder."""

    def test_create_token_expiry_scenario(self) -> None:
        """Test creating token expiry scenario."""
        strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token="expiry_token", expires_after_seconds=0.1)

        assert strategy.initial_token == "expiry_token"
        assert strategy.is_expired() is False

        # Wait for expiration
        time.sleep(0.15)
        assert strategy.is_expired() is True

    def test_create_concurrent_refresh_scenario(self) -> None:
        """Test creating concurrent refresh scenario."""
        strategy = AuthTestScenarioBuilder.create_concurrent_refresh_scenario()

        # Check that thread safety attributes are added
        assert hasattr(strategy, "_refresh_lock")
        assert strategy.concurrent_refreshes == 0
        assert strategy.max_concurrent_refreshes == 0

    def test_concurrent_refresh_tracking(self) -> None:
        """Test concurrent refresh tracking functionality."""
        strategy = AuthTestScenarioBuilder.create_concurrent_refresh_scenario()

        def refresh_worker() -> None:
            strategy.refresh()

        # Start multiple threads
        threads: list[threading.Thread] = []
        for _ in range(3):
            thread = threading.Thread(target=refresh_worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check that concurrent refreshes were tracked
        assert strategy.concurrent_refreshes == 0
        assert strategy.max_concurrent_refreshes >= 1

    def test_create_crudclient_integration_scenario(self) -> None:
        """Test creating crudclient integration scenario."""
        strategy = AuthTestScenarioBuilder.create_crudclient_integration_scenario()

        # Check that callback tracking attributes are added
        assert hasattr(strategy, "_callback_calls")
        assert hasattr(strategy, "_callback_errors")
        assert getattr(strategy, "_callback_calls", None) == 0
        assert getattr(strategy, "_callback_errors", None) == []

    def test_crudclient_integration_callback_tracking(self) -> None:
        """Test callback tracking in crudclient integration scenario."""
        strategy = AuthTestScenarioBuilder.create_crudclient_integration_scenario()

        callback = strategy.get_refresh_callback()
        assert callback is not None

        # Call the callback
        callback()

        assert getattr(strategy, "_callback_calls", None) == 1
        assert len(getattr(strategy, "_callback_errors", [])) == 0

    def test_crudclient_integration_error_tracking(self) -> None:
        """Test error tracking in crudclient integration scenario."""
        strategy = AuthTestScenarioBuilder.create_crudclient_integration_scenario()

        # Make refresh fail
        strategy._refresh_success = False  # pyright: ignore[reportPrivateUsage]

        callback = strategy.get_refresh_callback()
        assert callback is not None

        # Call the callback and expect error
        with pytest.raises(TokenRefreshError):
            callback()

        assert getattr(strategy, "_callback_calls", None) == 1
        callback_errors = getattr(strategy, "_callback_errors", [])
        assert len(callback_errors) == 1
        assert isinstance(callback_errors[0], TokenRefreshError)


class TestMockHttpRequestCallable:
    """Test cases for MockHttpRequestCallable."""

    def test_init_default_values(self) -> None:
        """Test initialization with default values."""
        mock_http = MockHttpRequestCallable()

        assert mock_http.responses == {}
        assert mock_http.delay == 0.0
        assert mock_http.failure_rate == 0.0
        assert mock_http.call_count == 0
        assert mock_http.call_history == []

    def test_init_custom_values(self) -> None:
        """Test initialization with custom values."""
        responses = {"GET:http://example.com": {"token": "test"}}
        mock_http = MockHttpRequestCallable(responses=responses, delay=1.0, failure_rate=0.5)

        assert mock_http.responses == responses
        assert mock_http.delay == 1.0
        assert mock_http.failure_rate == 0.5

    def test_call_default_response(self) -> None:
        """Test calling with default response generation."""
        mock_http = MockHttpRequestCallable()

        response = mock_http("POST", "http://example.com/token")

        assert mock_http.call_count == 1
        assert len(mock_http.call_history) == 1
        assert mock_http.call_history[0]["method"] == "POST"
        assert mock_http.call_history[0]["url"] == "http://example.com/token"

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        data = response.json()
        assert data["access_token"] == "mock_token_1"
        assert data["refresh_token"] == "mock_refresh_1"
        assert data["expires_in"] == 3600
        assert data["token_type"] == "Bearer"

    def test_call_custom_response(self) -> None:
        """Test calling with custom response."""
        custom_response = {"custom_token": "custom_value"}
        responses = {"POST:http://example.com/token": custom_response}
        mock_http = MockHttpRequestCallable(responses=responses)

        response = mock_http("POST", "http://example.com/token")

        assert response.json() == custom_response

    def test_call_with_delay(self) -> None:
        """Test calling with delay."""
        mock_http = MockHttpRequestCallable(delay=0.1)

        start_time = time.time()
        mock_http("GET", "http://example.com")
        end_time = time.time()

        assert end_time - start_time >= 0.1

    def test_call_with_failure_rate_always_fail(self) -> None:
        """Test calling with 100% failure rate."""
        mock_http = MockHttpRequestCallable(failure_rate=1.0)

        with pytest.raises(ConnectionError, match="Mock HTTP failure"):
            mock_http("GET", "http://example.com")

    def test_call_with_failure_rate_never_fail(self) -> None:
        """Test calling with 0% failure rate."""
        mock_http = MockHttpRequestCallable(failure_rate=0.0)

        response = mock_http("GET", "http://example.com")
        assert response is not None

    @patch("random.random")
    def test_call_with_failure_rate_controlled(self, mock_random: Any) -> None:
        """Test calling with controlled failure rate."""
        mock_random.return_value = 0.2  # Below 0.3 threshold
        mock_http = MockHttpRequestCallable(failure_rate=0.3)

        with pytest.raises(ConnectionError, match="Mock HTTP failure"):
            mock_http("GET", "http://example.com")

    def test_call_history_tracking(self) -> None:
        """Test call history tracking."""
        mock_http = MockHttpRequestCallable()

        mock_http("GET", "http://example.com", headers={"Auth": "Bearer token"})
        mock_http("POST", "http://example.com/data", data={"key": "value"})

        assert mock_http.call_count == 2
        assert len(mock_http.call_history) == 2

        assert mock_http.call_history[0]["method"] == "GET"
        assert mock_http.call_history[0]["url"] == "http://example.com"
        assert mock_http.call_history[0]["kwargs"]["headers"]["Auth"] == "Bearer token"

        assert mock_http.call_history[1]["method"] == "POST"
        assert mock_http.call_history[1]["url"] == "http://example.com/data"
        assert mock_http.call_history[1]["kwargs"]["data"]["key"] == "value"

    def test_multiple_calls_increment_tokens(self) -> None:
        """Test multiple calls increment token numbers."""
        mock_http = MockHttpRequestCallable()

        response1 = mock_http("POST", "http://example.com/token")
        response2 = mock_http("POST", "http://example.com/token")

        data1 = response1.json()
        data2 = response2.json()

        assert data1["access_token"] == "mock_token_1"
        assert data2["access_token"] == "mock_token_2"
        assert data1["refresh_token"] == "mock_refresh_1"
        assert data2["refresh_token"] == "mock_refresh_2"


class TestIntegrationScenarios:
    """Integration tests for complex scenarios."""

    def test_full_refresh_cycle_with_bearer_auth(self) -> None:
        """Test complete refresh cycle with Bearer auth."""
        strategy = MockBearerAuthWithRefresh(initial_token="initial_bearer", refresh_token="refresh_bearer")

        # Initial state
        headers: Dict[str, str] = {}
        strategy.apply_auth(headers)
        assert headers["Authorization"] == "Bearer initial_bearer"

        # Simulate expiration
        strategy.set_expired(True)
        assert strategy.is_expired() is True

        # Refresh token
        result = strategy.refresh()
        assert result is not None
        assert strategy.is_expired() is False

        # Use refreshed token
        headers = {}
        strategy.apply_auth(headers)
        assert headers["Authorization"] == "Bearer initial_bearer_refreshed_1"

    def test_error_injection_with_recovery(self) -> None:
        """Test error injection followed by recovery."""
        strategy = MockAuthErrorInjector.create_failing_refresh_strategy(
            failure_type="network", failure_after_attempts=1, initial_token="recovery_token"
        )

        # First refresh should succeed
        result1 = strategy.refresh()
        assert result1 is not None
        assert strategy.current_token == "recovery_token_refreshed_1"

        # Second refresh should fail
        with pytest.raises(ConnectionError):
            strategy.refresh()

        # Token should still be the last successful one
        assert strategy.current_token == "recovery_token_refreshed_1"

    def test_concurrent_refresh_with_callback(self) -> None:
        """Test concurrent refresh operations using callbacks."""
        strategy = AuthTestScenarioBuilder.create_concurrent_refresh_scenario()
        callback = strategy.get_refresh_callback()

        results: list[str] = []
        errors: list[Exception] = []

        def worker() -> None:
            try:
                if callback is not None:
                    callback()
                    results.append(strategy.current_token)
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads: list[threading.Thread] = []
        for _ in range(5):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # All should succeed (no errors)
        assert len(errors) == 0
        assert len(results) == 5

        # Check that concurrent tracking worked
        assert strategy.max_concurrent_refreshes >= 1


class TestMockAuthStrategyExceptionHandling:
    """Test cases for MockAuthStrategy exception handling."""

    def test_prepare_request_raises_configured_exception(self) -> None:
        """Test prepare_request raises the configured exception."""
        from apiconfig.testing.unit.mocks.auth import MockAuthStrategy

        test_exception = ValueError("Test exception")
        strategy = MockAuthStrategy(raise_exception=test_exception)

        with pytest.raises(ValueError, match="Test exception"):
            strategy.prepare_request()

    def test_prepare_request_headers_with_none_input(self) -> None:
        """Test prepare_request_headers with None input."""
        from apiconfig.testing.unit.mocks.auth import MockAuthStrategy

        strategy = MockAuthStrategy()
        result = strategy.prepare_request_headers(None)

        assert result == {}

    def test_prepare_request_params_with_none_input(self) -> None:
        """Test prepare_request_params with None input."""
        from apiconfig.testing.unit.mocks.auth import MockAuthStrategy

        strategy = MockAuthStrategy()
        result = strategy.prepare_request_params(None)

        assert result == {}

    def test_prepare_request_normal_flow(self) -> None:
        """Test prepare_request normal flow with headers and params."""
        from apiconfig.testing.unit.mocks.auth import MockAuthStrategy

        strategy = MockAuthStrategy(override_headers={"Override": "Header"}, override_params={"override": "param"})

        input_headers = {"Existing": "Header"}
        input_params = {"existing": "param"}

        result_headers, result_params = strategy.prepare_request(input_headers, input_params)

        # Should merge existing with overrides
        assert result_headers == {"Existing": "Header", "Override": "Header"}
        assert result_params == {"existing": "param", "override": "param"}


class TestMockAuthInheritance:
    """Test cases for MockAuth inheritance and initialization."""

    def test_mock_basic_auth_inheritance(self) -> None:
        """Test MockBasicAuth inheritance and initialization."""
        from apiconfig.testing.unit.mocks.auth import MockBasicAuth

        strategy = MockBasicAuth(
            username="testuser",
            password="testpass",
            override_headers={"Custom": "Header"},
            override_params={"param": "value"},
        )

        # Test that both parent classes are properly initialized
        assert hasattr(strategy, "username")
        assert hasattr(strategy, "password")
        assert strategy.override_headers == {"Custom": "Header"}
        assert strategy.override_params == {"param": "value"}

    def test_mock_bearer_auth_inheritance(self) -> None:
        """Test MockBearerAuth inheritance and initialization."""
        from apiconfig.testing.unit.mocks.auth import MockBearerAuth

        strategy = MockBearerAuth(
            token="testtoken",
            override_headers={"Custom": "Header"},
            override_params={"param": "value"},
        )

        # Test that both parent classes are properly initialized
        assert hasattr(strategy, "access_token")  # BearerAuth uses access_token, not token
        assert strategy.override_headers == {"Custom": "Header"}
        assert strategy.override_params == {"param": "value"}

    def test_mock_api_key_auth_inheritance(self) -> None:
        """Test MockApiKeyAuth inheritance and initialization."""
        from apiconfig.testing.unit.mocks.auth import MockApiKeyAuth

        strategy = MockApiKeyAuth(
            api_key="testapikey",
            header_name="X-API-Key",
            # param_name="api_key",  # Cannot provide both header_name and param_name
            override_headers={"Custom": "Header"},
            override_params={"param": "value"},
        )

        # Test that both parent classes are properly initialized
        assert hasattr(strategy, "api_key")
        assert hasattr(strategy, "header_name")
        assert strategy.override_headers == {"Custom": "Header"}
        assert strategy.override_params == {"param": "value"}

    def test_mock_custom_auth_inheritance(self) -> None:
        """Test MockCustomAuth inheritance and initialization."""
        from apiconfig.testing.unit.mocks.auth import MockCustomAuth

        strategy = MockCustomAuth(
            override_headers={"Custom": "Header"},
            override_params={"param": "value"},
        )

        # Test that MockAuthStrategy is properly initialized
        assert strategy.override_headers == {"Custom": "Header"}
        assert strategy.override_params == {"param": "value"}


class TestCrudclientIntegrationErrorHandling:
    """Test cases for crudclient integration error handling."""

    def test_crudclient_integration_callback_none_handling(self) -> None:
        """Test crudclient integration when original callback is None."""
        strategy = AuthTestScenarioBuilder.create_crudclient_integration_scenario()

        # Make the original get_refresh_callback return None
        strategy._can_refresh = False  # pyright: ignore[reportPrivateUsage]

        callback = strategy.get_refresh_callback()
        assert callback is None
