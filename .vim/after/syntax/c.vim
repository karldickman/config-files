" Better highlighting for octal zero
syn clear cOctalZero
syn match cOctalZero contained "0[1-7]"me=e-1

" GTK syntax stuff
"let glib_deprecated_errors = 1
"let gobject_deprecated_errors = 1
"let gdk_deprecated_errors = 1
"let gdkpixbuf_deprecated_errors = 1
"let gtk_deprecated_errors = 1
"let gimp_deprecated_errors = 1

"runtime! syntax/glib.vim
"runtime! syntax/gobject.vim
"runtime! syntax/gdk.vim
"runtime! syntax/gdkpixbuf.vim
"runtime! syntax/gtk.vim
"runtime! syntax/gimp.vim
