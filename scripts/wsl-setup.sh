#!/bin/bash

# This script runs the scripts to set up a ~/.bashrc_wsl file to customize bash under WSL
# It installs docker and configures it to work with Docker for Windows
# It installs and enables a git enabled bash prompt that will show the current branch of git
# It sets the default directory to start in when bash opens

set -o errexit
set -o pipefail
set -o nounset

# Set up some output colors
source util-definecolors.sh

# convert line separater LF
./util-lff.sh .

# RESET
# Clear ~/bashrc_wsl so that we start with a clean slate
if [ -f ~/.bashrc_wsl ]; then
  rm ~/.bashrc_wsl
fi

# INIT .BASHRC_WSL
./util-bashrc_wsl.sh

# DOCKER
./install-docker.sh

# GIT ENABLED  q
./git-prompt-install.sh

echo -e "${GREEN}"
echo WSL Bash Setup complete.
echo -e "${NOCOLOR}"

echo -e "${YELLOW}"
echo 'NOTE: Bash configuration changes will not be applied until WSL Bash is closed and restarted'
echo -e "${NOCOLOR}"
echo ''
