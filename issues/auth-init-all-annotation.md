---
title: "Missing type annotation for __all__ in auth/__init__.py"
severity: low
location: "apiconfig/auth/__init__.py, apiconfig/auth/__init__.pyi"
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