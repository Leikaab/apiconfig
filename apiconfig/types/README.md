# apiconfig.types

Shared type aliases and protocols for **apiconfig**. They keep the public API
small and make static analysis consistent across modules.

## Navigation
- [Project README](../README.md)

## Contents
- `types.py`

## Usage Examples
```python
from apiconfig.types import JsonObject, HeadersType, HttpMethod

headers: HeadersType = {"Authorization": "Bearer secret"}
method: HttpMethod = HttpMethod.GET
payload: JsonObject = {"ping": "pong"}
```

## Status
Stable – used throughout the library for type checking.
