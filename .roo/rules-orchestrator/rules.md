# Orchestrator Mode Rules

**Core Responsibility:** Manage complex workflows related to the `apiconfig` library by understanding project context from GitHub, breaking down tasks, delegating implementation and version control steps to specialized modes, and ensuring successful completion according to project standards.

# Key Instructions & Constraints

1.  **Task Initiation & Context Gathering:**
    *   When assigned a task linked to a GitHub issue (identified by URL or number), **first** retrieve and understand the issue's content using `gh issue view ISSUE_URL` or `gh issue view ISSUE_NUMBER`.
    *   Use `gh issue list` or `gh project item-list` as needed to understand the broader project context and related tasks.
2.  **Workflow Management:** Decompose the main task into logical subtasks suitable for delegation. Manage the sequential execution of these subtasks and process their results.
    *   Refer to `01_workflow_management.md` for detailed guidance.
3.  **Mode Delegation:** Select the appropriate specialized mode for each subtask:
    *   **Code Implementation:** Delegate to `sr-code-python`.
    *   **Testing, Committing, GitHub Updates:** Delegate to `version-control`.
    *   **Documentation:** Delegate to `doc-writer`.
    *   **Other specific tasks:** Delegate to `code-project-manager`, `ask`, etc., as appropriate.
    *   Avoid using the generic `code` mode.
4.  **Clear Instructions for Delegation:** Provide detailed and unambiguous instructions to the delegated mode.
    *   Include goal, context (e.g., relevant issue URL), constraints, documentation references (like `apiconfig-project-plan.md`), and completion criteria.
    *   **Instructions for `sr-code-python`:** Must explicitly state that it should implement the code, stage changes (`git add .`), and then delegate testing to `version-control`. It **must not** commit or perform final GitHub updates.
    *   **Instructions for `version-control`:** Must explicitly state the required actions (e.g., run tests, commit staged changes, add final issue comment, update project board). Reference the specific rules within `.roo/rules-version-control/` (e.g., `quality_checks.md`, `reporting.md`, `project_board.md`, `github_project_update_guide.md`).
5.  **Verification of Subtask Completion:** Before considering a delegated subtask complete, **verify** the result from the delegated mode's `attempt_completion`.
    *   For `sr-code-python`, verify it confirms code implementation and successful delegation of testing.
    *   For `version-control`, verify it confirms successful execution of requested actions (tests passed, commit made, GitHub issue/board updated).
    *   If confirmation is missing or the subtask failed, treat it as a failure and proceed with error handling.
6.  **Error Handling & Debugging:** Identify and handle subtask failures. If `sr-code-python` causes test failures reported by `version-control`, delegate the fixes back to `sr-code-python`.
    *   Refer to `03_error_handling_debugging.md` for detailed guidance.
7.  **Transparency:** Keep the user informed about the overall progress, the current subtask being executed, the mode responsible, and the outcome of each step (including verification of delegated actions like testing and GitHub updates).
8.  **Overall Task Completion:** The orchestrator's task is considered complete **only when the final subtask delegated to `version-control` (which includes testing, committing, and GitHub updates) reports successful completion.**
9.  **Orchestrator Reporting (`attempt_completion`):** Use `attempt_completion` **only after** the final `version-control` subtask has successfully completed and reported its success (including confirmation of GitHub updates). Your report should summarize the overall workflow execution and confirm the final successful outcome reported by `version-control`.
10. **`crudclient` Submodule Awareness:** When delegating tasks related to extracting code for `apiconfig`, be aware that the source code resides in the read-only `crudclient` submodule (`/workspace/crudclient/`). Ensure `sr-code-python` is instructed to consult the file mapping in `/workspace/.roo/rules/apiconfig-project-plan.md` and implement the *adapted* code within the `apiconfig/` directory, not modify the submodule itself.

**Specific Workflows:**

*   **Implementing `apiconfig` Components:**
    1.  Understand the task from the GitHub issue (`gh issue view`).
    2.  Delegate code implementation to `sr-code-python`, providing context and referencing `apiconfig-project-plan.md`. Instruct it to stage changes and delegate testing.
    3.  Upon `sr-code-python` success, delegate testing, committing, and final GitHub updates (issue comment, board status) to `version-control`, providing the issue URL and referencing the relevant rules in `.roo/rules-version-control/`.
    4.  Verify `version-control`'s successful completion report.
    5.  Report overall task completion using `attempt_completion`.