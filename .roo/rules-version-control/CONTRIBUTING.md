# Contributing as a Version Control Specialist

This document provides a concise summary of contribution guidelines specifically for the **Version Control** (`version-control`) role within this project. For comprehensive details, please refer to the main [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).

## Key Responsibilities & Guidelines

*   **Branching Model:** The project follows the Gitflow branching model (`main`, `develop`, `feature/*`, etc.). Your role involves executing Git commands related to this model, such as creating feature branches. Merging is typically handled via Pull Requests (PRs) reviewed by others.
*   **Commit Standards:** All commit messages **must** adhere to the [Conventional Commits](https://www.conventionalcommits.org/) format. This is crucial for automated changelog generation and semantic versioning.
*   **Pre-Commit Checks:** Before committing any changes, you **must** run all tests (`pytest`) and quality checks (`pre-commit run --all-files`). Commits **must not** proceed if any checks fail, unless explicitly instructed otherwise for specific setup or troubleshooting scenarios. Using the `--no-verify` flag (or similar) to bypass these checks is strictly prohibited.
*   **Repository Integrity:** A primary focus of this role is maintaining the integrity and clarity of the repository's history through careful and accurate Git operations.
*   **Full Guidelines:** For the complete contribution process, including detailed Gitflow instructions, the precise Conventional Commits format, testing procedures, and PR guidelines, please consult the main project [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).