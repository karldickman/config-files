" Vim color file
" Maintainer:  Thorsten Maerz <info@netztorte.de>
" Last Change:  2006 Dec 07
" grey on black
" optimized for TFT panels

set background=dark
highlight clear
if exists("syntax_on")
  syntax reset
endif
"colorscheme default
let g:colors_name = "karl_torte"

" hardcoded colors :
" GUI Comment : #80a0ff = Light blue

" GUI
highlight Normal      guifg=Grey80   guibg=Black
highlight Search      guifg=Black    guibg=#40ffff  gui=NONE
highlight Visual      guifg=Black                   gui=NONE
highlight Cursor      guifg=Black    guibg=#40ff40  gui=NONE
highlight Special     guifg=#ff8840
highlight Comment     guifg=#80a0ff
highlight Function    guifg=white
highlight StatusLine  guifg=blue     guibg=white
highlight Statement   guifg=Yellow                  gui=bold
highlight Operator    guifg=Yellow                  gui=NONE

" Console
highlight Normal      ctermfg=LightGrey  ctermbg=Black
highlight Search      ctermfg=Black      ctermbg=Cyan    cterm=NONE
highlight Visual      ctermfg=Black                      cterm=reverse
highlight Cursor      ctermfg=Black      ctermbg=Green   cterm=NONE
highlight Special     ctermfg=Brown
highlight Comment     ctermfg=Blue
highlight Function    ctermfg=white
highlight StatusLine  ctermfg=blue       ctermbg=white
highlight Statement   ctermfg=Yellow                     cterm=bold
highlight Operator    ctermfg=Yellow                     cterm=NONE

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
