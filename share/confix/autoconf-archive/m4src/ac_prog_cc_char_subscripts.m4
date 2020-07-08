dnl @synopsis AC_PROG_CC_CHAR_SUBSCRIPTS(substvar [,hard])
dnl
dnl Try to find a compiler option that enables usage of char-type to
dnl index a value-field. This one needs unsigned-chars and it must
dnl suppress warnings about usage of chars for subscripting. for gcc
dnl -funsigned-char -Wno-char-subscripts
dnl
dnl Currently this macro knows about GCC. hopefully will evolve to use:
dnl Solaris C compiler, Digital Unix C compiler, C for AIX Compiler,
dnl HP-UX C compiler, and IRIX C compiler.
dnl
dnl @category C
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2001-04-27
dnl @license GPLWithACException

AC_DEFUN([AC_PROG_CC_CHAR_SUBSCRIPTS], [
  pushdef([CV],ac_cv_prog_cc_char_subscripts)dnl
  hard=$2
  if test -z "$hard"; then
    msg="C to enable char subscripts"
  else
    msg="C to ensure char subscripts"
  fi
  AC_CACHE_CHECK($msg, CV, [
  cat > conftest.c <<EOF
int main (void)
{
   char v = 1;
   int x[[2]] = { 3 , 4 };
   return x[[v]];
}
EOF
  cp conftest.c writetest.c
  dnl GCC
  if test "$GCC" = "yes";
  then
      	if test -z "$hard"; then
      	   CV="-funsigned-char -Wno-char-subscripts"
    	else
      	   CV="-funsigned-char -Wno-char-subscripts"
    	fi

    	if test -n "`${CC-cc} -c $CV conftest.c 2>&1`" ; then
           CV="suppressed: did not work"
    	fi

  dnl Solaris C compiler
	# Solaris sunpro has no option for unsignedchar but
	# signedchar is the default for char. Duhh.

  dnl HP-UX C compiler

  dnl Digital Unix C compiler
  elif ! $CC > /dev/null 2>&1 &&
	$CC -c -unsigned conftest.c > /dev/null 2>&1 &&
	test -f conftest.o
  then
	# char :  unsigned char
	CV="-unsigned"

	rm conftest.o
    	if test -n "`${CC-cc} -c $CV conftest.c 2>&1`" ; then
           CV="suppressed: did not work"
    	fi

  dnl C for AIX Compiler

  dnl IRIX C compiler
	# char is unsigned by default for IRIX C.

  fi
  rm -f conftest.*
  ])
  if test -z "[$]$1" ; then
    if test -n "$CV" ; then
      case "$CV" in
        suppressed*) $1="" ;; # known but suppressed
        *)  $1="$CV" ;;
      esac
    fi
  fi
  AC_SUBST($1)
  popdef([CV])dnl
])
