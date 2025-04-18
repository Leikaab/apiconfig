# Orchestrator Mode Rules

**Core Responsibility:** Manage complex workflows by breaking them down into subtasks and delegating them to specialized modes, ensuring adherence to project standards and successful completion.

**Key Instructions & Constraints:**

1.  **Workflow Management:** Decompose tasks, manage sequential execution, and process subtask results.
    *   Refer to `01_workflow_management.md` for detailed guidance.
2.  **Mode Delegation:** Select the appropriate specialized mode (`sr-code-python`, `version-control`, `doc-writer`, `code-project-manager`, `ask`, etc.) for each subtask based on its requirements. Avoid using the generic `code` mode.
3.  **Clear Instructions:** Provide detailed and unambiguous instructions to the delegated mode.
    *   Include goal, context, constraints, documentation references, and completion criteria.
    *   **Crucially, instructions MUST explicitly state the mandatory reporting requirements:** Delegated modes **must** follow the GitHub workflow outlined in [/workspace/.roo/rules/reporting.md](/workspace/.roo/rules/reporting.md) and [/workspace/.roo/rules/project_board.md](/workspace/.roo/rules/project_board.md), including adding issue comments and updating the project board *before* using `attempt_completion`.
    *   For `sr-code-python`, follow the specific guidance in `02_sr_code_python_guidance.md`.
4.  **Verification of Subtask Completion:** Before considering a delegated subtask complete, **verify** that the delegated mode's `attempt_completion` result explicitly confirms that the mandatory GitHub issue comments and project board updates were successfully performed. If confirmation is missing or the subtask failed, treat it as a failure and proceed with error handling.
5.  **Error Handling & Debugging:** Identify and handle subtask failures, including failures related to GitHub updates.
    *   Refer to `03_error_handling_debugging.md` for detailed guidance.
6.  **Transparency:** Keep the user informed about the overall progress, the current subtask being executed, the mode responsible, the outcome of each step, and the verification status of GitHub updates.
7.  **Orchestrator Completion Process:** Follow the **mandatory** reporting process outlined in [/workspace/.roo/rules/reporting.md](/workspace/.roo/rules/reporting.md) for the *overall* task assigned to the orchestrator. This requires:
    *   Ensuring all subtasks, including their mandatory GitHub updates, have been successfully completed and verified.
    *   Adding a final comment to the main GitHub issue summarizing the overall work.
    *   Updating the main project board item status to 'Done' (or equivalent), using `gh` commands autonomously as detailed in [/workspace/.roo/rules/project_board.md](/workspace/.roo/rules/project_board.md).
    *   Only then, using the `attempt_completion` tool for the overall task.
8.  **Overall Task Completion (`attempt_completion`):** **Only** use `attempt_completion` **after** successfully completing and verifying all subtasks and performing the mandatory GitHub updates for the overall task (as outlined in point 7). Report the final success or failure of the overall task, confirming that all necessary GitHub updates (for subtasks and the main task) were completed.
9.  **`crudclient` Submodule Awareness:** When delegating tasks related to extracting code for `apiconfig`, be aware that the source code resides in the read-only `crudclient` submodule (`/workspace/crudclient/`). Ensure delegated modes (like `sr-code-python`) are instructed to consult the file mapping in `/workspace/.roo/rules/apiconfig-project-plan.md` and implement the *adapted* code within the `apiconfig/` directory, not modify the submodule itself.

**Specific Workflows:**

*   **Implementing `apiconfig` Components:** Delegate tasks like implementing authentication strategies, configuration providers, or utility functions according to the `apiconfig-project-plan.md`. Ensure delegation uses the detailed guidance from the referenced `.md` files (01, 02, 03) and includes reminders about the `crudclient` submodule context (see point 8 above).