dnl @synopsis smr_WITH_BUILD_PATH
dnl
dnl This macro adds a "--with-build-path" option to the configure
dnl script. This configure option provides a convenient way to add "-I"
dnl options to CPPFLAGS and "-L" options to LDFLAGS, at configure time.
dnl
dnl Invoking "./configure --with-build-path=DIR" results in "-I
dnl DIR/include" being added to CPPFLAGS if DIR/include exists, and "-L
dnl DIR/lib" being added to LDFLAGS if DIR/lib exists.
dnl
dnl Separate multiple directories using colons; e.g.
dnl "--with-build-path=DIR1:DIR2:DIR3".
dnl
dnl @category InstalledPackages
dnl @author Steve M. Robbins <smr@debian.org>
dnl @version 2001-07-29
dnl @license AllPermissive

AC_DEFUN([smr_WITH_BUILD_PATH],
[
    AC_ARG_WITH([build-path],
    [  --with-build-path=DIR   build using DIR/include and DIR/lib],
    [
        for d in `echo $withval | tr : ' '`; do
            test -d $d/include && CPPFLAGS="$CPPFLAGS -I$d/include"
            test -d $d/lib && LDFLAGS="$LDFLAGS -L$d/lib"
        done
    ])
])
