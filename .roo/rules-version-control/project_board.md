### Project Board Interaction (Mandatory)

Updating the "APIConfig Implementation" project board (ID: 1, Owner: `Leikaab`) is a **mandatory** step before completing a task, as outlined in `/workspace/.roo/rules/reporting.md`. Modes **must** use `gh` commands to autonomously manage project items.

**Workflow:**

1.  **Identify Issue URL:** Determine the URL of the GitHub issue associated with the current task.

2.  **Find Project Item ID:** Use `gh` and `jq` to find the project item ID linked to the issue URL.
    ```bash
    # Replace ISSUE_URL with the actual issue link
    ITEM_ID=$(gh project item-list 1 --owner Leikaab --format json | jq -r --arg url "$ISSUE_URL" '.items[] | select(.content.url == $url) | .id')
    # Handle cases where the item might not be found
    if [ -z "$ITEM_ID" ]; then echo "Error: Project item not found for $ISSUE_URL"; exit 1; fi
    ```

3.  **Find 'Status' Field ID:** Dynamically determine the ID of the 'Status' field on the project board.
    ```bash
    STATUS_FIELD_ID=$(gh project field-list 1 --owner Leikaab --format json | jq -r '.fields[] | select(.name == "Status") | .id')
    if [ -z "$STATUS_FIELD_ID" ]; then echo "Error: 'Status' field not found on project board"; exit 1; fi
    ```

4.  **Find Target Status Option ID (e.g., 'Done'):** Dynamically determine the ID for the desired status option (e.g., "Done") within the 'Status' field.
    ```bash
    # Replace "Done" with the target status name if different
    TARGET_STATUS_NAME="Done"
    TARGET_OPTION_ID=$(gh project field-list 1 --owner Leikaab --format json | jq -r --arg field_id "$STATUS_FIELD_ID" --arg status_name "$TARGET_STATUS_NAME" '.fields[] | select(.id == $field_id) | .options[] | select(.name == $status_name) | .id')
    if [ -z "$TARGET_OPTION_ID" ]; then echo "Error: '$TARGET_STATUS_NAME' option not found for 'Status' field"; exit 1; fi
    ```
    *Note: The exact `jq` query might need adjustment based on the output structure of `gh project field-list`.*

5.  **Update Item Status:** Use the obtained IDs to update the project item's status.
    ```bash
    gh project item-edit --id "$ITEM_ID" --project-id 1 --owner Leikaab --field-id "$STATUS_FIELD_ID" --single-select-option-id "$TARGET_OPTION_ID"
    ```

**Self-Sufficiency:** Modes **must not** ask the user for `ITEM_ID`, `FIELD_ID`, or `OPTION_ID`. These values **must** be determined programmatically using `gh` commands as shown above. Error handling should be included to manage cases where IDs cannot be found.