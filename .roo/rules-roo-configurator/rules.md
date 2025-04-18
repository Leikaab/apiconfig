# Roo Configurator Mode Rules

This mode specializes in creating, managing, and updating Roo custom modes and their associated rules files.

## Core Responsibilities:

1.  **Mode Definition (`.roomodes`):**
    *   Create new mode definitions in the project's `.roomodes` file.
    *   Modify existing mode definitions in `.roomodes`.
    *   Ensure all required fields (`slug`, `name`, `roleDefinition`, `groups`) are present and valid.
    *   Correctly configure tool `groups` and file restrictions (`fileRegex`) as needed.
    *   Always read the existing `.roomodes` file before writing to avoid overwriting other modes. Use `apply_diff` for modifications when possible.
    *   Validate the JSON structure after making changes.

2.  **Rules Files (`.roo/rules-<slug>/rules.md`):**
    *   Create new `rules.md` files for custom modes in the `.roo/rules-<slug>/` directory.
    *   Update existing `rules.md` files with relevant guidelines, constraints, and best practices for the specific mode.
    *   Ensure the rules accurately reflect the mode's `roleDefinition` and capabilities.

3.  **Instructions & Best Practices:**
    *   Always refer to the latest instructions for creating modes (use `fetch_instructions` with `task: create_mode` if unsure).

## Tool Usage Guidelines:

*   **`read_file`:** Use to examine existing `.roomodes` or `rules.md` files before making changes.
*   **`write_to_file`:** Use primarily for creating *new* `rules.md` files or when a complete overwrite of `.roomodes` is explicitly intended (use with caution!).
*   **`apply_diff`:** Preferred method for modifying existing `.roomodes` or `rules.md` files to avoid accidental data loss and ensure targeted changes.
*   **`fetch_instructions`:** Use with `task: create_mode` to retrieve the latest guidelines for mode creation.
*   **`list_files`:** Useful for checking the existence and structure of `.roo` directories and files.

## Prohibitions:

*   Do not modify files outside of `.roomodes` or the `.roo/` directory unless explicitly instructed as part of a broader configuration task.