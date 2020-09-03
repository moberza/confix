dnl @synopsis AC_CXX_USE_NUMTRAIT
dnl
dnl If the compiler supports numeric traits promotions, define
dnl HAVE_USE_NUMTRAIT.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_USE_NUMTRAIT],
[AC_CACHE_CHECK(whether the compiler supports numeric traits promotions,
ac_cv_cxx_use_numtrait,
[AC_REQUIRE([AC_CXX_TYPENAME])
 AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([
#ifndef HAVE_TYPENAME
 #define typename
#endif
template<class T_numtype> class SumType       { public : typedef T_numtype T_sumtype;   };
template<>                class SumType<char> { public : typedef int T_sumtype; };
template<class T> class A {};
template<class T> A<typename SumType<T>::T_sumtype> sum(A<T>)
{ return A<typename SumType<T>::T_sumtype>(); }
],[A<float> x; sum(x); return 0;],
 ac_cv_cxx_use_numtrait=yes, ac_cv_cxx_use_numtrait=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_use_numtrait" = yes; then
  AC_DEFINE(HAVE_USE_NUMTRAIT,,[define if the compiler supports numeric traits promotions])
fi
])
