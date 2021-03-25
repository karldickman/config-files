# If not running interactively don't do anything
if [[ -z "$PS1" ]]; then
    return
fi

# Settings
export HISTCONTROL=ignoredups

# Paths
export LOCAL_INSTALL=$HOME/.local
export GOPATH="$LOCAL_INSTALL/gopath"
export MONO_PATH="$LOCAL_INSTALL/lib/mono"
export TEXMFHOME="$LOCAL_INSTALL/share/texmf"
PATH="$LOCAL_INSTALL/bin:$GOPATH:$GOPATH/bin:$PATH"
export EDITOR=vim
export MANPAGER="sh -c \"col -b | view -u ~/.vimmanpager -\""
# export PAGER="sh -c \"col -b | view -u ~/.vimpager -\""
export PYTHONPATH=$LOCAL_INSTALL/lib/python

#Colorings
export RRESET="\017"
export RNORMAL="\033[0m"
export RGRAY="\033[30;1m"
export RRED="\033[31;1m"
export RGREEN="\033[32;1m"
export RYELLOW="\033[33;1m"
export RBLUE="\033[34;1m"
export RPURPLE="\033[35;1m"
export RCYAN="\033[36;1m"
export RWHITE="\033[37;1m"

export RESET="\[${RRESET}\]"
export NORMAL="\[${RNORMAL}\]"
export GRAY="\[${RGRAY}\]"
export RED="\[${RRED}\]"
export GREEN="\[${RGREEN}\]"
export YELLOW="\[${RYELLOW}\]"
export BLUE="\[${RBLUE}\]"
export PURPLE="\[${RPURPLE}\]"
export CYAN="\[${RCYAN}\]"
export WHITE="\[${RWHITE}\]"

# Aliases and other command modifications
if [[ -x /usr/bin/lesspipe ]]; then
    eval "$(lesspipe)"    #Make less more friendly to pipes
fi

if [[ "$TERM" != "dumb" ]]; then
    eval "$(dircolors -b)"   #Enable color support for ls
fi

alias gcc='gcc -masm=intel'                     #Use Intel assembly
alias indent='while read; do echo "  $REPLY"; done'
alias objdump='objdump -Mintel'                 #Use Intel assembly
alias patch='patch -b'
alias ssh='ssh -XY'
alias tree='tree -C'

scheme() {
    local has_file_arg=false
    for arg in "$@"
    do
        if [[ -e "$arg" ]]; then
            has_file_arg=true
            local file="$arg"
            break
        fi
    done
    if [[ $has_file_arg = true ]]; then
        local arg_string=$(echo "$@" | sed s/$file//g)
        /usr/bin/scheme < "$file" --quiet $arg_string
    else
        /usr/bin/scheme $@
    fi
}

# New commands
alias ls='ls -BX --color=auto'
alias clean='trash -f \#* *~ .*~ *.bak .*.bak  *.tmp .*.tmp core a.out'
alias errecho='echo >/dev/stderr'
alias texclean='trash -f *.toc *.aux *.log *.cp *.fn *.tp *.vr *.pg *.ky'
alias vimpager="vim -u ~/.vimpager"
alias vimmanpager="vim -u ~/.vimmanpager"

nav() {
    cd "$@"
    [[ $1 != "-h" ]] && [[ $1 != "--help" ]] && [[ $? == "0" ]] && ls
}

up() {
    nav ..
}

pskill() {
	local pid
	pid=$(ps -A | grep $1 | awk '{ print $1 }')
    if [[ $pid != "" ]]; then
        kill -9 $pid
    else
        errecho "No process $1 is currently running."
    fi
}

window_title() {
    echo -ne "\033]0;$*\007"
}

github() {
    git remote add github "git@github.com:karldickman/$1.git"
    git push -u github master
}

# Parse git branch
parse_git_branch() {
	git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* //'
}

#Color prompt
prompt_title() {
    window_title "$USER@${HOSTNAME%%.*}:${PWD/#$HOME/~}"
}

promptcolor() {
    if [[ $1 != "0" ]]; then
        printf "%s" "$RED"
    else
        printf "%s" "$YELLOW"
    fi
}

case "$TERM" in
    xterm*)
		PROMPT_COMMAND='PS1="$(promptcolor $?)\u@\h $(date +"%T")${GREEN} ($(parse_git_branch)) ${NORMAL}$ "; prompt_title;'
        ;;
    *)
        PROMPT_COMMAND='PS1="$(promptcolor $?)\u@\h $(date +"%T"):\w${NORMAL}\$ ";'
    esac

# Enable programmable completion features
if [[ -f /etc/bash_completion ]]; then
    source /etc/bash_completion
fi

# Moddifications to shell behavior
shopt -s checkwinsize   #Check window size
set -o vi       #vi mode for command entry

if [[ -f .bashrc_linux ]]; then
    source ~/.bashrc_linux
fi
if [[ -f .bashrc_darwin ]]; then
    source ~/.bashrc_darwin
fi
if [[ -f .bashrc_local ]]; then
    source ~/.bashrc_local
fi
