# helpers_for_tests.oneflow

Utilities for testing integrations with the OneFlow API.

## Navigation
- [Back to `helpers_for_tests`](../README.md)

## Contents
- `oneflow_client.py` – `OneFlowClient` with simple user and contract endpoints
- `oneflow_config.py` – configuration helpers (`create_oneflow_client_config`, etc.)
- `__init__.py` – package marker

## Usage example
```python
from helpers_for_tests.oneflow import create_oneflow_client_config, OneFlowClient

config = create_oneflow_client_config()
client = OneFlowClient(config)
users = client.list_users()
```

## Key classes/functions
| Name | Description |
| ---- | ----------- |
| `OneFlowClient` | Client built on `BaseClient` |
| `create_oneflow_client_config` | Build `ClientConfig` using `ONEFLOW_` environment variables |
| `create_oneflow_config_manager` | `ConfigManager` with defaults and `EnvProvider` |
| `create_oneflow_auth_strategy` | `ApiKeyAuth` using `ONEFLOW_API_KEY` |
| `skip_if_no_credentials` | Skip tests if credentials are missing |

### Environment
Typical environment variables:
```bash
ONEFLOW_API_KEY=token
ONEFLOW_USER_EMAIL=user@example.com
ONEFLOW_hostname=https://api.test.oneflow.com
ONEFLOW_version=v1
ONEFLOW_timeout=10.0
```

## Tests
```bash
poetry run pytest tests/integration/test_apiconfig_oneflow.py -q
```

## Status

- **Stability:** Internal – for example tests only.
- **API Version:** Matches sample endpoints used in tests.
- **Deprecations:** None.

### Maintenance Notes
- Provided for integration tests and may change without notice.

### Changelog
- No dedicated changelog. Refer to repository history.

### Future Considerations
- Update along with underlying Oneflow API changes.
