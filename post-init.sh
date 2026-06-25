#!/bin/bash

# 1. Install additional dependencies via Poetry
echo "Running poetry install..."
poetry install

# 2. Persist the PROJ_LIB environment variable for the user session
echo "Setting PROJ_LIB environment variable..."
export PROJ_LIB=/layers/paketo-buildpacks_conda-env-update/conda-env/share/proj

# Append it to .bashrc so it persists in any new terminal tabs the user opens
echo 'export PROJ_LIB=/layers/paketo-buildpacks_conda-env-update/conda-env/share/proj' >> ~/.bashrc
