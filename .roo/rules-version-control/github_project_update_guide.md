## Simple Guide: Updating GitHub Project Board Item Status

This guide outlines the simplified, step-by-step process for updating the status of a project item linked to a GitHub issue using the `gh` CLI. This approach uses sequential commands and verifies IDs at each stage.

**Prerequisites:**

*   `gh` CLI installed and authenticated.
*   `jq` installed for parsing JSON output.
*   Know the **Issue URL** (e.g., `https://github.com/OWNER/REPO/issues/ISSUE_NUMBER`).
*   Know the **Project Number** (e.g., `1`).
*   Know the **Project Owner's Login** (e.g., `Leikaab`).
*   Know the **Target Status Name** (e.g., `Done`).

**Steps:**

1.  **Get the Project's Global ID:**
    *   This ID (starting with `PVT_`) is needed for the final `item-edit` command.
    *   Command:
        ```bash
        gh project list --owner <OWNER_LOGIN> --format json | jq -r --argjson projNum <PROJECT_NUMBER> '.projects[] | select(.number == $projNum) | .id'
        ```
    *   *Store this value (e.g., in a variable `PROJECT_ID`).*

2.  **Get the Project Item ID:**
    *   This links the specific issue to its representation on the project board.
    *   Use the **Project Number** here.
    *   Command:
        ```bash
        gh project item-list <PROJECT_NUMBER> --owner <OWNER_LOGIN> --format json | jq -r --arg url "<ISSUE_URL>" '.items[] | select(.content.url == $url) | .id'
        ```
    *   *Store this value (e.g., in a variable `ITEM_ID`).*

3.  **Get the 'Status' Field ID:**
    *   Finds the specific ID for the "Status" column/field on the board.
    *   Use the **Project Number** here.
    *   Command:
        ```bash
        gh project field-list <PROJECT_NUMBER> --owner <OWNER_LOGIN> --format json | jq -r '.fields[] | select(.name == "Status") | .id'
        ```
    *   *Store this value (e.g., in a variable `STATUS_FIELD_ID`).*

4.  **Get the Target Status Option ID:**
    *   Finds the ID for the specific status value (e.g., "Done") within the "Status" field.
    *   Use the **Project Number** and the **Status Field ID** obtained above.
    *   Command:
        ```bash
        gh project field-list <PROJECT_NUMBER> --owner <OWNER_LOGIN> --format json | jq -r --arg field_id "<STATUS_FIELD_ID>" --arg status_name "<TARGET_STATUS_NAME>" '.fields[] | select(.id == $field_id) | .options[] | select(.name == $status_name) | .id'
        ```
    *   *Store this value (e.g., in a variable `TARGET_OPTION_ID`).*

5.  **Update the Item Status:**
    *   Uses all the gathered IDs to perform the final update.
    *   Requires the **Global Project ID** (from Step 1).
    *   Command:
        ```bash
        gh project item-edit --id "<ITEM_ID>" --project-id "<PROJECT_ID>" --field-id "<STATUS_FIELD_ID>" --single-select-option-id "<TARGET_OPTION_ID>"
        ```

This step-by-step approach, verifying each ID along the way, should be more robust. I will use this simpler method going forward.