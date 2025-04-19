---
title: "Docstring drift between testing/integration/helpers.py and helpers.pyi"
severity: medium
location: "apiconfig/testing/integration/helpers.py, apiconfig/testing/integration/helpers.pyi"
---

## Summary
The `apiconfig/testing/integration/helpers.pyi` stub provides detailed docstrings for all helper functions, including argument and return value descriptions. The implementation file `helpers.py` lacks function-level docstrings for all helpers. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/testing/integration/helpers.py
def make_request_with_config(...):
    # No function-level docstring

def setup_multi_provider_manager(...):
    # No function-level docstring

def simulate_token_endpoint(...):
    # No function-level docstring

# apiconfig/testing/integration/helpers.pyi
def make_request_with_config(...):
    """
    Makes an HTTP request using the provided config and auth strategy to a mock server.
    ...
    """

def setup_multi_provider_manager(...):
    """
    Sets up a ConfigManager with multiple MemoryProviders for testing.
    ...
    """

def simulate_token_endpoint(...):
    """
    Configures the mock server to simulate a simple token endpoint.
    ...
    """
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the integration helpers.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add detailed function-level docstrings to `helpers.py` to match the `.pyi` stub, including argument and return value descriptions.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.