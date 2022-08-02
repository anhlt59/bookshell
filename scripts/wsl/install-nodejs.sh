#!/bin/bash

# This script will install the Node programming language

curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential
sudo npm install -g yarn
