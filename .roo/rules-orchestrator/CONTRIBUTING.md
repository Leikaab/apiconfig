# Contributing as an Orchestrator

This document provides a concise summary of contribution guidelines specifically for the **Orchestrator** role within this project. For comprehensive details, please refer to the main [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).

## Workflow Management

As the Orchestrator, you manage complex workflows involving multiple modes. It's crucial that the outputs of these workflows (e.g., code changes, documentation updates) align with the project's Gitflow process. All contributions generated through orchestrated tasks must ultimately target the `develop` branch via Pull Requests (PRs) for integration.

## Standard Enforcement

You are responsible for ensuring that tasks delegated to other specialized modes adhere to the project's overall quality standards. This includes verifying compliance with:

*   Code style and formatting.
*   Testing requirements (e.g., unit tests, integration tests).
*   Documentation standards (e.g., docstrings, README updates).
*   Commit message conventions.

These standards are fully defined in the main contribution guidelines.

## Verification

Before proceeding from one step to the next in a workflow, you must verify the successful completion and standard adherence of the previous step. This often involves confirming results reported by other modes, such as passed tests indicated by the `version-control` or `sr-code-python` modes.

## Full Guidelines

For the complete contribution process, including detailed Gitflow instructions, coding standards, testing procedures, documentation guidelines, commit message formats, and the release process, please consult the main project [`/workspace/CONTRIBUTING.md`](/workspace/CONTRIBUTING.md).