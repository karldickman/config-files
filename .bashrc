export HISTCONTROL=ignoredups

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

# If not running interactively don't do anything
if [[ -z "$PS1" ]]; then
    return
fi

# Aliases and other command modifications
if [[ -x /usr/bin/lesspipe ]]; then
    eval "$(lesspipe)"    #Make less more friendly to pipes
fi

if [[ "$TERM" != "dumb" ]]; then
    eval "$(dircolors -b)"   #Enable color support for ls
fi

alias gcc='gcc -masm=intel'                     #Use Intel assembly
alias indent='while read; do echo "  $REPLY"; done'
alias mysql='mysql -p'
alias mysqldump='mysqldump -p'
alias objdump='objdump -Mintel'                 #Use Intel assembly
alias patch='patch -b'
alias ssh='ssh -XY'
alias tree='tree -C'

# New commands
alias clean='trash -f \#* *~ .*~ *.bak .*.bak  *.tmp .*.tmp core a.out'
alias errecho='echo >/dev/stderr'
alias texclean='trash -f *.toc *.aux *.log *.cp *.fn *.tp *.vr *.pg *.ky'
alias vimpager="vim -u ~/.vimpager"
alias vimmanpager="vim -u ~/.vimmanpager"

list() {
    git status >/dev/null 2>/dev/null
    if [[ $? == "0" ]]; then
        echo -e "${RWHITE}Git branch:${RNORMAL}"
        git branch | indent
        git status --untracked-files=no | grep nothing > /dev/null
        if [[ $? != "0" ]]; then
            echo -e "\n${RWHITE}Git status:${RNORMAL}"
            git status --untracked-files=no | indent
        fi
        echo
    fi
    ls -BX --color=auto $@
}

copy() {
    cp $@
    [[ $? == "0" ]] && list
}

link() {
    ln -s $@
    [[ $? == "0" ]] && list
}

makedir() {
    mkdir $@
    [[ $? == "0" ]] && nav $@
}

move() {
    mv -b $@
    [[ $? == "0" ]] && list
}

nav() {
    cd $@
    [[ $? == "0" ]] && list
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

trash() {
    /usr/bin/trash $@
    [[ $? == "0" ]] && list
}

window_title() {
    echo -ne "\033]0;$*\007"
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
        PROMPT_COMMAND='PS1="$(promptcolor $?)\u@\h${NORMAL}$ "; prompt_title;'
        ;;
    *)
        PROMPT_COMMAND='PS1="$(promptcolor $?)\u@\h:\w${NORMAL}\$ ";'
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
source ~/.bashrc_local
