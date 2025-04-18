# Code Project Manager - Debugging Facilitation Guidance

When `sr-code-python` reports issues, blockers, or failed checks:

1.  **Gather Information:**
    *   Request detailed error messages, full tracebacks, and the specific check that failed from `sr-code-python`.
    *   Understand the context: What was `sr-code-python` trying to do? What were the inputs?

2.  **Relay to Orchestrator:**
    *   Report the issue accurately and completely to the `orchestrator`. Include all gathered information.

3.  **Pass Down Guidance:**
    *   Relay any specific debugging instructions or suggestions received from the `orchestrator` back to `sr-code-python`.

4.  **Suggest Initial Steps (If Orchestrator Guidance Pending):**
    *   Suggest concrete debugging steps `sr-code-python` can try:
        *   "Try adding logging statements using the project's logger (`import logging; logger = logging.getLogger(__name__)`) to trace the data flow."
        *   "Review the API quirks notes in `02_pattern_verification.md` – could this be related to pagination, nested fields, etc.?"
        *   "Double-check the parameters being sent against the Swagger definition (`specs/swagger.json`)."
        *   Refer `sr-code-python` to `docs/create_new_endpoints/04_debugging_logs.md`.

5.  **Coordinate Advanced Debugging:**
    *   If the `orchestrator` suggests enabling debug logging in the `Client`, relay this instruction.

6.  **Follow Up:**
    *   Track the debugging progress.
    *   Ensure fixes are followed by re-running **all** required checks (as per `03_quality_assurance.md`).