# Vendored Type Stubs Investigation

## Overview

This document investigates the feasibility of vendoring type stubs for requests and httpx to solve the protocol typing issues without requiring users to install extras.

## Current State

### Requests
- **Type Package**: `types-requests` (separate package)
- **Version**: 2.32.0.20250328
- **Structure**: Collection of `.pyi` stub files
- **Key Files**:
  - `models.pyi` - Contains `Request`, `PreparedRequest`, and `Response` classes
  - `__init__.pyi` - Main exports

### httpx
- **Type Support**: Built-in (py.typed marker present)
- **No separate stubs needed** - httpx includes inline type annotations

## Key Type Definitions

### Requests Types (from stubs)
```python
class Request:
    method: str | None
    url: str | None
    headers: dict
    # ... other attributes

class Response:
    status_code: int
    headers: CaseInsensitiveDict[str]
    request: PreparedRequest
    reason: str
    text: str  # property
    # ... other attributes
```

### Our Protocols
```python
@runtime_checkable
class HttpRequestProtocol(Protocol):
    method: str
    url: str
    headers: Any

@runtime_checkable
class HttpResponseProtocol(Protocol):
    status_code: int
    headers: Any
    text: str
    request: Optional[Any]
    reason: Optional[str]
```

## Vendoring Options

### Option 1: Minimal Stub Vendoring
Create minimal stub files that only define the types we need:

```python
# apiconfig/_vendor/requests_stubs.pyi
from typing import Any, Optional

class PreparedRequest:
    method: str
    url: str
    headers: Any

class Response:
    status_code: int
    headers: Any
    text: str
    request: PreparedRequest
    reason: Optional[str]
```

**Pros:**
- Very lightweight
- No maintenance of unused types
- Clear what we support

**Cons:**
- Incomplete types might confuse users
- Need to maintain compatibility

### Option 2: Full Stub Vendoring
Copy entire `types-requests` package into our codebase:

```
apiconfig/_vendor/
├── requests/
│   ├── __init__.pyi
│   ├── models.pyi
│   └── ... (all stub files)
└── __init__.py
```

**Pros:**
- Complete type coverage
- Users get full requests typing

**Cons:**
- Large footprint (~17 files)
- Maintenance burden
- Version sync issues

### Option 3: Type Aliases with Conditional Imports
Use conditional imports to provide types when available:

```python
# apiconfig/types.py
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    try:
        from requests import Request as RequestsRequest, Response as RequestsResponse
        from httpx import Request as HttpxRequest, Response as HttpxResponse

        RequestType = Union[RequestsRequest, HttpxRequest, Any]
        ResponseType = Union[RequestsResponse, HttpxResponse, Any]
    except ImportError:
        RequestType = Any
        ResponseType = Any
else:
    RequestType = Any
    ResponseType = Any
```

**Pros:**
- No vendoring needed
- Works with user's installed versions
- Zero runtime overhead

**Cons:**
- Still requires users to have types installed
- Complex type unions

## Implementation Challenges

### 1. PEP 561 Compliance
- Need to ensure vendored stubs are discoverable by type checkers
- May need to add `py.typed` marker and configure package properly

### 2. Import Path Conflicts
- Vendored stubs might conflict with user-installed type packages
- Need careful import management

### 3. Version Compatibility
- Requests/httpx APIs change over time
- Our stubs might not match user's actual library version

## Proof of Concept

Let's test if vendoring would actually solve the issue:

```python
# test_vendored_typing.py
from typing import cast
from apiconfig.exceptions import ApiClientError
import requests

def test_without_cast():
    """This currently fails mypy --strict"""
    response = requests.get('https://example.com')
    # This line requires cast(Any, ...) currently
    error = ApiClientError("Error", request=response.request, response=response)
```

With vendored stubs, we'd modify our protocols to recognize the vendored types.

## Recommendation

**Best Approach: Hybrid Solution**

1. **Use TYPE_CHECKING imports** for zero-runtime cost
2. **Create minimal type definitions** that match our protocols exactly
3. **Provide clear documentation** on installing full type support
4. **Test extensively** with mypy --strict

This gives us:
- No runtime dependencies
- Basic typing that works out of the box
- Option for users to get full typing with extras

## Next Steps

1. Create a proof-of-concept with minimal vendored types
2. Test with mypy --strict to ensure it solves the casting issue
3. Evaluate the maintenance burden
4. Make final decision based on results
