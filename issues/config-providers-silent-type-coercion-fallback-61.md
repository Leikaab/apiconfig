---
issue_number: 61
title: "Silent Type Coercion Fallback in Config Providers"
url: "https://github.com/Leikaab/apiconfig/issues/61"
state: OPEN
created_at: "2025-04-20T00:10:50Z"
updated_at: "2025-04-20T00:10:50Z"
author:
  login: "Leikaab"
  id: "MDQ6VXNlcjQ5NzkxNzAx"
  is_bot: false
assignees: []
labels: []
---

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