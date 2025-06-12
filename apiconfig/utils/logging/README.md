# apiconfig.utils.logging

Logging helpers used across **apiconfig**. This package bundles custom
formatters, context filters and convenience functions for setting up redacted
logging output.

## Module Description

`apiconfig.utils.logging` centralises the library's logging utilities. It
collects handlers, formatters and context filters that work together to produce
structured log messages while scrubbing sensitive information.

The module exists so applications using **apiconfig** do not need to reinvent
logging setup for each service. By providing a ready-made configuration function
and building blocks like `RedactingFormatter`, it ensures consistent output and
safe handling of secrets across the ecosystem.

These helpers integrate tightly with the rest of the project. Authentication and
configuration components rely on them for debug output, and the design keeps
each piece modular so consumers can mix and match filters or handlers as needed.

## Navigation

**Parent Module:** [apiconfig.utils](../README.md)

**Submodules:**
- [formatters](./formatters/README.md) - Custom log formatters

## Contents
- `filters.py` – thread-local `ContextFilter` and helper functions for log context.
- `handlers.py` – `ConsoleHandler` and `RedactingStreamHandler` wrappers around `logging.StreamHandler`.
- `formatters/` – specialised formatters like `DetailedFormatter` and `RedactingFormatter`.
- `setup.py` – `setup_logging` function to configure the library's logger.
- `__init__.py` – exports the common classes and helpers.

## Example
```python
import logging
from apiconfig.utils.logging import setup_logging

setup_logging(level="INFO")
logger = logging.getLogger("apiconfig")
logger.info("configured")
```

### Advanced Usage
Use the building blocks directly when you need full control over handlers and
formatters.

```python
import logging
from apiconfig.utils.logging.formatters import RedactingFormatter
from apiconfig.utils.logging.handlers import ConsoleHandler
from apiconfig.utils.logging.filters import ContextFilter, set_log_context

handler = ConsoleHandler()
handler.setFormatter(
    RedactingFormatter("%(asctime)s - %(levelname)s - %(message)s")
)
handler.addFilter(ContextFilter())

logger = logging.getLogger("custom")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

set_log_context("request_id", "42")
logger.info({"token": "secret", "payload": "ok"})
```

## Key classes and functions
| Name | Description |
| ---- | ----------- |
| `ContextFilter` | Injects request or user context into log records via thread-local storage. |
| `DetailedFormatter` | Formats log messages with extra location information. |
| `RedactingFormatter` | Strips sensitive data using the redaction utilities. |
| `setup_logging` | Convenience function to configure handlers and formatters. |

### Design
The components follow a compositional approach: formatters delegate redaction to
`apiconfig.utils.redaction` and `setup_logging` wires up handlers with chosen
formatters. Context injection is optional via the filter.

```mermaid
flowchart TD
    Logger -- filter --> ContextFilter
    Logger --> Handler
    Handler --> Formatter
    Formatter -->|redact| Redaction
```

## Tests
Run the logging-related unit tests:
```bash
python -m pip install -e .
python -m pip install pytest pytest-xdist
pytest tests/unit/utils/logging -q
```

## Status

**Stability:** Stable
**API Version:** Follows Semantic Versioning starting at version 0.x
**Deprecations:** None

### Maintenance Notes
- Logging helpers are maintained alongside the core library. Minor improvements
  and bug fixes are accepted on a best-effort basis.

### Changelog
- See [CHANGELOG.md](../../../CHANGELOG.md) for the release history.

### Future Considerations
- Potential enhancements include new handler types and richer context management.
