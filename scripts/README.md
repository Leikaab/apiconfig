# scripts

Utility scripts for working with **apiconfig**. Currently only `local_dev_setup.sh` is provided.

## `local_dev_setup.sh`

This script mimics the important parts of the devcontainer setup so that developers without Docker can create a similar environment.

### Prerequisites

- Bash shell on Linux/macOS (Windows via WSL or Git Bash)
- [Python](https://www.python.org/) 3.11+
- [Poetry](https://python-poetry.org/) on your `PATH`
- Optional: `curl` to install [`act`](https://github.com/nektos/act) for local GitHub Actions

### Usage

Run the script from the repository root:

```bash
./scripts/local_dev_setup.sh
```

The script will:

1. Create `.env` from `.env.example` if it doesn't exist (or create a blank one)
2. Configure Poetry to match devcontainer settings:
   - `virtualenvs.in-project true` (creates `.venv/` in project root)
   - `installer.parallel true` (parallel installation)
   - `virtualenvs.create true` (ensures virtual environment creation)
3. Install dependencies with the `dev` group
4. Install pre-commit hooks (both pre-commit and pre-push)
5. Install `act` if missing (for running GitHub Actions locally)
6. Add a snippet to `.bashrc` so new shells automatically load `.env`

When complete, activate the virtual environment with:

```bash
poetry shell
```

### Note

This script mirrors the devcontainer configuration from `.devcontainer/` to ensure consistency between local and containerized development environments.
