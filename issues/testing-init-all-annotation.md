---
title: "Missing type annotation for __all__ in testing/__init__.py"
severity: low
location: "apiconfig/testing/__init__.py, apiconfig/testing/__init__.pyi"
---

## Summary
The `apiconfig/testing/__init__.pyi` stub provides an explicit type annotation for `__all__` (`list[str]`), but the implementation file `__init__.py` does not. This is a minor inconsistency that could lead to confusion or missed type errors in static analysis.

## Evidence
```python
# apiconfig/testing/__init__.py
__all__ = [
    "BaseAuthStrategyTest",
    "BaseConfigProviderTest",
    "MockConfigManager",
    "MockConfigProvider",
    "assert_auth_header_correct",
    "assert_client_config_valid",
    "assert_provider_loads",
    "check_auth_strategy_interface",
    "create_auth_credentials",
    "create_invalid_client_config",
    "create_mock_client_config",
    "create_provider_dict",
    "create_valid_client_config",
    "temp_config_file",
    "temp_env_vars",
    # Integration Testing (Placeholder - Add when implemented)
    # "integration", # Example
]

# apiconfig/testing/__init__.pyi
__all__: list[str] = [
    "BaseAuthStrategyTest",
    "BaseConfigProviderTest",
    "MockConfigManager",
    "MockConfigProvider",
    "assert_auth_header_correct",
    "assert_client_config_valid",
    "assert_provider_loads",
    "check_auth_strategy_interface",
    "create_auth_credentials",
    "create_invalid_client_config",
    "create_mock_client_config",
    "create_provider_dict",
    "create_valid_client_config",
    "temp_config_file",
    "temp_env_vars",
    # Integration Testing (Placeholder - Add when implemented)
    # "integration", # Example
]
```

## Impact
- Minor: Static analysis tools may not infer the type of `__all__` in the implementation.
- Could lead to future drift if not kept consistent.

## Suggested Direction
- Add an explicit type annotation for `__all__` in `testing/__init__.py` to match the stub.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project type annotation guidelines.