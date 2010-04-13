syn match   SCConstant    /\U/
syn match   SCIdentifier  /\u/
syn match   SCOperator    /[=/#_()]/
syn region  SCComment     start=/\*/ end=/$/

hi link     SCIdentifier  Identifier
hi link     SCConstant    Constant
hi link     SCOperator    Operator
hi link     SCComment     Comment
