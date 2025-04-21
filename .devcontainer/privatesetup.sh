#!/bin/sh

# This script is intended for optional, user-specific setup within the dev container.
# It is ignored by git.

echo "Running private setup..."

# Install VS Code extensions
echo "Installing VS Code extension: RooVeterinaryInc.roo-cline"
code --install-extension RooVeterinaryInc.roo-cline --force


# Check for private .roomodes and copy if exists
if [ -f ".roo/.roomodes" ]; then
  echo "Found .roo/.roomodes, copying to workspace root..."
  cp .roo/.roomodes .roomodes
else
  echo ".roo/.roomodes not found, skipping copy."
fi

echo "Private setup complete."