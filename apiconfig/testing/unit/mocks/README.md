# apiconfig.testing.unit.mocks

Mocks used for unit testing **apiconfig** components.  These helpers provide
lightweight stand-ins for the real authentication strategies and configuration
classes so that tests can run without talking to external services.

## Contents
- `auth.py` – mock implementations of the authentication strategies (`BasicAuth`,
  `BearerAuth`, `ApiKeyAuth`, `CustomAuth`) plus refreshable variants and a
  `MockHttpRequestCallable` for simulating HTTP refresh endpoints.
- `config.py` – `MockConfigProvider`, the `create_mock_client_config` helper and
  `MockConfigManager` for testing configuration loading logic.
- `__init__.py` – re-exports the most common mocks for convenience.

## Usage
```python
from apiconfig.testing.unit.mocks import (
    MockConfigManager,
    MockConfigProvider,
    create_mock_client_config,
)
from apiconfig.testing.unit.mocks.auth import MockBasicAuth

# Create a simple configuration using a mock provider
provider = MockConfigProvider({"hostname": "api.test.com"})
manager = MockConfigManager(providers=[provider])
config = manager.load_config()

# Use a mock auth strategy when constructing clients
auth = MockBasicAuth()
headers, params = auth.prepare_request()
```

## Key Classes
| Class | Description |
| ----- | ----------- |
| `MockAuthStrategy` | Base class that merges header/param overrides and can raise configured exceptions. |
| `MockBasicAuth` / `MockBearerAuth` / `MockApiKeyAuth` | Concrete mocks mirroring the real auth strategies. |
| `MockRefreshableAuthStrategy` | Adds refresh behaviour and helpers for testing concurrent refresh scenarios. |
| `MockHttpRequestCallable` | Callable returning dummy HTTP responses for token refresh tests. |
| `MockConfigProvider` | Duck-typed provider returning a predefined dictionary. |
| `MockConfigManager` | Subclass of `ConfigManager` whose `load_config` method is a `MagicMock`. |

### Design
The mocks follow a minimal design where behaviour is simulated through simple
attributes and `MagicMock`. The auth mocks implement the same interfaces as the
real strategies so tests can swap them in without modifying production code.

```mermaid
flowchart TD
    MockConfigManager -->|uses| MockConfigProvider
    MockConfigManager --> ClientConfig
    MockBasicAuth --> AuthStrategy
```

## Tests
Run only the tests related to the mocks package:
```bash
python -m pip install -e .
python -m pip install pytest pytest-xdist
pytest tests/unit/testing/unit/mocks -q
```

## Status
Internal – provided solely for unit testing purposes but kept stable.
