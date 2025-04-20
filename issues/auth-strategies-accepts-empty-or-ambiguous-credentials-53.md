---
issue_number: 53
github_issue_url: https://github.com/Leikaab/apiconfig/issues/53
title: Accepts Empty or Ambiguous Credentials
labels: [bug]
---

# Accepts Empty or Ambiguous Credentials

**Module**: `apiconfig/auth/strategies/`
**Category**: Edge Case

## Problem
Authentication strategies accept empty or whitespace credentials, and allow both `header_name` and `param_name` to be set simultaneously, leading to ambiguous placement of credentials.

## Impact
- May result in silent authentication failures or credentials being sent in unintended locations.
- Increases risk of subtle security or integration bugs.

## Reproduction / Scenario
- Instantiate an auth strategy with empty or whitespace credentials.
- Pass both `header_name` and `param_name` to a strategy and observe ambiguous behavior.

## Notes
- Consider input validation for credentials and mutually exclusive parameters.