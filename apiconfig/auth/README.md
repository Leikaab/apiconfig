# apiconfig.auth

Authentication framework for **apiconfig**.  This package defines the common `AuthStrategy` base class and bundles the built in authentication strategies and token utilities.

## Contents
- `base.py` – abstract `AuthStrategy` with refresh support.
- `strategies/` – collection of ready to use strategies such as `BasicAuth`, `BearerAuth` and `ApiKeyAuth`.
- `token/` – helpers for OAuth2 token refresh and storage.
- `__init__.py` – re-exports the most used classes for convenience.

## Usage example
```python
from datetime import datetime, timedelta, timezone
from apiconfig.auth import AuthStrategy
from apiconfig.auth.strategies import BearerAuth
from apiconfig.config import ClientConfig

# Set up bearer authentication with expiry
auth = BearerAuth(
    access_token="secret",
    expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
)

config = ClientConfig(hostname="api.example.com", auth_strategy=auth)
headers = auth.prepare_request_headers()
```

## Key classes
| Name | Description |
| ---- | ----------- |
| `AuthStrategy` | Base class defining `prepare_request_headers`, `prepare_request_params` and optional refresh logic. |
| `ApiKeyAuth` | Sends an API key either in a header or as a query parameter. |
| `BasicAuth` | Adds `Authorization: Basic ...` headers with a username and password. |
| `BearerAuth` | Uses a bearer token and can refresh it when expired. |
| `CustomAuth` | Allows user provided callbacks for headers, parameters and refresh. |

### Design pattern
All strategies implement **Strategy** pattern via the `AuthStrategy` interface and can be swapped without affecting client code.

## Diagram
```mermaid
sequenceDiagram
    participant Client
    participant Strategy as AuthStrategy
    Client->>Strategy: prepare_request_headers()
    Strategy-->>Client: headers
    Client->>Server: HTTP request with headers
```

## Tests
Install dependencies and run the unit tests for the authentication package:
```bash
python -m pip install -e .
python -m pip install pytest pytest-xdist
pytest tests/unit/auth -q
```

## Status
Stable – used by the configuration system and tested via the unit suite.
