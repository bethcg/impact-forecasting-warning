#!/bin/bash

# Force execution from the correct project directory
cd /home/renku/work/impact-forecasting-warning

# 1. Locate the Conda environment's Python/Pip binary
# Based on your PROJ_LIB path, it should live here:
CONDA_PYTHON="/layers/paketo-buildpacks_conda-env-update/conda-env/bin/python"

echo "Locating Python and installing Poetry..."
# Use the absolute Python path to invoke pip as a module
$CONDA_PYTHON -m pip install --user poetry

# 2. Force the current script session to see the new poetry install path
export PATH="/home/renku/.local/bin:$PATH"

echo "Running poetry install..."
# Run poetry using the explicit path
/home/renku/.local/bin/poetry install
