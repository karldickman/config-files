"syn match csInterface /\<I\u\w*\>/
syn match csGenericType /\<\h\w*<\h\w*>/
syn match csConstant /\<\u*\>/
syn match csLocalVariable /\<\l\w*\>/
syn match csFunction /\<\h\w*\s*(/me=e-1
syn keyword csNull null
syn keyword csBoolean true
syn keyword csBoolean false
syn match csOperator        "[-=+%*&|\^]"
syn match csOperator          "/[^/]"
syn match csAssignment      "[-+*/%]="
syn match csRelation        "[<>]"
syn match csRelation        "[!=<>]="
syn match csClass /\u\w*\ze\.\w\+(/
syn match csClass /class\s\+\zs\w\+/

hi link csGenericType csType
hi link csClass csType
hi link csConstant csIdentifier
hi link csLocalVariable csIdentifier
hi link csIdentifier Identifier
hi link csFunction Function
hi link csNull Constant
hi link csBoolean Constant
hi Function gui=bold
hi link csAssignment csOperator
hi link csRelation csOperator
hi link csOperator Operator
