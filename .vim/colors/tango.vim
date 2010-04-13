" Vim color file
" Maintainer:  Karl Dickman <karldickman@gmail.com>
" Last Change:  2008 Apr 03

highlight clear
if exists("syntax_on")
  syntax reset
endif

let colors_name = "tango"

set background=dark

" GUI
highlight Normal      guifg=#d3d7cf guibg=#000030
highlight Search      guifg=#2e3436 guibg=#34e2e2 gui=NONE
highlight Visual      guifg=#2e3436               gui=NONE
highlight Cursor      guifg=#2e3436 guibg=#8fe234 gui=NONE
highlight StatusLine  guifg=blue    guibg=#eeeeec

highlight Identifier  guifg=#34e2e2
highlight Function    guifg=#eeeeec
highlight Statement   guifg=#fce94f               gui=bold
highlight Operator    guifg=#fce94f               gui=NONE
highlight Type        guifg=#8fe234
highlight Comment     guifg=#80a0ff

" Console
highlight Normal      ctermfg=LightGrey ctermbg=Black
highlight Search      ctermfg=Black     ctermbg=Cyan  cterm=NONE
highlight Visual      ctermfg=Black                   cterm=reverse
highlight Cursor      ctermfg=Black     ctermbg=Green cterm=NONE
highlight Special     ctermfg=Brown
highlight Comment     ctermfg=Blue
highlight Function    ctermfg=white
highlight StatusLine  ctermfg=blue      ctermbg=white
highlight Statement   ctermfg=Yellow                  cterm=bold
highlight Operator    ctermfg=Yellow                  cterm=NONE

" only for vim 5
if has("unix")
  if v:version<600
    highlight Normal  ctermfg=Grey    ctermbg=Black   cterm=NONE  guifg=Grey80      guibg=Black   gui=NONE
    highlight Search  ctermfg=Black   ctermbg=Red     cterm=bold  guifg=Black       guibg=Red     gui=bold
    highlight Visual  ctermfg=Black   ctermbg=yellow  cterm=bold  guifg=#404040                   gui=bold
    highlight Special ctermfg=LightBlue               cterm=NONE  guifg=LightBlue                 gui=NONE
    highlight Comment ctermfg=Cyan                    cterm=NONE  guifg=LightBlue                 gui=NONE
  endif
endif
