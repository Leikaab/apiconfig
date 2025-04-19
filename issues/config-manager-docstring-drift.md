---
title: "Minor docstring drift between config/manager.py and manager.pyi for ConfigManager"
severity: low
location: "apiconfig/config/manager.py, apiconfig/config/manager.pyi"
---

## Summary
The `apiconfig/config/manager.pyi` stub provides a more detailed class-level docstring and method docstrings for `ConfigManager`, especially regarding the orchestration of providers and the merging process. The implementation file `manager.py` has docstrings, but they are less explicit about these details. This leads to minor inconsistencies in documentation.

## Evidence
```python
# apiconfig/config/manager.py
class ConfigManager:
    """Manages loading configuration from multiple providers."""
    # Method docstrings present but less detailed

# apiconfig/config/manager.pyi
class ConfigManager:
    """
    Manages loading configuration from multiple providers.

    This class orchestrates the process of gathering configuration settings
    from various sources (like environment variables, files, or in-memory dictionaries)
    and merging them into a single configuration dictionary.
    """
    # Method docstrings are more detailed
```

## Impact
- Users may not see the full intent or contract of the class at runtime.
- Slightly increases the risk of misunderstanding the merging logic or provider orchestration.

## Suggested Direction
- Update the class-level and method docstrings in `manager.py` to match the detail and structure of the `.pyi` stub.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.