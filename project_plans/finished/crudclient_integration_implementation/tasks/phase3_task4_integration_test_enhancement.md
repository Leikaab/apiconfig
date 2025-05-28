# Phase 3, Task 4: Tripletex Integration Test Enhancement

## Overview
Enhance the Tripletex integration tests with refresh capabilities to demonstrate the complete auth refresh functionality in a real-world scenario. This focuses on live API testing with Tripletex's session-based authentication rather than mocked scenarios.

## Objective
Create comprehensive integration tests that demonstrate auth refresh functionality using the Tripletex API as a real-world example, validating the complete refresh flow from auth strategy through to successful API calls.

## Requirements

### 1. Enhanced TripletexSessionAuth Strategy
Based on the original plan's Section 10.1.1, enhance the existing Tripletex auth strategy with refresh capabilities:

```python
# Enhancement to existing TripletexSessionAuth in helpers_for_tests/tripletex/
class TripletexSessionAuth(AuthStrategy):
    """
    Enhanced Tripletex session authentication with refresh capabilities.

    This strategy performs two-step auth (consumer+employee tokens → session token → Basic auth)
    and supports session token refresh when expired.
    """

    def __init__(
        self,
        consumer_token: str,
        employee_token: str,
        company_id: str,
        session_token_hostname: str,
        http_request_callable: Optional[HttpRequestCallable] = None
    ):
        """
        Initialize Tripletex session auth with refresh capabilities.

        Parameters
        ----------
        consumer_token : str
            Tripletex consumer token
        employee_token : str
            Tripletex employee token
        company_id : str
            Company ID for session creation
        session_token_hostname : str
            Hostname for session token requests
        http_request_callable : Optional[HttpRequestCallable]
            HTTP callable for making refresh requests
        """
        super().__init__(http_request_callable)
        self.consumer_token = consumer_token
        self.employee_token = employee_token
        self.company_id = company_id
        self.session_token_hostname = session_token_hostname
        self._session_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    def can_refresh(self) -> bool:
        """Tripletex session tokens can be refreshed using consumer/employee tokens."""
        return self._http_request_callable is not None

    def is_expired(self) -> bool:
        """Check if session token is expired or close to expiring."""
        if self._token_expires_at is None:
            return True  # No token yet
        # Refresh 5 minutes before expiration
        return datetime.now(timezone.utc) >= (self._token_expires_at - timedelta(minutes=5))

    def refresh(self) -> Optional[TokenRefreshResult]:
        """Refresh the session token using consumer/employee tokens."""
        if not self.can_refresh():
            return None

        try:
            # Use _http_request_callable to fetch new session token
            new_token = self._fetch_session_token()
            self._session_token = new_token
            self._token_expires_at = datetime.now(timezone.utc) + timedelta(days=2)  # 2 day expiry

            # Return structured result for application persistence
            refreshed_token_data: RefreshedTokenData = {
                "access_token": new_token,
                "expires_in": 172800,  # 2 days in seconds
                "token_type": "session"
            }

            result: TokenRefreshResult = {
                "token_data": refreshed_token_data,
                "config_updates": None
            }

            return result

        except Exception as e:
            raise TokenRefreshError(f"Failed to refresh Tripletex session token: {str(e)}") from e

    def get_refresh_callback(self) -> Optional[Callable[[], None]]:
        """Get callback function for crudclient-style refresh integration."""
        if self.can_refresh():
            def refresh_callback():
                self.refresh()
            return refresh_callback
        return None
```

### 2. Integration Test Enhancements
Create comprehensive integration tests in `tests/integration/test_tripletex_auth_refresh.py`:

```python
class TestTripletexAuthRefresh:
    """Test auth refresh functionality with Tripletex live API."""

    def test_session_token_refresh_on_expiry(self, tripletex_client):
        """Test that session token is refreshed when expired."""
        auth_strategy = tripletex_client.config.auth_strategy

        # Force token expiration
        auth_strategy._token_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        assert auth_strategy.is_expired()

        # Make request - should trigger refresh
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # Verify new token was obtained and is not expired
        assert not auth_strategy.is_expired()
        assert auth_strategy._session_token is not None

    def test_refresh_callback_integration(self, tripletex_client):
        """Test integration with crudclient-style refresh callback."""
        auth_strategy = tripletex_client.config.auth_strategy

        # Get refresh callback
        refresh_callback = auth_strategy.get_refresh_callback()
        assert refresh_callback is not None

        # Simulate crudclient retry logic calling the callback
        old_token = auth_strategy._session_token
        refresh_callback()  # Should refresh without error

        # Verify token was refreshed
        new_token = auth_strategy._session_token
        assert new_token is not None
        assert not auth_strategy.is_expired()

    def test_token_refresh_result_structure(self, tripletex_client):
        """Test that refresh returns proper TokenRefreshResult structure."""
        auth_strategy = tripletex_client.config.auth_strategy

        if auth_strategy.can_refresh():
            result = auth_strategy.refresh()
            assert result is not None
            assert "token_data" in result
            assert "config_updates" in result

            token_data = result["token_data"]
            assert "access_token" in token_data
            assert "expires_in" in token_data
            assert "token_type" in token_data
            assert token_data["token_type"] == "session"

    def test_concurrent_refresh_thread_safety(self, tripletex_client):
        """Test that concurrent refresh operations are thread-safe."""
        import threading
        import time

        auth_strategy = tripletex_client.config.auth_strategy
        results = []
        errors = []

        def refresh_worker():
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

        # Verify final state is consistent
        assert not auth_strategy.is_expired()

    def test_refresh_failure_handling(self, tripletex_client):
        """Test proper error handling when refresh fails."""
        auth_strategy = tripletex_client.config.auth_strategy

        # Temporarily break the auth strategy to force failure
        original_consumer_token = auth_strategy.consumer_token
        auth_strategy.consumer_token = "invalid_token"

        try:
            with pytest.raises(TokenRefreshError):
                auth_strategy.refresh()
        finally:
            # Restore original token
            auth_strategy.consumer_token = original_consumer_token

    def test_logging_during_refresh(self, tripletex_client, caplog):
        """Test that refresh operations are properly logged."""
        auth_strategy = tripletex_client.config.auth_strategy

        with caplog.at_level(logging.DEBUG):
            auth_strategy.refresh()

        # Verify refresh operation was logged
        refresh_logs = [record for record in caplog.records if "refresh" in record.message.lower()]
        assert len(refresh_logs) > 0, "No refresh operations logged"

        # Verify sensitive data is redacted
        for record in caplog.records:
            assert auth_strategy.consumer_token not in record.message
            assert auth_strategy.employee_token not in record.message
```

### 3. Live Testing Scenarios
Create specific test scenarios that validate real-world usage:

```python
class TestTripletexLiveScenarios:
    """Test real-world scenarios with Tripletex API."""

    def test_full_auth_refresh_cycle(self, tripletex_client):
        """Test complete auth refresh cycle with actual API calls."""
        # 1. Make initial API call to establish session
        countries = tripletex_client.list_countries()
        assert isinstance(countries, dict)

        # 2. Force token expiration
        auth_strategy = tripletex_client.config.auth_strategy
        auth_strategy._token_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

        # 3. Make another API call - should trigger refresh
        companies = tripletex_client.list_companies()
        assert isinstance(companies, dict)

        # 4. Verify refresh occurred and new token is valid
        assert not auth_strategy.is_expired()

        # 5. Make final API call to confirm everything works
        currencies = tripletex_client.list_currencies()
        assert isinstance(currencies, dict)

    def test_crudclient_compatibility_pattern(self, tripletex_client):
        """Test patterns that crudclient would use for integration."""
        auth_strategy = tripletex_client.config.auth_strategy

        # Simulate crudclient's setup_auth_func pattern
        setup_auth_func = auth_strategy.get_refresh_callback()
        assert setup_auth_func is not None

        # Simulate 401 error scenario
        auth_strategy._token_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

        # Call setup_auth_func (as crudclient retry logic would)
        setup_auth_func()

        # Verify auth is now valid for retry
        assert not auth_strategy.is_expired()

        # Make API call to confirm
        result = tripletex_client.list_countries()
        assert isinstance(result, dict)
```

## Implementation Steps

1. **Enhance TripletexSessionAuth** in `helpers_for_tests/tripletex/tripletex_auth.py`
2. **Create new integration test file** `tests/integration/test_tripletex_auth_refresh.py`
3. **Add comprehensive test scenarios** covering all refresh patterns
4. **Test thread safety** and concurrent refresh operations
5. **Validate logging** and error handling
6. **Test crudclient compatibility** patterns

## Files to Create/Modify
- `helpers_for_tests/tripletex/tripletex_auth.py` (enhance existing)
- `tests/integration/test_tripletex_auth_refresh.py` (new)
- Update existing Tripletex integration tests if needed

## Dependencies
- All previous Phase 3 tasks
- [Phase 1: Core Auth Interface](../orchestrator_plan.md#phase-1-core-auth-interface-high-priority) completion
- [Phase 2: Testing Enhancement](../orchestrator_plan.md#phase-2-testing-enhancement-medium-priority) completion

## Quality Gates

### Live API Testing
- [ ] All tests pass against live Tripletex API
- [ ] Refresh functionality works in real-world scenarios
- [ ] Thread safety validated with concurrent operations
- [ ] Error handling works with actual API failures

### Integration Validation
- [ ] CrudClient compatibility patterns validated
- [ ] Logging provides useful debugging information
- [ ] Sensitive data properly redacted in logs
- [ ] Performance acceptable for production use

### Documentation
- [ ] Integration examples are clear and comprehensive
- [ ] Real-world usage patterns documented
- [ ] Error scenarios and handling documented

## Success Criteria
- [ ] Tripletex integration tests demonstrate complete refresh functionality
- [ ] Live API testing validates real-world usage patterns
- [ ] Thread safety confirmed for concurrent refresh operations
- [ ] CrudClient compatibility patterns work correctly
- [ ] Comprehensive error handling and logging validated

## Notes
- Focus only on Tripletex since it's the only live API integration test
- Avoid mocked scenarios - this is for real integration testing
- Ensure thread safety since refresh may happen concurrently
- Validate actual crudclient usage patterns
- Consider rate limiting and API quotas during testing

## Estimated Effort
8-10 hours

## Next Task
[Phase 3, Task 5: Documentation and Examples](phase3_task5_documentation_examples.md)