#!/bin/bash

source util-definecolors.sh

printf "email: "
read -r email
echo -e "${GREEN}ssh-keygen -y -t rsa -b 4096 -C ${email}${NOCOLOR}"
ssh-keygen -y -t rsa -b 4096 -C "$email"
