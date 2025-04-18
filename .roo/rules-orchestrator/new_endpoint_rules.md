# Orchestrator Rules for Adding New Endpoints

**Objective:** Manage the end-to-end process of adding a new Tripletex API endpoint by breaking it into logical phases, delegating each phase to the `code-project-manager`, sequencing tasks, and ensuring detailed context is passed down.

**Core Workflow & Delegation:**

1.  **Primary Guide:** The overall process is documented starting at `docs/create_new_endpoints/00_overview.md`. Understand this workflow.
2.  **Initial Context Gathering (Optional):** If necessary details (e.g., endpoint structure from Swagger, related existing code, potential dependency needs) are missing, delegate to `code-reader` to analyze relevant files. Gather comprehensive context for the overall task.
3.  **Decomposition into Phases:** Break the high-level task ("Add endpoint X") into logical implementation phases (e.g., Models, API Logic, Stubs, Tests, Registration) based on `docs/create_new_endpoints/03_implementation_steps_overview.md`.
4.  **Phase Execution (Iterate through phases):**
    *   **Assess Need for DevOps:** Before delegating a phase, consider if it might require changes to files restricted from `sr-code-python` (e.g., adding a new dependency in `pyproject.toml`).
    *   **If DevOps Change Needed:** Use `ask_followup_question` to confirm with the user if proceeding with a change via `devops-specialist` is desired *before* delegating the phase. If approved, delegate the specific DevOps task (e.g., "Add library X using poetry") to `devops-specialist`. Await its completion before proceeding with the main phase delegation.
    *   **Delegate Phase to `code-project-manager`:** For **each phase**, delegate the task to `code-project-manager`.
    *   **Provide Detailed Context:** When delegating, provide:
        *   The original high-level goal (e.g., "Add endpoint X").
        *   The specific goal for *this phase* (e.g., "Implement Pydantic models for endpoint X").
        *   All relevant gathered context (Swagger details, related file paths/summaries from `code-reader`, relevant documentation links like `docs/create_new_endpoints/03b_data_models.md`).
        *   Clear expectation: "Manage the implementation and verification for this phase, reporting back only 'PHASE COMPLETE' upon success."
    *   Await `code-project-manager`'s report of successful phase completion. Handle any reported errors or blocks by potentially gathering more info or asking the user.
5.  **Final Commit:** After all implementation phases are successfully completed:
    *   Delegate final checks (`pytest`, `pre-commit run --all-files`) AND commit action to `version-control`. Provide the final commit message (e.g., "feat: Add endpoint X") and relevant context. Await confirmation of successful commit or failure summary.
6.  **Documentation (Optional):** After successful commit, delegate documentation updates to `doc-writer` if needed, providing context about the new endpoint.
7.  **Transparency:** Report the current overall step, phase being delegated/completed, and outcomes to the user.
8.  **Completion:** Report overall success via `attempt_completion` once the endpoint is implemented, tested, committed, and documented (if applicable).

**Delegation Principles:**

*   Use `new_task` for delegation.
*   **Maximize Context Down:** Pass comprehensive context (overall goal, phase goal, technical details, file paths, history if relevant) to sub-modes.
*   **Expect Conciseness Up:** Expect concise status reports (e.g., "PHASE COMPLETE", "COMMIT SUCCESSFUL", "TESTS FAILED: [summary]") from sub-modes.
*   Frame instructions clearly, specifying the exact task and expected report-back signal.

**Reference:** Refer to the specific guides within `docs/create_new_endpoints/` for details on each step.