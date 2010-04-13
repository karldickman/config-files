" General
set mousemodel=popup_setpos
                        "Allow right-click menu
set mousehide           "Automatically hide mouse when typing

set guioptions-=T       "Kill toolbar

map <S-Insert> <MiddleMouse>
                        "Map shift-insert to middle-click

" Colors and fonts
highlight cursorline guibg=#222222
                        "Highlight current line

let do_syntax_sel_menu = 1|runtime! synmenu.vim|aunmenu &Syntax.&Show\ filetypes\ in\ menu
                        "Activate syntax options in menu
