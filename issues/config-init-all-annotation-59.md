---
issue_number: 59
github_issue_id: I_kwDOObjluc6zNtbK
github_issue_url: https://github.com/Leikaab/apiconfig/issues/59
title: "Missing type annotation for __all__ in config/__init__.py"
state: OPEN
created_at: "2025-04-20T00:09:11Z"
updated_at: "2025-04-20T00:09:11Z"
author:
  login: Leikaab
  id: MDQ6VXNlcjQ5NzkxNzAx
  is_bot: false
assignees: []
labels: []
---

## Summary
The `apiconfig/config/__init__.pyi` stub provides an explicit type annotation for `__all__` (`List[str]`), but the implementation file `__init__.py` does not. This is a minor inconsistency that could lead to confusion or missed type errors in static analysis.

## Evidence
```python
# apiconfig/config/__init__.py
__all__ = [
    "ClientConfig",
    "ConfigManager",
    "EnvProvider",
    "FileProvider",
    "MemoryProvider",
]

# apiconfig/config/__init__.pyi
__all__: List[str] = [
    "ClientConfig",
    "ConfigManager",
    "EnvProvider",
    "FileProvider",
    "MemoryProvider",
]
```

## Impact
- Minor: Static analysis tools may not infer the type of `__all__` in the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit type annotation for `__all__` in `config/__init__.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project type annotation guidelines.