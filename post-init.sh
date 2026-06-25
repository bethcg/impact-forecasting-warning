#!/bin/bash

# Force execution from the correct project directory
cd /home/renku/work/impact-forecasting-warning

echo "Running pip install poetry..."
pip install poetry

# Force the current script session to see the new poetry install path
export PATH="/home/renku/.local/bin:$PATH"

echo "Running poetry install..."

# Use the absolute path to poetry just to be absolutely safe
/home/renku/.local/bin/poetry install
