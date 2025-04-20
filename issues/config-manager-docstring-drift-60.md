---
issue_number: 60
title: "Minor docstring drift between config/manager.py and manager.pyi for ConfigManager"
url: "https://github.com/Leikaab/apiconfig/issues/60"
state: OPEN
created_at: "2025-04-20T00:10:04Z"
updated_at: "2025-04-20T00:10:04Z"
author:
  login: "Leikaab"
  id: "MDQ6VXNlcjQ5NzkxNzAx"
  is_bot: false
labels:
  - name: "documentation"
    id: "LA_kwDOObjluc8AAAAB-S4H2w"
    description: "Improvements or additions to documentation"
    color: "0075ca"
assignees: []
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