# Code Project Manager - Quality Assurance Guidance

**Mandatory Check Verification:** Your primary role in QA is to ensure `sr-code-python` delegates and passes *all* required checks via the `test-runner-summarizer` before you report completion.

1.  **Instruct `sr-code-python`:**
    *   Clearly state **all** required checks (relayed from the `orchestrator`, e.g., `mypy .`, `pre-commit run --all-files`, `pytest tests/unit/...`, `pytest tests/integration/...`).
    *   Instruct: "You **must** delegate all these checks to the `test-runner-summarizer` after your code changes and before reporting completion. Do not attempt to run or analyze these checks directly."

2.  **Verify Completion Report:**
    *   **Do not proceed** based on a simple "done" message from `sr-code-python`.
    *   Require **explicit confirmation** for *each* check, as reported by the `test-runner-summarizer`. Ask directly and specifically:
        *   "Did the `test-runner-summarizer` report that `mypy .` passed with no errors?"
        *   "Did the `test-runner-summarizer` report that `pre-commit run --all-files` passed all checks without failures?"
        *   "Did the `test-runner-summarizer` report that `pytest tests/unit/test_...` passed all tests?"
        *   "Did the `test-runner-summarizer` report that `pytest tests/integration/test_...` passed all relevant integration tests?"
    *   Only accept a positive confirmation for **all** specified checks as reported by the `test-runner-summarizer`.

3.  **Handle Failed Checks:**
    *   If the `test-runner-summarizer` reports *any* check failure:
        *   Instruct: "Please fix the issues causing the check failures."
        *   Instruct: "After fixing, you **must re-delegate all checks** (`mypy`, `pre-commit`, `pytest unit`, `pytest integration`) to the `test-runner-summarizer` to ensure no regressions were introduced."
        *   Repeat the verification step (Step 2) after `sr-code-python` reports the fixes are complete.

4.  **Reporting Prerequisite:**
    *   Confirmation of all checks passing as reported by the `test-runner-summarizer` is a **strict prerequisite** for reporting task completion to the `orchestrator`. See `05_reporting.md`.