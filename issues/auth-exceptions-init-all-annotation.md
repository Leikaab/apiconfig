---
title: "Missing type annotation for __all__ in exceptions/auth.py"
severity: low
location: "apiconfig/exceptions/auth.py, apiconfig/exceptions/auth.pyi"
---

## Summary
The `apiconfig/exceptions/auth.pyi` stub provides an explicit type annotation for `__all__` (`list[str]`), but the implementation file `auth.py` does not. This is a minor inconsistency that could lead to confusion or missed type errors in static analysis.

## Evidence
```python
# apiconfig/exceptions/auth.py
__all__ = [
    "AuthenticationError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "AuthStrategyError",
]

# apiconfig/exceptions/auth.pyi
__all__: list[str] = [
    "AuthenticationError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "AuthStrategyError",
]
```

## Impact
- Minor: Static analysis tools may not infer the type of `__all__` in the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit type annotation for `__all__` in `exceptions/auth.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project type annotation guidelines.