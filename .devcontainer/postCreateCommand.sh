#!/bin/sh

# Reload the shell environment
. ~/.bashrc

# Check if the .env file exists
if [ -f .env ]; then
    # Export the variables from .env
    export $(grep -v '^#' .env | xargs)
fi

# Authenticate GitHub CLI if GITHUB_TOKEN is set
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Attempting GitHub CLI authentication..."
    echo "$GITHUB_TOKEN" | gh auth login --with-token
    gh auth status # Optional: verify status
else
    echo "GITHUB_TOKEN not set, skipping GitHub CLI authentication."
fi

# set up pre-commit hooks, commented out for now
poetry run pre-commit install -t pre-commit
poetry run pre-commit install -t pre-push

# Wait until poetry is available
for i in {1..5}; do
    if command -v poetry &> /dev/null
    then
        echo "Poetry found"
        break
    else
        echo "Waiting for Poetry to be available..."
        sleep 2
    fi
done

echo "Checking poetry by direct invocation:"
if /usr/local/py-utils/bin/poetry --version &> /dev/null
then
    echo "Poetry is available and working"
    poetry config virtualenvs.create false --local
else
    echo "Poetry could not be found"
fi

echo "Development environment setup complete!"
# Append .env loading logic to /root/.bashrc if not already present
BASHRC_CONTENT=$(cat /root/.bashrc 2>/dev/null || true) # Read bashrc, ignore error if missing
ENV_LOAD_MARKER="# Load workspace .env"
if ! echo "$BASHRC_CONTENT" | grep -qF "$ENV_LOAD_MARKER"; then
  echo "Appending .env loading logic to /root/.bashrc..."
  echo '' >> /root/.bashrc # Add a newline for separation
  echo "$ENV_LOAD_MARKER" >> /root/.bashrc
  echo 'if [ -f "/workspace/.env" ]; then' >> /root/.bashrc
  echo '  set -a # Automatically export all variables' >> /root/.bashrc
  echo '  source "/workspace/.env"' >> /root/.bashrc
  echo '  set +a # Stop automatically exporting variables' >> /root/.bashrc
  # Optional: echo '  echo "Loaded environment variables from /workspace/.env"' >> /root/.bashrc
  echo 'fi' >> /root/.bashrc
  echo "Logic appended to /root/.bashrc."
else
  echo ".env loading logic already present in /root/.bashrc."
fi