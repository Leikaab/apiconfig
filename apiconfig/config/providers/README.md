# apiconfig.config.providers

## Module Description
Configuration providers for **apiconfig** supply configuration values from different
sources so they can be combined by `ConfigManager`.

These classes exist to decouple configuration retrieval from application code. Each
provider focuses on a single source&mdash;environment variables, JSON files or an
in-memory dictionary&mdash;and exposes a simple `load()` method returning a
dictionary.

`ConfigManager` merges provider outputs in order, enabling layering of defaults and
overrides. This strategy-like design keeps the module extensible while presenting a
consistent interface to API clients.

## Navigation

**Parent Module:** [apiconfig.config](../README.md)

**Submodules:** None

## Contents
- `env.py` – load configuration from environment variables with optional type inference.
- `file.py` – read configuration from JSON files.
- `memory.py` – in-memory provider useful for tests or defaults.
- `__init__.py` – exports the provider classes.

## Usage
```python
from apiconfig.config.providers import EnvProvider, FileProvider, MemoryProvider
from apiconfig.config.manager import ConfigManager

providers = [
    EnvProvider(prefix="MYAPP_"),
    FileProvider("config.json"),
    MemoryProvider({"timeout": 10})
]

manager = ConfigManager(providers)
config = manager.load_config()
print(config["timeout"])
```

## Key Classes
| Class | Description |
| ----- | ----------- |
| `EnvProvider` | Loads variables with a prefix (default `APICONFIG_`) and coerces simple types when possible. |
| `FileProvider` | Reads JSON files and allows retrieval of values with dot notation and type conversion. |
| `MemoryProvider` | Stores configuration in an internal dictionary. |

### Design
Providers follow a simple strategy-like pattern: each exposes a `load()` method returning
a dictionary which `ConfigManager` merges in order. Later providers override earlier ones.

```mermaid
flowchart TB
    A[EnvProvider] --> M(ConfigManager)
    B[FileProvider] --> M
    C[MemoryProvider] --> M
    M --> D[Config dict]
```

## Testing
Install requirements and run the unit tests for this package:
```bash
python -m pip install -e .
python -m pip install pytest
pytest tests/unit/config/providers -q
```

## Status
**Stability:** Stable – used internally by other modules in the package.
**API Version:** 0.0.0
**Deprecations:** None

