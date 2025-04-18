# Contributing as a Senior Python Code Generator

This document provides a concise summary of contribution guidelines specifically for the **Senior Python Code Generator** (`sr-code-python`) role within this project. For comprehensive details, please refer to the main [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).

## Workflow Context

*   The project follows the standard Git workflow. See [/workspace/.roo/rules/git_workflow.md](/workspace/.roo/rules/git_workflow.md) for details on branching, commit messages, and Pull Requests.
*   All code implementation must occur on `feature/*` branches and target the `develop` branch via Pull Requests (PRs).

## Coding Standards

Adherence to the project's coding standards is mandatory:

*   **Formatting, Linting, Type Checking:** Code must pass all checks defined in [/workspace/.roo/rules/quality_checks.md](/workspace/.roo/rules/quality_checks.md).
*   **Docstrings:** Clear and informative docstrings are required for all modules, classes, functions, and methods.

## Testing

*   Comprehensive **unit tests** using `pytest` are required for all new or modified code. Place unit tests in the `tests/unit/` directory.
*   **Integration tests** should be added in `tests/integration/` where applicable to test interactions between components.

## Quality Checks

*   Pre-commit hooks and Continuous Integration (CI) checks are configured to automatically enforce standards.
*   Contributions **must pass** all quality checks before they can be merged. See [/workspace/.roo/rules/quality_checks.md](/workspace/.roo/rules/quality_checks.md) for details.

## Full Guidelines

For the complete contribution process, including detailed coding standards, testing procedures, Gitflow workflow, commit message format, and review procedures, please consult the main project [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).