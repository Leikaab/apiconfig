---
title: "Docstring drift between types.py and types.pyi"
severity: medium
location: "apiconfig/types.py, apiconfig/types.pyi"
---

## Summary
The `apiconfig/types.pyi` stub provides detailed docstrings for each type alias, but the implementation file `types.py` only has a module-level docstring and lacks per-type documentation. This means runtime users and documentation generators do not see the detailed type information, leading to incomplete or misleading documentation.

## Evidence
```python
# apiconfig/types.py
JsonPrimitive: TypeAlias = Union[str, int, float, bool, None]
# (no docstring)

# apiconfig/types.pyi
JsonPrimitive: TypeAlias = Union[str, int, float, bool, None]
"""Type alias for primitive JSON types."""
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see type details.
- Increases the risk of misunderstanding or misuse of public types.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add concise docstrings to each public type alias in `types.py` to match the `.pyi` stub.
- Ensure future changes to type aliases and their documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.