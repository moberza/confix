dnl @synopsis AC_CXX_HAVE_IEEE_MATH
dnl
dnl If the compiler has the double math functions acosh, asinh, atanh,
dnl cbrt, expm1, erf, erfc, isnan, j0, j1, jn, gamma, lgamma, ilogb,
dnl logb, log1p, rint, y0, y1, yn, hypot, nextafter, remainder and
dnl scalb, define HAVE_IEEE_MATH.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-09-27
dnl @license AllPermissive

AC_DEFUN([AC_CXX_HAVE_IEEE_MATH],
[AC_CACHE_CHECK(whether the compiler supports IEEE math library,
ac_cv_cxx_have_ieee_math,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 ac_save_LIBS="$LIBS"
 LIBS="$LIBS -lm"
 AC_TRY_LINK([
#ifndef _ALL_SOURCE
 #define _ALL_SOURCE
#endif
#ifndef _XOPEN_SOURCE
 #define _XOPEN_SOURCE
#endif
#ifndef _XOPEN_SOURCE_EXTENDED
 #define _XOPEN_SOURCE_EXTENDED 1
#endif
#include <math.h>],[double x = 1.0; double y = 1.0; int i = 1;
acosh(x); asinh(x); atanh(x); cbrt(x); expm1(x); erf(x); erfc(x); isnan(x);
j0(x); j1(x); jn(i,x); ilogb(x); logb(x); log1p(x); rint(x);
y0(x); y1(x); yn(i,x);
#ifdef _THREAD_SAFE
gamma_r(x,&i);
lgamma_r(x,&i);
#else
gamma(x);
lgamma(x);
#endif
hypot(x,y); nextafter(x,y); remainder(x,y); scalb(x,y);
return 0;],
 ac_cv_cxx_have_ieee_math=yes, ac_cv_cxx_have_ieee_math=no)
 LIBS="$ac_save_LIBS"
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_ieee_math" = yes; then
  AC_DEFINE(HAVE_IEEE_MATH,,[define if the compiler supports IEEE math library])
fi
])
