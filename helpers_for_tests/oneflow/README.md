# helpers_for_tests.oneflow

Utilities for testing integrations with the OneFlow API.

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

## Status
Internal – for example tests only.
