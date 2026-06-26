#!/bin/bash
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Navigate into the project directory safely
pushd . > /dev/null
cd $SCRIPT_DIR

echo "Running poetry install..."
# Because the lifecycle launcher runs this, 'poetry' is now perfectly in your path!
poetry install --no-root

echo "Configuring environment variables..."

popd > /dev/null
echo "Initialization complete!"
