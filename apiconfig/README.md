# apiconfig

Simplifies configuration and authentication for Python API clients.

## Module Description
**apiconfig** centralises configuration and authentication logic for Python API
clients. The library provides a small, stable surface area that applications can
depend on while hiding complex implementation details behind well defined
interfaces.

The project exists so that the many in-house tools and microservices speak to
vendor APIs in a consistent way. Each service can focus on business logic while
`apiconfig` handles configuration merging, secure credential storage and token
refresh flows.

At the top level this package ties together the submodules that actually
implement the work. `auth` offers pluggable authentication strategies, `config`
manages settings providers and loading order, `exceptions` defines a structured
error hierarchy and `utils` contains logging helpers and other small utilities.

## Navigation
- [auth](./auth/README.md) – authentication framework and strategies
- [config](./config/README.md) – configuration providers and management
- [exceptions](./exceptions/README.md) – structured error hierarchy
- [testing](./testing/README.md) – helpers and fixtures for tests
- [utils](./utils/README.md) – logging and miscellaneous utilities
- [types](./types/README.md) – shared type definitions

## Contents
- `auth/` – authentication framework and built‑in strategies.
- `config/` – `ClientConfig` class and configuration providers.
- `exceptions/` – structured error hierarchy for configuration and HTTP issues.
- `testing/` – helpers and fixtures for unit and integration tests.
- `utils/` – assorted utilities such as logging setup and URL helpers.
- `__init__.py` – re‑exports common classes and determines the package version.

## Usage Examples

### Basic Usage
```python
from apiconfig import ClientConfig, ApiKeyAuth

config = ClientConfig(
    hostname="api.example.com",
    auth_strategy=ApiKeyAuth(api_key="key", header_name="X-API-Key"),
)
print(config.base_url)
```

### Advanced Usage
```python
from apiconfig.auth import AuthStrategy
from apiconfig import ClientConfig


class CustomAuth(AuthStrategy):
    def prepare_request_headers(self) -> dict[str, str]:
        return {"X-Custom-Auth": "secret"}

    def prepare_request_params(self) -> dict[str, str]:
        return {}


config = ClientConfig(hostname="api.example.com", auth_strategy=CustomAuth())
print(config.base_url)
```

## Key components
| Component | Description |
| --------- | ----------- |
| `ClientConfig` | Holds API connection settings like base URL, timeouts and authentication. |
| `AuthStrategy` and friends | Base class and built‑in strategies for headers or token handling. |
| `ConfigManager` | Loads and merges configuration from providers. |
| `EnvProvider` / `FileProvider` / `MemoryProvider` | Sources for configuration data. |
| `APIConfigError` and subclasses | Domain specific exceptions for reporting failures. |

## Architecture
`apiconfig` is organised into small focused modules. Authentication strategies
implement the **Strategy** pattern while configuration providers can be combined
in any order via `ConfigManager`.

```mermaid
flowchart TD
    Provider1 --> Manager
    Provider2 --> Manager
    Manager --> ClientConfig
    ClientConfig --> AuthStrategy
```

## Testing
Install dependencies and run the full test suite:
```bash
python -m pip install -e .
python -m pip install pytest pytest-httpserver pytest-xdist
pytest -q
```

## Dependencies

### External Dependencies
- Python 3.11 or later

### Internal Dependencies
- `apiconfig.auth` – authentication strategies
- `apiconfig.config` – configuration management
- `apiconfig.exceptions` – error hierarchy
- `apiconfig.utils` – utility helpers


## Status

**Stability:** Stable
**API Version:** 0.0.0
**Deprecations:** None

### Maintenance Notes
- Library is used in production and receives regular updates.

### Changelog
- 0.0.0 – Initial public release.

### Future Considerations
- Expand documentation for custom provider integrations.
