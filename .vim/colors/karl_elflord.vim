" local syntax file - set colors on a per-machine basis:
" vim: tw=0 ts=4 sw=4
" Vim color file
" Maintainer:	Ron Aaron <ron@ronware.org>
" Last Change:	2003 May 02

set background=dark
highlight clear
if exists("syntax_on")
  syntax reset
endif
let g:colors_name = "karl_elflord"

highlight Normal		guifg=cyan			guibg=black
highlight Comment	term=bold		ctermfg=DarkCyan		guifg=#80a0ff
highlight Constant	term=underline	ctermfg=Magenta		guifg=Magenta
" guifg was formerly Red
highlight Special	term=bold		ctermfg=DarkMagenta	guifg=#ffff40
highlight Identifier term=underline	cterm=bold			ctermfg=Cyan guifg=#40ffff
highlight Statement term=bold		ctermfg=Yellow gui=bold	guifg=#aa4444
highlight PreProc	term=underline	ctermfg=LightBlue	guifg=#ff80ff
highlight Type	term=underline		ctermfg=LightGreen	guifg=#60ff60 gui=bold
highlight Function	term=bold		ctermfg=White guifg=White
highlight Repeat	term=underline	ctermfg=White		guifg=white
" ctermfg and guifg were originally Red
highlight Operator				ctermfg=Yellow			guifg=#ffff40
highlight Ignore				ctermfg=black		guifg=bg
highlight Error	term=reverse ctermbg=Red ctermfg=White guibg=Red guifg=White
highlight Todo	term=standout ctermbg=Yellow ctermfg=Black guifg=Blue guibg=Yellow

" Common groups that link to default highlighting.
" You can specify other highlighting easily.
highlight link String	Constant
highlight link Character	Constant
highlight link Number	Constant
highlight link Boolean	Constant
highlight link Float		Number
highlight link Conditional	Repeat
highlight link Label		Statement
highlight link Keyword	Statement
highlight link Exception	Statement
highlight link Include	PreProc
highlight link Define	PreProc
highlight link Macro		PreProc
highlight link PreCondit	PreProc
highlight link StorageClass	Type
highlight link Structure	Type
highlight link Typedef	Type
highlight link Tag		Special
highlight link SpecialChar	Special
highlight link Delimiter	Special
highlight link SpecialComment Special
highlight link Debug		Special
