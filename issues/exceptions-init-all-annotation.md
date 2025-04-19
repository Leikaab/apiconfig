---
title: "Missing type annotation for __all__ in exceptions/__init__.py"
severity: low
location: "apiconfig/exceptions/__init__.py, apiconfig/exceptions/__init__.pyi"
---

## Summary
The `apiconfig/exceptions/__init__.pyi` stub provides an explicit type annotation for `__all__` (`list[str]`), but the implementation file `__init__.py` does not. This is a minor inconsistency that could lead to confusion or missed type errors in static analysis.

## Evidence
```python
# apiconfig/exceptions/__init__.py
__all__ = [
    "APIConfigError",
    "ConfigurationError",
    "AuthenticationError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "AuthStrategyError",
    "InvalidConfigError",
    "MissingConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
]

# apiconfig/exceptions/__init__.pyi
__all__: list[str] = [
    "APIConfigError",
    "ConfigurationError",
    "AuthenticationError",
    "InvalidCredentialsError",
    "ExpiredTokenError",
    "MissingCredentialsError",
    "TokenRefreshError",
    "AuthStrategyError",
    "InvalidConfigError",
    "MissingConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
]
```

## Impact
- Minor: Static analysis tools may not infer the type of `__all__` in the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit type annotation for `__all__` in `exceptions/__init__.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project type annotation guidelines.