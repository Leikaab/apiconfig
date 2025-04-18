#!/bin/sh

ENV_FILE="../.env"
ENV_EXAMPLE_FILE="../.env.example"

# Only create .env if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
  if [ -f "$ENV_EXAMPLE_FILE" ]; then
    cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
  else
    touch "$ENV_FILE"
  fi
fi