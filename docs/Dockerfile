ARG VARIANT=1-3.13-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED=1



# Install system dependencies needed for Poetry, Git, and Sphinx Makefiles
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipx
RUN pip install --user pipx
RUN pip install --upgrade pip

# Install Poetry using pipx
RUN pipx install poetry


# Set the working directory in the container
WORKDIR /workspace

# Set the PATH environment variable
ENV PATH="/root/.local/bin:$PATH"

# Disable poetry from creating virtual environments globally
RUN poetry config virtualenvs.create false

# Verify the poetry configuration
#RUN poetry config --list | grep virtualenvs.create

# First, copy only the pyproject.toml file
COPY pyproject.toml ./

# Now copy the lock file and other files
COPY poetry.lock README.md ./

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi --with dev,docs --no-root


# Copy the rest of the application code into the container
# This ensures Sphinx autodoc can find the source files
COPY . .

# Default command to keep container running (will be overridden by docker-compose)
CMD ["sleep", "infinity"]