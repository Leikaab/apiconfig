---
issue_number: 62
title: "Minor docstring drift between auth/strategies/custom.py and custom.pyi"
url: "https://github.com/Leikaab/apiconfig/issues/62"
state: OPEN
createdAt: "2025-04-20T00:11:40Z"
updatedAt: "2025-04-20T00:11:40Z"
author:
  login: "Leikaab"
  id: "MDQ6VXNlcjQ5NzkxNzAx"
  is_bot: false
id: "I_kwDOObjluc6zNtoZ"
isPinned: false
labels: []
milestone: null
assignees: []
closed: false
closedAt: null
stateReason: ""
reactionGroups: []
projectCards: []
projectItems: []
comments: []
---

## Summary
The `apiconfig/auth/strategies/custom.pyi` stub provides more detailed docstrings for `CustomAuth` methods, especially regarding raised exceptions and error conditions. The implementation file `custom.py` has docstrings, but they are less explicit about all error cases. This leads to minor inconsistencies in documentation.

## Evidence
```python
# apiconfig/auth/strategies/custom.py
def prepare_request_headers(self) -> Dict[str, str]:
    """
    Generates request headers using the header_callback, if provided.

    Returns:
        A dictionary of headers.

    Raises:
        AuthStrategyError: If the header_callback does not return a dictionary.
    """
    # (implementation does raise for callback exceptions, but docstring does not mention it)

# apiconfig/auth/strategies/custom.pyi
def prepare_request_headers(self) -> Dict[str, str]:
    """
    Generates request headers using the header_callback, if provided.

    Returns:
        A dictionary of headers.

    Raises:
        AuthStrategyError: If the header_callback does not return a dictionary
                           or raises an exception.
    """
    ...
```

## Impact
- Users may not be fully aware of all error conditions at runtime.
- Slightly increases the risk of misunderstanding or misuse of the `CustomAuth` class.

## Suggested Direction
- Update the docstrings in `custom.py` to explicitly mention all error conditions, matching the `.pyi` stub.
- Ensure future changes to method documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.