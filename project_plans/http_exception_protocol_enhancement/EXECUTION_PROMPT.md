# CRITICAL: HTTP Exception Protocol Enhancement Implementation

**THIS IS A BREAKING CHANGE IMPLEMENTATION. NO BACKWARDS COMPATIBILITY IS ALLOWED.**

## MANDATORY READING BEFORE STARTING

You MUST read these files in order before writing ANY code:
1. `/workspace/project_plans/http_exception_protocol_enhancement/README.md` - Overview and requirements
2. `/workspace/project_plans/http_exception_protocol_enhancement/core_design.md` - Protocol definitions and mixin implementation
3. `/workspace/project_plans/http_exception_protocol_enhancement/implementation_details.md` - Usage examples and phases
4. `/workspace/project_plans/http_exception_protocol_enhancement/testing_strategy.md` - Test adaptation requirements

**DO NOT PROCEED WITHOUT READING ALL FOUR FILES.**

## CRITICAL RULES - VIOLATIONS WILL FAIL REVIEW

### 1. NO BACKWARDS COMPATIBILITY
- **REMOVE** all `request_context` and `response_context` parameters
- **REMOVE** all TypedDict context types (HttpRequestContext, HttpResponseContext)
- **DO NOT** accept both old and new parameters
- **DO NOT** add deprecation warnings
- **DO NOT** create compatibility shims
- This is a **CLEAN BREAK** - old API is completely replaced

### 2. NO TEST HACKS
When tests fail after your changes:
- **DO NOT** add `@pytest.mark.xfail` or `@pytest.mark.skip`
- **DO NOT** modify the implementation to make old tests pass
- **DO NOT** add backwards compatibility to "fix" failing tests
- **PROPERLY ADAPT** all tests to use the new API (`request`/`response` parameters)
- Tests WILL fail initially - this is expected and correct

### 3. IMPLEMENTATION ORDER (STRICT)

#### Phase 1: Core Protocol Implementation (4 hours)
1. Add Protocol definitions to `src/apiconfig/types.py`:
   - HttpRequestProtocol
   - HttpResponseProtocol
2. Create HttpContextMixin in `src/apiconfig/exceptions/base.py`
3. Update ApiClientError and AuthenticationError to:
   - Inherit from HttpContextMixin
   - Accept `request` and `response` parameters ONLY
   - Remove ALL references to context parameters

#### Phase 2: Test Migration (8 hours)
1. Update ALL tests in `tests/unit/test_exceptions.py`:
   - Replace `request_context=` with `request=`
   - Replace `response_context=` with `response=`
   - Use mock objects with Protocol-compliant attributes
2. Update ALL tests in `tests/unit/auth/` that use exceptions
3. Update ALL tests in `tests/integration/` that use exceptions
4. **Every test must be adapted - no skips, no xfails**

#### Phase 3: New Protocol Tests (3 hours)
1. Create `tests/unit/test_exception_protocols.py` for Protocol testing
2. Create `tests/integration/test_requests_compatibility.py`
3. Create `tests/integration/test_httpx_compatibility.py`

#### Phase 4: Documentation (1 hour)
1. Update all docstrings to reflect new parameters
2. Update API documentation
3. Update usage examples

## VERIFICATION CHECKLIST

Before marking any phase complete, verify:

- [ ] NO backwards compatibility code exists
- [ ] NO test skips or xfails added
- [ ] ALL tests properly adapted to new API
- [ ] NO references to `request_context` or `response_context` remain
- [ ] NO TypedDict context types remain in exceptions
- [ ] Protocol definitions match specification exactly
- [ ] HttpContextMixin implements ALL extraction methods

## EXAMPLE OF CORRECT CHANGES

### WRONG (Backwards Compatible):
```python
def __init__(self, message, request=None, response=None, 
             request_context=None, response_context=None):  # NO!
    # Backwards compatibility handling - FORBIDDEN
    if request_context:
        self._request_context = request_context
```

### RIGHT (Clean Break):
```python
def __init__(self, message: str, *, 
             request: Optional[HttpRequestProtocol] = None,
             response: Optional[HttpResponseProtocol] = None) -> None:
    super().__init__(message)
    self._request = request
    self._response = response
```

### WRONG (Test Hack):
```python
@pytest.mark.xfail(reason="Needs update for new API")  # NO!
def test_old_api():
    exc = ApiClientError("test", request_context={...})
```

### RIGHT (Proper Adaptation):
```python
def test_exception_with_request():
    mock_request = Mock(spec=['method', 'url', 'headers'])
    mock_request.method = 'GET'
    mock_request.url = 'https://api.example.com'
    mock_request.headers = {'Authorization': 'Bearer token'}
    
    exc = ApiClientError("test", request=mock_request)
    assert exc.method == 'GET'
```

## FINAL WARNINGS

1. **Tests will fail** when you implement Phase 1. This is EXPECTED.
2. **Do not "fix" the implementation** to make tests pass. Fix the TESTS.
3. **Every occurrence** of `request_context` and `response_context` must be removed.
4. **No gradual migration** - this is an immediate, complete replacement.
5. If you find yourself adding ANY backwards compatibility, STOP and re-read this prompt.

Remember: The goal is a CLEAN, BREAKING CHANGE that improves the API. Users will need to update their code - this is intentional and desired.