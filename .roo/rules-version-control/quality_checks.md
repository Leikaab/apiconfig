### Quality Checks

Running and passing all quality checks is mandatory before committing code or reporting task completion. All test, lint, and quality check execution and analysis must be delegated to the `test-runner-summarizer` mode. This mode is responsible for executing commands such as:

1.  **Running Tests:** The test-runner-summarizer executes the test suite using `pytest`.
    ```bash
    pytest
    ```
2.  **Running Linters/Formatters:** The test-runner-summarizer executes pre-commit hooks against all files.
    ```bash
    pre-commit run --all-files
    ```

Any failures reported by the test-runner-summarizer **must** be fixed, and the checks must be re-delegated and re-run until they pass successfully. Do not attempt to run or analyze tests or quality checks directly.