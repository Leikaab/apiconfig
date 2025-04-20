---
github_issue:
  number: 73
  title: "Missing type annotation for __all__ in testing/integration/__init__.py"
  url: "https://github.com/Leikaab/apiconfig/issues/73"
  state: OPEN
  author: "Leikaab"
  created_at: "2025-04-20T00:41:13Z"
  updated_at: "2025-04-20T00:41:13Z"
  closed_at: null
  assignees: []
  labels: []
---
title: "Missing type annotation for __all__ in testing/integration/__init__.py"
severity: low
location: "apiconfig/testing/integration/__init__.py, apiconfig/testing/integration/__init__.pyi"
---

## Summary
The `apiconfig/testing/integration/__init__.pyi` stub provides an explicit type annotation for `__all__` (`list[str]`), but the implementation file `__init__.py` does not. This is a minor inconsistency that could lead to confusion or missed type errors in static analysis.

## Evidence
```python
# apiconfig/testing/integration/__init__.py
__all__ = [
    "configure_mock_response",
    "make_request_with_config",
    "setup_multi_provider_manager",
]

# apiconfig/testing/integration/__init__.pyi
__all__: list[str] = [
    "configure_mock_response",
    "make_request_with_config",
    "setup_multi_provider_manager",
]
```

## Impact
- Minor: Static analysis tools may not infer the type of `__all__` in the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit type annotation for `__all__` in `testing/integration/__init__.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project type annotation guidelines.