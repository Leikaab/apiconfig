---
github_issue_number: 77
github_issue_url: https://github.com/Leikaab/apiconfig/issues/77
github_issue_state: OPEN
github_issue_title: Double-Slash Collapse Breaks Legitimate Paths
github_issue_author: Leikaab
github_issue_author_id: MDQ6VXNlcjQ5NzkxNzAx
github_issue_created_at: 2025-04-20T00:45:47Z
github_issue_updated_at: 2025-04-20T00:45:47Z
github_issue_labels:
  - name: bug
    id: LA_kwDOObjluc8AAAAB-S4H2Q
    description: Something isn't working
    color: d73a4a
github_issue_assignees: []
---

# Double-Slash Collapse Breaks Legitimate Paths

**Module**: `apiconfig/utils/url/building.py`
**Category**: Pattern Smell

## Problem
URL building logic collapses double slashes, which breaks legitimate URLs like `http://host//resource`.

## Impact
- Some APIs require double slashes in the path; collapsing them can cause incorrect routing or 404 errors.

## Reproduction / Scenario
- Build a URL with a double slash in the path and observe the result.

## Notes
- Only collapse slashes where not semantically significant.