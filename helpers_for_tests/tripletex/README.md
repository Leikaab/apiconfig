# helpers_for_tests.tripletex

Test helpers for the Tripletex API using apiconfig.

## Contents
- `tripletex_client.py` – `TripletexClient` with basic endpoints
- `tripletex_auth.py` – `TripletexSessionAuth` for session token handling
- `tripletex_config.py` – configuration helpers (`create_tripletex_client_config`, etc.)
- `__init__.py` – package marker

## Usage example
```python
from helpers_for_tests.tripletex import create_tripletex_client_config, TripletexClient

config = create_tripletex_client_config()
client = TripletexClient(config)
info = client.get_session_info()
```

## Key classes/functions
| Name | Description |
| ---- | ----------- |
| `TripletexClient` | Client built on `BaseClient` |
| `TripletexSessionAuth` | Session-based auth strategy |
| `create_tripletex_client_config` | Build `ClientConfig` using `TRIPLETEX_TEST_` environment variables |
| `create_tripletex_config_manager` | `ConfigManager` with defaults and `EnvProvider` |
| `create_tripletex_auth_strategy` | Helper for constructing `TripletexSessionAuth` |
| `skip_if_no_credentials` | Skip tests if credentials are missing |

### Environment
Example environment variables:
```bash
TRIPLETEX_TEST_CONSUMER_TOKEN=consumer
TRIPLETEX_TEST_EMPLOYEE_TOKEN=employee
TRIPLETEX_TEST_company_id=0
TRIPLETEX_TEST_hostname=https://api-test.tripletex.tech
TRIPLETEX_TEST_version=v2
TRIPLETEX_TEST_timeout=30.0
```

## Status
Internal – for example tests only.
