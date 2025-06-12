# apiconfig.utils

## Module Description

The utilities package houses small, focused helpers that other
**apiconfig** modules depend on. It includes HTTP status helpers,
URL construction functions, logging configuration and tools for
redacting sensitive information.

These utilities simplify writing API clients by handling common tasks
like normalising URLs or removing secrets from logs. Each subpackage
is lightweight and can be used independently of the rest of
**apiconfig**.

## Navigation

**Parent Module:** [apiconfig](../README.md)

**Submodules:**
- [logging](./logging/README.md) - configure redacted log output
- [redaction](./redaction/README.md) - scrub secrets from requests and logs
- [url](./url.py) - build and normalise URLs safely

## Contents
- `http.py` – simple helpers for working with HTTP status codes and JSON payloads.
- `url.py` – safe wrappers around `urllib.parse` for building URLs.
- `redaction/` – functions for scrubbing secrets from bodies and headers.
- `logging/` – custom formatters and setup helpers for the library's logging.
- `__init__.py` – exposes the modules above for convenience.

## Example
```python
from apiconfig.utils import http, url

if http.is_success(200):
    full_url = url.build_url("https://api.example.com", "/ping")
    print(full_url)
```

## Key modules
| Module | Purpose |
| ------ | ------- |
| `http` | HTTP status helpers and safe JSON encode/decode with custom exceptions. |
| `url` | Build URLs and normalise query parameters with type safety. |
| `redaction` | Remove sensitive data before logging or output. |
| `logging` | Formatters, handlers and setup utilities for clean log output. |

### Design
Utility modules are kept lightweight and independent. Logging utilities compose
the redaction helpers to avoid code duplication.

```mermaid
flowchart TD
    Redaction --> Logging
    URL --> HTTP
```

## Dependencies

### External Dependencies
- `typing` – runtime type hints and conditional imports
- `urllib.parse` – safe URL parsing and construction
- `logging` – configure loggers and handlers

### Internal Dependencies
- `apiconfig.utils.redaction` – shared helpers for scrubbing secrets
- `apiconfig.types` – common type aliases used in URL helpers

### Optional Dependencies
- `httpx` – used in certain helpers for async HTTP utilities

## Tests
Run the unit tests for utility modules:
```bash
python -m pip install -e .
python -m pip install pytest pytest-xdist
pytest tests/unit/utils -q
```

## Status
Stable – used throughout the project.
