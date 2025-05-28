ARG VARIANT=1-3.13-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED=1

# Install pyenv prerequisites
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install pyenv
ENV PYENV_ROOT="/root/.pyenv"
# Update PATH for pyenv shims and bin
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN curl https://pyenv.run | bash

# Install required Python versions
# Using recent stable patch versions
RUN pyenv install 3.11.9 && \
    pyenv install 3.12.4 && \
    pyenv install 3.13.0

# Set global versions - pyenv will manage these, tox will find them
# The base image's 3.13 is also available directly
RUN pyenv global 3.12.4 3.11.9 3.13.0

# Install pipx
RUN pip install --user pipx
RUN pip install --upgrade pip

# Install Poetry using pipx
RUN pipx install poetry

# Set the PATH environment variable
ENV PATH="/root/.local/bin:$PATH"

# Ensure Poetry respects project settings for virtual environments
# (Commented out or remove the line below)
# RUN poetry config virtualenvs.create false

# Verify the poetry configuration
#RUN poetry config --list | grep virtualenvs.create

# First, copy only the pyproject.toml file
COPY pyproject.toml ./

# Run poetry lock to update the lock file if needed
RUN poetry lock

# Now copy the lock file and other files
COPY poetry.lock README.md ./

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi --with dev --no-root