# Contributor Guidelines for apiconfig

This project uses Poetry for dependency management and relies on strict quality checks.

## Setup

### Initial Setup
1. Install dependencies with `poetry install --with dev` and activate the venv using `poetry shell`.
2. Install pre-commit hooks:
   ```bash
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

### Environment Variables
- For local development: Create a `.env` file from `.env.example` with necessary API credentials
- **For agent/test environments**: Environment variables needed for integration tests (e.g., `TRIPLETEX_CONSUMER_TOKEN`, `FIKEN_API_TOKEN`) are automatically loaded from secrets, so you can run `poetry run pytest` without manual configuration

## Quality Checks

### Test Priority Order
When testing or fixing code, ALWAYS follow this strict order:
1. pytest error
2. pytest fail
3. pytest skipped
4. mypy error
5. flake8, isort, and black error
6. tox errors
7. coverage (if relevant)

### Running Tests
- Run unit tests: `poetry run pytest tests/unit/`
- Run component tests: `poetry run pytest tests/component/`
- Run integration tests: `poetry run pytest tests/integration/`
- Run all tests: `poetry run pytest`
- Run all tests with coverage: `poetry run pytest --cov=apiconfig --cov-report=html`

### Test Types
- **Unit tests** (`tests/unit/`): Test individual functions and classes in isolation
- **Component tests** (`tests/component/`): Test interactions between multiple components
- **Integration tests** (`tests/integration/`): Test against real external APIs (requires credentials)

### Pre-commit Checks
- Run checks on changed files: `poetry run pre-commit run --files <changed files>`
- Run all checks: `poetry run pre-commit run --all-files`
- Hooks include: autoflake, isort, black, flake8, mypy, pyright, and pytest

## Project Structure

```
apiconfig/
├── auth/          # Authentication strategies (basic, bearer, API key, custom)
├── config/        # API client configuration and providers
├── exceptions/    # Structured exception hierarchy
├── testing/       # Test utilities and helpers
├── utils/         # Logging, redaction, and utilities
└── types.py       # Shared type definitions
```

## Key Commands

### Development
- Add dependency: `poetry add package-name`
- Add dev dependency: `poetry add --group dev package-name`
- Update dependencies: `poetry update`
- Show dependency tree: `poetry show --tree`

### Testing
- Unit tests only: `poetry run pytest tests/unit/`
- Component tests only: `poetry run pytest tests/component/`
- Integration tests only: `poetry run pytest tests/integration/`
- Specific test: `poetry run pytest tests/unit/test_file.py::test_function`
- With coverage: `poetry run pytest --cov=apiconfig --cov-report=html`

### Code Quality
- Type checking: `poetry run mypy apiconfig/ tests/`
- Linting: `poetry run flake8 apiconfig/ tests/`
- Format check: `poetry run black --check apiconfig/ tests/`
- Import sorting: `poetry run isort --check-only apiconfig/ tests/`

### Documentation
- Build docs: `cd docs && poetry run make html`

## Best Practices

1. **Type Hints**: Required for all public APIs
2. **Docstrings**: Numpy-style for all public classes/methods/functions
3. **Testing**: Aim for 100% unit test coverage
4. **Error Handling**: Use specific exceptions from `apiconfig.exceptions`
5. **Sensitive Data**: Use redaction utilities from `apiconfig.utils.redaction`

## Commit Messages
Follow the Conventional Commits specification:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

## Pull Requests
- Ensure all pre-commit and pre-push checks pass
- Create PRs against the `develop` branch
- All tests must pass before merging
