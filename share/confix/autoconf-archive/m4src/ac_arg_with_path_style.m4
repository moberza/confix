dnl @synopsis AC_ARG_WITH_PATH_STYLE
dnl
dnl _AC_DEFINE(PATH_STYLE) describing the filesys interface. The value
dnl is numeric, where the basetype is encoded as 16 = dos/win, 32 =
dnl unix, 64 = url/www, 0 = other
dnl
dnl some extra semantics are described in other bits of the value,
dnl especially
dnl
dnl  1024  accepts "/" as a dir separator
dnl  2048  accepts ";" as a path separator
dnl  4096  accepts "," as a path separator
dnl
dnl the macro provides a configure' --with-path-style option that can
dnl be used with descriptive arg names. If not explicitly given, the
dnl $target_os will be checked to provide a sane default. Additional
dnl (lower) bits can be used by the user for some additional magic,
dnl higher bits are reserved for this macro.
dnl
dnl the mnemonic "strict" or "also" is used to instruct the code that
dnl additional seperators shall be accepted but converted to the
dnl seperator of the underlying pathstyle system. (or-512)
dnl
dnl  example: --with-path-style=win,slash
dnl           to make it accept ";" as pathsep, and
dnl           both "/" and "\" as dirseps.
dnl
dnl @category Misc
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2005-12-18
dnl @license GPLWithACException

AC_DEFUN([AC_ARG_WITH_PATH_STYLE],
[
 AC_ARG_WITH(path-style,
[  --with-path-style=[dos,unix,url,also,slash,comma],
[ac_with_path_style="$withval"],
[dnl
  case "$target_os" in
    *djgpp | *mingw32* | *emx*) ac_with_path_style="dos" ;;
    *) case `eval echo $exec_prefix` in
       *:*) ac_with_path_style="url" ;;
       *) ac_with_path_style="posix" ;;
       esac
    ;;
  esac
])
   case ",$ac_with_path_style," in
    *,unx,*|*,unix,*|*,bsd,*|*,posix,*) :
	ac_with_path_style__unx="32" ;;
    *) 	ac_with_path_style__unx="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,dos,*|*,win,*|*,windows,*) :
	ac_with_path_style__dos="16" ;;
    *)  ac_with_path_style__dos="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,web,*|*,url,*|*,www,*) :
	ac_with_path_style__url="64" ;;
    *) 	ac_with_path_style__url="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,mac,*|*,macintosh,*|*,apple,*) :
	ac_with_path_style__mac="128" ;;
    *) 	ac_with_path_style__mac="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,def,*|*,define,*|*,special,*) :
	ac_with_path_style__def="256" ;;
    *) 	ac_with_path_style__def="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,also,*|*,strict,*|*,accept,*|*,convert,*) :
	ac_with_path_style__use="512" ;;
    *) 	ac_with_path_style__use="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,sl,*|*,slash,*|*,forwslash,*|*,slashsep,*) :
	ac_with_path_style__slash="1024" ;;
    *) 	ac_with_path_style__slash="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,sc,*|*,semi,*|*,semisep,*|*,semicolon,*|*,semicolonsep,*) :
	ac_with_path_style__semic="2048" ;;
    *) 	ac_with_path_style__semic="0" ;;
   esac
   case ",$ac_with_path_style," in
    *,cm,*|*,comma,*|*,commasep,*) :
	ac_with_path_style__comma="4096" ;;
    *) 	ac_with_path_style__comma="0" ;;
   esac

   if test "$ac_with_path_style__unx" != "0" ; then
	ac_with_path_style__slash="1024"
   fi
   if test "$ac_with_path_style__dos" != "0" ; then
	ac_with_path_style__semic="2048"
   fi
   if test "$ac_with_path_style__url" != "0" ; then
	ac_with_path_style__slash="1024"
	ac_with_path_style__semic="2048"
   fi

   case ",$ac_with_path_style," in
    *,7,*|*,all,*|*,muchmore,*)
	ac_with_path_style__level="7" ;;
    *,6,*|*,extra,*|*,manymore,*)
	ac_with_path_style__level="6" ;;
    *,5,*|*,much,*)
	ac_with_path_style__level="5" ;;
    *,4,*|*,many,*)
	ac_with_path_style__level="4" ;;
    *,3,*|*,plus,*|*,somemore,*)
	ac_with_path_style__level="3" ;;
    *,2,*|*,more,*)
	ac_with_path_style__level="2" ;;
    *,1,*|*,some,*)
	ac_with_path_style__level="1" ;;
    *)
	ac_with_path_style__level="0" ;;
   esac

   PATH_STYLE=`expr \
	$ac_with_path_style__unx '+' \
	$ac_with_path_style__dos '+' \
	$ac_with_path_style__win '+' \
	$ac_with_path_style__mac '+' \
	$ac_with_path_style__def '+' \
	$ac_with_path_style__use '+' \
	$ac_with_path_style__slash '+' \
	$ac_with_path_style__semic '+' \
	$ac_with_path_style__comma '+' \
        $ac_with_path_style__level `

 AC_DEFINE_UNQUOTED(PATH_STYLE,$PATH_STYLE,
 [ the OS pathstyle, 16=dos 32=unx 64=url 1024=slash 2048=semic 4096=comma ])
])
