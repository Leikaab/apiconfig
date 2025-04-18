# Contributing as a Senior Python Code Generator

This document provides a concise summary of contribution guidelines specifically for the **Senior Python Code Generator** (`sr-code-python`) role within this project. For comprehensive details, please refer to the main [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).

## Workflow Context

*   The project follows the **Gitflow** branching model.
*   All code implementation must occur on `feature/*` branches created from the `develop` branch.
*   Pull Requests (PRs) containing new features or fixes should target the `develop` branch for review and merging.

## Coding Standards

Adherence to the project's coding standards is mandatory:

*   **Formatting:** Code must be formatted using **Black** and **isort**.
*   **Linting:** Code must pass **Flake8** checks.
*   **Type Checking:** Strict type hints are required and checked using **Mypy**.
*   **Docstrings:** Clear and informative docstrings are required for all modules, classes, functions, and methods.

## Testing

*   Comprehensive **unit tests** using `pytest` are required for all new or modified code. Place unit tests in the `tests/unit/` directory.
*   **Integration tests** should be added in `tests/integration/` where applicable to test interactions between components.

## Quality Checks

*   **Pre-commit hooks** are configured to automatically enforce formatting and linting standards before commits.
*   **Continuous Integration (CI)** checks, defined in `.github/workflows/tests.yaml`, automatically run tests and quality checks on PRs.
*   Contributions **must pass** all pre-commit hooks and CI checks before they can be merged.

## Full Guidelines

For the complete contribution process, including detailed coding standards, testing procedures, Gitflow workflow, commit message format, and review procedures, please consult the main project [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).