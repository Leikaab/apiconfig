### Task Reporting and GitHub Workflow

This project mandates specific GitHub interactions integrated with the task completion reporting process. All steps involving GitHub interaction are **mandatory**.

1.  **Task Initiation:**
    *   When assigned a task linked to a GitHub issue (identified by its URL or number), the mode **must** first retrieve and understand the issue's content. Use `gh issue view ISSUE_URL` or `gh issue view ISSUE_NUMBER`.

2.  **Progress Updates:**
    *   After making significant code changes or completing logical sub-tasks, the mode **must** add a comment to the corresponding GitHub issue summarizing the progress. Use `gh issue comment ISSUE_URL --body "Detailed summary of changes made..."`.

3.  **Task Completion & GitHub Updates:**
    *   **Before** using `attempt_completion`, the mode **must** perform the following GitHub updates:
        *   **Add a final comment** to the issue summarizing the completed work, referencing any relevant commits or Pull Requests. Use `gh issue comment ISSUE_URL --body "Task completed. Summary: ..."`.
        *   **Update the project board item status** to 'Done' (or equivalent). This involves identifying the item ID, status field ID, and 'Done' option ID using `gh` commands as detailed in `/workspace/.roo/rules/project_board.md`.
    *   Failure to successfully complete these GitHub updates means the task itself is not complete.

4.  **Final Reporting (`attempt_completion`):**
    *   Only after successfully updating the GitHub issue and project board, the mode **must** use the `attempt_completion` tool.
    *   The `result` parameter within `attempt_completion` must accurately reflect the task's completion and explicitly state that the corresponding GitHub issue and project board item have been updated accordingly.