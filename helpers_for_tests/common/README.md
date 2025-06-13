# helpers_for_tests.common

## Module Description

Shared helpers used by the example integration clients. This package exposes a simple `BaseClient` class that builds on top of **apiconfig**'s configuration and authentication system.

## Navigation
- [helpers_for_tests](../README.md) – overview of test helper clients.

## Contents
- `base_client.py` – generic HTTP client with error handling and JSON parsing.
- `__init__.py` – package marker.

## Usage Examples
```python
from typing import Dict, Optional

from helpers_for_tests.common.base_client import BaseClient
from apiconfig.auth.base import AuthStrategy
from apiconfig.config import ClientConfig
from apiconfig.types import HttpMethod

class DummyAuth(AuthStrategy):
    def prepare_request_headers(self) -> Dict[str, str]:
        return {"Authorization": "Bearer token"}

    def prepare_request_params(self) -> Optional[dict]:
        return None

config = ClientConfig(hostname="https://api.example.com", auth_strategy=DummyAuth())
client = BaseClient(config)

result = client._request(HttpMethod.GET, "/ping")
print(result)
```

## Key Components
| Name | Description |
| ---- | ----------- |
| `BaseClient` | Base class that prepares URLs and headers and parses JSON responses. |

## Architecture
`BaseClient` follows a light template approach where `_request` delegates authentication details to the configured `AuthStrategy`.

```mermaid
sequenceDiagram
    participant Client as BaseClient
    participant Auth as AuthStrategy
    Client->>Auth: prepare_request_headers()
    Auth-->>Client: headers
    Client->>Server: HTTP request
    Server-->>Client: httpx.Response
    Client->>Client: _handle_response()
```

## Testing
```bash
python -m pip install -e .
python -m pip install pytest
pytest tests/unit/helpers/common -q
```

## Dependencies
### External Dependencies
- `httpx` – HTTP client used for requests.

### Internal Dependencies
- `apiconfig.config`
- `apiconfig.exceptions.http`
- `apiconfig.types`
- `apiconfig.utils.http`
- `apiconfig.utils.url`

## Status

- **Stability:** Internal – intended only for the helper clients used in tests.
- **API Version:** 0.3.2
- **Deprecations:** None

### Maintenance Notes
- APIs may change to support evolving test requirements.

### Changelog
- No dedicated changelog. See repository history for details.

### Future Considerations
- Updates will track new testing patterns as needed.
