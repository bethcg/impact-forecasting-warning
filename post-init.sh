#!/bin/bash

# 1. Force execution from the correct project directory
cd /home/renku/work/impact-forecasting-warning

# 2. Define the absolute paths inside the Paketo Conda layer
CONDA_ENV_BIN="/layers/paketo-buildpacks_conda-env-update/conda-env/bin"

echo "Running poetry install inside a localized virtualenv..."
# Explicitly override the poetry.toml file using environment variables.
# This forces poetry to build a local `.venv` inside your project directory.
POETRY_VIRTUALENVS_CREATE=true \
POETRY_VIRTUALENVS_IN_PROJECT=true \
$CONDA_ENV_BIN/poetry install

echo "Configuring environment variables..."
# Define your local virtual environment binary directory
VENV_BIN_PATH="/home/renku/work/impact-forecasting-warning/.venv/bin"

# Persist everything for your interactive terminal sessions
# Crucial: Prepend VENV_BIN_PATH so your code runs using the poetry packages, 
# but keep CONDA_ENV_BIN right next to it so it falls back to the system's GDAL/PROJ binaries!

echo "export PATH=\"$VENV_BIN_PATH:$CONDA_ENV_BIN:\${PATH}\"" >> ~/.bashrc
echo "cd /home/renku/work/impact-forecasting-warning" >> ~/.bashrc

echo "Initialization complete! Your workflow is now fully automated."
