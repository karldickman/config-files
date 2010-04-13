"Variables and methods
" The following patterns assume the following conventions:
" * Identifiers and functions begin with a lowercase letter
" * Macros are in all caps
" * Types begin with an uppercase letter
syn match       javaIdentifier          "\<\h\w*\>"
syn match       javaFunction            /\<\h\w*\>\s*(/me=e-1
syn match       javaType                "\<\u\(\w\&[^(]\)*\>"
syn cluster     javaTop                 add=javaIdentifier,javaFunction,javaLogicalOperator

"Highlihgting variables overrides some keywords
syn keyword     javaClassDecl           class
syn keyword     javaKeyword             extends implements
syn keyword     javaExternal            import nextgroup=javaImported skipwhite
syn match       javaImported            /.*\w*\s*\ze;\s*$/ contained
syn keyword     javaExternal            package nextgroup=javaPackageName skipwhite
syn match       javaPackageName         ".*\w*;$"me=e-1 contained
  
"Operators
syn match       javaOperator            "[-=+%*]"
syn match       javaOperator            +/[^*/]+me=e-1
syn match       javaAssignment          "[-+*/%]="
syn match       javaLogicalOperator     "[!<>]"
syn match       javaLogicalOperator     "[!=<>]="
"syn match       javaBinaryOperator      "\~"
"syn match       javaBinaryOperator      "\~="
"TODO: fix problematic binary operator
"syn match     javaBinaryOperator      "\(\||\|\^\|<<\|>>\)=\="
"Highlight && and || in preference to binary
syn match       javaLogicalOperator     "&&\|||"

"Object should be a type
syn keyword     javaKeyword             this

"Necessary links
hi link         javaIdentifier          Identifier
hi link         javaImported            Constant
hi link         javaPackageName         Constant
hi link         javaFunction            Function
hi link         javaOperator            Operator
hi link         javaAssignment          Operator
hi link         javaLogicalOperator     Operator
hi link         javaBinaryOpeartor      Operator
hi link         javaKeyword             Keyword
