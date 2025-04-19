# Current Project Focus: Polish, Test Coverage, Integration, and Documentation

**As of April 2025, the apiconfig project is in its finalization phase.**

Pattern verification must now also ensure:
- 100% unit test coverage for all code
- Robust integration tests for real-world scenarios
- Code and docstring quality (clarity, completeness, consistency)
- Identification of design or pattern weaknesses
- Adherence to documentation and best practices

The following guidance should be interpreted in light of these priorities.

---

# Code Project Manager - Pattern Verification Guidance

**Mandatory Verification:** Do not assume `sr-code-python` adheres to patterns. Actively verify implementation details.

1.  **Guidance & Verification on apiconfig Patterns:**
    *   **Instruct Before Implementation:** Remind `sr-code-python` to follow apiconfig's current module structure and best practices:
        *   Use the appropriate modules (e.g., `config/base.py` for configuration, `auth/strategies/` for authentication, `utils/` for helpers).
        *   Follow extensibility patterns (base classes, clear interfaces).
        *   Use type hints and .pyi stub files for all public interfaces.
        *   Raise specific exceptions from the `exceptions/` module.
        *   Ensure all new code is accompanied by unit and integration tests.
    *   **Verify During/After Coding:** Ask specific questions or review snippets:
        *   "Are you using the correct apiconfig module for this functionality?"
        *   "Are all public types and docstrings in the .pyi file?"
        *   "Are you raising specific exceptions and not using generic Exception?"
        *   "Are all new features fully tested and documented?"
2.  **Guidance & Verification on Stub Files (`.pyi`):**
    *   **Instruct:** "Docstrings and public type hints **must** be in the `.pyi` file only."
    *   **Verify:** Ask: "Confirm docstrings/public types are in the `.pyi` file?" Review snippets if necessary, checking `.py` files for misplaced docstrings/public types.

3.  **Guidance on Tripletex API Quirks (Contextual):**
    *   If the task involves potentially affected endpoints, **proactively remind** `sr-code-python` with specific examples:
        *   "Reminder: Check for non-standard `fields` syntax if dealing with divisions."
        *   "Reminder: Account for the 10k pagination limit if fetching all records."
        *   "Reminder: Watch for contextual validation on `organizationNumber`."
        *   "Reminder: Use ID-only object referencing in payloads (e.g., `{'projectManager': {'id': 123}}`)."