export LOCAL_INSTALL=$HOME/.local
PATH=$LOCAL_INSTALL/bin:$PATH
export EDITOR=vim
export MANPAGER="sh -c \"col -b | view -u ~/.vimmanpager -\""
export PAGER="sh -c \"col -b | view -u ~/.vimpager -\""
export PYTHONPATH=$LOCAL_INSTALL/lib/python

if [[ -e "~/.profile_local" ]]
then
    source ~/.profile_local
fi
