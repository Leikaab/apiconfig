# Core Design - HTTP Exception Protocol Enhancement

[← Back to README](README.md)

## Protocol Definitions

We define minimal protocols that match the common interface of HTTP libraries:

```python
# In apiconfig/types.py

from typing import Protocol, Optional, Any, runtime_checkable

@runtime_checkable
class HttpRequestProtocol(Protocol):
    """Protocol matching common HTTP request objects (requests.Request, httpx.Request, etc.)."""
    method: str
    url: str
    headers: Any  # Different libraries use different header types

@runtime_checkable
class HttpResponseProtocol(Protocol):
    """Protocol matching common HTTP response objects (requests.Response, httpx.Response, etc.)."""
    status_code: int
    headers: Any
    text: str  # For body preview
    request: Optional[Any]  # Most responses have .request
    reason: Optional[str]
```

## Mixin Architecture

To avoid code duplication between `ApiClientError` and `AuthenticationError`, we use a shared mixin:

```python
# In apiconfig/exceptions/base.py

class HttpContextMixin:
    """Mixin to add HTTP context extraction capabilities to exceptions."""
    
    def _init_http_context(self, 
                          request: Optional[Union[HttpRequestContext, HttpRequestProtocol]] = None,
                          response: Optional[Union[HttpResponseContext, HttpResponseProtocol]] = None,
                          status_code: Optional[int] = None) -> None:
        """Initialize HTTP context attributes from request/response objects."""
        # Initialize all attributes
        self.status_code = status_code
        self.method: Optional[str] = None
        self.url: Optional[str] = None
        self.reason: Optional[str] = None
        self.request = None  # Original request object
        self.response = None  # Original response object
        
        # Handle response parameter
        if response is not None:
            if isinstance(response, dict):  # TypedDict
                self.status_code = response.get('status_code', status_code)
                self.reason = response.get('reason')
                # Extract request info from TypedDict if present
                if request and isinstance(request, dict):
                    self.method = request.get('method')
                    self.url = request.get('url')
            else:  # Protocol object (requests.Response, httpx.Response, etc.)
                self.response = response
                self._extract_from_response(response)
                
                # Extract request from response if available
                if hasattr(response, 'request') and response.request:
                    self.request = response.request
                    self._extract_from_request(response.request)
        
        # Handle direct request parameter (less common case)
        elif request is not None:
            if isinstance(request, dict):  # TypedDict
                self.method = request.get('method')
                self.url = request.get('url')
            else:  # Protocol object
                self.request = request
                self._extract_from_request(request)
```

## Exception Updates

### ApiClientError (exceptions/http.py)

```python
from .base import APIConfigError, HttpContextMixin

class ApiClientError(APIConfigError, HttpContextMixin):
    """Base exception for errors during HTTP API client operations."""
    
    def __init__(self, message: str, status_code: Optional[int] = None,
                 request: Optional[Union[HttpRequestContext, HttpRequestProtocol]] = None,
                 response: Optional[Union[HttpResponseContext, HttpResponseProtocol]] = None) -> None:
        super().__init__(message)
        self._init_http_context(request=request, response=response, status_code=status_code)
    
    def __str__(self) -> str:
        """Return string representation with HTTP context."""
        base_message = super().__str__()
        
        context_parts = []
        if self.status_code:
            context_parts.append(f"HTTP {self.status_code}")
        
        if self.method and self.url:
            context_parts.append(f"{self.method} {self.url}")
        
        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"
        
        return base_message
```

### AuthenticationError (exceptions/base.py)

```python
class AuthenticationError(APIConfigError, HttpContextMixin):
    """Base exception for authentication-related errors."""
    
    def __init__(self, message: str,
                 request: Optional[Union[HttpRequestContext, HttpRequestProtocol]] = None,
                 response: Optional[Union[HttpResponseContext, HttpResponseProtocol]] = None,
                 *args: Any, **kwargs: Any) -> None:
        super().__init__(message, *args, **kwargs)
        self._init_http_context(request=request, response=response)
    
    def __str__(self) -> str:
        """Return string representation with context if available."""
        base_message = super().__str__()
        
        context_parts = []
        
        if self.method and self.url:
            context_parts.append(f"Request: {self.method} {self.url}")
        
        if self.status_code is not None:
            status_info = f"{self.status_code}"
            if self.reason:
                status_info += f" {self.reason}"
            context_parts.append(f"Response: {status_info}")
        
        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"
        
        return base_message
```

## Design Principles

1. **Minimal Extraction**: Only extract commonly needed attributes (method, url, status_code, reason)
2. **Protocol Flexibility**: Works with any object that has the expected attributes
3. **TypedDict Support**: Maintains support for manual dictionary construction
4. **Original Object Access**: Store original request/response objects for advanced use cases
5. **No Dependencies**: Protocols are pure type hints, no runtime dependencies

## Attribute Storage

Each exception instance will have these attributes:

- `self.request` - Original request object (if provided)
- `self.response` - Original response object (if provided)
- `self.method` - Extracted HTTP method
- `self.url` - Extracted URL
- `self.status_code` - HTTP status code
- `self.reason` - HTTP reason phrase