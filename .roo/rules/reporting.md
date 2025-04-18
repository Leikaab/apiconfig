### Hybrid Reporting Mechanism

This project utilizes a hybrid approach for reporting task completion status.

1.  **Secondary Action (Best Effort): Project Board Update**
    *   Before finalizing task completion, modes should *attempt* to update the status of the relevant item on the "APIConfig Implementation" project board (ID 1).
    *   Refer to `/workspace/.roo/rules/project_board.md` for conceptual examples of how to interact with the project board using `gh` commands.
    *   This update is considered a secondary action and is performed on a best-effort basis. Its success or failure does not block the primary reporting step.

2.  **Primary Action (Mandatory): `attempt_completion`**
    *   Regardless of the outcome of the project board update attempt, the mode **must** use the `attempt_completion` tool.
    *   This tool provides the definitive signal to the delegating mode or user about whether the assigned task was successfully completed or failed.
    *   The `result` parameter within `attempt_completion` should accurately reflect the final status of the task itself.