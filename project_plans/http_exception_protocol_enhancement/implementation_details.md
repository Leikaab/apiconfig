# Implementation Details - HTTP Exception Protocol Enhancement

[← Back to README](README.md)

## Extraction Methods

Add these methods to the `HttpContextMixin` class:

```python
def _extract_from_request(self, request: Any) -> None:
    """Extract attributes from protocol-compliant request object."""
    if hasattr(request, 'method'):
        self.method = str(request.method)

    if hasattr(request, 'url'):
        self.url = str(request.url)

def _extract_from_response(self, response: Any) -> None:
    """Extract attributes from protocol-compliant response object."""
    if hasattr(response, 'status_code'):
        self.status_code = int(response.status_code)

    if hasattr(response, 'reason'):
        self.reason = str(response.reason) if response.reason else None
```

## Usage Examples

### With requests library

```python
import requests
from apiconfig.exceptions import ApiClientBadRequestError

try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
except requests.HTTPError as e:
    # Just pass the response directly!
    raise ApiClientBadRequestError("API request failed", response=e.response)

    # The exception now has:
    # - exception.response (original requests.Response)
    # - exception.request (original requests.Request via response.request)
    # - exception.status_code (extracted from response)
    # - exception.method (extracted from request)
    # - exception.url (extracted from request)
    # - exception.reason (extracted from response)
```

### With httpx library

```python
import httpx
from apiconfig.exceptions import create_api_client_error

async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/data")
    if response.status_code >= 400:
        # Works seamlessly with httpx too
        raise create_api_client_error(
            response.status_code,
            "Request failed",
            response=response
        )
```

### With TypedDicts (still supported)

```python
# Can still use TypedDicts when needed
raise ApiClientError(
    "Error",
    request={"method": "GET", "url": "..."},
    response={"status_code": 400}
)
```

## Implementation Phases

### Phase 1: Core Protocol Support (3-4 hours)

1. Add Protocol definitions to `types.py`
2. Add `HttpContextMixin` to `exceptions/base.py`
3. Update `ApiClientError` base class in `exceptions/http.py`
4. Update `AuthenticationError` base class in `exceptions/base.py`

### Phase 2: Update Existing Tests (4-5 hours)

1. Update all tests in `test_http_exceptions.py` (~340 lines to review)
2. Update all tests in `test_auth_exceptions.py` (~280 lines to review)
3. Update component tests that use exceptions
4. Run full test suite to ensure no regressions

### Phase 3: New Test Implementation (3-4 hours)

1. Create `test_http_protocol_support.py` for unit tests
2. Create `test_http_protocol_integration.py` for component tests
3. Create separate integration test files for each HTTP library
4. Add requests and httpx as dev dependencies for integration tests

### Phase 4: Documentation & Polish (2-3 hours)

1. Update all exception docstrings
2. Add usage examples to user guide
3. Update API documentation
4. Add type stubs if needed

## Key Implementation Notes

### Parameter Handling

The new exception signatures support both old TypedDict style and new protocol objects:

```python
# TypedDict style (dictionaries)
if isinstance(response, dict):
    self.status_code = response.get('status_code', status_code)
    self.reason = response.get('reason')

# Protocol object style
else:
    self.response = response
    self._extract_from_response(response)
```

### Edge Cases

1. **Response without request**: Some response objects may not have a `.request` attribute
2. **Partial compliance**: Objects may have only some expected attributes
3. **Type conversion**: Always convert extracted values to expected types (str, int)
4. **None handling**: Check for None values before string conversion

### Factory Function Update

The `create_api_client_error` function signature changes:

```python
def create_api_client_error(
    status_code: int,
    message: Optional[str] = None,
    request: Optional[Union[HttpRequestContext, HttpRequestProtocol]] = None,
    response: Optional[Union[HttpResponseContext, HttpResponseProtocol]] = None,
) -> ApiClientError:
    """Create appropriate ApiClientError subclass based on HTTP status code."""
    # Implementation remains similar, just parameter names change
```

## Dependencies

### Runtime Dependencies
- None! Protocols are pure type hints

### Dev Dependencies (for integration tests only)
```toml
[tool.poetry.group.dev.dependencies]
requests = "^2.31.0"
httpx = "^0.25.0"
```

## Type Checking Considerations

1. Use `@runtime_checkable` decorator on protocols for isinstance() checks
2. Import protocols conditionally for older Python versions
3. Ensure mypy understands the Union types
4. Add type: ignore comments sparingly where needed