#!/bin/bash

# Installs a git enabled prompt so that the current git branch will displayed on the prompt

# Set up some output colors
source util-definecolors.sh

# INIT .BASHRC_WSL
./util-bashrc_wsl.sh

# GIT ENABLED PROMPT
echo -e "${GREEN}"
echo 'Installing Git integrated Bash prompt ...'
echo -e "${NOCOLOR}"
rm -rf ~/.bash/git-aware-prompt
git clone https://github.com/jimeh/git-aware-prompt.git ~/.bash/git-aware-prompt
# Add lines to .bashrc_wsl to enable the git-aware-prompt
grep -q -F '# GIT AWARE PROMPT' ~/.bashrc_wsl || printf "\n# GIT AWARE PROMPT\n" >>  ~/.bashrc_wsl
grep -q -F 'export GITAWAREPROMPT' ~/.bashrc_wsl || echo "export GITAWAREPROMPT=~/.bash/git-aware-prompt" >>  ~/.bashrc_wsl
grep -q -F 'source "${GITAWAREPROMPT}' ~/.bashrc_wsl || echo 'source "${GITAWAREPROMPT}/main.sh"' >>  ~/.bashrc_wsl
grep -q -F 'export PS1=' ~/.bashrc_wsl || echo 'export PS1="\${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;37m\]\w\[\033[00m\] \[\033[01;33m\]\$git_branch\[$txtred\]\$git_dirty\[$txtrst\]\$ "' >> ~/.bashrc_wsl

# BASH-GIT-PROMPT
# This is an alternative, more fully featured Git integrated prompt, but it may be slower
# Comment out the prompt install lines above and uncomment the lines below to use it instead
#rm -rf ~/.bash/bash-git-prompt

