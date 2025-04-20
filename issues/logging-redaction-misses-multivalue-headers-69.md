---
github_issue_number: 69
github_issue_url: https://github.com/Leikaab/apiconfig/issues/69
github_issue_id: I_kwDOObjluc6zNvRj
github_issue_state: OPEN
github_issue_created_at: 2025-04-20T00:26:04Z
github_issue_updated_at: 2025-04-20T00:26:04Z
github_issue_author_login: Leikaab
github_issue_author_id: MDQ6VXNlcjQ5NzkxNzAx
---

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