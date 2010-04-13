syn clear sqlSpecial

syn match sqlIdentifier /\<\h\w*\>/
syn match sqlIdentifier /`\h\w*`/
syn keyword sqlKeyword auto_increment
syn match sqlKeyword /primary key/
syn keyword sqlConstant true false null
syn keyword sqlType int double time year
syn keyword sqlType unsigned

hi link sqlIdentifier Identifier
hi link sqlConstant Constant
hi link sqlSpecial Special
