# apiconfig.types

## Module Description

Shared type aliases and protocols for **apiconfig** keep the public API small
and make static analysis consistent across modules.

Centralizing these definitions ensures every component relies on the same
contracts when exchanging data. This reduces duplication and helps type
checkers catch integration errors early.

## Navigation
**Parent Module:** [apiconfig](../README.md)

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

### Maintenance Notes
New type aliases are added only when multiple modules need the same
structure. Every addition is documented in the changelog and covered by unit
tests. Deprecated aliases are marked and removed during the next major
release cycle.

### Changelog
- Type alias changes are tracked in the project changelog.

### Future Considerations
- Additional generic types may be introduced as new modules appear.
