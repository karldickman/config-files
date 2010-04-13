" Compare current buffer to original file
command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis | wincmd p | diffthis

" Finds all files containing the word under the cursor
map \* "syiw:Grep^Rs<cr>
function! Grep(name)
    let l:pattern = input("Other pattern: ")
    "let l:_name = substitute(a:name, '\\s', '*', 'g')
    let l:list=system("grep -nIR '".a:name."' * | grep -v 'svn-base' | grep '" .l:pattern. "' | cat -n -")
        let l:num=strlen(substitute(l:list, "[^\n]", "", "g"))
        if l:num < 1
            echo "'".a:name."' not found"
            return
        endif

        echo l:list
        let l:input=input("Which?\n")

        if strlen(l:input)==0
            return
        endif

        if strlen(substitute(l:input, "[0-9]", "", "g"))>0
            echo "Not a number"
            return
        endif

        if l:input<1 || l:input>l:num
            echo "Out of range"
            return
        endif

        let l:line=matchstr("\n".l:list, "".l:input."\t[^\n]*")
        let l:lineno=matchstr(l:line,":[0-9]*:")
        let l:lineno=substitute(l:lineno,":","","g")
        "echo ''.l:line
        let l:line=substitute(l:line, "^[^\t]*\t", "", "")
        "echo ''.l:line
        let l:line=substitute(l:line, "\:.*", "", "")
        "echo ''.l:line
        "echo '\n'.l:line
        execute ":e ".l:line
        execute "normal ".l:lineno."gg"
    endfunction
command! -nargs=1 Grep :call Grep("<args>")

"Finds all files with the word under the cursor in their name
map \f "syiw:Find^Rs<cr>
function! Find(name)
    let l:_name = substitute(a:name, "\\s", "*", "g")
    let l:list=system("find . -iname '*".l:_name."*' -not -name \"*.class\" -and -not -name \"*.swp\" | perl -ne 'print \"$.\\t$_\"'")
    let l:num=strlen(substitute(l:list, "[^\n]", "", "g"))
    if l:num < 1
        echo "'".a:name."' not found"
        return
    endif

    if l:num != 1
        echo l:list
        let l:input=input("Which ? (=nothing)\n")

        if strlen(l:input)==0
            return
        endif

        if strlen(substitute(l:input, "[0-9]", "", "g"))>0
            echo "Not a number"
            return
        endif

        if l:input<1 || l:input>l:num
            echo "Out of range"
            return
        endif

        let l:line=matchstr("\n".l:list, "\n".l:input."\t[^\n]*")
    else
        let l:line=l:list
    endif

    let l:line=substitute(l:line, "^[^\t]*\t./", "", "")
    "echo ''.l:line
    execute ":e ".l:line
    endfunction
command! -nargs=1 Find :call Find("<args>")
