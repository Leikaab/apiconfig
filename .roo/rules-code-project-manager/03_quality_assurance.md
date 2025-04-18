# Code Project Manager - Quality Assurance Guidance

**Mandatory Check Verification:** Your primary role in QA is to ensure `sr-code-python` runs and passes *all* required checks before you report completion.

1.  **Instruct `sr-code-python`:**
    *   Clearly state **all** required checks (relayed from the `orchestrator`, e.g., `mypy .`, `pre-commit run --all-files`, `pytest tests/unit/...`, `pytest tests/integration/...`).
    *   Instruct: "You **must** run all these checks after your code changes and before reporting completion."

2.  **Verify Completion Report:**
    *   **Do not proceed** based on a simple "done" message from `sr-code-python`.
    *   Require **explicit confirmation** for *each* check. Ask directly and specifically:
        *   "Did `mypy .` pass with no errors?"
        *   "Did `pre-commit run --all-files` pass all checks without failures?"
        *   "Did `pytest tests/unit/test_...` pass all tests?"
        *   "Did `pytest tests/integration/test_...` pass all relevant integration tests?"
    *   Only accept a positive confirmation for **all** specified checks.

3.  **Handle Failed Checks:**
    *   If `sr-code-python` reports *any* check failure:
        *   Instruct: "Please fix the issues causing the check failures."
        *   Instruct: "After fixing, you **must re-run all checks** (`mypy`, `pre-commit`, `pytest unit`, `pytest integration`) to ensure no regressions were introduced."
        *   Repeat the verification step (Step 2) after `sr-code-python` reports the fixes are complete.

4.  **Reporting Prerequisite:**
    *   Confirmation of all checks passing is a **strict prerequisite** for reporting task completion to the `orchestrator`. See `05_reporting.md`.