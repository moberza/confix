dnl @synopsis MERK_SIP_DEVEL([<min_version>])
dnl
dnl Searches for the sip executable and the sip include path. The sip
dnl include path consists of two components, one which contains the
dnl file qt/qtmod.sip and the other one the path to sip.h, which should
dnl be found in the include/pythonX.Y directory.
dnl
dnl The macro bails out if the executable or the file cannot be
dnl located. Otherwise it defines:
dnl
dnl   SIP           the path to the sip executable
dnl   SIP_CPPFLAGS  include path: -I<path-to-qt/qtmod.sip> -I<path-to-sip.h-dir>
dnl
dnl Example:
dnl
dnl   MERK_SIP_DEVEL
dnl   MERK_SIP_DEVEL([4.1])
dnl
dnl Requires: perl (for version string comparison)
dnl
dnl @category InstalledPackages
dnl @author Uwe Mayer <merkosh@hadiko.de>
dnl @version 2005-06-03
dnl @license AllPermissive

AC_DEFUN([MERK_SIP_DEVEL],[
#-- provice --with-sip=PATH command line argument
AC_ARG_WITH([sip],
        AS_HELP_STRING([--with-sip=PATH], [specify the location of the qt/qtmod.sip file]),
        [sip_search_dir="$withval"],
        [sip_search_dir=""])

#-- check for sip executable
AC_PATH_PROG([SIP], [sip], [no])
if test x"$SIP" == x"no"; then
        AC_MSG_ERROR([failed to find required command sip])
fi
AC_SUBST([SIP])

#-- check for minimum sip version
if test x"$1" != x""; then
        AC_CHECK_PROG([PERL], [perl], [$(which perl)])
        if test x"$PERL" == x""; then
                AC_MSG_ERROR([perl required for checking sip version])
        fi
        AC_MSG_CHECKING([sip version >= $1])
        sip_version=$($SIP -V |cut -f 1 -d " ")
        merk_sip_devel_result=$(echo "$sip_version" |perl -e '("$1" lt <STDIN>) && print "ok"')
        if test x"$merk_sip_devel_result" == x""; then
                AC_MSG_RESULT([$sip_version])
                AC_MSG_ERROR([a newer version of sip is required])
        else
                AC_MSG_RESULT([ok])
        fi
fi

#-- Check for SIP include path
AC_MSG_CHECKING([for sip include path])

# check for qt/qtmod.sip
for i in "$sip_search_dir" "/usr/share/sip"; do
        sip_path1=`find $i -type f -name qtmod.sip -print | sed "1q"`
        if test -n "$sip_path1"; then
                break
        fi
done

sip_path1=`echo "$sip_path1" | sed 's,/qt/qtmod.sip,,'`
if test -z "$sip_path1" ; then
        AC_MSG_ERROR([cannot find qt/qtmod.sip; try --with-sip=PATH])
fi

# check for sip.h
dnl this part of the code to detect python version and include path
dnl  was taken from ac_python_devel macro, (rev. 2005-06-03)
python_path=`echo $PYTHON | sed "s,/bin.*$,,"`
for i in "$python_path/include/python$PYTHON_VERSION/" "$python_path/include/python/" "$python_path/" ; do
	python_path=`find $i -type f -name Python.h -print | sed "1q"`
        if test -n "$python_path" ; then
        	break
        fi
done
sip_path2=`echo $python_path | sed "s,/Python.h$,,"`
if ! test -f "$sip_path2/sip.h"; then
	AC_MSG_ERROR([cannot find include path to sip.h])
fi

AC_MSG_RESULT([$sip_path1,$sip_path2])

AC_SUBST([SIP_CPPFLAGS],["-I$sip_path1 -I$sip_path2"])
])
