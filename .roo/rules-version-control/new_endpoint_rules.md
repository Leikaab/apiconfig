# Version Control Rules for Adding New Endpoints

**Objective:** Perform final safeguard verification checks and commit the implemented code for a new Tripletex API endpoint, as instructed by the orchestrator.

**Core Workflow:**

1.  **Receive Handoff for Commit:** Await instructions from the orchestrator to perform the final checks and commit. This instruction implies that prior implementation and verification steps (potentially involving `sr-code-python` and `test-runner-summarizer`) have already been completed successfully. You will be provided with the commit message.
2.  **Mandatory Final Safeguard Checks:** Execute the following checks in order, even if they were run previously:
    *   `pytest` (Run the full test suite)
    *   `pre-commit run --all-files` (Run all hooks)
3.  **Analyze Results:**
    *   **If ALL checks pass:**
        *   Stage all changes: `git add .` (Ensures any hook modifications are included).
        *   Commit using the exact message provided by the orchestrator: `git commit -m "<commit_message>"`
        *   Report **successful commit** using `attempt_completion`.
    *   **If ANY check fails:**
        *   **STOP.** **DO NOT COMMIT.**
        *   Report **failure** using `attempt_completion`. Include a summary of the errors (failed tests/hooks). Mention test logs location (`/workspace/tests/logs/`). The orchestrator will handle delegating fixes.

**Reference:** This final check-and-commit step is part of the overall workflow detailed starting at `docs/create_new_endpoints/00_overview.md` and specifically mentioned in `docs/create_new_endpoints/03h_verification_commit.md`.