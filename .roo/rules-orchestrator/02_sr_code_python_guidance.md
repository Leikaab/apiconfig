# Current Project Focus: Polish, Test Coverage, Integration, and Documentation

**As of April 2025, the apiconfig project is in its finalization phase.**

All instructions to sr-code-python must ensure:
- 100% unit test coverage for all code
- Robust integration tests for all features
- Comprehensive and up-to-date documentation

Completion criteria should explicitly confirm these standards are met.

---

# Orchestrator Guidance for Instructing `sr-code-python`

When delegating implementation tasks to `sr-code-python`, provide clear, specific instructions including the following project-specific guidance:

1.  **Task Specifics:**
    *   Clearly state the goal (e.g., implement `GET /v2/project/{id}`).
    *   Provide necessary context: required parameters, expected response structure (referencing `specs/swagger.json`), relevant documentation (`docs/create_new_endpoints/`).

2.  **`crudclient` Usage Instructions:**
    *   **Explicitly instruct** on the correct pattern for the task:
        *   "For standard operations (list, get-by-id, create, update, delete) on the main resource path, you **must** use the inherited base `CRUD` methods (e.g., `self.list()`, `self.get(id=...)`)."
        *   "For non-standard operations (sub-resources, custom actions), you **must** use the `custom_action` method. Specify the `action` path segment, `method`, and `params`/`data`."
    *   **Emphasize:** "Do **not** manually construct URLs or reimplement base `CRUD` logic. Use the provided base methods."

3.  **Stub File (`.pyi`) Instructions:**
    *   Remind: "All docstrings and public type hints belong **only** in the `.pyi` file. Keep the `.py` file for implementation logic."

4.  **Tripletex API Quirk Reminders (If Applicable):**
    *   If the task involves endpoints known to have quirks, **proactively remind** `sr-code-python`:
        *   "Be aware of potential non-standard `fields` parameter syntax (e.g., `fields=*,parent(*)`) for this endpoint."
        *   "Remember the 10,000 record pagination limit if fetching large datasets."
        *   "Watch for contextual validation errors (e.g., `organizationNumber` based on country) not defined in Swagger."
        *   "Ensure only the `id` field is included when sending nested object references in payloads."

5.  **Mandatory Quality Checks:**
    *   Specify the **exact** checks `sr-code-python` **must** delegate to the `test-runner-summarizer` mode before reporting completion (e.g., `mypy .`, `pre-commit run --all-files`, `pytest tests/unit/test_your_endpoint.py`, `pytest tests/integration/test_your_endpoint.py`).
    *   Instruct: "You **must** confirm in your completion report that the `test-runner-summarizer` reported all specified checks as passed, and do not attempt to run or analyze these checks directly."

6.  **Completion Criteria:**
    *   State the expected output (e.g., working endpoint method, passing tests).
    *   Instruct `sr-code-python` to use `attempt_completion` and explicitly confirm all specified checks passed.