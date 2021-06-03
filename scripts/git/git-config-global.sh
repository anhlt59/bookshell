#!/bin/bash


printf "git config --global user.name: "
read -r name
printf "git config --global user.email: "
read -r email

git config --global user.name "$name"
git config --global user.email "$email"
git config --global help.autocorrect 10

echo -e "GIT config global done!"
