---
issue_number: 57
issue_url: https://github.com/Leikaab/apiconfig/issues/57
title: ClientConfig Version and Timeout Validation
labels: [bug]
assignee: @me
status: open
created: 2025-04-20
---

# ClientConfig Version and Timeout Validation

**Module**: `apiconfig/config/base.py`
**Category**: Pattern Smell

## Problem
`ClientConfig` concatenates `version` strings without guarding for a leading or trailing slash, and allows negative or zero values for `timeout` and `retries`.

## Impact
- Can produce malformed URLs or cause requests to fail unexpectedly.
- May result in infinite timeouts or retry loops.

## Reproduction / Scenario
- Set `version="v1"` and base URL ending with `/`, or vice versa.
- Pass `timeout=0` or `retries=-1` to the config.

## Notes
- Validate and normalize `version` and numeric parameters on init.