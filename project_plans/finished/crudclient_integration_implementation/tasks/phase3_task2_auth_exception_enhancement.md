# Phase 3, Task 2: Auth Exception Enhancement

## Overview
Enhance [`apiconfig/exceptions/auth.py`](/workspace/apiconfig/exceptions/auth.py) to include HTTP context information for richer debugging during auth-related failures.

## Objective
Add HTTP request and response context to existing auth exceptions to provide richer debugging information for auth-related failures, especially during token refresh operations.

## Requirements

### 1. Enhance Base AuthenticationError
Modify the base `AuthenticationError` class to optionally accept HTTP context:

```python
from apiconfig.types import HttpRequestContext, HttpResponseContext

class AuthenticationError(APIConfigError):
    """Base exception for authentication-related errors."""

    def __init__(
        self,
        message: str,
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize authentication error with optional HTTP context.

        Parameters
        ----------
        message : str
            Error message describing the authentication failure
        request_context : Optional[HttpRequestContext]
            HTTP request context for debugging (optional)
        response_context : Optional[HttpResponseContext]
            HTTP response context for debugging (optional)
        *args : Any
            Additional positional arguments for base exception
        **kwargs : Any
            Additional keyword arguments for base exception
        """
        super().__init__(message, *args, **kwargs)
        self.request_context = request_context
        self.response_context = response_context

    def __str__(self) -> str:
        """Return string representation with context if available."""
        base_message = super().__str__()

        context_parts = []
        if self.request_context:
            method = self.request_context.get('method', 'UNKNOWN')
            url = self.request_context.get('url', 'UNKNOWN')
            context_parts.append(f"Request: {method} {url}")

        if self.response_context:
            status = self.response_context.get('status_code', 'UNKNOWN')
            reason = self.response_context.get('reason', '')
            status_info = f"{status} {reason}".strip()
            context_parts.append(f"Response: {status_info}")

        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"

        return base_message
```

### 2. Update Existing Auth Exception Classes
Ensure all existing auth exception classes can accept the new context parameters:

```python
class ExpiredTokenError(AuthenticationError):
    """Exception raised when an authentication token has expired."""

    def __init__(
        self,
        message: str = "Authentication token has expired",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, request_context, response_context, *args, **kwargs)

class TokenRefreshError(AuthenticationError):
    """Exception raised when token refresh operations fail."""

    def __init__(
        self,
        message: str = "Failed to refresh authentication token",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, request_context, response_context, *args, **kwargs)

class AuthStrategyError(AuthenticationError):
    """Exception raised when authentication strategy operations fail."""

    def __init__(
        self,
        message: str = "Authentication strategy error",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, request_context, response_context, *args, **kwargs)
```

### 3. Usage Examples
The enhanced exceptions support both simple and context-rich usage:

```python
# Simple usage:
# raise AuthenticationError("Simple message")
# raise ExpiredTokenError()
# raise TokenRefreshError("Custom message")

# Enhanced usage with context:
# raise TokenRefreshError(
#     "Token refresh failed",
#     request_context={"method": "POST", "url": "https://api.example.com/token"},
#     response_context={"status_code": 401, "reason": "Unauthorized"}
# )
```

## Implementation Steps

1. **Read current auth.py** to understand existing exception hierarchy
2. **Add required imports** for new HTTP context types
3. **Enhance AuthenticationError base class** with context parameters
4. **Update all existing exception classes** to support context
5. **Add comprehensive docstrings** following numpy style
6. **Add context-aware string representation** for better debugging

## Files to Modify
- [`apiconfig/exceptions/auth.py`](/workspace/apiconfig/exceptions/auth.py)

## Dependencies
- [Phase 3, Task 1: HTTP Context Type Definitions](phase3_task1_http_context_types.md)

## Quality Gates

### Exception Enhancement
- [ ] HTTP context properly stored and accessible
- [ ] Context parameters are optional and don't break existing usage
- [ ] Enhanced string representation works correctly
- [ ] All exception classes support the new context parameters

### Functionality
- [ ] HTTP context properly stored and accessible
- [ ] String representation includes context when available
- [ ] Context information is useful for debugging
- [ ] Sensitive data redaction considered

### Testing Requirements
- [ ] Unit tests for enhanced exception classes
- [ ] Tests for context-aware string representation
- [ ] Tests for optional context parameters

## Success Criteria
- [ ] All auth exceptions support optional HTTP context
- [ ] Enhanced debugging information available when context provided
- [ ] Comprehensive test coverage for new functionality
- [ ] Clear documentation for new context parameters

## Notes
- Consider security implications when displaying context information
- Ensure context information is helpful for debugging auth issues
- Design should support both apiconfig internal use and crudclient integration

## Estimated Effort
3-4 hours

## Next Task
[Phase 3, Task 3: HTTP API Client Error Hierarchy](phase3_task3_http_api_client_errors.md)