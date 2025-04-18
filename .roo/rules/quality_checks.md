### Quality Checks

Running and passing all quality checks is mandatory before committing code or reporting task completion. This typically involves:

1.  **Running Tests:** Execute the test suite using `pytest`.
    ```bash
    pytest
    ```
2.  **Running Linters/Formatters:** Execute pre-commit hooks against all files.
    ```bash
    pre-commit run --all-files
    ```

Any failures reported by these checks **must** be fixed, and the checks must be re-run until they pass successfully.