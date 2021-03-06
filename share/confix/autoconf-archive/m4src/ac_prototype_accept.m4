dnl @synopsis AC_PROTOTYPE_ACCEPT
dnl
dnl Requires the AC_PROTOTYPE macro.
dnl
dnl Find the type of argument two and three of accept. User must
dnl include the following in acconfig.h:
dnl
dnl  /* Type of second argument of accept */
dnl  #undef ACCEPT_ARG2
dnl
dnl  /* Type of third argument of accept */
dnl  #undef ACCEPT_ARG3
dnl
dnl @category Misc
dnl @author Loic Dachary <loic@senga.org>
dnl @version 2005-01-19
dnl @license GPLWithACException

AC_DEFUN([AC_PROTOTYPE_ACCEPT],[
AC_PROTOTYPE(accept,
 [
  #include <sys/types.h>
  #include <sys/socket.h>
 ],
 [
  int a = 0;
  ARG2 * b = 0;
  ARG3 * c = 0;
  accept(a, b, c);
 ],
 ARG2, [struct sockaddr, void],
 ARG3, [socklen_t, size_t, int, unsigned int, long unsigned int])
])
