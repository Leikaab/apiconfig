# apiconfig.auth.strategies

`apiconfig.auth.strategies` contains the built-in authentication strategies bundled with **apiconfig**. Every strategy implements the `AuthStrategy` interface and can be injected into a `ClientConfig` to attach credentials to outgoing HTTP requests.

This package hides authentication details behind a common interface so client code stays the same regardless of how credentials are provided. The design follows the Strategy pattern, allowing you to swap or extend authentication mechanisms without modifying other parts of the client.

## Navigation
**Parent Module:** [apiconfig.auth](../README.md)

- [`api_key.py`](./api_key.py) – API key authentication via header or query parameter.
- [`basic.py`](./basic.py) – HTTP Basic authentication.
- [`bearer.py`](./bearer.py) – Bearer token authentication with optional expiry and refresh support.
- [`custom.py`](./custom.py) – User-defined strategies with callbacks.
- [`__init__.py`](./__init__.py) – Re-exports all strategies for convenience.

## Contents
- `api_key.py` – API key authentication via header or query parameter.
- `basic.py` – HTTP Basic authentication.
- `bearer.py` – Bearer token with optional expiry and refresh support.
- `custom.py` – User-defined strategies with callbacks.
- `__init__.py` – re-exports all strategies for easy import.

## Usage example
```python
from datetime import datetime, timedelta, timezone
from apiconfig import ClientConfig
from apiconfig.auth.strategies import ApiKeyAuth, BasicAuth, BearerAuth, CustomAuth

# API key in a header
auth_header = ApiKeyAuth(api_key="secret", header_name="X-API-Key")

# Basic Auth
basic_auth = BasicAuth(username="user", password="pass")

# Bearer token with expiry
bearer_auth = BearerAuth(
    access_token="token",
    expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
)

# Custom strategy using a callback
custom_auth = CustomAuth(header_callback=lambda: {"X-Custom": "value"})

config = ClientConfig(hostname="api.example.com", auth_strategy=auth_header)
```

## Key classes
| Class | Description |
| ------ | ----------- |
| `ApiKeyAuth` | Sends an API key in a header or as a query parameter. |
| `BasicAuth` | Adds an `Authorization: Basic` header using a username and password. |
| `BearerAuth` | Uses a bearer token and can refresh it when `expires_at` is set and a refresh function is available. |
| `CustomAuth` | Allows custom callbacks for headers, parameters and refresh logic. |

### Design pattern
The strategies implement the **Strategy pattern**: each one conforms to `AuthStrategy` so they can be swapped without changing client code.

## Sequence diagram
```mermaid
sequenceDiagram
    participant Client
    participant Strategy as AuthStrategy
    Client->>Strategy: prepare_request_headers()
    Strategy-->>Client: headers
    Client->>Server: HTTP request with auth headers
```

## Test instructions
Install dependencies and run the unit tests for this module:
```bash
python -m pip install -e .
python -m pip install pytest
pytest tests/unit/auth/strategies -q
```

## Status
Stable – the strategies are used by other parts of **apiconfig** and have dedicated test coverage.
