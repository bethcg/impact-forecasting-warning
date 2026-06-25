#!/bin/bash

# Force execution from the correct project directory
cd /home/renku/work/impact-forecasting-warning

# Define the absolute paths inside the Paketo Conda layer
CONDA_ENV_BIN="/layers/paketo-buildpacks_conda-env-update/conda-env/bin"

echo "Configuring Poetry isolation settings..."
# Force Poetry to create virtualenvs and drop them into a writeable directory (~/.cache/pypoetry)
$CONDA_ENV_BIN/poetry config virtualenvs.create true
$CONDA_ENV_BIN/poetry config virtualenvs.in-project false

echo "Running poetry install into localized virtualenv..."
# This will now succeed because it installs cleanly without attempting to modify the /layers directory
$CONDA_ENV_BIN/poetry install
