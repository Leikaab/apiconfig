---
issue_number: 74
issue_url: https://github.com/Leikaab/apiconfig/issues/74
repository: Leikaab/apiconfig
labels: [bug]
title: No Timeout or JSON Error Handling in Token Refresh
---

# No Timeout or JSON Error Handling in Token Refresh

**Module**: `apiconfig/auth/token/refresh.py`
**Category**: Edge Case

## Problem
The token refresh logic does not handle timeouts or retries, and if JSON decoding fails, raw bytes are returned instead of raising a `TokenRefreshError`.

## Impact
- Network stalls or transient failures can hang or crash the client.
- Downstream code may receive unexpected data types, complicating error handling.

## Reproduction / Scenario
- Simulate a slow or unresponsive token endpoint.
- Return invalid JSON from the endpoint and observe the error propagation.

## Notes
- Add timeout/retry logic and wrap JSON decode errors in `TokenRefreshError`.