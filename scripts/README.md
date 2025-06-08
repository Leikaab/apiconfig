# scripts

Utility scripts for working with **apiconfig**. Currently only `local_dev_setup.sh` is provided.

## `local_dev_setup.sh`

This script recreates the important parts of the devcontainer environment so you can set up
local development without Docker.

### Prerequisites

- Bash shell on Linux/macOS (Windows via WSL or Git Bash)
- [Python](https://www.python.org/) 3.11+
- [Poetry](https://python-poetry.org/) on your `PATH`
- Optional: [GitHub CLI](https://cli.github.com/) if you want automatic authentication via `GITHUB_TOKEN`
- Optional: `curl` to install [`act`](https://github.com/nektos/act) for local GitHub Actions

### Usage

Run the script from the repository root:

```bash
./scripts/local_dev_setup.sh
```

The script will:

1. Create `.env` from `.env.example` if it doesn't exist
2. Configure Poetry to use `.venv/` and install dependencies with the `dev` group
3. Install pre-commit hooks
4. Authenticate GitHub CLI when `GITHUB_TOKEN` is set
5. Install `act` if missing
6. Add a snippet to `.bashrc` so new shells load `.env`

When complete, activate the virtual environment with:

```bash
poetry shell
```
