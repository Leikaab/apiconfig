# Redaction Misses Multi-Value Headers

**Module**: `apiconfig/utils/logging/filters.py`
**Category**: Edge Case

## Problem
Redaction filters do not properly handle multi-value headers like `Cookie` or `Set-Cookie`, leaving sensitive data exposed in logs.

## Impact
- Sensitive information may be leaked in logs, violating security policies.

## Reproduction / Scenario
- Log a request/response with multi-value `Cookie` or `Set-Cookie` headers.

## Notes
- Update redaction logic to handle multi-value header formats.