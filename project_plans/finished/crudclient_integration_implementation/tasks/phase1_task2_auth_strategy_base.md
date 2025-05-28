# Phase 1, Task 2: Auth Strategy Base Class Enhancement ✅ **COMPLETED**

## Overview
Extend the [`apiconfig/auth/base.py`](/workspace/apiconfig/auth/base.py) `AuthStrategy` base class with refresh interface methods to support auth refresh scenarios and crudclient integration.

## Objective
Add the core refresh interface to the `AuthStrategy` base class, enabling all auth strategies to support refresh capabilities and provide callbacks compatible with crudclient's retry logic.

## ✅ Completion Status
**Completed**: May 27, 2025
**Commit**: `feat: implement phase 1 crudclient integration - auth refresh capabilities`
**Status**: All refresh interface methods successfully implemented in base class

## Requirements

### 1. Add HTTP Request Callable Support
Extend the `AuthStrategy` class to accept an optional HTTP request callable:

```python
from typing import Optional, Callable, Any
from apiconfig.types import HttpRequestCallable, TokenRefreshResult, AuthRefreshCallback

class AuthStrategy(ABC):
    def __init__(self, http_request_callable: Optional[HttpRequestCallable] = None):
        """
        Initialize the AuthStrategy.

        Args:
            http_request_callable: An optional callable that the strategy can use
                                   to make HTTP requests (e.g., for token refresh).
                                   This callable should handle the actual HTTP communication.
                                   Its signature should be compatible with the needs of
                                   the refresh mechanism (e.g., taking URL, method, data, headers).
        """
        self._http_request_callable = http_request_callable
```

### 2. Add Refresh Interface Methods
Add the following abstract/default methods to support refresh functionality:

```python
def can_refresh(self) -> bool:
    """
    Check if this auth strategy supports refresh and is configured to do so.
    A strategy can refresh if it implements refresh logic AND has been
    provided with necessary components (like an _http_request_callable).

    Returns:
        bool: True if refresh is supported and possible, False otherwise.
    """
    return False

def refresh(self) -> Optional[TokenRefreshResult]:
    """
    Refresh authentication credentials.
    This method will typically use the injected _http_request_callable
    to perform the refresh operation (e.g., call a token refresh endpoint).
    It should update the strategy's internal state with the new access token.

    Returns:
        Optional[TokenRefreshResult]: A structure containing:
            - 'token_data': RefreshedTokenData with the new access token,
              potentially a new refresh token, expiry time, etc.
              The application is responsible for persisting the new refresh
              token (if provided) using a TokenStorage implementation.
            - 'config_updates': Optional dictionary of configuration values
              (e.g., a new API endpoint URL) that were updated during the
              refresh process. The calling client would be responsible for applying these.
        Returns None if refresh is not supported, fails critically, or if
        there's nothing to return.

    Raises:
        NotImplementedError: If the strategy does not support refresh.
        TokenRefreshError: If refresh fails due to invalid credentials or network issues.
        AuthStrategyError: If refresh fails due to strategy-specific issues.
    """
    raise NotImplementedError("This auth strategy does not support refresh")

def is_expired(self) -> bool:
    """
    Check if current credentials are known to be expired.
    This might involve checking an expiry timestamp if available.

    Returns:
        bool: True if credentials are known to be expired, False otherwise.
              Returns False by default if expiry cannot be determined.
    """
    return False

def get_refresh_callback(self) -> Optional[AuthRefreshCallback]:
    """
    Get a callback function suitable for crudclient's setup_auth_func parameter.
    This allows the retry mechanism to trigger this strategy's refresh logic.

    Returns:
        Optional[AuthRefreshCallback]: A callable that performs refresh when called,
                                      or None if refresh is not supported.
    """
    if self.can_refresh():
        def refresh_callback() -> None:
            """Callback wrapper for refresh operation."""
            self.refresh()
        return refresh_callback
    return None
```

### 3. Update Existing Methods
Ensure existing methods are compatible with the new refresh interface:
- Keep existing `prepare_request_headers()` and `prepare_request_params()` methods unchanged
- Ensure thread safety considerations for refresh scenarios
- Note: Auth strategies should continue using `prepare_request_headers()` for applying authentication

## Implementation Steps

1. **Read current auth/base.py** to understand existing structure
2. **Add required imports** from the new types module
3. **Modify `__init__` method** to accept `http_request_callable` parameter
4. **Add the four new interface methods** with comprehensive docstrings
5. **Update existing method signatures** if needed for compatibility
6. **Add logging imports** for future logging integration
7. **Ensure thread safety** considerations are documented

## Files to Modify
- [`apiconfig/auth/base.py`](/workspace/apiconfig/auth/base.py)

## Dependencies
- [Phase 1, Task 1: Type Definitions Enhancement](phase1_task1_type_definitions.md)

## Quality Gates

### Interface Consistency
- [ ] All new methods have consistent signatures and return types
- [ ] Docstrings follow numpy style and are comprehensive
- [ ] Abstract base class principles are maintained

### Interface Enhancement
- [ ] New refresh interface methods properly implemented
- [ ] No breaking changes to public API
- [ ] Default implementations provide safe fallbacks

### Type Safety
- [ ] All new methods pass mypy validation
- [ ] Type hints are accurate and complete
- [ ] Import statements are correct

### Testing Requirements
- [ ] Unit tests for each new method
- [ ] Tests for default implementations
- [ ] Tests for interface consistency across strategies
- [ ] Mock tests for refresh callback functionality

## Success Criteria
- [x] `AuthStrategy` base class has complete refresh interface
- [x] All new methods have default implementations that don't break existing code
- [x] `get_refresh_callback()` returns callable compatible with crudclient interface
- [x] Thread safety considerations are documented
- [x] All existing auth strategies continue to work without modification
- [x] Comprehensive unit test coverage for new interface methods

## Notes
- The `refresh()` method should be designed to be called multiple times safely
- Consider thread safety implications for concurrent refresh operations
- The `get_refresh_callback()` wrapper ensures compatibility with crudclient's expected signature
- Default implementations should be safe and non-breaking
- Future tasks will implement these methods in concrete strategy classes

## Estimated Effort
4-5 hours

## Next Task
[Phase 1, Task 3: Bearer Auth Strategy Enhancement](phase1_task3_bearer_auth_enhancement.md)