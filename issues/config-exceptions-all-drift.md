---
title: "Missing __all__ in exceptions/config.py"
severity: low
location: "apiconfig/exceptions/config.py, apiconfig/exceptions/config.pyi"
---

## Summary
The `apiconfig/exceptions/config.pyi` stub defines `__all__`, but the implementation file `config.py` does not. This is a minor inconsistency that could lead to confusion or missed static analysis of the public API.

## Evidence
```python
# apiconfig/exceptions/config.py
# No __all__ defined

# apiconfig/exceptions/config.pyi
__all__ = [
    "InvalidConfigError",
    "MissingConfigError",
    "ConfigLoadError",
    "ConfigProviderError",
]
```

## Impact
- Minor: Static analysis tools may not infer the public API surface from the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit `__all__` definition to `exceptions/config.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project public API and type annotation guidelines.