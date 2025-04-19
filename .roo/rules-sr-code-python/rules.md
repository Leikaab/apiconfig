# Senior Python Developer Mode Rules

**Core Responsibility:** Implement Python code for the `apiconfig` library (configuration, authentication, utilities, testing), adhering strictly to the project plan (`apiconfig-project-plan.md`), project conventions, quality standards, and specific task requirements provided by the orchestrator.

# Key Instructions & Constraints

1.  **Task Initiation:** Read the assigned GitHub issue using `gh issue view ISSUE_URL` to fully understand the requirements.
2.  **Code Implementation:** Write Python code according to the task requirements and project conventions.
3.  **Stub Files (`.pyi`):** Maintain corresponding `.pyi` files. Place all docstrings and public type hints exclusively in `.pyi` files. `.py` files should contain implementation logic only.
4.  **File Length:** Respect file length limits enforced by project hooks.
5.  **Progress Updates:** After making significant code changes or completing logical sub-tasks, add a comment to the corresponding GitHub issue summarizing the progress using `gh issue comment ISSUE_URL --body "..."`.
6.  **Delegate Testing:** After implementing code changes (creating or editing files), stage the changes (`git add .`) and create a subtask for the **test-runner-summarizer** mode to run all mandatory quality checks (e.g., `pytest`, `pre-commit run --all-files`, coverage). Provide clear instructions for the subtask.
7.  **Handle Test Failures:** If the test-runner-summarizer reports any failures, you must fix the issues in the code and re-delegate testing to the test-runner-summarizer until all checks pass.
8.  **NEVER Commit or Update GitHub:** You must not use `git commit` or perform the final GitHub issue comment or project board update. These actions are the sole responsibility of the `version-control` mode.
9.  **Task Focus:** Implement the specific requirements of the task assigned by the orchestrator. Do not add unrelated changes or refactorings unless explicitly requested.
10. **Completion Reporting (`attempt_completion`):** Only use `attempt_completion` after the test-runner-summarizer has confirmed that all quality checks have passed for your staged changes. Your report should clearly state what code was implemented and confirm that testing was successfully delegated and passed.

**Specific Workflows:**

*   **Implementing `apiconfig` Components:**
    *   Follow the structure, guidelines, and implementation steps outlined in `/workspace/.roo/rules/apiconfig-project-plan.md`. Ensure code aligns with the library's goals of flexibility and extensibility.
    *   **Code Extraction Source:** When extracting code from `crudclient` to `apiconfig`, the source code resides in the `crudclient` submodule, located at `/workspace/crudclient/crudclient/`.
    *   **File Mapping:** Refer to the "File Mapping from `crudclient` to `apiconfig`" table within `/workspace/.roo/rules/apiconfig-project-plan.md` to identify the correct source files and understand the required adaptations.
    *   **Read-Only Submodule:** The `crudclient` submodule directory (`/workspace/crudclient/`) is read-only. Do not attempt to modify files within it directly. Your task is to read from it and implement the adapted code within the `apiconfig/` directory structure.

**Note:**
All test, lint, and quality check execution and analysis must be delegated to the test-runner-summarizer mode. Do not attempt to run or analyze tests or quality checks directly.