# Portable options
PATH=$HOME/.local/bin:$PATH
export HISTCONTROL=ignoredups       #Ignore duplicate lines in the history

# Nonportable options
export CLASSPATH=$HOME/.local/lib/java
export CVSROOT=~/.local/share/cvs
export EDITOR=vim
export DJANGO=/usr/share/python-support/python-django
export JAVA_HOME=/usr/lib/jvm/java-6-openjdk
export LIBCHECKLOC=/usr/lib
export LOCAL_INSTALL=$HOME/.local
export MANPAGER="sh -c \"col -b | view -u ~/.vimmanpager -\""
export PAGER="sh -c \"col -b | view -u ~/.vimpager -\""
export PYTHONPATH=$HOME/.local/lib/python
export TEXINPUTS=".:$LOCAL_INSTALL/share/texmf//:"
export XCA_CNX=mysql://xcanalyze@localhost/xca_database
export XCA_CNXT=mysql://xcanalyze@localhost/xca_test
