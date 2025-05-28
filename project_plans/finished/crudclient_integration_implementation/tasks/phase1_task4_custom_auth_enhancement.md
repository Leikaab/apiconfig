# Phase 1, Task 4: Custom Auth Strategy Enhancement ✅ **COMPLETED**

## Overview
Enhance the [`apiconfig/auth/strategies/custom.py`](/workspace/apiconfig/auth/strategies/custom.py) Custom authentication strategy to fully support the refresh interface, enabling custom strategies to implement refresh capabilities.

## Objective
Ensure that custom authentication strategies can implement the complete refresh interface, providing examples and documentation for custom refresh implementations while maintaining the flexibility that makes custom strategies valuable.

## ✅ Completion Status
**Completed**: May 27, 2025
**Commit**: `feat: implement phase 1 crudclient integration - auth refresh capabilities`
**Status**: Custom auth strategy enhanced with configurable refresh functions and factory methods

## Requirements

### 1. Enhanced Constructor
Update the `CustomAuth` class to support refresh functionality:

```python
from typing import Optional, Callable, Dict, Any
from apiconfig.types import HttpRequestCallable, TokenRefreshResult

class CustomAuth(AuthStrategy):
    def __init__(
        self,
        header_callback: Optional[Callable[[], Dict[str, str]]] = None,
        param_callback: Optional[Callable[[], Dict[str, str]]] = None,
        refresh_func: Optional[Callable[[], Optional[TokenRefreshResult]]] = None,
        can_refresh_func: Optional[Callable[[], bool]] = None,
        is_expired_func: Optional[Callable[[], bool]] = None,
        http_request_callable: Optional[HttpRequestCallable] = None
    ):
        """
        Initialize custom authentication with optional refresh capabilities.

        Args:
            header_callback: Function to generate authentication headers
            param_callback: Function to generate authentication parameters
            refresh_func: Optional function to perform refresh operations
            can_refresh_func: Optional function to check if refresh is possible
            is_expired_func: Optional function to check if credentials are expired
            http_request_callable: Optional HTTP callable for refresh operations
        """
        super().__init__(http_request_callable)

        # Validate that at least one callback is provided (existing validation)
        if header_callback is None and param_callback is None:
            raise AuthStrategyError("At least one callback (header or param) must be provided for CustomAuth.")

        self._header_callback = header_callback
        self._param_callback = param_callback
        self.refresh_func = refresh_func
        self.can_refresh_func = can_refresh_func
        self.is_expired_func = is_expired_func
```

### 2. Implement Refresh Interface Methods

```python
def can_refresh(self) -> bool:
    """
    Check if this custom auth strategy can perform refresh operations.

    Returns:
        bool: True if refresh function is provided and indicates refresh is possible
    """
    if self.can_refresh_func is not None:
        return self.can_refresh_func()
    return self.refresh_func is not None

def is_expired(self) -> bool:
    """
    Check if current credentials are expired.

    Returns:
        bool: True if expired function indicates expiration, False otherwise
    """
    if self.is_expired_func is not None:
        return self.is_expired_func()
    return False  # Default to not expired if no function provided

def refresh(self) -> Optional[TokenRefreshResult]:
    """
    Refresh authentication credentials using the provided refresh function.

    Returns:
        Optional[TokenRefreshResult]: Result from refresh function or None

    Raises:
        AuthStrategyError: If no refresh function is configured
    """
    if self.refresh_func is None:
        raise AuthStrategyError("Custom auth strategy has no refresh function configured")

    try:
        return self.refresh_func()
    except Exception as e:
        raise AuthStrategyError(f"Custom auth refresh failed: {str(e)}") from e

def prepare_request_headers(self) -> Dict[str, str]:
    """
    Generate request headers using the header_callback, if provided.
    Enhanced to work with refresh scenarios.

    Returns:
        Dict[str, str]: A dictionary of headers

    Raises:
        AuthStrategyError: If the header_callback fails or returns invalid data
    """
    if self._header_callback:
        try:
            result = self._header_callback()
            if not isinstance(result, dict):
                raise AuthStrategyError("CustomAuth header callback must return a dictionary.")
            return result
        except Exception as e:
            raise AuthStrategyError(f"CustomAuth header callback failed: {e}") from e
    return {}

def prepare_request_params(self) -> Optional[QueryParamType]:
    """
    Generate request parameters using the param_callback, if provided.
    Enhanced to work with refresh scenarios.

    Returns:
        Optional[QueryParamType]: A dictionary of parameters

    Raises:
        AuthStrategyError: If the param_callback fails or returns invalid data
    """
    if self._param_callback:
        try:
            result = self._param_callback()
            if not isinstance(result, dict):
                raise AuthStrategyError("CustomAuth parameter callback must return a dictionary.")
            return result
        except Exception as e:
            raise AuthStrategyError(f"CustomAuth parameter callback failed: {e}") from e
    return {}
```

### 3. Factory Methods for Common Patterns
Add factory methods to simplify creation of common custom auth patterns:

```python
@classmethod
def create_api_key_custom(
    cls,
    api_key: str,
    header_name: str = "X-API-Key",
    http_request_callable: Optional[HttpRequestCallable] = None
) -> 'CustomAuth':
    """
    Create a custom auth strategy for simple API key authentication.

    Args:
        api_key: The API key value
        header_name: Header name for the API key (default: "X-API-Key")
        http_request_callable: Optional HTTP callable for operations

    Returns:
        CustomAuth: Configured custom auth strategy
    """
    def auth_func(headers: Dict[str, str]) -> None:
        headers[header_name] = api_key

    return cls(
        auth_func=auth_func,
        http_request_callable=http_request_callable
    )

@classmethod
def create_session_token_custom(
    cls,
    session_token: str,
    session_refresh_func: Callable[[], str],
    header_name: str = "Authorization",
    token_prefix: str = "Session",
    http_request_callable: Optional[HttpRequestCallable] = None
) -> 'CustomAuth':
    """
    Create a custom auth strategy for session token authentication with refresh.

    Args:
        session_token: Initial session token
        session_refresh_func: Function to refresh the session token
        header_name: Header name for the token (default: "Authorization")
        token_prefix: Prefix for the token value (default: "Session")
        http_request_callable: Optional HTTP callable for refresh operations

    Returns:
        CustomAuth: Configured custom auth strategy
    """
    current_token = {"token": session_token}

    def auth_func(headers: Dict[str, str]) -> None:
        headers[header_name] = f"{token_prefix} {current_token['token']}"

    def refresh_func() -> Optional[TokenRefreshResult]:
        new_token = session_refresh_func()
        current_token["token"] = new_token

        return {
            "token_data": {
                "access_token": new_token,
                "token_type": "session"
            },
            "config_updates": None
        }

    return cls(
        auth_func=auth_func,
        refresh_func=refresh_func,
        can_refresh_func=lambda: True,
        http_request_callable=http_request_callable
    )
```

### 4. Documentation and Examples
Add comprehensive docstring examples:

```python
class CustomAuth(AuthStrategy):
    """
    Custom authentication strategy with optional refresh capabilities.

    This strategy allows for completely custom authentication logic while
    still supporting the refresh interface for integration with retry mechanisms.

    Examples:
        Basic custom auth without refresh:

        >>> def my_auth(headers):
        ...     headers["X-Custom-Auth"] = "my-secret-token"
        >>> auth = CustomAuth(auth_func=my_auth)

        Custom auth with refresh capabilities:

        >>> def my_auth(headers):
        ...     headers["Authorization"] = f"Bearer {current_token['value']}"
        >>> def my_refresh():
        ...     new_token = fetch_new_token()
        ...     current_token['value'] = new_token
        ...     return {"token_data": {"access_token": new_token}}
        >>> auth = CustomAuth(
        ...     auth_func=my_auth,
        ...     refresh_func=my_refresh,
        ...     can_refresh_func=lambda: True
        ... )

        Using factory methods:

        >>> auth = CustomAuth.create_api_key_custom(
        ...     api_key="my-key",
        ...     header_name="X-API-Key"
        ... )
    """
```

## Implementation Steps

1. **Read current custom.py** to understand existing implementation
2. **Add required imports** for new types and exceptions
3. **Enhance the constructor** with refresh-related parameters
4. **Implement the refresh interface methods** with proper delegation
5. **Add factory methods** for common custom auth patterns
6. **Add comprehensive documentation** with examples
7. **Add validation** for function parameters

## Files to Modify
- [`apiconfig/auth/strategies/custom.py`](/workspace/apiconfig/auth/strategies/custom.py)

## Dependencies
- [Phase 1, Task 1: Type Definitions Enhancement](phase1_task1_type_definitions.md)
- [Phase 1, Task 2: Auth Strategy Base Class Enhancement](phase1_task2_auth_strategy_base.md)

## Quality Gates

### Functionality
- [ ] Custom auth strategies can implement full refresh interface
- [ ] Factory methods work for common patterns
- [ ] Backward compatibility maintained for existing usage
- [ ] Proper error handling and validation

### Documentation
- [ ] Comprehensive docstrings with examples
- [ ] Clear guidance for implementing custom refresh logic
- [ ] Factory method documentation with use cases
- [ ] Migration guide for existing custom auth users

### Testing Requirements
- [ ] Unit tests for all new methods and factory methods
- [ ] Tests for refresh interface implementation
- [ ] Tests for error scenarios and edge cases
- [ ] Example implementations that demonstrate patterns
- [ ] Backward compatibility tests

## Success Criteria
- [x] `CustomAuth` fully supports refresh interface through function delegation
- [x] Factory methods provide easy creation of common custom auth patterns
- [x] Comprehensive documentation and examples for custom refresh implementations
- [x] Enhanced custom auth functionality works correctly
- [x] Clear guidance for implementing custom refresh strategies
- [x] Proper error handling and validation throughout

## Notes
- Custom auth strategies should remain maximally flexible
- Factory methods provide convenience without limiting customization
- Function delegation allows for any custom refresh logic
- Examples should cover common real-world scenarios
- Backward compatibility is critical for existing users

## Estimated Effort
3-4 hours

## Next Task
[Phase 1 Component Validation](phase1_component_validation.md)