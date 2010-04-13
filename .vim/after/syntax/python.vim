if !exists("python_use_karl_capitalization")
  let python_use_karl_capitalization = 0
endif
if python_use_karl_capitalization == 1
  " The following patterns assume the following conventions:
  " * Identifiers and functions begin with a lowercase letter
  " * Macros are in all caps
  " * Types begin with an uppercase letter
  syn match   pythonType            /\<\u\+\U\(\w\&[^(]\)*\>/
  syn match   pythonIdentifier      /\<[a-z_]\w*\>\ze[^'"]\?/
  syn match   pythonFinalIdentifier /\<\u\(\u\|\d\|_\)*\>/
else
  syn match   pythonIdentifier      /\<\h\w*\>[^'"]\?/
endif
syn match   pythonFunction        /\<\U\w*\>\ze\s*(/
"syn match   pythonFunction        /\<\u\+\w*\>\ze\s*(/

" Numbers overwritten by identifier highlighting
syn match   pythonHexNumber	      "\<0[xX]\x\+[lL]\=\>" display
syn match   pythonHexNumber	      "\<0[xX]\>" display
syn match   pythonBinNumber	      "\<0[bB]\x\+[lL]\=\>" display
syn match   pythonBinNumber	      "\<0[bB]\>" display
syn match   pythonNumber	        "\<\d\+[lLjJ]\=\>" display
syn match   pythonFloat		        "\.\d\+\([eE][+-]\=\d\+\)\=[jJ]\=\>" display
syn match   pythonFloat		        "\<\d\+[eE][+-]\=\d\+[jJ]\=\>" display
syn match   pythonFloat		        "\<\d\+\.\d*\([eE][+-]\=\d\+\)\=[jJ]\=" display

" Raw strings overwritten by identifier highlighting
syn region pythonRawString	start=+[rR]'+ skip=+\\\\\|\\'\|\\$+ excludenl end=+'+ end=+$+ keepend contains=pythonRawEscape,@Spell
syn region pythonRawString	start=+[rR]"+ skip=+\\\\\|\\"\|\\$+ excludenl end=+"+ end=+$+ keepend contains=pythonRawEscape,@Spell
syn region pythonRawString	start=+[rR]"""+ end=+"""+ keepend contains=pythonDocTest2,pythonSpaceError,@Spell
syn region pythonRawString	start=+[rR]'''+ end=+'''+ keepend contains=pythonDocTest,pythonSpaceError,@Spell

syn region pythonUniRawString	start=+[uU][rR]'+ skip=+\\\\\|\\'\|\\$+ excludenl end=+'+ end=+$+ keepend contains=pythonRawEscape,pythonUniRawEscape,pythonUniRawEscapeError,@Spell
syn region pythonUniRawString	start=+[uU][rR]"+ skip=+\\\\\|\\"\|\\$+ excludenl end=+"+ end=+$+ keepend contains=pythonRawEscape,pythonUniRawEscape,pythonUniRawEscapeError,@Spell
syn region pythonUniRawString	start=+[uU][rR]"""+ end=+"""+ keepend contains=pythonUniRawEscape,pythonUniRawEscapeError,pythonDocTest2,pythonSpaceError,@Spell
syn region pythonUniRawString	start=+[uU][rR]'''+ end=+'''+ keepend contains=pythonUniRawEscape,pythonUniRawEscapeError,pythonDocTest,pythonSpaceError,@Spell

syn match   pythonOperator        "[-=+%*/&|\^]"
"syn match   pythonOperator        +/[^*/]+me=e-1
syn match   pythonAssignment      "[-+*/%]="
syn match   pythonRelation        "[<>]"
syn match   pythonRelation        "[!=<>]="

syn keyword pythonKeyword         self cls as

syn keyword pythonBoolean         True False
syn keyword pythonConstant        None

syn clear   pythonBuiltinFunc
syn match   pythonFunction        /\(^\|[^.]\)\zs\(__import__\|abs\|all\|any\|apply\|callable\|chr\|cmp\|coerce\|compile\|delattr\|dir\|divmod\|eval\|filter\|getattr\|globals\|hasattr\|hash\|help\|hex\|id\|input\|intern\|isinstance\|issubclass\|iter\|len\|locals\|map\|max\|min\|oct\|open\|ord\|pow\|range\|raw_input\|reduce\|reload\|repr\|reversed\|round\|setattr\|sorted\|sum\|unichr\|vars\|zip\)\>/
syn match   pythonGenerator       /\(^\|[^.]\)\zs\(enumerate\|xrange\)\>/
syn match   pythonType            /\(^\|[^.]\)\zs\(basestring\|bool\|buffer\|classmethod\|complex\|dict\|execfile\|file\|float\|frozenset\|int\|list\|long\|object\|property\|set\|slice\|staticmethod\|str\|super\|tuple\|type\|unicode\)\>/

"syn keyword pythonImport         import from as nextgroup=pythonImported skipwhite
syn clear   pythonImport
syn region  pythonImport          start="import\>\|from\>" end="$" contains=pythonImportKeyword
syn keyword pythonImportKeyword import from as contained


"Catch syntax errors
"syn match   pythonError           /^\s*def\s\+\w\+(.*)\s*$/ display
"syn match   pythonError           /^\s*class\s\+\w\+(.*)\s*$/ display
"syn match   pythonError           /^\s*for\s.*[^:]$/ display
"syn match   pythonError           /^\s*except\s*$/ display
"syn match   pythonError           /^\s*finally\s*$/ display
"syn match   pythonError           /^\s*try\s*$/ display
"syn match   pythonError           /^\s*else\s*$/ display
"syn match   pythonError           /^\s*else\s*[^:].*/ display
"syn match   pythonError           /^\s*if\s.*[^\:]$/ display
"syn match   pythonError           /^\s*except\s.*[^\:]$/ display
"syn match   pythonError           /[;]$/ display
"syn keyword pythonError           do

if !exists("python_highlight_custom_errors")
  let python_highlight_custom_errors = 0
endif
if python_highlight_custom_errors == 1
  syn match   pythonExClass         "\<\h\w*Error\>"
endif

hi link     pythonAssignment      Operator
hi link     pythonBoolean         Boolean
hi link     pythonConstant        Constant
hi link     pythonExClass         Constant
hi link     pythonException       Exception
hi link     pythonFormat          Special
hi link     pythonGenerator       pythonFunction
hi link     pythonIdentifier      Identifier
hi link     pythonFinalIdentifier pythonIdentifier
hi link     pythonImport          Constant
hi link     pythonImportKeyword   Include
hi link     pythonKeyword         Keyword
hi link     pythonRelation        Operator
hi link     pythonStructure       Structure
hi link     pythonType            Type
hi link     pythonBinNumber       pythonNumber
