---
issue_number: 70
title: "Stub and implementation drift in __init__.py: __all__ and type annotations"
state: OPEN
url: https://github.com/Leikaab/apiconfig/issues/70
created_at: 2025-04-20T00:29:09Z
updated_at: 2025-04-20T00:29:09Z
author:
  login: Leikaab
  id: MDQ6VXNlcjQ5NzkxNzAx
  is_bot: false
assignees: []
labels: []
---

## Summary
The public API definition in `__init__.py` and its stub (`__init__.pyi`) are not perfectly synchronized. The order of items in `__all__` differs, and the stub includes type annotations for `__version__` and `__all__` that are missing in the implementation. This can lead to confusion for users relying on static analysis, IDEs, or type checkers, and increases the risk of future drift.

## Evidence
```python
# apiconfig/__init__.py
__all__ = [
    "ClientConfig", "ConfigManager", ... # (order and content)
]

# apiconfig/__init__.pyi
__all__: List[str] = [
    "ClientConfig", "ConfigManager", ... # (order and content may differ)
]
__version__: str
```

## Impact
- Static analysis tools and IDEs may show inconsistent or incomplete API surfaces.
- Type checkers may infer different types or miss exports.
- Future changes may cause further drift, making maintenance harder.

## Suggested Direction
- Ensure the order and content of `__all__` are identical in both files.
- Add explicit type annotations for `__version__` and `__all__` in the implementation.
- Consider a single source of truth for `__all__` to avoid duplication.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- General stub maintenance guidelines.