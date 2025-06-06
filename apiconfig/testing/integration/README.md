# apiconfig.testing.integration

Utilities for end-to-end tests of **apiconfig** based clients. The package contains helpers for spinning up mock HTTP servers and convenient pytest fixtures so integrations can be validated without hitting real services.

## Contents
- `fixtures.py` – pytest fixtures that provide temporary config files, HTTP server addresses and ready-made `ConfigManager` instances.
- `helpers.py` – helper functions such as `make_request_with_config` and `simulate_token_endpoint` for interacting with the mock server.
- `servers.py` – utilities to configure and verify responses of `pytest_httpserver`.
- `__init__.py` – exports the public helpers mentioned above.

## Usage
```python
from apiconfig.testing.integration import (
    configure_mock_response,
    make_request_with_config,
    setup_multi_provider_manager,
)
from apiconfig.auth.strategies import BasicAuth
from apiconfig.config.base import ClientConfig

# Prepare a ConfigManager using the helper
manager = setup_multi_provider_manager([
    ("defaults", {"api": {"hostname": "example.com"}}),
])
config = manager.load_config()

# Configure the mock HTTP server in a test
configure_mock_response(
    httpserver,
    path="/ping",
    response_data={"ok": True},
)

# Make a request using an auth strategy and ClientConfig
response = make_request_with_config(
    config=config,
    auth_strategy=BasicAuth("user", "pass"),
    mock_server_url=str(httpserver.url_for("/")),
    path="/ping",
)
assert response.json() == {"ok": True}
```

## Key Functions
| Name | Description |
| ---- | ----------- |
| `configure_mock_response` | Set up expectations on the mock server for a given path and method. |
| `assert_request_received` | Validate that the server received the expected requests. |
| `make_request_with_config` | Convenience wrapper around `httpx` that injects headers and parameters from an `AuthStrategy`. |
| `setup_multi_provider_manager` | Create a `ConfigManager` using multiple in-memory providers. |
| `simulate_token_endpoint` | Configure a mock token endpoint for testing OAuth2 flows. |

### Diagram
```mermaid
sequenceDiagram
    participant Test
    participant HTTPServer
    Test->>HTTPServer: configure_mock_response()
    Test->>HTTPServer: simulate_token_endpoint()
    Test->>Test: make_request_with_config()
```

## Testing
Install dependencies and run the integration tests for this package:
```bash
python -m pip install -e .
python -m pip install pytest pytest-httpserver
pytest tests/integration -q
```

## Status
Experimental – helpers may change as integration needs evolve.
