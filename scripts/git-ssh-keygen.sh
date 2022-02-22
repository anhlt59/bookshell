#!/bin/bash

printf "email: "
read -r email
echo -e "ssh-keygen -y -t rsa -b 4096 -C ${email}${NOCOLOR}"
ssh-keygen -y -t rsa -b 4096 -C "$email"
