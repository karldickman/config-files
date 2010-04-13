runtime! syntax/yaml.vim

syn keyword kwalifyTypeName       seq map set str int bool null float date
syn keyword kwalifyReserved       mapping sequence required pattern type classname unique enum

highlight link kwalifyTypeName    type
highlight link kwalifyReserved    special
