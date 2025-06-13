# helpers_for_tests

## Module Description
This directory provides thin example clients used in the test suite. Each package offers minimal wrappers around **apiconfig** to simplify integration scenarios.

## Navigation
- [common](common/README.md) – shared `BaseClient` utilities
- [fiken](fiken/README.md) – Fiken API helpers
- [oneflow](oneflow/README.md) – OneFlow API helpers
- [tripletex](tripletex/README.md) – Tripletex API helpers

## Contents
- `README.md` – this guide
- `__init__.py` – package marker
- `common/` – shared base client utilities
- `fiken/` – Fiken helpers
- `oneflow/` – OneFlow helpers
- `tripletex/` – Tripletex helpers

## Usage example
```python
from helpers_for_tests.fiken import create_fiken_client_config, FikenClient

config = create_fiken_client_config()
client = FikenClient(config)
companies = client.list_companies()
```

## Status
- **Stability**: Internal-only helpers
- **API Version**: Mirrors project defaults
- **Deprecations**: None
- **Maintenance**: Updated as tests evolve

### Future Considerations
- Expand examples with new API patterns as needed.
