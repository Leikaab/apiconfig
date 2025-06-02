# Phase 3, Task 3: HTTP API Client Error Hierarchy

## Overview
Implement a new `ApiClientError` hierarchy in [`apiconfig/exceptions/http.py`](/workspace/apiconfig/exceptions/http.py) to provide specific HTTP status code exceptions for API client operations, including the multiple inheritance pattern specified in the original plan.

## Objective
Create a foundational HTTP API client error hierarchy that provides specific details about HTTP failures and includes request/response context, serving as the primary mechanism for handling HTTP status code errors for both `apiconfig`-initiated calls and general API calls made by `crudclient`.

## Requirements

### 1. Base ApiClientError Class
Create a base exception class for HTTP API client errors:

```python
from .base import APIConfigError
from apiconfig.types import HttpRequestContext, HttpResponseContext
from apiconfig.exceptions.auth import AuthenticationError

class ApiClientError(APIConfigError):
    """
    Base exception for errors during HTTP API client operations.

    This exception provides a foundation for handling HTTP-related errors
    with rich context information for debugging and error handling.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        """
        Initialize API client error with HTTP context.

        Parameters
        ----------
        message : str
            Error message describing the API client failure
        status_code : Optional[int]
            HTTP status code associated with the error
        request_context : Optional[HttpRequestContext]
            HTTP request context for debugging
        response_context : Optional[HttpResponseContext]
            HTTP response context for debugging
        """
        super().__init__(message)
        self.status_code = status_code
        self.request_context = request_context
        self.response_context = response_context

    def __str__(self) -> str:
        """Return string representation with HTTP context."""
        base_message = super().__str__()

        context_parts = []
        if self.status_code:
            context_parts.append(f"HTTP {self.status_code}")

        if self.request_context:
            method = self.request_context.get('method', 'UNKNOWN')
            url = self.request_context.get('url', 'UNKNOWN')
            context_parts.append(f"{method} {url}")

        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"

        return base_message
```

### 2. Specific HTTP Status Code Exceptions
Create specific exceptions for common HTTP status codes:

```python
class ApiClientBadRequestError(ApiClientError):
    """HTTP 400 Bad Request from an API client operation."""

    def __init__(
        self,
        message: str = "Bad Request",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=400, request_context=request_context, response_context=response_context)

class ApiClientUnauthorizedError(ApiClientError, AuthenticationError):
    """
    HTTP 401 Unauthorized from an API client operation.
    Indicates an authentication failure during an HTTP call.
    """

    def __init__(
        self,
        message: str = "Unauthorized",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        ApiClientError.__init__(self, message, status_code=401, request_context=request_context, response_context=response_context)
        # Ensure AuthenticationError's __init__ can handle being called this way
        # or is adjusted to accept the shared context.
        AuthenticationError.__init__(self, message,
                                     request_context=request_context,
                                     response_context=response_context)

class ApiClientForbiddenError(ApiClientError):
    """HTTP 403 Forbidden from an API client operation."""

    def __init__(
        self,
        message: str = "Forbidden",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=403, request_context=request_context, response_context=response_context)

class ApiClientNotFoundError(ApiClientError):
    """HTTP 404 Not Found from an API client operation."""

    def __init__(
        self,
        message: str = "Not Found",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=404, request_context=request_context, response_context=response_context)

class ApiClientConflictError(ApiClientError):
    """HTTP 409 Conflict from an API client operation."""

    def __init__(
        self,
        message: str = "Conflict",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=409, request_context=request_context, response_context=response_context)

class ApiClientUnprocessableEntityError(ApiClientError):
    """HTTP 422 Unprocessable Entity from an API client operation."""

    def __init__(
        self,
        message: str = "Unprocessable Entity",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=422, request_context=request_context, response_context=response_context)

class ApiClientRateLimitError(ApiClientError):
    """HTTP 429 Too Many Requests from an API client operation."""

    def __init__(
        self,
        message: str = "Rate Limit Exceeded",
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=429, request_context=request_context, response_context=response_context)

class ApiClientInternalServerError(ApiClientError):
    """HTTP 5xx Server Error from an API client operation."""

    def __init__(
        self,
        message: str = "Internal Server Error",
        status_code: int = 500,
        request_context: Optional[HttpRequestContext] = None,
        response_context: Optional[HttpResponseContext] = None,
    ):
        super().__init__(message, status_code=status_code, request_context=request_context, response_context=response_context)
```

### 3. Status Code Mapping Utility
Add a utility function to map status codes to appropriate exceptions:

```python
def create_api_client_error(
    status_code: int,
    message: Optional[str] = None,
    request_context: Optional[HttpRequestContext] = None,
    response_context: Optional[HttpResponseContext] = None,
) -> ApiClientError:
    """
    Create appropriate ApiClientError subclass based on HTTP status code.

    Parameters
    ----------
    status_code : int
        HTTP status code
    message : Optional[str]
        Custom error message (uses default if not provided)
    request_context : Optional[HttpRequestContext]
        HTTP request context
    response_context : Optional[HttpResponseContext]
        HTTP response context

    Returns
    -------
    ApiClientError
        Appropriate exception subclass for the status code
    """
    error_classes = {
        400: ApiClientBadRequestError,
        401: ApiClientUnauthorizedError,
        403: ApiClientForbiddenError,
        404: ApiClientNotFoundError,
        409: ApiClientConflictError,
        422: ApiClientUnprocessableEntityError,
        429: ApiClientRateLimitError,
    }

    if status_code in error_classes:
        error_class = error_classes[status_code]
        if message:
            return error_class(message, request_context=request_context, response_context=response_context)
        else:
            return error_class(request_context=request_context, response_context=response_context)
    elif 500 <= status_code < 600:
        return ApiClientInternalServerError(
            message or f"Server Error (HTTP {status_code})",
            status_code=status_code,
            request_context=request_context,
            response_context=response_context
        )
    else:
        return ApiClientError(
            message or f"HTTP Error {status_code}",
            status_code=status_code,
            request_context=request_context,
            response_context=response_context
        )
```

## Implementation Steps

1. **Read current http.py** to understand existing structure
2. **Add required imports** for HTTP context types and base exceptions
3. **Implement base ApiClientError class** with HTTP context support
4. **Create specific status code exception classes** for common HTTP errors
5. **Add status code mapping utility** for easy exception creation
6. **Add comprehensive docstrings** following numpy style
7. **Update module exports** to include new exceptions

## Files to Modify
- [`apiconfig/exceptions/http.py`](/workspace/apiconfig/exceptions/http.py)

## Dependencies
- [Phase 3, Task 1: HTTP Context Type Definitions](phase3_task1_http_context_types.md)
- [Phase 3, Task 2: Auth Exception Enhancement](phase3_task2_auth_exception_enhancement.md)

## Quality Gates

### Exception Hierarchy
- [ ] Multiple inheritance pattern implemented for ApiClientUnauthorizedError as specified
- [ ] Consistent constructor patterns across all exception classes
- [ ] Proper status code mapping for all common HTTP errors
- [ ] Integration between HTTP errors and auth-specific errors where appropriate

### Functionality
- [ ] HTTP context properly stored and accessible
- [ ] Status code mapping utility works correctly
- [ ] String representation includes useful debugging information
- [ ] Default messages are appropriate for each status code

### Testing Requirements
- [ ] Unit tests for all exception classes
- [ ] Tests for status code mapping utility
- [ ] Tests for HTTP context integration
- [ ] Tests for string representation formatting

## Success Criteria
- [ ] Complete HTTP API client error hierarchy implemented
- [ ] Status code mapping utility provides easy exception creation
- [ ] Rich HTTP context available for debugging
- [ ] Clean, maintainable exception hierarchy with appropriate multiple inheritance
- [ ] Comprehensive test coverage for all exception classes

## Notes
- Implements multiple inheritance pattern as specified in original plan for ApiClientUnauthorizedError
- Links HTTP client errors with authentication errors where appropriate (401 status)
- Focus on providing useful debugging information through context
- Design for easy integration with crudclient error handling patterns

## Estimated Effort
5-6 hours

## Next Task
[Phase 3, Task 4: Integration Test Enhancement](phase3_task4_integration_test_enhancement.md)