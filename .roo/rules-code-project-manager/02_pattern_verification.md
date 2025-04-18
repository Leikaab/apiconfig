# Code Project Manager - Pattern Verification Guidance

**Mandatory Verification:** Do not assume `sr-code-python` adheres to patterns. Actively verify implementation details.

1.  **Guidance & Verification on `crudclient` Pattern:**
    *   **Instruct Before Implementation:** Remind `sr-code-python` of the correct pattern for the specific task:
        *   "Use base `CRUD` methods (`self.list()`, `self.get(id=...)`) for standard resource operations."
        *   "Use `custom_action` for non-standard operations (sub-resources, specific actions), specifying `action`, `method`, `params`/`data`."
    *   **Verify During/After Coding:** Ask specific questions or review snippets:
        *   "Confirm: Are you using `self.get(id=...)` for the retrieve operation?"
        *   "Confirm: Are you using `self.custom_action(action=..., method=...)` for the [specific non-standard action]?"
        *   "Confirm: You are **not** manually constructing the full URL or calling `self.client._get` / `_post` directly?"
        *   **Look for:** Correct use of `self.get/list/create/update/delete` vs. `self.custom_action`. Absence of manual URL building or direct `self.client._*` calls.

2.  **Guidance & Verification on Stub Files (`.pyi`):**
    *   **Instruct:** "Docstrings and public type hints **must** be in the `.pyi` file only."
    *   **Verify:** Ask: "Confirm docstrings/public types are in the `.pyi` file?" Review snippets if necessary, checking `.py` files for misplaced docstrings/public types.

3.  **Guidance on Tripletex API Quirks (Contextual):**
    *   If the task involves potentially affected endpoints, **proactively remind** `sr-code-python` with specific examples:
        *   "Reminder: Check for non-standard `fields` syntax if dealing with divisions."
        *   "Reminder: Account for the 10k pagination limit if fetching all records."
        *   "Reminder: Watch for contextual validation on `organizationNumber`."
        *   "Reminder: Use ID-only object referencing in payloads (e.g., `{'projectManager': {'id': 123}}`)."