# Code Project Manager Contribution Guidelines (Summary)

This document provides a concise summary of contribution guidelines relevant to the **Code Project Manager** role. For complete details, please refer to the main [/workspace/CONTRIBUTING.md](/workspace/CONTRIBUTING.md).

## 1. Workflow Context

*   This project follows the Gitflow workflow. The `develop` branch serves as the main integration branch.
*   All development work should occur on `feature/*` branches.
*   All code changes managed or coordinated by the Code Project Manager must ultimately be merged into the `develop` branch via Pull Requests.

## 2. Quality Standards

*   All contributions must adhere to the project's established quality standards. This includes:
    *   **Code Style:** Formatting with Black, linting with Flake8, and import sorting with isort.
    *   **Type Checking:** Static analysis using Mypy.
    *   **Testing:** Comprehensive unit and integration tests using `pytest`.
*   Pre-commit hooks and Continuous Integration (CI) checks are in place to automatically enforce these standards.

## 3. Role Responsibility

*   The Code Project Manager is responsible for overseeing coding tasks and ensuring that any code produced by delegated sub-tasks (e.g., work done by the `sr-code-python` mode) meets the project's quality standards *before* reporting the completion of a development phase or merging code.

## 4. Full Guidelines

*   The complete and detailed contribution guidelines for this project can be found in [/workspace/CONTRIBUTING.md](/workspace/CONTRIBUTING.md). Please consult that document for comprehensive information.