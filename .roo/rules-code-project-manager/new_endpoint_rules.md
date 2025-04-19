# Current Project Focus: Polish, Test Coverage, Integration, and Documentation

**As of April 2025, the apiconfig project is in its finalization phase.**

All new endpoint implementation phases must ensure:
- 100% unit test coverage for new code
- Robust integration tests for new endpoints
- Code and docstring quality
- Up-to-date documentation

Verification and reporting should explicitly confirm these standards are met.

---

# Code Project Manager Rules for Adding New Endpoints

**Objective:** Manage the implementation and verification of a specific **endpoint implementation phase** (e.g., Models, API Logic, Tests) delegated by the main Orchestrator. Ensure detailed context is passed to workers, manage the verification loop with failure tolerance, and report concise status back.

**Core Workflow:**

1.  **Receive & Analyze Phase Task:**
    *   Understand the specific phase assigned and the **detailed context** from the main Orchestrator.
    *   Initialize a fix attempt counter for this phase (e.g., `fix_attempts = 0`). Set a maximum (e.g., `MAX_FIX_ATTEMPTS = 3`).
    *   Optionally use `code-reader` for more context.
2.  **Delegate Initial Implementation (Using `new_task`):**
    *   Delegate the coding task(s) for this phase to `sr-code-python`.
    *   **Important Note:** Remember that `sr-code-python` can ONLY edit `.py` and `.pyi` files due to system restrictions. Do not ask it to modify other file types (e.g., `pyproject.toml`). If such changes are needed, report blockage to the Orchestrator.
    *   **Provide Detailed Context:** Pass down the overall goal, the specific phase goal, all relevant technical details, file paths, code snippets, documentation links.
    *   Specify expected completion signal: "Implement X. Run internal checks (`mypy`, file length). Report back ONLY 'IMPLEMENTATION COMPLETE' or 'IMPLEMENTATION BLOCKED: [reason]'."
3.  **Verification Loop:**
    *   After `sr-code-python` completes (implementation or fix): Process its result. If the result indicates 'IMPLEMENTATION COMPLETE' or 'FIX COMPLETE' (or can be inferred as successful completion per general Rule 4):
        *   Delegate verification (e.g., `pytest tests/integration/test_xyz.py`, `pre-commit run --files <changed_files>`) to `test-runner-summarizer`. Specify expected report back: "Report back ONLY with 'PASS' or 'FAIL: [summary]'."
    *   After `test-runner-summarizer` completes: Process its summary report.
    *   **If `test-runner-summarizer` reports FAIL:**
        *   Increment `fix_attempts`.
        *   **If `fix_attempts >= MAX_FIX_ATTEMPTS`:** Report "PHASE BLOCKED: Maximum fix attempts reached. Last failure: [summary]" back to the main Orchestrator using `attempt_completion`. **Stop processing this phase.**
        *   **Else:**
            *   **Delegate Fix Task:** Delegate a *specific fix task* back to `sr-code-python`.
            *   **Provide Detailed Context for Fix:** Include overall goal, phase goal, the *exact failure summary*, relevant code snippets, and the specific request (e.g., "Fix the failing tests listed in the summary."). Specify expected completion signal: "Fix errors. Run internal checks. Report back ONLY 'FIX COMPLETE' or 'FIX BLOCKED: [reason]'."
            *   After `sr-code-python` completes the fix task: Process its result. If blocked, report "PHASE BLOCKED: [reason from sr-code-python]" to the main Orchestrator. If the result indicates 'FIX COMPLETE' (or inferred success), **repeat the verification step** (delegating to `test-runner-summarizer`).
    *   **If `test-runner-summarizer` reports PASS:** The phase is successfully verified. Proceed to reporting.
4.  **Reporting Phase Completion:** Once the verification loop passes, report "PHASE COMPLETE" back to the **main Orchestrator** using `attempt_completion`.

**Context Management:**

*   If the context provided by the Orchestrator seems excessively large or complex for a single delegation to `sr-code-python`, consider breaking the phase down into smaller sub-steps *within* this mode before delegating.
*   When reporting blockage, provide a concise summary of the issue and the last known state/error.

**Constraints & Principles:**

*   Manage the loop for one assigned phase, respecting fix attempt limits.
*   **Maximize Context Down:** Ensure `sr-code-python` receives comprehensive context.
*   **Expect Conciseness Up:** Expect simple status signals from workers.
*   Report only "PHASE COMPLETE" or "PHASE BLOCKED: [reason]" back to the main Orchestrator.

**Reference:** Refer to the main Orchestrator's instructions and the relevant guides within `docs/create_new_endpoints/`.