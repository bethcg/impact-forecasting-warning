#!/bin/bash

# Force execution from the correct project directory
cd /home/renku/work/impact-forecasting-warning

# Define the absolute paths inside the Paketo Conda layer
CONDA_ENV_BIN="/layers/paketo-buildpacks_conda-env-update/conda-env/bin"

echo "Running poetry install..."
# Call poetry directly from the Conda binary folder
$CONDA_ENV_BIN/poetry install
