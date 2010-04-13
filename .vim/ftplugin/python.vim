so ~/.vim/scripts/pythoncomplete.vim

let python_highlight_numbers = 1
let python_highlight_builtins = 1
let python_highlight_exceptions = 1
let python_highlight_space_errors = 1
let python_highlight_string_formatting = 1
let python_highlight_indent_errors = 1
let python_highlight_doctests = 1

let python_use_karl_capitalization = 1
let python_highlight_custom_errors = 1

"Make path
setlocal makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
setlocal efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m

"Shortcut key for execution
map <buffer> <C-x> :w<CR>:!/usr/bin/env python %<CR>

setlocal textwidth=79

setlocal omnifunc=pythoncomplete#Complete

python << EOF
import vim
def evaluate_curr_range():
    eval(compile("\n".join(vim.current.range), "", "exec").globals())
EOF

map <C-h> :py evaluate_curr_range()

"Use gf key to go to file where class is declared
python << EOF
import os
import sys
import vim
for p in sys.path:
    if os.path.isdir(p):
        vim.command(r"set path+=%s" % (p.replace(" ", r"\ ")))
EOF

set tags+=$HOME/.vim/tags/python.ctags

" Folding
set foldmethod=expr
set foldexpr=PythonFoldExpr(v:lnum)
set foldtext=PythonFoldText() 

function! PythonFoldText()
    let size = 1 + v:foldend - v:foldstart
    if size < 10
        let size = " " . size
    endif
    if size < 100
        let size = " " . size
    endif
    if size < 1000
        let size = " " . size
    endif
    
    if match(getline(v:foldstart), '"""') >= 0
        let text = substitute(getline(v:foldstart), '"""', '', 'g' ) . ' '
    elseif match(getline(v:foldstart), "'''") >= 0
        let text = substitute(getline(v:foldstart), "'''", '', 'g' ) . ' '
    else
        let text = getline(v:foldstart)
    endif
    
    return size . ' lines:'. text . ' '
endfunction

function! PythonFoldExpr(lnum)
    if indent( nextnonblank(a:lnum) ) == 0
        return 0
    endif
    
    if getline(a:lnum-1) =~ '^\(class\|def\)\s'
        return 1
    endif
        
    if getline(a:lnum) =~ '^\s*$'
        return "="
    endif
    
    if indent(a:lnum) == 0
        return 0
    endif

    return '='
endfunction

" In case folding breaks down
function! ReFold()
    set foldmethod=expr
    set foldexpr=0
    set foldnestmax=1
    set foldmethod=expr
    set foldexpr=PythonFoldExpr(v:lnum)
    set foldtext=PythonFoldText()
    echo
endfunction 
