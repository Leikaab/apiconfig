# Phase 3, Task 1: HTTP Context Type Definitions

## Overview
Add HTTP context type definitions to [`apiconfig/types.py`](/workspace/apiconfig/types.py) to support enriched exception handling and provide library-agnostic request/response information structures.

## Objective
Establish type definitions for HTTP request and response context that can be used to enrich exceptions with meaningful debugging information without coupling to specific HTTP libraries.

## Requirements

### 1. HttpRequestContext TypedDict
Add a TypedDict to represent essential HTTP request information:

```python
class HttpRequestContext(TypedDict, total=False):
    """
    Library-agnostic HTTP request context for exception enrichment.

    This structure holds essential request information that can be used
    to provide meaningful context in exceptions without coupling to
    specific HTTP client libraries.
    """
    method: str                                    # HTTP method (GET, POST, etc.)
    url: str                                      # Request URL
    headers: Optional[Mapping[str, str]]          # Request headers (redacted if needed)
    body_preview: Optional[str]                   # Safe preview of request body (redacted)
```

### 2. HttpResponseContext TypedDict
Add a TypedDict to represent essential HTTP response information:

```python
class HttpResponseContext(TypedDict, total=False):
    """
    Library-agnostic HTTP response context for exception enrichment.

    This structure holds essential response information that can be used
    to provide meaningful context in exceptions without coupling to
    specific HTTP client libraries.
    """
    status_code: int                              # HTTP status code
    headers: Optional[Mapping[str, str]]          # Response headers (redacted if needed)
    body_preview: Optional[str]                   # Safe preview of response body (redacted)
    reason: Optional[str]                         # HTTP reason phrase (e.g., "Not Found")
```

### 3. ResponseBodyType Type Alias
Add a type alias for raw API response bodies that apiconfig components might process:

```python
# Type alias for API response body types
ResponseBodyType: TypeAlias = Union[JsonObject, JsonList, bytes, str, None]
```

## Implementation Steps

1. **Read current types.py** to understand existing structure and imports
2. **Add required imports** if not already present:
   - `TypedDict` from `typing` (should already be added from Phase 1, Task 1)
   - `Mapping` from `typing` (already present)
   - `Union` from `typing` (already present)
3. **Add the new type definitions** in logical order after existing HTTP types
4. **Update module exports** in `__all__` list
5. **Add comprehensive docstrings** following numpy style

## Files to Modify
- [`apiconfig/types.py`](/workspace/apiconfig/types.py)

## Dependencies
- [Phase 1, Task 1: Type Definitions Enhancement](phase1_task1_type_definitions.md) (for TypedDict import)
- [Phase 2 completion](../orchestrator_plan.md#phase-2-testing-enhancement-medium-priority)

## Quality Gates

### Type Validation
- [ ] All new types pass mypy validation
- [ ] Types are properly exported and importable
- [ ] No circular import issues introduced
- [ ] Consistent with existing type naming conventions

### Documentation
- [ ] All new types have comprehensive docstrings
- [ ] Docstrings follow numpy style format
- [ ] Usage examples provided where helpful
- [ ] Clear explanation of library-agnostic design

### Integration
- [ ] Types integrate well with existing HTTP types
- [ ] Compatible with planned exception enhancements
- [ ] Suitable for use in auth refresh scenarios

## Success Criteria
- [ ] `HttpRequestContext` and `HttpResponseContext` TypedDicts are defined and usable
- [ ] `ResponseBodyType` type alias is available for API response handling
- [ ] All types pass mypy validation without errors
- [ ] Types are properly documented and follow project conventions
- [ ] No breaking changes to existing type definitions
- [ ] Types are library-agnostic and suitable for exception enrichment

## Notes
- These types will be used in Phase 3, Task 2 for auth exception enhancement
- Design should be library-agnostic to avoid coupling to specific HTTP clients
- Consider security implications - ensure sensitive data can be redacted
- Types should be suitable for both apiconfig internal use and crudclient integration

## Estimated Effort
2-3 hours

## Next Task
[Phase 3, Task 2: Auth Exception Enhancement](phase3_task2_auth_exception_enhancement.md)