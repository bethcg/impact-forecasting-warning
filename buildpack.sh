#!/bin/bash
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# 1. Run your original post-init.sh via the launcher if you have other tasks there
/cnb/lifecycle/launcher $SCRIPT_DIR/post-init.sh

# 2. Source the Paketo/Conda environment explicitly into THIS shell process
# This makes 'poetry' and 'python' immediately available in this script
if [ -d "/layers/paketo-buildpacks_conda-env-update/conda-env/bin" ]; then
    export PATH="/layers/paketo-buildpacks_conda-env-update/conda-env/bin:$PATH"
fi

# 3. Execute poetry install right here in the main startup sequence
echo "Persisting poetry installation into the workspace..."
cd /home/renku/work/impact-forecasting-warning
poetry install --no-root

# 4. Inject the PROJ_LIB fix into the user profile for new terminal windows
echo "export PROJ_LIB=/layers/paketo-buildpacks_conda-env-update/conda-env/share/proj" >> /home/renku/.bashrc
echo "cd /home/renku/work/impact-forecasting-warning" >> /home/renku/.bashrc

echo "All environments ready. Launching VS Codium..."#!/bin/bash

/cnb/process/vscodium
