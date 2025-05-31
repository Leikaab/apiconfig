# Testing Strategy - HTTP Exception Protocol Enhancement

[← Back to README](README.md)

## Test Categories

### 1. Unit Tests - Core Functionality

**File**: `tests/unit/exceptions/test_http_protocol_support.py`

```python
import pytest
from typing import Any

from apiconfig.exceptions.http import ApiClientError, ApiClientBadRequestError
from apiconfig.exceptions.auth import AuthenticationError, TokenRefreshError

class MockResponse:
    """Mock that satisfies HttpResponseProtocol."""
    def __init__(self, status_code: int = 200, reason: str = None):
        self.status_code = status_code
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"error": "Bad request"}'
        self.reason = reason or f"HTTP {status_code}"
        self.request = MockRequest()

class MockRequest:
    """Mock that satisfies HttpRequestProtocol."""
    def __init__(self, method: str = "GET", url: str = "https://api.example.com/data"):
        self.method = method
        self.url = url
        self.headers = {"Authorization": "Bearer token"}

def test_exception_with_response_protocol():
    """Test creating exception with protocol-compliant response."""
    response = MockResponse(400, "Bad Request")
    exc = ApiClientBadRequestError("Failed", response=response)
    
    assert exc.response is response
    assert exc.request is response.request
    assert exc.status_code == 400
    assert exc.method == 'GET'
    assert exc.url == 'https://api.example.com/data'
    assert exc.reason == 'Bad Request'

def test_exception_with_request_only():
    """Test creating exception with only request object."""
    request = MockRequest("POST", "https://api.example.com/users")
    exc = ApiClientError("Request failed", request=request)
    
    assert exc.request is request
    assert exc.response is None
    assert exc.method == 'POST'
    assert exc.url == 'https://api.example.com/users'

def test_exception_with_typeddict():
    """Ensure TypedDict still works."""
    exc = ApiClientError(
        "Failed",
        request={"method": "PUT", "url": "/api/resource"},
        response={"status_code": 409, "reason": "Conflict"}
    )
    
    assert exc.request is None  # No protocol object stored
    assert exc.response is None
    assert exc.method == "PUT"
    assert exc.url == "/api/resource"
    assert exc.status_code == 409
    assert exc.reason == "Conflict"

def test_auth_exception_with_response():
    """Test authentication exception with response object."""
    response = MockResponse(401, "Unauthorized")
    exc = AuthenticationError("Auth failed", response=response)
    
    assert exc.response is response
    assert exc.status_code == 401
    assert exc.method == 'GET'
    assert str(exc) == "Auth failed (Request: GET https://api.example.com/data, Response: 401 Unauthorized)"
```

### 2. Component Tests - Complex Scenarios

**File**: `tests/component/test_http_protocol_integration.py`

```python
import pytest
from unittest.mock import Mock

from apiconfig.exceptions import create_api_client_error
from apiconfig.exceptions.auth import TokenRefreshError

def test_create_api_client_error_with_protocol():
    """Test factory function with protocol objects."""
    response = MockResponse(422, "Unprocessable Entity")
    error = create_api_client_error(422, "Validation failed", response=response)
    
    assert error.__class__.__name__ == "ApiClientUnprocessableEntityError"
    assert error.response is response
    assert error.status_code == 422

def test_exception_without_request_attribute():
    """Test response object without .request attribute."""
    response = Mock(status_code=500, reason="Server Error")
    # Don't set response.request
    
    exc = ApiClientError("Server error", response=response)
    assert exc.response is response
    assert exc.request is None
    assert exc.status_code == 500

def test_partial_protocol_compliance():
    """Test objects with only some expected attributes."""
    response = Mock(status_code=404)
    # No reason attribute
    
    exc = ApiClientError("Not found", response=response)
    assert exc.status_code == 404
    assert exc.reason is None

def test_inheritance_chain():
    """Test all subclasses inherit the new functionality."""
    response = MockResponse(404)
    
    # Test different subclasses
    not_found = ApiClientNotFoundError("Not found", response=response)
    assert not_found.status_code == 404
    assert not_found.method == 'GET'
    
    unauthorized = ApiClientUnauthorizedError("Unauthorized", response=response)
    assert unauthorized.status_code == 404  # From response, not hardcoded 401
    assert unauthorized.url == 'https://api.example.com/data'
```

### 3. Integration Tests - Real HTTP Libraries

Each HTTP library gets its own integration test file for proper separation of concerns:

#### Requests Library Tests

**File**: `tests/integration/test_requests_compatibility.py`

```python
import pytest

# Only run if requests is available
requests = pytest.importorskip("requests")

from apiconfig.exceptions import ApiClientError, ApiClientBadRequestError

def test_with_real_requests_response():
    """Test with actual requests.Response object."""
    # Create a mock requests response
    response = requests.Response()
    response.status_code = 400
    response.reason = "Bad Request"
    response.url = "https://api.example.com/test"
    response.request = requests.Request(method="POST", url=response.url).prepare()
    
    exc = ApiClientBadRequestError("Request failed", response=response)
    
    assert exc.response is response
    assert exc.request is response.request
    assert exc.status_code == 400
    assert exc.method == "POST"
    assert exc.url == "https://api.example.com/test"

def test_requests_error_chaining():
    """Test exception chaining from requests.HTTPError."""
    response = requests.Response()
    response.status_code = 404
    response.reason = "Not Found"
    
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        exc = ApiClientError("Resource not found", response=e.response)
        assert exc.status_code == 404
        assert exc.__cause__ is None  # We don't chain by default
```

#### HTTPX Library Tests

**File**: `tests/integration/test_httpx_compatibility.py`

```python
import pytest

# Only run if httpx is available
httpx = pytest.importorskip("httpx")

from apiconfig.exceptions import ApiClientError, create_api_client_error

@pytest.mark.asyncio
async def test_with_real_httpx_response():
    """Test with actual httpx.Response object."""
    # Create a mock httpx response
    request = httpx.Request("GET", "https://api.example.com/data")
    response = httpx.Response(
        status_code=404,
        headers={"content-type": "application/json"},
        request=request,
    )
    
    exc = ApiClientError("Not found", response=response)
    
    assert exc.response is response
    assert exc.request is request
    assert exc.status_code == 404
    assert exc.method == "GET"

def test_httpx_sync_client():
    """Test with httpx sync client response."""
    request = httpx.Request("DELETE", "https://api.example.com/resource/123")
    response = httpx.Response(
        status_code=403,
        request=request,
    )
    
    exc = create_api_client_error(403, "Forbidden", response=response)
    
    assert exc.__class__.__name__ == "ApiClientForbiddenError"
    assert exc.method == "DELETE"
```

**Note**: Each library's tests are in separate files to maintain clean separation and allow for library-specific test configurations.

## Test Migration Strategy

### Systematic Updates Required

1. **Parameter Renaming**:
   - Replace all `request_context=` with `request=`
   - Replace all `response_context=` with `response=`

2. **Assertion Updates**:
   - Remove assertions for `error.request_context` and `error.response_context`
   - Add assertions for individual attributes: `error.method`, `error.url`, etc.

3. **Example Migration**:

**Before:**
```python
def test_initialization_with_request_context(self) -> None:
    request_context: HttpRequestContext = {"method": "GET", "url": "https://api.example.com/users"}
    error = ApiClientError("Test error", request_context=request_context)
    assert str(error) == "Test error (GET https://api.example.com/users)"
    assert error.request_context == request_context
```

**After:**
```python
def test_initialization_with_request_context(self) -> None:
    request: HttpRequestContext = {"method": "GET", "url": "https://api.example.com/users"}
    error = ApiClientError("Test error", request=request)
    assert str(error) == "Test error (GET https://api.example.com/users)"
    assert error.method == "GET"
    assert error.url == "https://api.example.com/users"
```

## Test Coverage Goals

1. **Protocol Compliance**: Test with objects that satisfy the protocol
2. **TypedDict Support**: Ensure dictionaries still work
3. **Partial Compliance**: Test objects missing some attributes
4. **Edge Cases**: None values, missing attributes, type conversions
5. **Real Libraries**: Integration tests with requests and httpx
6. **Inheritance**: Verify all subclasses inherit functionality
7. **Factory Functions**: Test `create_api_client_error` with new params

## CI/CD Considerations

1. **Optional Dependencies**: Integration tests should skip if libraries not installed
2. **Test Isolation**: Each HTTP library gets its own test file
3. **Performance**: Mock-based tests should be fast
4. **Type Checking**: Ensure mypy passes on all test files