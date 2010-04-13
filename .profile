# Portable options
export LOCAL_INSTALL=$HOME/.local
PATH=$LOCAL_INSTALL/bin:$PATH
export HISTCONTROL=ignoredups       #Ignore duplicate lines in the history

# Nonportable options
export CLASSPATH=$LOCAL_INSTALL/lib/java
export EDITOR=vim
export GNU_UTILS=$LOCAL_INSTALL/gnu
export MANPAGER="sh -c \"col -b | view -u ~/.vimmanpager -\""
export PAGER="sh -c \"col -b | view -u ~/.vimpager -\""
export PYTHONPATH=$LOCAL_INSTALL/lib/python
