#!/bin/bash
# Convert line separator CRLF to LF
# Params are file or folder path

source util-definecolors.sh

format() {
  if [[ -d $1 ]]; then
    # if $1 is a directory
    ITEMS=$(ls "$1")
    for item in $ITEMS; do
      format "${1}/${item}"
    done
  elif [[ -f $1 ]]; then
    # if $1 is a file
    echo -e "${1} ${GREEN} formated!${NOCOLOR}"
    sudo sed -i 's/\r$//g' "$1"
    sudo chmod +x "$1"
    ((count++))
  else
    echo -e "${RED} ${1} is not valid file or folder. ignored!"
  fi
}

count=0
while [[ $# -gt 0 ]]; do
  format "$1"
  shift # past argument
done
echo -e "${GREEN} ${count} files formated"
