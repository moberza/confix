dnl @synopsis AX_DIST_MSI([File])
dnl
dnl Adds support for a msi (Microsoft Installer) dist target.
dnl
dnl You must manually build the msi file yourself (probably from
dnl another computer). But it will be added to the list of extra bin
dnl dists and flagged for uploading (see ax_extra_dist.m4 and
dnl ax_upload.m4 for details).
dnl
dnl @category Automake
dnl @author Tom Howard <tomhoward@users.sf.net>
dnl @version 2005-01-14
dnl @license AllPermissive

AC_DEFUN([AX_DIST_MSI],
[
AC_REQUIRE([AX_INSTALL_FILES])
AC_MSG_NOTICE([adding dist-msi support])
MSI_SETUP_FILE="$1"
AC_SUBST(MSI_SETUP_FILE)
if test "x$MSI_SETUP_FILE" != "x"; then
    AC_MSG_NOTICE([setting msi file... $MSI_SETUP_FILE])
    AC_SUBST(USING_DIST_MSI)
    AC_ARG_ENABLE(dist-msi,
		  AS_HELP_STRING(--enable-dist-msi[=ARG],
				 [enable support for msi (Microsoft Installer)
				  dist target. ARG can be
                                  "yes" or "no".  The default is "yes"]),
		  if test "x$enableval" != "x"; then
		      if test "x$enableval" = "xyes"; then
		     	  USING_DIST_MSI=true
		          AC_MSG_NOTICE([dist-msi support enabled])
		      elif test "x$enableval" = "xno"; then
		     	  USING_DIST_MSI=false
		          AC_MSG_NOTICE([dist-msi support disabled])
		      fi
                  fi,
		  USING_DIST_MSI=true
		  AC_MSG_NOTICE([dist-msi support enabled]))
    if test "x$USING_DIST_MSI" = "xtrue"; then
        AX_ADD_AM_MACRO([[

msi dist-msi: \$(top_builddir)/$PACKAGE-$VERSION.msi

\$(top_builddir)/$PACKAGE-$VERSION.msi: \$(top_builddir)/$MSI_SETUP_FILE
	@cp -f \"\$(top_builddir)/$MSI_SETUP_FILE\" \"${AX_DOLLAR}@\"

]])

        if test "x$AX_HAVE_INSTALL_FILES" = "xtrue"; then
            AX_ADD_AM_MACRO([[

\$(top_builddir)/$MSI_SETUP_FILE: \$(top_builddir)/install_files
	@echo \"the msi file ($MSI_SETUP_FILE) must be (re)created\"; \\
	echo \"by building it with VC++\"; \\
	exit -1

]])
        else
            AX_ADD_AM_MACRO([[

\$(top_builddir)/$MSI_SETUP_FILE: msi_up_to_date_notice
	@if test ! -f \"\$(top_builddir)/$MSI_SETUP_FILE\"; then \\
	    echo \"the msi file ($MSI_SETUP_FILE) must be created\"; \\
	    echo \"by building it with VC++\"; \\
	    exit -1; \\
        fi

msi_up_to_date_notice:
	@if test -f \"\$(top_builddir)/$MSI_SETUP_FILE\"; then \\
	    echo \"Warning: Depedancy tracking cannot be enabled\"; \\
	    echo \"Warning: the msi file ($MSI_SETUP_FILE)\"; \\
	    echo \"Warning: Please make sure it is up to date.\"; \\
	    exit -1; \\
        fi
]])
        fi

        if test "x$USING_AX_EXTRA_DIST" != "x"; then
	    AX_ADD_AM_MACRO([[

EXTRA_BIN_DISTS += msi

]])
        fi

        if test "x$USING_AX_UPLOAD" != "x"; then
	    AX_ADD_AM_MACRO([[

UPLOAD_BIN += upload-msi
UPLOAD_TARGETS += {msi=>$PACKAGE-$VERSION.msi}

]])
        fi
    fi
else
    AC_MSG_NOTICE([setting msi file... not set])
    AC_MSG_ERROR([a file must be specified when addind msi support])
fi
])
