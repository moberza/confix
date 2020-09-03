dnl @synopsis AC_CXX_COMPLEX_MATH_IN_NAMESPACE_STD
dnl
dnl If the C math functions are in the cmath header file and std::
dnl namespace, define HAVE_MATH_FN_IN_NAMESPACE_STD.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_COMPLEX_MATH_IN_NAMESPACE_STD],
[AC_CACHE_CHECK(whether complex math functions are in std::,
ac_cv_cxx_complex_math_in_namespace_std,
[AC_REQUIRE([AC_CXX_NAMESPACES])
 AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([#include <complex>
namespace S { using namespace std;
              complex<float> pow(complex<float> x, complex<float> y)
              { return std::pow(x,y); }
            };
],[using namespace S; complex<float> x = 1.0, y = 1.0; S::pow(x,y); return 0;],
 ac_cv_cxx_complex_math_in_namespace_std=yes, ac_cv_cxx_complex_math_in_namespace_std=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_complex_math_in_namespace_std" = yes; then
  AC_DEFINE(HAVE_COMPLEX_MATH_IN_NAMESPACE_STD,,
            [define if complex math functions are in std::])
fi
])
