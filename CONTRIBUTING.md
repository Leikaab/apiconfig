# Contributing to apiconfig

Thank you for your interest in contributing to `apiconfig`! We welcome contributions from the community. Follow these guidelines to ensure a smooth process.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
  - [Using Dev Containers (Recommended)](#using-dev-containers-recommended)
- [Running Tests](#running-tests)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [Integration Tests & Environment Variables](#integration-tests--environment-variables)
  - [Coverage](#coverage)
- [Code Style and Quality](#code-style-and-quality)
  - [Linters and Formatters](#linters-and-formatters)
  - [Type Checking](#type-checking)
- [Contributing Core Components](#contributing-core-components)
- [Pre-Commit Hooks](#pre-commit-hooks)
- [Managing Dependencies](#managing-dependencies)
  - [Adding Dependencies](#adding-dependencies)
  - [Updating Dependencies](#updating-dependencies)
- [Branching Strategy (Gitflow)](#branching-strategy-gitflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request (PR) Process](#pull-request-pr-process)
- [Release Process](#release-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

All contributions and interactions must align with the project's [Code of Conduct](CODE_OF_CONDUCT.md).

## Setting Up the Development Environment

### Prerequisites

- [Python](https://www.python.org/downloads/) (Versions 3.10, 3.11, 3.12 are tested in CI)
- [Poetry](https://python-poetry.org/docs/#installation) (for dependency management)
- [Docker](https://www.docker.com/get-started) (required for Dev Containers)
- [Visual Studio Code](https://code.visualstudio.com/) (required for Dev Containers)
- [Remote - Containers VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (required for Dev Containers)

### Setup Steps

1.  **Clone the repository:**
    ```bash
    # Replace with the actual URL for the apiconfig repository
    git clone https://github.com/your-org/apiconfig.git
    cd apiconfig
    ```
2.  **Install dependencies:**
    - Poetry manages project dependencies and the virtual environment.
    - Run the following command to install all required dependencies, including development tools:
    ```bash
    poetry install --all-extras
    ```
    - Activate the virtual environment created by Poetry:
    ```bash
    poetry shell
    ```
    (Alternatively, prefix commands with `poetry run`, e.g., `poetry run pytest`)

### Using Dev Containers (Recommended)

This project includes a Dev Container configuration (`.devcontainer/devcontainer.json`), providing a pre-configured Docker container as a fully-featured development environment. This ensures consistency across different developer setups and **automatically installs pre-commit hooks** via the `postCreateCommand.sh` script.

1.  **Open the project in the container:**
    -   With the prerequisites installed, VS Code prompts you to "Reopen in Container" when you open the project folder. Click it.
    -   Alternatively, open the VS Code Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and select "Remote-Containers: Reopen in Container".
2.  **Wait for the container to build:** This occurs only the first time.
3.  **Develop inside the container:** VS Code connects to the container. Your terminal, debugger, and extensions run inside the container environment, which has Python, Poetry, project dependencies, and pre-commit hooks installed and configured.

## Running Tests

Tests are written using `pytest`.

### Unit Tests

Unit tests mock external dependencies and test individual components in isolation. They are located in `tests/unit`.

```bash
pytest tests/unit
```

### Integration Tests

Integration tests interact with actual external services or test the integration between multiple components. They are located in `tests/integration`.

```bash
pytest tests/integration
```

### Integration Tests & Environment Variables

Running the integration tests locally requires access to live API credentials or tokens for the services being tested. The Continuous Integration (CI) system (`.github/workflows/tests.yaml`) runs the full test suite using secrets.

1.  **Required Variables:** The names of the necessary environment variables are listed in the `.env.example` file.
2.  **Local Setup:** To run these tests locally:
    *   Create a file named `.env` (copy `.env.example` as a starting point).
    *   Populate this `.env` file with your actual API credentials, matching the variable names found in `.env.example`.
    *   **Important:** The `.env` file is listed in `.gitignore` by default to prevent accidentally committing secrets.
3.  **When to Run Locally:** Running integration tests locally is useful when:
    *   Working on or modifying integration tests.
    *   Working on a feature that directly impacts an integrated service.
    *   Verifying changes before submitting a Pull Request involving integrated services.

### Coverage

The pre-push hook (`.pre-commit-config.yaml`) runs unit tests with coverage. To run unit tests locally and generate a coverage report:

```bash
# Command specified in the pre-push hook
poetry run pytest tests/unit/ --cov --cov-report=term-missing --cov-branch
```

To generate an HTML report for unit test coverage:

```bash
poetry run pytest tests/unit/ --cov=apiconfig --cov-report=html
```
This creates an HTML report in the `htmlcov/` directory (default for `pytest-cov`).

## Code Style and Quality

We use several tools to maintain code quality and consistency. These are configured in `.pre-commit-config.yaml` and run automatically via pre-commit hooks.

### Linters and Formatters

- **Black:** Code formatting.
- **isort:** Import sorting (using Black profile).
- **Flake8:** General linting (style guide enforcement, complexity checks). Configuration is in `setup.cfg` or `pyproject.toml`.
- **autoflake:** Removes unused imports and variables.

### Type Checking

- **Mypy:** Static type checking. Configuration is in `mypy.ini` or `pyproject.toml`. Type hints are required for all code.

## Contributing Core Components

When contributing to core parts of `apiconfig`, such as configuration providers, `ClientConfig`, or `AuthStrategy` implementations:

1.  **Understand Existing Patterns:** Familiarize yourself with the existing design and interfaces (e.g., base classes, protocols).
2.  **Maintain Consistency:** Follow established patterns for naming, structure, and error handling.
3.  **Immutability:** Favor immutable objects where practical, especially for configuration components.
4.  **Documentation:** Provide clear docstrings explaining the purpose, parameters, and usage of new or modified components.
5.  **Testing:** Write comprehensive unit tests covering different scenarios and edge cases for your changes.

## Pre-Commit Hooks

We use [`pre-commit`](https://pre-commit.com/) to automatically run checks before commits and pushes, configured in `.pre-commit-config.yaml`.

**Setup:**

-   **Using Dev Containers:** The pre-commit hooks are **automatically installed** when the Dev Container environment is built (`.devcontainer/postCreateCommand.sh`). No manual setup is needed.
-   **Manual Setup (Not using Dev Containers):** If not using the Dev Container, ensure `pre-commit` is installed (it's included in the development dependencies via `poetry install --all-extras`). Then, install the git hooks manually:
    ```bash
    # Install hooks (run once per clone if not using Dev Container)
    pre-commit install       # Installs pre-commit hooks
    pre-commit install --hook-type pre-push  # Installs pre-push hooks
    ```

**Checks Performed:**

-   **On `git commit`:** Includes checks like trailing whitespace, code formatting (`autoflake`, `isort`, `black`), linting (`flake8`), static type checking (`mypy`), and running all tests (`pytest tests/`).
-   **On `git push`:** Includes running unit tests with coverage (`pytest tests/unit --cov`).

If any hook fails, the commit or push is aborted. Address the reported issues and try again. Run hooks manually on all files: `pre-commit run --all-files`.

## Managing Dependencies

We use [Poetry](https://python-poetry.org/) to manage project dependencies, defined in `pyproject.toml`.

### Adding Dependencies

- **Runtime Dependency:**
  ```bash
  poetry add <package_name>
  ```
- **Development Dependency (tools, testing, etc.):**
  ```bash
  poetry add --group dev <package_name>
  ```

Commit both the updated `pyproject.toml` and `poetry.lock` files.

### Updating Dependencies

```bash
# Update all dependencies to latest allowed versions
poetry update

# Update a specific package
poetry update <package_name>
```

Commit the updated `poetry.lock` file.

## Branching Strategy (Gitflow)

We follow the Gitflow branching model:

-   **`main`:** Represents the latest stable release. This branch is protected. Code arrives here via merges from `develop` or `release/*` branches during the release process. Direct commits are disallowed.
-   **`develop`:** Represents the latest development changes and serves as the integration branch for new features. This branch is protected. **All feature branches must be based on `develop`, and Pull Requests must target `develop`.**
-   **`feature/*` (e.g., `feature/add-env-provider`, `feature/improve-config-validation`):** Branched from `develop` for new features, bug fixes, or improvements. These are the primary branches for contribution. Once complete, submit a Pull Request to merge back into `develop`.
-   **`release/*`:** Used to prepare for a new production release. Branched from `develop`, they allow for final testing, documentation updates, and minor bug fixes before merging into `main` (and back into `develop`).
-   **`hotfix/*`:** Branched from `main` to address critical bugs in a production release. Once fixed, they are merged back into both `main` and `develop`.

For most contributions, create a `feature/*` branch from `develop`.

## Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This enables automated changelog generation and versioning.

Examples:

- `feat: add environment variable configuration provider`
- `fix: handle missing keys gracefully in dict provider`
- `docs: update CONTRIBUTING.md with Gitflow model`
- `refactor: simplify ClientConfig merging logic`
- `test: add unit tests for custom AuthStrategy`
- `chore: update pre-commit hook versions`

## Pull Request (PR) Process

1.  Ensure all pre-commit and pre-push checks pass locally.
2.  Push your `feature/*` branch to your fork on GitHub.
3.  Create a Pull Request targeting the **`develop`** branch of the main `apiconfig` repository (e.g., `your-org/apiconfig`).
4.  Provide a clear description of the changes in the PR. Link to any relevant issues using `Fixes #issue_number` or `Relates #issue_number`.
5.  **CI Checks:** Automated checks (linters, type checkers, tests across multiple Python versions and OS) run via GitHub Actions (`.github/workflows/tests.yaml`) on your PR. Ensure these pass.
6.  Engage in code review and address any feedback promptly.

## Release Process

Our release process is automated via GitHub Actions (`.github/workflows/publish.yaml`):

-   **Pre-releases:** Merging changes into the `develop` branch automatically triggers a workflow that builds and publishes a pre-release version (e.g., `X.Y.Z.devN`, where N is the commit count since the last tag) to PyPI.
-   **Stable Releases:** Merging changes into the `main` branch triggers the publish workflow. This workflow publishes a stable version (e.g., `X.Y.Z`) to PyPI and creates a corresponding Git tag **only if** the version specified in `pyproject.toml` is greater than the latest Git tag on the `main` branch. Successful completion of the test workflow (`.github/workflows/tests.yaml`) is an implicit prerequisite, as merges to `main` typically require passing checks.

Version bumping in `pyproject.toml` (done on `develop` or a `release` branch before merging) is required for stable releases.

## Reporting Issues

If you encounter a bug or have a feature request, check existing issues first. If it's a new issue, create one using the appropriate template on GitHub Issues for the `apiconfig` repository. Provide as much detail as possible, including:

-   Steps to reproduce the issue.
-   Expected behavior.
-   Actual behavior.
-   `apiconfig` version, Python version, and OS.
-   Relevant code snippets or configuration examples.