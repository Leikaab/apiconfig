---
issue_number: 52
issue_url: "https://github.com/Leikaab/apiconfig/issues/52"
issue_id: "I_kwDOObjluc6zNs1Q"
title: "Missing type annotation for __all__ in auth/__init__.py"
state: OPEN
author:
  login: "Leikaab"
  id: "MDQ6VXNlcjQ5NzkxNzAx"
created_at: "2025-04-20T00:02:26Z"
updated_at: "2025-04-20T00:02:26Z"
labels: []
---

## Summary
The `apiconfig/auth/__init__.pyi` stub provides an explicit type annotation for `__all__` (`List[str]`), but the implementation file `__init__.py` does not. This is a minor inconsistency that could lead to confusion or missed type errors in static analysis.

## Evidence
```python
# apiconfig/auth/__init__.py
__all__ = [
    "AuthStrategy",
    "BasicAuth",
    "BearerAuth",
    "ApiKeyAuth",
    "CustomAuth",
]

# apiconfig/auth/__init__.pyi
__all__: List[str] = [
    "AuthStrategy",
    "BasicAuth",
    "BearerAuth",
    "ApiKeyAuth",
    "CustomAuth",
]
```

## Impact
- Minor: Static analysis tools may not infer the type of `__all__` in the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit type annotation for `__all__` in `auth/__init__.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project type annotation guidelines.