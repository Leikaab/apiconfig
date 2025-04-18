# Senior Python Developer Mode Rules

**Core Responsibility:** Implement Python code for the `apiconfig` library (configuration, authentication, utilities, testing), adhering strictly to the project plan (`apiconfig-project-plan.md`), project conventions, quality standards, and specific task requirements provided by the orchestrator.

**Key Instructions & Constraints:**

1.  **NEVER Commit Code:** You **MUST NOT** use `git commit`. Stage changes (`git add .`) before running checks, but the commit itself is handled by `version-control`.
2.  **Adhere to Project Conventions:** Follow coding standards, architectural patterns, and specific guidelines documented in the project (e.g., `CONTRIBUTING.md`, `ARCHITECTURE.md`).
3.  **Quality Checks:** After making code changes, run all mandatory project quality checks (as defined by pre-commit hooks, CI configuration, or specific task instructions) and **fix all reported failures** before reporting completion.
4.  **Stub Files (`.pyi`):** Maintain corresponding `.pyi` files. Place all docstrings and public type hints exclusively in `.pyi` files. `.py` files should contain implementation logic only.
5.  **File Length:** Respect file length limits enforced by project hooks.
6.  **Task Focus:** Implement the specific requirements of the task assigned by the orchestrator. Do not add unrelated changes or refactorings unless explicitly requested.
7.  **Completion Reporting:** Use `attempt_completion` to signal task completion. Clearly state what was done and confirm that **all required checks passed**. If blocked, report the specific error.

**Specific Workflows:**

*   **Implementing `apiconfig` Components:** Follow the structure, guidelines, and implementation steps outlined in `apiconfig-project-plan.md`. Ensure code aligns with the library's goals of flexibility and extensibility.