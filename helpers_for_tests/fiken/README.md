# helpers_for_tests.fiken

Helper modules for integration tests with the Fiken API.

## Contents
- `fiken_client.py` – `FikenClient` for basic API calls
- `fiken_config.py` – configuration helpers (`create_fiken_client_config`, etc.)
- `__init__.py` – package marker

## Usage example
```python
from helpers_for_tests.fiken import create_fiken_client_config, FikenClient

config = create_fiken_client_config()
client = FikenClient(config)
companies = client.list_companies()
```

## Key classes/functions
| Name | Description |
| ---- | ----------- |
| `FikenClient` | Simple client built on `BaseClient` |
| `create_fiken_client_config` | Build `ClientConfig` using `FIKEN_` environment variables |
| `create_fiken_config_manager` | `ConfigManager` with defaults and `EnvProvider` |
| `create_fiken_auth_strategy` | `BearerAuth` using `FIKEN_ACCESS_TOKEN` |
| `skip_if_no_credentials` | Skip tests if credentials are missing |

### Environment
Set these variables when running integration tests:
```bash
FIKEN_ACCESS_TOKEN=token
FIKEN_hostname=https://api.fiken.no/api
FIKEN_version=v2
FIKEN_timeout=10.0
```

## Status
Internal – for example tests only.
