# Contributing as a Test Runner & Summarizer

This document provides a concise summary of contribution guidelines specifically for the **Test Runner & Summarizer** role within this project. For comprehensive details, please refer to the main [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).

## Testing Framework & Quality Checks

*   The project utilizes `pytest` for executing automated tests.
*   `pre-commit` is used to run various code quality checks. See [/workspace/.roo/rules/quality_checks.md](/workspace/.roo/rules/quality_checks.md) for details on the specific checks enforced.

## Test Locations

*   Unit tests are located in the `tests/unit` directory.
*   Integration tests are located in the `tests/integration` directory.

## Role Focus

Your primary responsibility in this role is to:

1.  Accurately execute the specific test or linting commands provided (e.g., `pytest tests/unit`, `pre-commit run --all-files`).
2.  Clearly report the success or failure status of the executed commands.
3.  Provide a concise summary of the results, highlighting any failures or significant outputs. See [/workspace/.roo/rules/reporting.md](/workspace/.roo/rules/reporting.md) for the standard reporting process.

## Full Guidelines

For the complete contribution process, including detailed testing procedures, quality standards, and how to handle test failures, please consult the main project [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).