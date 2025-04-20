---
issue_number: 68
github_id: I_kwDOObjluc6zNvNs
url: https://github.com/Leikaab/apiconfig/issues/68
state: OPEN
created_at: 2025-04-20T00:25:16Z
updated_at: 2025-04-20T00:25:16Z
author:
  login: Leikaab
  id: MDQ6VXNlcjQ5NzkxNzAx
assignees: []
labels: []
title: "Docstring drift between testing/integration/servers.py and servers.pyi"
---

## Summary
The `apiconfig/testing/integration/servers.pyi` stub provides detailed docstrings for all helper functions, including argument and return value descriptions, and raised exceptions. The implementation file `servers.py` lacks function-level docstrings for all helpers. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/testing/integration/servers.py
def configure_mock_response(...):
    # No function-level docstring

def assert_request_received(...):
    # No function-level docstring

# apiconfig/testing/integration/servers.pyi
def configure_mock_response(...):
    """
    Configures a specific response expectation for the mock HTTPServer.
    ...
    """

def assert_request_received(...):
    """
    Asserts that specific requests were received by the mock server.
    ...
    """
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the integration server helpers.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add detailed function-level docstrings to `servers.py` to match the `.pyi` stub, including argument and return value descriptions, and raised exceptions.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.