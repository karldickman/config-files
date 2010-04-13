"syn match   perlType            /\<\u\(\w\&[^(]\)*\>/
syn match   perlFunction        /\<\U\w*\>\s*(/me=e-1

syn clear   perlFloat
syn match   perlFloat           /[-+]\=\<\d\+[eE][\-+]\=\d\+/
syn match   perlFloat           /[-+]\=\<\d\+\.\d\+\([eE][\-+]\=\d\+\)\=/
syn match   perlFloat           /[-+]\=\<\.\d\+\([eE][\-+]\=\d\+\)\=/    

hi link     perlFloat     Float
