set spelllang=en_us

set viminfo='20,<50,%,!

filetype on
filetype plugin on
filetype indent on

autocmd! bufwritepost vimrc source ~/.vimrc

colorscheme tango

syntax on

" ==User interface==
set cursorline

set scrolloff=3
set paste

set wildmenu

set ruler
set number
set laststatus=2

set backspace=indent,eol,start

set wrapscan
set hlsearch
set incsearch
set magic

set showcmd             " Show partial command in the last line of the screen

set history=400         " Expand history to 400

set mouse=a


set showmatch
set matchtime=2

" ==Moving around and tabs==
map <C-J> <C-W>j
map <C-K> <C-W>k
map <C-H> <C-W>h
map <C-L> <C-W>l
map <C-_> <C-W>_

map <leader>tn :tabnew<cr>
map <leader>te :tabedit
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove

" ==Text options==
set shiftwidth=4
set tabstop=4
set softtabstop=4
set expandtab
set smarttab
set shiftround

set textwidth=79
set nowrap
set linebreak

set smartindent

"set cinoptions=>s,e0,n0,fs,{s,}0,^s,:s,=s,l1,gs,hs,ts,cs,C0,/s,(s,us,U1,w0,m0

source ~/.vim/scripts/commands.vim
source ~/.vim/scripts/minibufexpl.vim
"source ~/.vim/scripts/taglist.vim
source ~/.vim/scripts/tasklist.vim
source ~/.vim/scripts/localvimrc.vim
source ~/.vim/scripts/NERD_tree.vim
