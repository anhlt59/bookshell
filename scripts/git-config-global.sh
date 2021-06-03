#!/bin/bash

source util-definecolors.sh

printf "git config --global user.name: "
read -r name
printf "git config --global user.email: "
read -r email

git config --global user.name "$name"
git config --global user.email "$email"

echo -e "${GREEN}GIT config global done!${NOCOLOR}"