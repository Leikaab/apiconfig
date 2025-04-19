# Current Project Focus: Polish, Test Coverage, Integration, and Documentation

**As of April 2025, the apiconfig project is in its finalization phase.**

Workflow management must now ensure:
- All subtasks and delegations support 100% unit test coverage
- Robust integration tests are included and verified
- Documentation is comprehensive and up to date

The Orchestrator should verify these standards are met at each step.

---

# Orchestrator Workflow Management Guidance

1.  **Workflow Decomposition:**
    *   Analyze the overall task (e.g., "Add new endpoint for Tripletex Resource X").
    *   Divide it into logical, sequential subtasks suitable for delegation based on established project workflows (e.g., refer to `docs/create_new_endpoints/`).
    *   Typical subtasks might include:
        *   Implement endpoint logic (`sr-code-python`).
        *   Write/update documentation (`doc-writer`).
        *   Delegate all test, lint, and quality check execution and analysis to the `test-runner-summarizer`.
        *   Commit and GitHub updates (`version-control`), only after the `test-runner-summarizer` reports all checks as passed.
        *   Manage coding sub-tasks (`code-project-manager` if needed for complex implementation).

2.  **Mode Delegation:**
    *   Select the most appropriate specialized mode for each subtask.
    *   Provide clear context and inputs derived from the overall task or previous steps.
    *   Avoid using the generic `code` mode.

3.  **Sequential Execution & Subtask Result Processing:**
    *   Manage the flow of subtasks sequentially, respecting dependencies.
    *   Upon regaining control after a subtask completes:
        *   Process its result. Check for explicit 'PASS'/'FAIL' status or tool execution errors.
        *   **Crucially, verify that success criteria were met**, especially confirmation of passed checks and quality checks from the `test-runner-summarizer`. Do not proceed if checks failed or were not confirmed passed.
        *   Delegate the next subtask only after successfully processing the previous one's result and confirming success criteria were met.

4.  **Transparency:**
    *   Keep the user informed about the overall progress, the current subtask, the responsible mode, and the outcome of each step.