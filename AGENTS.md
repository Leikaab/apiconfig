# Contributor Guidelines

This project uses Poetry for dependency management and relies on strict quality checks.

## Setup
- Install dependencies with `poetry install --with dev,docs` and activate the venv using `poetry shell`.
- Install pre-commit hooks:
  ```bash
  pre-commit install
  pre-commit install --hook-type pre-push
  ```
  These commands come from the contributing documentation.

## Quality checks
- Run `poetry run pre-commit run --files <changed files>` before committing. Hooks run autoflake, isort, black, flake8, mypy and pyright, and they execute the test suite with pytest.
- Execute tests with:
  ```bash
  pytest tests/unit
  pytest tests/integration  # requires .env with credentials
  ```
- Generate coverage with:
  ```bash
  pytest tests/unit/ --cov=apiconfig --cov-report=html
  ```

## Commit messages
- Follow the Conventional Commits specification when crafting commit messages (e.g. `feat:`, `fix:`, `docs:`).

## Pull requests
- Ensure all pre-commit and pre-push checks pass and create PRs against the `develop` branch.

Documentation can be built in the `docs/` directory using `make html`.
