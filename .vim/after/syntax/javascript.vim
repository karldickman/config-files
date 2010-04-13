syn match   javaScriptIdentifier    "<\h\w*\>"

syn match   javaScriptFunctionName  "\<\h\w*\>\s*("me=e-1

syn match   javaScriptOperator      "[-=+%*]"
syn match   javaScriptOperator      "/[^*/]"me=e-1
syn match   javaScriptAssignment    #[-+*/%]=#
syn match   javaScriptRelation      "[!<>]\|&&\|||"
syn match   javaScriptRelation      "[!=<>]="

syn keyword javaScriptBranch        exit

syn keyword javaScriptKeyword       var this function

syn clear   javaScriptBraces

hi link     javaScriptKeyword       Keyword
hi link     javaScriptNumber        Number
