syn match dosiniIdentifier  /\<\h\w*\>\ze\s*:/ nextgroup=dosColon skipwhite
syn match dosColon          /:/

highlight link dosiniIdentifier Identifier
highlight link dosColon         dosDelimiter
highlight link dosDelimiter     Delimiter
