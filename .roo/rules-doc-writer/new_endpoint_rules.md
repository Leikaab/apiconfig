# Documentation Writer Rules for New Endpoints

**Objective:** Update user-facing documentation after a new Tripletex API endpoint has been successfully added and committed.

**Core Workflow:**

1.  **Receive Context:** Await instructions and context from the orchestrator about the newly added endpoint (e.g., endpoint name/group, key features, usage examples if provided).
2.  **Identify Documentation:** Locate relevant user-facing documentation files that need updating (e.g., `README.md`, usage guides, examples).
3.  **Update Documentation:**
    *   Add information about the new endpoint.
    *   Include basic usage examples if possible.
    *   Ensure the documentation targets the end-user of the library.
4.  **Completion:** Report successful documentation updates using `attempt_completion`.

**Note:** Your focus is on the *user documentation* based on the *completed* endpoint, not the internal implementation process guides.