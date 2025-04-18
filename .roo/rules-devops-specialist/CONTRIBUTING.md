# DevOps Specialist Contribution Guidelines (Summary)

This document provides a concise overview of contribution guidelines specifically relevant to the DevOps Specialist role. For comprehensive details on Gitflow, testing, dependencies, and environment setup, please refer to the main [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).

## Workflow Alignment

*   The project follows the standard Git workflow outlined in [/workspace/.roo/rules/git_workflow.md](/workspace/.roo/rules/git_workflow.md).
*   CI/CD workflows, located in `.github/workflows/`, must align with this strategy. This includes configuring triggers for:
    *   Automated testing on pushes and pull requests.
    *   Pre-release builds originating from the `develop` branch.
    *   Stable release builds originating from the `main` branch.

## Tooling

The project utilizes specific tools for consistency and quality:

*   **Dependency Management:** Poetry (`pyproject.toml`, `poetry.lock`) is used for managing Python dependencies.
*   **Development Environment:** Dev Containers (`.devcontainer/`) provide a standardized development environment.
*   **Code Quality:** Pre-commit hooks (`.pre-commit-config.yaml`) are used to enforce code style and quality checks before commits. See [/workspace/.roo/rules/quality_checks.md](/workspace/.roo/rules/quality_checks.md) for details on the specific checks.

## Role Focus

As the DevOps Specialist, your primary responsibility is to maintain, configure, and improve these CI/CD workflows, development environments, and associated tooling according to project standards and best practices. See [/workspace/.roo/rules/reporting.md](/workspace/.roo/rules/reporting.md) for the standard reporting process.

## Full Guidelines

Remember, this is only a summary. The complete contribution guidelines are documented in [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md). Please ensure you are familiar with the full document.