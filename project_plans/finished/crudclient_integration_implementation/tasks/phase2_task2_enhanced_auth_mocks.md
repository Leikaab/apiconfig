# Phase 2, Task 3: Enhanced Auth Mocks for Refresh Scenarios

## Overview
Enhance [`apiconfig/testing/unit/mocks/auth.py`](/workspace/apiconfig/testing/unit/mocks/auth.py) with comprehensive mock implementations for refresh scenarios and error injection capabilities.

## Objective
Provide sophisticated mock auth strategies that can simulate refresh operations, token expiration, and various failure scenarios for comprehensive testing of the auth refresh functionality.

## Requirements

### 1. Enhanced Mock Base Classes
Extend existing mock auth strategies with refresh capabilities:

```python
# Enhanced MockAuthStrategy with refresh support
class MockRefreshableAuthStrategy(MockAuthStrategy):
    """Mock auth strategy with refresh capabilities for testing."""

    def __init__(self,
                 initial_token: str = "mock_token",
                 refresh_token: str = "mock_refresh",
                 can_refresh: bool = True,
                 refresh_success: bool = True,
                 refresh_delay: float = 0.0,
                 max_refresh_attempts: int = 3,
                 **kwargs):
        super().__init__(**kwargs)
        self.initial_token = initial_token
        self.current_token = initial_token
        self.refresh_token = refresh_token
        self._can_refresh = can_refresh
        self._refresh_success = refresh_success
        self._refresh_delay = refresh_delay
        self._max_refresh_attempts = max_refresh_attempts
        self._refresh_attempts = 0
        self._is_expired = False

    def can_refresh(self) -> bool:
        return self._can_refresh and self._refresh_attempts < self._max_refresh_attempts

    def is_expired(self) -> bool:
        return self._is_expired

    def set_expired(self, expired: bool = True) -> None:
        """Set token expiration state for testing."""
        self._is_expired = expired

    def refresh(self) -> Optional[TokenRefreshResult]:
        """Mock refresh implementation with configurable behavior."""
        import time
        from apiconfig.exceptions.auth import TokenRefreshError

        if self._refresh_delay > 0:
            time.sleep(self._refresh_delay)

        self._refresh_attempts += 1

        if not self._refresh_success:
            raise TokenRefreshError("Mock refresh failure")

        if not self.can_refresh():
            raise TokenRefreshError("Mock refresh not available")

        # Generate new token
        new_token = f"{self.initial_token}_refreshed_{self._refresh_attempts}"
        self.current_token = new_token
        self._is_expired = False

        return {
            "token_data": {
                "access_token": new_token,
                "refresh_token": f"{self.refresh_token}_new",
                "expires_in": 3600,
                "token_type": "Bearer"
            },
            "config_updates": None
        }
```

### 2. Specialized Mock Strategies
Create mock implementations for each auth strategy type:

```python
class MockBearerAuthWithRefresh(MockRefreshableAuthStrategy):
    """Mock Bearer auth with refresh capabilities."""

    def apply_auth(self, headers: Dict[str, str]) -> None:
        headers["Authorization"] = f"Bearer {self.current_token}"


    def __init__(self, header_name: str = "X-API-Key", **kwargs):
        super().__init__(**kwargs)
        self.header_name = header_name

    def apply_auth(self, headers: Dict[str, str]) -> None:
        headers[self.header_name] = self.current_token

class MockCustomAuthWithRefresh(MockRefreshableAuthStrategy):
    """Mock Custom auth with configurable refresh behavior."""

    def __init__(self, auth_header_format: str = "Custom {token}", **kwargs):
        super().__init__(**kwargs)
        self.auth_header_format = auth_header_format

    def apply_auth(self, headers: Dict[str, str]) -> None:
        headers["Authorization"] = self.auth_header_format.format(token=self.current_token)
```

### 3. Error Injection Utilities
Add utilities for simulating various error scenarios:

```python
class MockAuthErrorInjector:
    """Utility for injecting errors into mock auth strategies."""

    @staticmethod
    def create_failing_refresh_strategy(
        failure_type: str = "network",
        failure_after_attempts: int = 1,
        **kwargs
    ) -> MockRefreshableAuthStrategy:
        """
        Create a mock strategy that fails refresh after specified attempts.

        Args:
            failure_type: Type of failure ("network", "auth", "timeout")
            failure_after_attempts: Number of successful attempts before failure
            **kwargs: Additional arguments for mock strategy
        """
        strategy = MockRefreshableAuthStrategy(**kwargs)
        original_refresh = strategy.refresh

        def failing_refresh():
            if strategy._refresh_attempts >= failure_after_attempts:
                if failure_type == "network":
                    raise ConnectionError("Mock network failure")
                elif failure_type == "auth":
                    raise TokenRefreshError("Mock authentication failure")
                elif failure_type == "timeout":
                    raise TimeoutError("Mock timeout failure")
                else:
                    raise Exception(f"Mock {failure_type} failure")
            return original_refresh()

        strategy.refresh = failing_refresh
        return strategy

    @staticmethod
    def create_intermittent_failure_strategy(
        failure_probability: float = 0.3,
        **kwargs
    ) -> MockRefreshableAuthStrategy:
        """Create a strategy with intermittent refresh failures."""
        import random

        strategy = MockRefreshableAuthStrategy(**kwargs)
        original_refresh = strategy.refresh

        def intermittent_refresh():
            if random.random() < failure_probability:
                raise TokenRefreshError("Mock intermittent failure")
            return original_refresh()

        strategy.refresh = intermittent_refresh
        return strategy
```

### 4. Test Scenario Builders
Add builders for common test scenarios:

```python
class AuthTestScenarioBuilder:
    """Builder for creating complex auth test scenarios."""

    @staticmethod
    def create_token_expiry_scenario(
        initial_token: str = "initial_token",
        expires_after_seconds: float = 1.0
    ) -> MockRefreshableAuthStrategy:
        """Create a scenario where token expires after specified time."""
        import threading
        import time

        strategy = MockRefreshableAuthStrategy(initial_token=initial_token)

        def expire_token():
            time.sleep(expires_after_seconds)
            strategy.set_expired(True)

        threading.Thread(target=expire_token, daemon=True).start()
        return strategy

    @staticmethod
    def create_concurrent_refresh_scenario(
        num_concurrent_refreshes: int = 5
    ) -> MockRefreshableAuthStrategy:
        """Create a scenario for testing concurrent refresh operations."""
        strategy = MockRefreshableAuthStrategy()

        # Add thread safety tracking
        strategy._refresh_lock = threading.Lock()
        strategy._concurrent_refreshes = 0
        strategy._max_concurrent_refreshes = 0

        original_refresh = strategy.refresh

        def thread_safe_refresh():
            with strategy._refresh_lock:
                strategy._concurrent_refreshes += 1
                strategy._max_concurrent_refreshes = max(
                    strategy._max_concurrent_refreshes,
                    strategy._concurrent_refreshes
                )

            try:
                result = original_refresh()
                return result
            finally:
                with strategy._refresh_lock:
                    strategy._concurrent_refreshes -= 1

        strategy.refresh = thread_safe_refresh
        return strategy

    @staticmethod
    def create_crudclient_integration_scenario() -> MockRefreshableAuthStrategy:
        """Create a scenario that mimics crudclient integration patterns."""
        strategy = MockRefreshableAuthStrategy()

        # Track callback usage
        strategy._callback_calls = 0
        strategy._callback_errors = []

        original_get_refresh_callback = strategy.get_refresh_callback

        def tracked_get_refresh_callback():
            callback = original_get_refresh_callback()
            if callback is None:
                return None

            def tracked_callback():
                strategy._callback_calls += 1
                try:
                    return callback()
                except Exception as e:
                    strategy._callback_errors.append(e)
                    raise

            return tracked_callback

        strategy.get_refresh_callback = tracked_get_refresh_callback
        return strategy
```

### 5. Mock HTTP Request Callable
Create mock HTTP callable for testing refresh operations:

```python
class MockHttpRequestCallable:
    """Mock HTTP request callable for testing auth refresh."""

    def __init__(self,
                 responses: Optional[Dict[str, Any]] = None,
                 delay: float = 0.0,
                 failure_rate: float = 0.0):
        self.responses = responses or {}
        self.delay = delay
        self.failure_rate = failure_rate
        self.call_count = 0
        self.call_history = []

    def __call__(self, method: str, url: str, **kwargs) -> Any:
        """Mock HTTP request implementation."""
        import time
        import random

        self.call_count += 1
        self.call_history.append({
            "method": method,
            "url": url,
            "kwargs": kwargs
        })

        if self.delay > 0:
            time.sleep(self.delay)

        if random.random() < self.failure_rate:
            raise ConnectionError("Mock HTTP failure")

        # Return configured response or default
        response_key = f"{method}:{url}"
        if response_key in self.responses:
            response_data = self.responses[response_key]
        else:
            response_data = {
                "access_token": f"mock_token_{self.call_count}",
                "refresh_token": f"mock_refresh_{self.call_count}",
                "expires_in": 3600,
                "token_type": "Bearer"
            }

        # Create mock response object
        class MockResponse:
            def __init__(self, data):
                self.data = data
                self.status_code = 200
                self.headers = {"Content-Type": "application/json"}

            def json(self):
                return self.data

        return MockResponse(response_data)
```

## Implementation Steps

1. **Review existing mock implementations** in auth.py
2. **Add enhanced mock base classes** with refresh capabilities
3. **Create specialized mock strategies** for each auth type
4. **Implement error injection utilities** for failure scenarios
5. **Add test scenario builders** for complex scenarios
6. **Create mock HTTP callable** for refresh testing
7. **Add comprehensive documentation** and examples
8. **Create unit tests** for all mock implementations

## Files to Modify
- [`apiconfig/testing/unit/mocks/auth.py`](/workspace/apiconfig/testing/unit/mocks/auth.py)

## Dependencies
- [Phase 1 completion](phase1_component_validation.md)
- [Phase 2, Task 1: Auth Verification Utilities](phase2_task1_auth_verification.md)

## Quality Gates

### Functionality
- [ ] Mock strategies support all refresh interface methods
- [ ] Error injection works for various failure scenarios
- [ ] Scenario builders create realistic test conditions
- [ ] Mock HTTP callable handles refresh requests properly

### Testing
- [ ] Unit tests for all mock implementations
- [ ] Integration tests with real auth strategies
- [ ] Performance tests for mock overhead
- [ ] Thread safety tests for concurrent scenarios

### Usability
- [ ] Easy to configure for different test scenarios
- [ ] Clear documentation and examples
- [ ] Intuitive API for test writers
- [ ] Good error messages for debugging

## Success Criteria
- [ ] Comprehensive mock implementations for all auth refresh scenarios
- [ ] Easy simulation of error conditions and edge cases
- [ ] Support for testing concurrent refresh operations
- [ ] Integration with existing test infrastructure
- [ ] Clear documentation and examples for test writers
- [ ] Minimal performance overhead in test environments

## Notes
- Focus on test utility functionality, not production behavior
- Provide realistic simulation of auth refresh scenarios
- Support both positive and negative test cases
- Consider performance impact in large test suites
- Design for easy configuration and customization

## Estimated Effort
5-6 hours

## Next Task
[Phase 2 Component Validation](phase2_component_validation.md)