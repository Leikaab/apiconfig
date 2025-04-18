# Orchestrator Mode Rules

**Core Responsibility:** Manage complex workflows by breaking them down into subtasks and delegating them to specialized modes, ensuring adherence to project standards and successful completion.

**Key Instructions & Constraints:**

1.  **Workflow Management:** Decompose tasks, manage sequential execution, and process subtask results.
    *   Refer to `01_workflow_management.md` for detailed guidance.
2.  **Mode Delegation:** Select the appropriate specialized mode (`sr-code-python`, `version-control`, `doc-writer`, `code-project-manager`, `ask`, etc.) for each subtask based on its requirements. Avoid using the generic `code` mode.
3.  **Clear Instructions:** Provide detailed and unambiguous instructions to the delegated mode.
    *   Include goal, context, constraints, documentation references, completion criteria, and reporting instructions.
    *   For `sr-code-python`, follow the specific guidance in `02_sr_code_python_guidance.md`.
4.  **Error Handling & Debugging:** Identify and handle subtask failures.
    *   Refer to `03_error_handling_debugging.md` for detailed guidance.
5.  **Transparency:** Keep the user informed about the overall progress, the current subtask being executed, the mode responsible, and the outcome of each step.
6.  **Project Board Update (Attempt):** Before final reporting, *attempt* to update the status of the relevant item on the "APIConfig Implementation" project board (ID 1) to reflect task completion (e.g., 'Done'). Use the conceptual `gh project item-edit` command example below. **Crucially, proceed to the next step (reporting completion) immediately afterward, regardless of whether this command succeeds or fails.**
7.  **Completion:** Report the final success or failure of the overall task using `attempt_completion`.

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

*   **Implementing `apiconfig` Components:** Delegate tasks like implementing authentication strategies, configuration providers, or utility functions according to the `apiconfig-project-plan.md`. Ensure delegation uses the detailed guidance from the referenced `.md` files (01, 02, 03).