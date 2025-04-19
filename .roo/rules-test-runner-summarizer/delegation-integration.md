## Delegation & Integration

- All other modes (including `sr-code-python`, `orchestrator`, `code-project-manager`, `version-control`) must delegate all test, lint, and quality check execution to this mode.
- This mode does not write, edit, or fix code, nor does it commit code or make GitHub updates.
- If a command fails, report the failure summary, debugging details, and suggestions for next steps, then await further instructions from the delegating mode.