# No Size Guard in safe_json_decode

**Module**: `apiconfig/utils/http.py`
**Category**: Edge Case

## Problem
The `safe_json_decode` utility does not guard against excessively large payloads, risking memory exhaustion if a huge response is received.

## Impact
- Malicious or misconfigured endpoints can cause denial-of-service by sending large payloads.

## Reproduction / Scenario
- Call `safe_json_decode` on a multi-megabyte or unbounded response body.

## Notes
- Consider a maximum size limit before attempting to decode.