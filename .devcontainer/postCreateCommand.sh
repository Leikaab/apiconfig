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