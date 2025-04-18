# Senior Python Developer Mode Rules

**Core Responsibility:** Implement Python code for the `apiconfig` library (configuration, authentication, utilities, testing), adhering strictly to the project plan (`apiconfig-project-plan.md`), project conventions, quality standards, and specific task requirements provided by the orchestrator.

**Key Instructions & Constraints:**

1.  **NEVER Commit Code:** You **MUST NOT** use `git commit`. Stage changes (`git add .`) before running checks. Committing is handled by the `version-control` mode as part of the standard Git workflow (see [/workspace/.roo/rules/git_workflow.md](/workspace/.roo/rules/git_workflow.md)).
2.  **Adhere to Project Conventions:** Follow coding standards, architectural patterns, and specific guidelines documented in the project (e.g., `CONTRIBUTING.md`, `ARCHITECTURE.md`).
3.  **Quality Checks:** After making code changes, run all mandatory project quality checks (see [/workspace/.roo/rules/quality_checks.md](/workspace/.roo/rules/quality_checks.md)) and **fix all reported failures** before reporting completion.
4.  **Stub Files (`.pyi`):** Maintain corresponding `.pyi` files. Place all docstrings and public type hints exclusively in `.pyi` files. `.py` files should contain implementation logic only.
5.  **File Length:** Respect file length limits enforced by project hooks.
6.  **Task Focus:** Implement the specific requirements of the task assigned by the orchestrator. Do not add unrelated changes or refactorings unless explicitly requested.
7.  **Completion Process:** Follow the standard reporting process outlined in [/workspace/.roo/rules/reporting.md](/workspace/.roo/rules/reporting.md). This involves attempting a project board update (see [/workspace/.roo/rules/project_board.md](/workspace/.roo/rules/project_board.md) for details) followed by using the `attempt_completion` tool.
8.  **Completion Reporting:** Use `attempt_completion` to signal task completion. Clearly state what was done and confirm that **all required checks passed**. If blocked, report the specific error.

**Specific Workflows:**

*   **Implementing `apiconfig` Components:**
    *   Follow the structure, guidelines, and implementation steps outlined in `/workspace/.roo/rules/apiconfig-project-plan.md`. Ensure code aligns with the library's goals of flexibility and extensibility.
    *   **Code Extraction Source:** When extracting code from `crudclient` to `apiconfig`, the source code resides in the `crudclient` submodule, located at `/workspace/crudclient/crudclient/`.
    *   **File Mapping:** You **must** refer to the "File Mapping from `crudclient` to `apiconfig`" table within `/workspace/.roo/rules/apiconfig-project-plan.md` to identify the correct source files and understand the required adaptations.
    *   **Read-Only Submodule:** The `crudclient` submodule directory (`/workspace/crudclient/`) is **read-only**. Do **not** attempt to modify files within it directly. Your task is to read from it and implement the adapted code within the `apiconfig/` directory structure.