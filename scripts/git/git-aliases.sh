#!/bin/bash

git config --global help.autocorrect 10
git config --global alias.last 'log -1 HEAD --stat'
git config --global alias.search '!git rev-list --all | xargs git grep -F'
git config --global alias.alias 'config --get-regexp ^alias'
git config --global alias.pf 'push --force-with-lease'
git config --global alias.save 'commit -m "chore: save point"'
git config --global alias.undo 'reset HEAD~1 --mixed'
git config --global alias.br 'branch --format="%(HEAD) %(color:yellow)%(refname:short)%(color:reset) - %(contents:subject) %(color:green)(%(committerdate:relative)) [%(authorname)]" --sort=-committerdate'
