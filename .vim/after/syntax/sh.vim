let b:is_bash=1
syn clear     shStatement
if exists("b:is_bash")
  syn clear   bashStatement   bashAdminStatement
  syn match   bashStatement  "[^-]\zs\<\(chmod\|clear\|complete\|du\|egrep\|expr\|ggrep\|find\|gnufind\|gnugrep\|grep\|install\|less\|ls\|mkdir\|mv\|rm\|rmdir\|rpm\|sed\|sleep\|sort\|strip\|tail\|touch\)\>"
  syn match   bashStatement   "[^-]\zs\<\(bind\|builtin\|dirs\|disown\|enable\|help\|local\|logout\|popd\|pushd\|shopt\|source\)\>"
  syn match   bashAdminStatement  "[^-]\zs\<\(daemon\|killall\|killproc\|nice\|reload\|restart\|start\|status\|stop\)\>"
elseif exists("b:is_kornshell")
  syn match   kshStatement    "[^-]\zs\<\(cat\|chmod\|clear\|cp\|du\|egrep\|expr\|fgrep\|find\|grep\|install\|killall\|less\|ls\|mkdir\|mv\|nice\|printenv\|rm\|rmdir\|sed\|sort\|strip\|stty\|tail\|touch\|tput\)\>"
else
  syn match   shStatement     "[^-]\zs\<\(set\|export\|unset\)\>"
  syn match   shStatement     "[^-]\zs\<\(login\|newgrp\)\>"
endif
syn match   shStatement  "[^-]\zs\<\(break\|cd\|chdir\|continue\|eval\|exec\|exit\|kill\|newgrp\|pwd\|read\|readonly\|return\|shift\|test\|trap\|ulimit\|umask\|wait\)\>"
if exists("b:is_kornshell") || exists("b:is_bash")
  syn match   shStatement  "[^-]\zs\<\(autoload\|bg\|false\|fc\|fg\|functions\|getopts\|hash\|history\|integer\|jobs\|let\|nohup\|print\|printf\|r\|stop\|suspend\|time\|times\|true\|type\|unalias\|whence\)\>"
endif

hi link     bashStatement shStatement
hi link     kshStatement  shStatement
hi link     shStatement   Function
hi link     shLoop        shRepeat
