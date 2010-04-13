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

alias cowsay='cowsay -f bong -s'
alias gcc='gcc -masm=intel'                     #Use Intel assembly
alias gnome-terminal='gnome-terminal --geometry=125x43'
alias gvim='gvim -geometry 125x43'
alias objdump='objdump -Mintel'                 #Use Intel assembly
alias patch='patch -b'
alias ssh='ssh -XY'
alias tree='tree -C'
alias zigford='zigford -v'

# New commands
alias clean='trash -f \#* *~ .*~ *.bak .*.bak  *.tmp .*.tmp core a.out'
alias errecho='echo >/dev/stderr'
alias list='ls -X -B --color=auto'
alias texclean='trash -f *.toc *.aux *.log *.cp *.fn *.tp *.vr *.pg *.ky'
alias vimpager="vim -u ~/.vimpager"
alias vimmanpager="vim -u ~/.vimmanpager"

copy() {
    cp $@
    [[ $? == "0" ]] && list
}

link() {
    ln -s $@
    [[ $? == "0" ]] && list
}

move() {
    mv -b $@
    [[ $? == "0" ]] && list
}

makedir() {
    mkdir $@
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

#Colorings
export RESET="\[\017\]"
export NORMAL="\[\033[0m\]"
export GRAY="\[\033[30;1m\]"
export RED="\[\033[31;1m\]"
export GREEN="\[\033[32;1m\]"
export YELLOW="\[\033[33;1m\]"
export BLUE="\[\033[34;1m\]"
export PURPLE="\[\033[35;1m\]"
export CYAN="\[\033[36;1m\]"
export WHITE="\[\033[37;1m\]"

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
[[ -f /etc/bash_completion ]] && source /etc/bash_completion

# Moddifications to shell behavior
shopt -s checkwinsize   #Check window size
set -o vi       #vi mode for command entry
