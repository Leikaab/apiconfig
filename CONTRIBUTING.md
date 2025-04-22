# Contributing to apiconfig

Thank you for your interest in contributing to **apiconfig**! We welcome contributions from the community. Please read these guidelines to ensure a smooth and productive process.

---

## Quick Contribution Guide

- **Read the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.**
- **Fork the repository and create a feature branch from `develop`.**
- **Use [Dev Containers](#using-dev-containers-recommended) for a consistent development environment (recommended).**
- **Run all tests and pre-commit hooks before submitting a Pull Request.**
- **Target your PR to the `develop` branch.**

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Running Tests](#running-tests)
- [Code Style and Quality](#code-style-and-quality)
- [Contributing Core Components](#contributing-core-components)
- [Pre-Commit Hooks](#pre-commit-hooks)
- [Managing Dependencies](#managing-dependencies)
- [Branching Strategy (Gitflow)](#branching-strategy-gitflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request (PR) Process](#pull-request-pr-process)
- [Release Process](#release-process)
- [Reporting Issues](#reporting-issues)
- [Related Documentation](#related-documentation)

---

## Code of Conduct

All contributions and interactions must align with the project's [Code of Conduct](CODE_OF_CONDUCT.md).

---

## How to Contribute

1. **Fork the repository** and create a feature branch from `develop`.
2. **Set up your development environment** (see below).
3. **Write clear, well-tested code** following the project's style and patterns.
4. **Document your changes** with clear docstrings and, if needed, user documentation.
5. **Run all tests and pre-commit hooks** before pushing.
6. **Submit a Pull Request** targeting the `develop` branch.

---

## Setting Up the Development Environment

### Prerequisites

- [Python](https://www.python.org/downloads/) (3.11, 3.12, 3.13)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://www.docker.com/get-started) (for Dev Containers)
- [Visual Studio Code](https://code.visualstudio.com/) (for Dev Containers)
- [Remote - Containers VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/apiconfig.git
   cd apiconfig
   ```
2. **Install dependencies:**
   ```bash
   poetry install --all-extras
   poetry shell
   ```
   (Or prefix commands with `poetry run`, e.g., `poetry run pytest`)

### Using Dev Containers (Recommended)

> **Recommended:** Use the provided Dev Container (`.devcontainer/devcontainer.json`) for a consistent, pre-configured environment. This ensures all dependencies and pre-commit hooks are set up automatically.

1. Open the project in VS Code and select "Reopen in Container" when prompted.
2. Wait for the container to build (first time only).
3. Develop inside the container—your terminal, debugger, and extensions run inside the environment.

---

## Running Tests

- **Unit tests:** `pytest tests/unit`
- **Integration tests:** `pytest tests/integration`
- **Coverage:** `poetry run pytest tests/unit/ --cov --cov-report=term-missing --cov-branch`
- **HTML coverage report:** `poetry run pytest tests/unit/ --cov=apiconfig --cov-report=html` (output in `htmlcov/`)

> **Note:** Integration tests require API credentials. Copy `.env.example` to `.env` and fill in your secrets. `.env` is gitignored.

---

## Code Style and Quality

- **Black:** Code formatting
- **isort:** Import sorting
- **Flake8:** Linting (configured in `setup.cfg` or `pyproject.toml`)
- **autoflake:** Removes unused imports/variables
- **Mypy:** Static type checking (configured in `mypy.ini` or `pyproject.toml`)

All are run automatically via pre-commit hooks.

---

## Contributing Core Components

- Follow existing design patterns and interfaces.
- Favor immutability for configuration objects.
- Provide clear numpy-style docstrings for all public classes/functions.
- Write comprehensive unit tests for all new/changed code.

---

## Pre-Commit Hooks

- **Automatic in Dev Containers.**
- **Manual setup:** `pre-commit install && pre-commit install --hook-type pre-push`
- **Run all hooks manually:** `pre-commit run --all-files`

Hooks check formatting, linting, typing, and run all tests before commit/push.

---

## Managing Dependencies

- **Add runtime dependency:** `poetry add <package_name>`
- **Add dev dependency:** `poetry add --group dev <package_name>`
- **Update all:** `poetry update`
- **Update specific:** `poetry update <package_name>`

Commit both `pyproject.toml` and `poetry.lock` after changes.

---

## Branching Strategy (Gitflow)

- **main:** Latest stable release (protected)
- **develop:** Latest development changes (protected)
- **feature/*:** New features/fixes (branch from `develop`)
- **release/*:** Release preparation (branch from `develop`)
- **hotfix/*:** Critical production fixes (branch from `main`)

---

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

- `feat: add environment variable configuration provider`
- `fix: handle missing keys gracefully in dict provider`
- `docs: update CONTRIBUTING.md with Gitflow model`
- `refactor: simplify ClientConfig merging logic`
- `test: add unit tests for custom AuthStrategy`
- `chore: update pre-commit hook versions`

---

## Pull Request (PR) Process

1. Ensure all pre-commit and pre-push checks pass.
2. Push your `feature/*` branch to your fork.
3. Create a PR targeting `develop`.
4. Provide a clear description and link relevant issues.
5. Pass all CI checks.
6. Address code review feedback.

---

## Release Process

- **Pre-releases:** Merging to `develop` triggers a pre-release to PyPI.
- **Stable releases:** Merging to `main` triggers a stable release to PyPI (if version is bumped in `pyproject.toml`).
- **Version bumping:** Update `pyproject.toml` before merging to `main`.

---

## Reporting Issues

If you encounter a bug or have a feature request:

- Check existing issues first.
- Create a new issue if needed, using the template.
- Provide steps to reproduce, expected/actual behavior, version info, and relevant code/config.

---

## Related Documentation

- [README.md](README.md) — Project overview and usage
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community standards
- [Bug Tracker](https://github.com/Leikaab/apiconfig/issues)
- [PyPI Project Page](https://pypi.org/project/apiconfig/)

---

Thank you for helping make **apiconfig** better!