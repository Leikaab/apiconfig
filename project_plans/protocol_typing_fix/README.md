# Protocol Typing Fix for External Libraries

## Problem Statement

Users of the apiconfig library report that when using requests library, they need to cast `requests.Request` and `requests.Response` objects to `Any` when passing them to exception classes. This is required even though the code works perfectly at runtime.

Example of the issue:
```python
if issubclass(exception_class, APIError):
    # Cast to Any to handle protocol mismatch - apiconfig will extract what it needs
    raise exception_class(error_message, request=cast(Any, response.request), response=cast(Any, response))
```

The specific pain point is with the `requests` library, though similar issues may affect `httpx` users.

## Root Cause Analysis

1. **Library Independence**: apiconfig uses Protocol types (`HttpRequestProtocol` and `HttpResponseProtocol`) to maintain compatibility with multiple HTTP libraries without depending on them
2. **Type Checker Limitations**: Type checkers (mypy with strict mode) don't recognize that httpx/requests objects satisfy these protocols
3. **No Runtime Dependencies**: httpx and requests are only dev dependencies, so their types aren't available to library users

## Solution Overview

Create a multi-pronged approach that:
- Maintains library independence (no runtime dependencies on httpx/requests)
- Provides optional type support through extras
- Improves protocol definitions for better type inference
- Adds comprehensive typing tests to catch issues early

## Implementation Plan

### Phase 0: Vendored Stubs Proof of Concept (NEW)

Based on investigation, implement minimal vendored stubs approach:

1. **Create minimal stubs**:
   ```
   apiconfig/_typing/
   ├── __init__.py
   └── vendor/
       ├── __init__.py
       └── requests.pyi  # Minimal Request/Response definitions
   ```

   Note: No need for py.typed here - the existing `/workspace/apiconfig/py.typed` already marks the entire package as type-aware

2. **Modify protocols to use TYPE_CHECKING**:
   ```python
   from typing import TYPE_CHECKING, Union

   if TYPE_CHECKING:
       from apiconfig._typing.vendor.requests import Request, Response
       RequestLike = Union[Request, "httpx.Request", HttpRequestProtocol]
       ResponseLike = Union[Response, "httpx.Response", HttpResponseProtocol]
   ```

3. **Test with mypy --strict** to verify no casting needed

### Phase 1: Create Typing Test Infrastructure

Create a new test suite that simulates how external libraries use apiconfig with strict typing:

```
tests/typing/
├── __init__.py
├── conftest.py                    # Shared typing test configuration
├── test_external_httpx.py         # Simulates external lib using httpx
├── test_external_requests.py      # Simulates external lib using requests
├── test_external_generic.py       # Tests with custom implementations
└── run_typing_tests.py            # Script to run mypy with strict mode
```

These tests will:
- Run with `mypy --strict`
- Simulate real-world usage patterns
- Verify no casting is required
- Test both direct instantiation and factory functions

### Phase 2: Analyze and Fix Protocol Definitions

Based on test results, improve the protocol definitions in `apiconfig/types.py`:

1. **Make protocols more flexible**:
   - Ensure `request` attribute in `HttpResponseProtocol` is truly optional
   - Use appropriate variance annotations
   - Consider using `Union` types for known variations

2. **Potential improvements**:
   ```python
   @runtime_checkable
   class HttpRequestProtocol(Protocol):
       """Protocol matching common HTTP request objects."""
       method: Union[str, bytes]  # Some libs use bytes
       url: Union[str, Any]  # URL objects vary
       headers: Any

   @runtime_checkable
   class HttpResponseProtocol(Protocol):
       """Protocol matching common HTTP response objects."""
       status_code: int
       headers: Any
       text: str
       request: Optional[Any] = None  # Make truly optional with default
       reason: Optional[str] = None
   ```

### Phase 3: Add Optional Type Support via Extras

Update `pyproject.toml` to include optional extras:

```toml
[tool.poetry.extras]
requests = ["types-requests"]
httpx = ["httpx"]  # httpx includes its own type stubs
all = ["types-requests", "httpx"]
typing = ["types-requests", "httpx"]  # Convenience alias
```

This allows users to install with proper typing support:
- `pip install apiconfig[httpx]`
- `pip install apiconfig[requests]`
- `pip install apiconfig[typing]`

### Phase 4: Create Type-Safe Helper Functions

If protocol improvements aren't sufficient, add helper functions that provide better type inference:

```python
# apiconfig/exceptions/helpers.py
from typing import TypeVar, Type, overload
from .http import ApiClientError

E = TypeVar('E', bound=ApiClientError)

@overload
def create_exception(
    exc_class: Type[E],
    message: str,
    *,
    response: "httpx.Response"  # type: ignore[name-defined]
) -> E: ...

@overload
def create_exception(
    exc_class: Type[E],
    message: str,
    *,
    response: "requests.Response"  # type: ignore[name-defined]
) -> E: ...

def create_exception(exc_class, message, *, response):
    """Create exception with proper type inference for known HTTP libraries."""
    return exc_class(message, response=response)
```

### Phase 5: Update Documentation

1. **Add typing guide** (`docs/source/typing_guide.rst`):
   - Explain the protocol approach and why it exists
   - Show how to install with type support
   - Provide examples without casting
   - Document any remaining limitations

2. **Update README** with typing section:
   ```markdown
   ## Type Checking Support

   For full type checking support with httpx or requests:
   ```bash
   pip install apiconfig[httpx]   # For httpx users
   pip install apiconfig[requests] # For requests users
   ```
   ```

3. **Update existing docs** to mention typing considerations

### Phase 6: CI/CD Updates

1. **Add typing tests to CI**:
   - Run typing tests in GitHub Actions
   - Test with and without optional dependencies
   - Test multiple Python versions

2. **Update tox.ini** to include typing tests:
   ```ini
   [testenv:typing]
   deps =
       mypy
       httpx
       types-requests
   commands =
       mypy --strict tests/typing/
   ```

## Success Criteria

1. **No casting required**: Users can pass httpx/requests objects directly to exceptions
2. **Maintains independence**: No runtime dependencies on HTTP libraries
3. **Opt-in type support**: Users can choose to install type stubs
4. **Comprehensive testing**: Typing tests catch issues before release
5. **Clear documentation**: Users understand the approach and options

## Timeline

- Phase 1-2: Create tests and analyze issues (1 day)
- Phase 3-4: Implement fixes (1 day)
- Phase 5: Documentation (0.5 days)
- Phase 6: CI/CD updates (0.5 days)

Total: ~3 days

## Risks and Mitigations

1. **Risk**: Type stubs don't fully solve the problem
   - **Mitigation**: Helper functions as fallback, clear documentation

2. **Risk**: Different mypy versions behave differently
   - **Mitigation**: Test with multiple versions, document minimum version

**Note**: Since apiconfig is in alpha, we are not concerned with backwards compatibility. Breaking changes are acceptable to achieve the best solution.

## Alternative Approaches Considered

1. **Vendor type stubs**: Include httpx/requests stubs in package
   - **Status**: RECONSIDERING - This could be the simplest solution
   - **Pros**:
     - Users get typing support out of the box
     - No need for extras or additional installs
     - We control exactly which stubs are used
   - **Cons**:
     - Need to keep stubs updated (but we already test against these libs)
     - Potential conflicts if user has different stub versions
   - **Implementation**: See detailed investigation in `vendored_stubs_investigation.md`
     - Minimal stub approach looks most promising
     - httpx already has inline types (py.typed)
     - requests needs stub vendoring
   - **Recommended approach**: Hybrid solution with TYPE_CHECKING imports

2. **Remove protocols entirely**: Use `Any` types
   - Rejected: Loses type safety benefits

3. **Depend on HTTP libraries**: Add as required dependencies
   - Rejected: Goes against library design philosophy

## Next Steps

1. Review and approve this plan
2. Begin with Phase 1 (typing test infrastructure)
3. Iterate based on test findings
4. Implement the solution incrementally
