#!/usr/bin/env bash
set -euo pipefail

# This script mimics the important parts of the devcontainer setup so that
# developers without Docker can create a similar environment.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "🔧 Setting up apiconfig local development environment..."

# Ensure .env exists
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Created .env from .env.example"
    else
        touch .env
        echo "Created blank .env"
    fi
fi

# Configure Poetry like in devcontainer
poetry config virtualenvs.in-project true
poetry config installer.parallel true

# Install dependencies with dev extras
echo "📦 Installing dependencies..."
poetry install --with dev --no-interaction --no-ansi

# Install pre-commit hooks
echo "🔗 Installing pre-commit hooks..."
poetry run pre-commit install -t pre-commit
poetry run pre-commit install -t pre-push

# Authenticate GitHub CLI if available and token provided
if command -v gh >/dev/null 2>&1 && [ -n "${GITHUB_TOKEN:-}" ]; then
    echo "$GITHUB_TOKEN" | gh auth login --with-token
    gh auth status || true
fi

# Install act for running GitHub Actions locally if not present
if ! command -v act >/dev/null 2>&1; then
    echo "Installing act..."
    curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
    mkdir -p "$HOME/.config/act"
    echo "-P ubuntu-latest=catthehacker/ubuntu:full-latest" > "$HOME/.config/act/actrc"
fi

# Ensure .env is loaded for new shells
ENV_MARKER="# Load workspace .env"
if ! grep -qF "$ENV_MARKER" "$HOME/.bashrc" 2>/dev/null; then
    cat <<'BASH' >> "$HOME/.bashrc"

# Load workspace .env
if [ -f "/workspace/.env" ]; then
  set -a
  source "/workspace/.env"
  set +a
fi
BASH
fi

echo "✅ Environment ready. Virtual environment: .venv/"
echo "   Run 'poetry shell' to activate"
