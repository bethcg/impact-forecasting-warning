#!/bin/bash
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# 1. Use the official Paketo launcher to execute your post-init environment setup script
/cnb/lifecycle/launcher $SCRIPT_DIR/post-init.sh

echo "" >> /home/renku/.bashrc

# 2. Hand control back over to JupyterLab (or your default Renku interface) so the session stays open
/cnb/process/vscodium
