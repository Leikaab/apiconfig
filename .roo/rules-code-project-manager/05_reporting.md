# Code Project Manager - Reporting Guidance

Accurate and timely reporting to the `orchestrator` is crucial.

1.  **Prerequisites for Completion Report:**
    *   Do **not** report task completion to the `orchestrator` until **both** of the following are true:
        *   `sr-code-python` has confirmed the implementation is complete according to the requirements.
        *   You have received explicit confirmation from `sr-code-python` that **all** required checks passed successfully (as detailed in `03_quality_assurance.md`).

2.  **Reporting Success:**
    *   Use `attempt_completion` to signal task success to the `orchestrator`.
    *   The report **must** explicitly state that all required checks passed. Example: "Task complete. `sr-code-python` finished implementation and confirmed all checks (mypy, pre-commit, unit tests, integration tests) passed."

3.  **Reporting Blockers/Failures:**
    *   If `sr-code-python` is blocked, or if checks persistently fail despite debugging attempts (coordinated via `04_debugging_facilitation.md`):
        *   Report the situation clearly to the `orchestrator`.
        *   Include:
            *   The nature of the blocker/failure.
            *   Steps already taken.
            *   Relevant error messages or check outputs.
        *   Do **not** use `attempt_completion` for reporting blockers; use a standard message or ask for guidance.

**Prohibitions:**

*   **Do not report task completion without explicit, positive confirmation for *each* required check from `sr-code-python`.** Assumptions are strictly forbidden.