# Silent Type Coercion Fallback in Config Providers

**Module**: `apiconfig/config/providers/`
**Category**: Pattern Smell

## Problem
`EnvProvider` and `FileProvider` silently fall back to `str` when type coercion fails (e.g., on `ValueError`), masking configuration errors.

## Impact
- Invalid configuration values may go undetected, leading to subtle runtime bugs.

## Reproduction / Scenario
- Set an environment or file config value to an invalid type (e.g., `timeout="not-a-number"`).

## Notes
- Consider raising or logging on type coercion failure.