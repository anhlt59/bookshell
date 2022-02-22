#!/bin/bash

# Installs docker and docker-compose
# Adds a DOCKER_HOST environment variable in .bashrc_wsl to allow docker to connect to Docker for Windows
# Adds a symlink /c that points to the c drive shared by Docker for Windows so that docker paths work properly

echo -e "Installing and Configuring Docker ..."
sudo apt-get update -y
# Remove any existing legacy docker installations
sudo apt-get remove -y docker docker-engine docker.io
# Make sure we can connect to a repository over https
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
# Add the official Docker Community Edition repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
# Install Docker CE, docker-compose, and PuTTY
sudo apt -q install -y docker-ce docker-compose putty
# Add the current user to the docker group
sudo usermod -aG docker $USER
# Tell docker to connect to the Docker of Windows HOST
grep -q -F '# DOCKER' ~/.bashrc_wsl || printf "\n# DOCKER\n" >>  ~/.bashrc_wsl
grep -q -F 'export DOCKER_HOST' ~/.bashrc_wsl || echo "export DOCKER_HOST=tcp://127.0.0.1:2375" >> ~/.bashrc_wsl
sudo ln -s /mnt/c /c
echo -e "Docker installed!"
