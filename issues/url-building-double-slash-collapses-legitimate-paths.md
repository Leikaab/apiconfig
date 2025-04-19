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