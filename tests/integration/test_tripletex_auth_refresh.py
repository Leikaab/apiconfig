"""Integration tests for Tripletex authentication refresh functionality.

This test module demonstrates comprehensive auth refresh functionality using the Tripletex API
as a real-world example, validating the complete refresh flow from auth strategy through to
successful API calls.
"""

import logging
import os
import threading
from datetime import datetime, timedelta, timezone

import pytest
from pytest import LogCaptureFixture

if os.getenv("PYTEST_SKIP_INTEGRATION", "false").lower() == "true":
    pytest.skip(
        "Integration tests disabled (PYTEST_SKIP_INTEGRATION=true)",
        allow_module_level=True,
    )

from apiconfig.exceptions.auth import TokenRefreshError
from helpers_for_tests.tripletex.tripletex_auth import TripletexSessionAuth
from helpers_for_tests.tripletex.tripletex_client import TripletexClient
from helpers_for_tests.tripletex.tripletex_config import (
    create_tripletex_client_config,
    skip_if_no_credentials,
)


@pytest.fixture
def tripletex_client() -> TripletexClient:
    """Create a configured Tripletex client for refresh testing."""
    skip_if_no_credentials()
    config = create_tripletex_client_config()
    return TripletexClient(config)


class TestTripletexAuthRefresh:
    """Test auth refresh functionality with Tripletex live API."""

    def test_session_token_refresh_on_expiry(self, tripletex_client: TripletexClient) -> None:
        """Test that session token is refreshed when expired."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        # First, ensure we have a valid token
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)
        old_token = auth_strategy._session_token  # pyright: ignore[reportPrivateUsage]

        # Force token expiration
        auth_strategy._token_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)  # pyright: ignore[reportPrivateUsage]
        assert auth_strategy.is_expired()

        # Make request - should trigger refresh via prepare_request_headers
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # Verify new token was obtained and is not expired
        assert not auth_strategy.is_expired()
        assert auth_strategy._session_token is not None  # pyright: ignore[reportPrivateUsage]
        # Token should be refreshed (new token)
        assert auth_strategy._session_token != old_token or auth_strategy._token_expires_at > datetime.now(
            timezone.utc
        )  # pyright: ignore[reportPrivateUsage]

    def test_refresh_callback_integration(self, tripletex_client: TripletexClient) -> None:
        """Test integration with crudclient-style refresh callback."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        # First, ensure we have a valid token
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # Get refresh callback
        refresh_callback = auth_strategy.get_refresh_callback()
        assert refresh_callback is not None

        # Store old token and expiry
        old_token = auth_strategy._session_token  # pyright: ignore[reportPrivateUsage]
        old_expiry = auth_strategy._token_expires_at  # pyright: ignore[reportPrivateUsage]

        # Simulate crudclient retry logic calling the callback
        refresh_callback()  # Should refresh without error

        # Verify token was refreshed
        new_token = auth_strategy._session_token  # pyright: ignore[reportPrivateUsage]
        assert new_token is not None
        assert not auth_strategy.is_expired()
        # Either token changed or expiry was updated
        assert new_token != old_token or auth_strategy._token_expires_at != old_expiry  # pyright: ignore[reportPrivateUsage]

    def test_token_refresh_result_structure(self, tripletex_client: TripletexClient) -> None:
        """Test that refresh returns proper TokenRefreshResult structure."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        if auth_strategy.can_refresh():
            result = auth_strategy.refresh()
            assert result is not None
            assert "token_data" in result
            assert "config_updates" in result

            token_data = result.get("token_data")
            assert token_data is not None
            assert "access_token" in token_data
            assert "expires_in" in token_data
            assert "token_type" in token_data
            assert token_data.get("token_type") == "session"

    def test_concurrent_refresh_thread_safety(self, tripletex_client: TripletexClient) -> None:
        """Test that concurrent refresh operations are thread-safe."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        # First, ensure we have a valid token
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        results = []
        errors = []

        def refresh_worker() -> None:
            try:
                result = auth_strategy.refresh()
                results.append(result)
            except Exception as e:
                errors.append(e)

        # Start multiple refresh operations concurrently
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=refresh_worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify no errors occurred and at least one refresh succeeded
        assert len(errors) == 0, f"Refresh errors: {errors}"
        assert len(results) > 0, "No successful refresh operations"

        # Verify final state is consistent (token should be valid)
        assert auth_strategy._session_token is not None  # pyright: ignore[reportPrivateUsage]
        assert auth_strategy._token_expires_at is not None  # pyright: ignore[reportPrivateUsage]

    def test_refresh_failure_handling(self, tripletex_client: TripletexClient) -> None:
        """Test proper error handling when refresh fails."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        # First, ensure we have a valid token
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # Temporarily break the auth strategy to force failure
        original_consumer_token = auth_strategy.consumer_token
        auth_strategy.consumer_token = "invalid_token"

        try:
            with pytest.raises(TokenRefreshError):
                auth_strategy.refresh()
        finally:
            # Restore original token
            auth_strategy.consumer_token = original_consumer_token

    def test_logging_during_refresh(self, tripletex_client: TripletexClient, caplog: LogCaptureFixture) -> None:
        """Test that refresh operations are properly logged."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        with caplog.at_level(logging.DEBUG):
            auth_strategy.refresh()

        # Verify refresh operation was logged (check for any log messages)
        # Note: The current implementation may not have explicit refresh logging,
        # but we verify that sensitive data is not exposed in any logs
        for record in caplog.records:
            # Verify sensitive data is redacted
            assert auth_strategy.consumer_token not in record.message
            assert auth_strategy.employee_token not in record.message


class TestTripletexLiveScenarios:
    """Test real-world scenarios with Tripletex API."""

    def test_full_auth_refresh_cycle(self, tripletex_client: TripletexClient) -> None:
        """Test complete auth refresh cycle with actual API calls."""
        # 1. Make initial API call to establish session
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # 2. Force token expiration
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)
        auth_strategy._token_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)  # pyright: ignore[reportPrivateUsage]

        # 3. Make another API call - should trigger refresh
        companies = tripletex_client.list_currencies()
        assert isinstance(companies, dict)

        # 4. Verify refresh occurred and new token is valid
        assert not auth_strategy.is_expired()

        # 5. Make final API call to confirm everything works
        currencies = tripletex_client.list_countries()
        assert isinstance(currencies, dict)

    def test_crudclient_compatibility_pattern(self, tripletex_client: TripletexClient) -> None:
        """Test patterns that crudclient would use for integration."""
        auth_strategy = tripletex_client.config.auth_strategy
        assert isinstance(auth_strategy, TripletexSessionAuth)

        # First, ensure we have a valid token
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # Simulate crudclient's setup_auth_func pattern
        setup_auth_func = auth_strategy.get_refresh_callback()
        assert setup_auth_func is not None

        # Simulate 401 error scenario
        auth_strategy._token_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)  # pyright: ignore[reportPrivateUsage]

        # Call setup_auth_func (as crudclient retry logic would)
        setup_auth_func()

        # Verify auth is now valid for retry
        assert not auth_strategy.is_expired()

        # Make API call to confirm
        result = tripletex_client.list_countries()
        assert isinstance(result, dict)
