# Current Project Focus: Polish, Test Coverage, Integration, and Documentation

**As of April 2025, the apiconfig project is in its finalization phase.**

Reporting must now ensure:
- 100% unit test coverage is achieved and maintained
- Robust integration tests are in place and passing
- Code and docstring quality is confirmed
- Documentation is up to date

Completion reports should explicitly confirm these standards are met, in addition to all required checks passing.

---

# Code Project Manager - Reporting Guidance

Accurate and timely reporting to the `orchestrator` is crucial.

1.  **Prerequisites for Completion Report:**
    *   Do **not** report task completion to the `orchestrator` until **both** of the following are true:
        *   `sr-code-python` has confirmed the implementation is complete according to the requirements.
        *   You have received explicit confirmation from `sr-code-python` that the `test-runner-summarizer` reported **all** required checks passed successfully (as detailed in `03_quality_assurance.md`). Do not rely on `sr-code-python`'s own analysis of check results.

2.  **Reporting Success:**
    *   Use `attempt_completion` to signal task success to the `orchestrator`.
    *   The report **must** explicitly state that all required checks passed as reported by the `test-runner-summarizer`. Example: "Task complete. `sr-code-python` finished implementation and the `test-runner-summarizer` confirmed all checks (mypy, pre-commit, unit tests, integration tests) passed."

3.  **Reporting Blockers/Failures:**
    *   If `sr-code-python` is blocked, or if checks persistently fail despite debugging attempts (coordinated via `04_debugging_facilitation.md`):
        *   Report the situation clearly to the `orchestrator`.
        *   Include:
            *   The nature of the blocker/failure.
            *   Steps already taken.
            *   Relevant error messages or check outputs.
        *   Do **not** use `attempt_completion` for reporting blockers; use a standard message or ask for guidance.

**Prohibitions:**

*   **Do not report task completion without explicit, positive confirmation for *each* required check from the `test-runner-summarizer` (via `sr-code-python`).** Assumptions are strictly forbidden.