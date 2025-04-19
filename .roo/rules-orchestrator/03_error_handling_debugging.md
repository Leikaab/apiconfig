# Orchestrator Error Handling & Debugging Guidance

1.  **Failure Detection:**
    *   Identify failures when a subtask's final tool use results in an execution error.
    *   Identify failures when a subtask explicitly reports a 'FAIL' status.
    *   Identify failures when a subtask (especially `sr-code-python` or `test-runner-summarizer`) completes but does *not* confirm that all required checks passed.

2.  **Failure Analysis:**
    *   Analyze the failure report provided by the sub-mode. Look for specific error messages, tracebacks, or reasons for failed checks.

3.  **Debugging Delegation/Guidance:**
    *   **Provide Debugging Guidance (especially to `sr-code-python`):**
        *   Suggest checking project logs (configured via `tests/logging_config.py`).
        *   Suggest enabling debug logging in the `Client` if the issue seems related to API requests/responses (coordinate if necessary).
        *   Refer to specific Tripletex API notes (from `02_sr_code_python_guidance.md`) if potentially relevant to the error (e.g., pagination, nested fields).
        *   Point to relevant documentation, like `docs/create_new_endpoints/04_debugging_logs.md`.
    *   **Consider Delegating to Debug Mode:** If the issue is complex, consider delegating to a specialized debugging mode if available.

4.  **Resolution Path:**
    *   Based on the analysis and debugging attempts, decide the next step:
        *   Re-delegate the task to the same mode with corrections or additional guidance.
        *   Delegate a specific debugging task.
        *   If blocked, report the situation, the error, and steps taken to the user.

5.  **Verification After Fix:**
    *   If a fix is implemented, ensure the previously failed checks (or relevant new checks) are re-delegated to the `test-runner-summarizer` and confirmed passed before proceeding with the workflow.