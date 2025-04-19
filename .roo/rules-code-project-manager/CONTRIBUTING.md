# Code Project Manager Contribution Guidelines (Summary)

This document provides a concise summary of contribution guidelines relevant to the **Code Project Manager** role. For complete details, please refer to the main [/workspace/CONTRIBUTING.md](/workspace/CONTRIBUTING.md).

## 1. Workflow Context

*   This project follows the standard Git workflow outlined in [/workspace/.roo/rules/git_workflow.md](/workspace/.roo/rules/git_workflow.md).
*   All code changes managed or coordinated by the Code Project Manager must ultimately be merged into the `develop` branch via Pull Requests.

## 2. Quality Standards

*   All contributions must adhere to the project's established quality standards. See [/workspace/.roo/rules/quality_checks.md](/workspace/.roo/rules/quality_checks.md) for details on required checks (formatting, linting, type checking, testing).
*   Pre-commit hooks and Continuous Integration (CI) checks are in place to automatically enforce these standards.
*   All test, lint, and quality check execution and analysis must be delegated to the `test-runner-summarizer` mode. The Code Project Manager is responsible for verifying that the `test-runner-summarizer` has reported all checks as passed before reporting completion or merging code.

## 3. Role Responsibility

*   The Code Project Manager is responsible for overseeing coding tasks and ensuring that any code produced by delegated sub-tasks (e.g., work done by the `sr-code-python` mode) meets the project's quality standards *before* reporting the completion of a development phase or merging code. See [/workspace/.roo/rules/reporting.md](/workspace/.roo/rules/reporting.md) for the standard reporting process.

## 4. Full Guidelines

*   The complete and detailed contribution guidelines for this project can be found in [/workspace/CONTRIBUTING.md](/workspace/CONTRIBUTING.md). Please consult that document for comprehensive information.