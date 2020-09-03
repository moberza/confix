dnl @synopsis AG_CHECK_ALLOCATED_CTIME
dnl
dnl Check whether we need to free the memory returned by ctime.
dnl
dnl @category C
dnl @author Bruce Korb <bkorb@gnu.org>
dnl @version 2001-12-01
dnl @license GPLWithACException

dnl DO NOT EDIT THIS FILE   (ag_check_allocated_ctime.m4)
dnl
dnl It has been AutoGen-ed  Saturday December  1, 2001 at 09:21:27 PM PST
dnl From the definitions    bkorb.def
dnl and the template file   conftest.tpl
dnl See: http://autogen.sf.net for a description of the AutoGen project
dnl
AC_DEFUN([AG_CHECK_ALLOCATED_CTIME],[
  AC_MSG_CHECKING([whether ctime() allocates memory for its result])
  AC_CACHE_VAL([ag_cv_allocated_ctime],[
  AC_TRY_RUN([#include <time.h>
int main (int argc, char** argv) {
   time_t  timeVal = time( (time_t*)NULL );
   char*   pzTime  = ctime( &timeVal );
   free( (void*)pzTime );
   return 0; }],[ag_cv_allocated_ctime=yes],[ag_cv_allocated_ctime=no],[ag_cv_allocated_ctime=no]
  ) # end of TRY_RUN]) # end of CACHE_VAL

  AC_MSG_RESULT([$ag_cv_allocated_ctime])
  if test x$ag_cv_allocated_ctime = xyes
  then
    AC_DEFINE(HAVE_ALLOCATED_CTIME, 1,
       [Define this if ctime() allocates memory for its result])
  fi
]) # end of AC_DEFUN of AG_CHECK_ALLOCATED_CTIME
