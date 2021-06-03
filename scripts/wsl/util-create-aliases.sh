#!/bin/bash

# Create an alias that overrides the ls command to use human readable sizes and to group directories first
grep -q -F 'alias ls=' ~/.bash_aliases || echo 'alias ls="ls --color=auto --file-type --human-readable --group-directories-first"' >> ~/.bash_aliases

# Create an alias that overrides the tree command to show two levels by default and show directories first
sudo apt install tree
grep -q -F 'alias tree=' ~/.bash_aliases || echo 'alias tree="tree --dirsfirst -L 2"' >> ~/.bash_aliases
