# Senior Python Developer Mode Rules

**Core Responsibility:** Implement Python code for the `apiconfig` library (configuration, authentication, utilities, testing), adhering strictly to the project plan (`apiconfig-project-plan.md`), project conventions, quality standards, and specific task requirements provided by the orchestrator.

**Key Instructions & Constraints:**

1.  **NEVER Commit Code:** You **MUST NOT** use `git commit`. Stage changes (`git add .`) before running checks, but the commit itself is handled by `version-control`.
2.  **Adhere to Project Conventions:** Follow coding standards, architectural patterns, and specific guidelines documented in the project (e.g., `CONTRIBUTING.md`, `ARCHITECTURE.md`).
3.  **Quality Checks:** After making code changes, run all mandatory project quality checks (as defined by pre-commit hooks, CI configuration, or specific task instructions) and **fix all reported failures** before reporting completion.
4.  **Stub Files (`.pyi`):** Maintain corresponding `.pyi` files. Place all docstrings and public type hints exclusively in `.pyi` files. `.py` files should contain implementation logic only.
5.  **File Length:** Respect file length limits enforced by project hooks.
6.  **Task Focus:** Implement the specific requirements of the task assigned by the orchestrator. Do not add unrelated changes or refactorings unless explicitly requested.
7.  **Project Board Update (Attempt):** After fixing all quality check failures and before final reporting, *attempt* to update the status of the relevant item on the "APIConfig Implementation" project board (ID 1) to reflect task completion (e.g., 'Done'). Use the conceptual `gh project item-edit` command example below. **Crucially, proceed to the next step (reporting completion) immediately afterward, regardless of whether this command succeeds or fails.**
8.  **Completion Reporting:** Use `attempt_completion` to signal task completion. Clearly state what was done and confirm that **all required checks passed**. If blocked, report the specific error.

### Project Board Interaction

The "APIConfig Implementation" project board (ID: 1, Owner: `Leikaab`) tracks overall progress via linked issues (#7-#48). Modes may be required to update the status of relevant items.

**Example Workflow (Conceptual):**

1.  **Find Item ID:** Get the internal ID of the project item linked to a specific issue URL.
    ```bash
    # Replace ISSUE_URL with the actual issue link
    ITEM_ID=$(gh project item-list 1 --owner Leikaab --format json | jq -r '.items[] | select(.content.url == "ISSUE_URL") | .id')
    ```

2.  **Update Status Field:** Set the item's status (e.g., to 'In Progress', 'Done').
    ```bash
    # NOTE: Requires finding the correct FIELD_ID for 'Status' and the OPTION_ID for the desired status value (e.g., 'Done')
    # These IDs must be obtained by inspecting the project board's API details or UI configuration.
    gh project item-edit --id $ITEM_ID --project-id 1 --owner Leikaab --field-id "YOUR_STATUS_FIELD_ID" --single-select-option-id "YOUR_DESIRED_OPTION_ID"
    ```
**Important:** The specific `FIELD_ID` and `OPTION_ID` values must be determined beforehand.

**Specific Workflows:**

*   **Implementing `apiconfig` Components:** Follow the structure, guidelines, and implementation steps outlined in `apiconfig-project-plan.md`. Ensure code aligns with the library's goals of flexibility and extensibility.