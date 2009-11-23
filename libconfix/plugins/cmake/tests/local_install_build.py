# Copyright (C) 2009 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake import commands

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.utils import const
from libconfix.testutils.persistent import PersistentTestCase

from libconfix.setups.c import C
from libconfix.setups.c import AutoC
from libconfix.setups.cmake import CMake
from libconfix.setups.boilerplate import Boilerplate

import unittest
import time
import os

class LocalInstallBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LocalInstallTest('test_basic'))
        self.addTest(LocalInstallTest('test_explicit_no_public_visibility'))
        self.addTest(LocalInstallTest('test_auto_no_public_visibility'))
        self.addTest(LocalInstallTest('test_no_timestamp_clobber'))
        self.addTest(LocalInstallTest('test_sourcefile_dependency'))
        pass
    pass

class LocalInstallTest(PersistentTestCase):
    def test_basic(self):
        source = Directory()
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("Local-Install")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["headers-only"])',
                              'DIRECTORY(["headers-with-library"])',
                              'DIRECTORY(["exe"])']))

        headers_only = source.add(
            name='headers-only',
            entry=Directory())
        headers_with_library = source.add(
            name='headers-with-library',
            entry=Directory())
        exe = source.add(
            name='exe',
            entry=Directory())

        headers_only.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['H(filename="header-1.h", install=["headers-only-install"])',
                              'H(filename="header-2.h", install=["headers-only-install"])']))
        headers_only.add(
            name='header-1.h',
            entry=File())
        headers_only.add(
            name='header-2.h',
            entry=File())

        headers_with_library.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(members=[H(filename="library-1.h", install=["headers-with-library-install"]),'
                              '                 H(filename="library-2.h", install=["headers-with-library-install"]),'
                              '                 C(filename="library-1.c"),'
                              '                 C(filename="library-2.c")',
                              '                ]',
                              '       )'
                              ]))
        headers_with_library.add(
            name='library-1.h',
            entry=File(lines=['void library1(void);']))
        headers_with_library.add(
            name='library-2.h',
            entry=File(lines=['void library2(void);']))
        headers_with_library.add(
            name='library-1.c',
            entry=File(lines=['#include <headers-only-install/header-1.h>',
                              'void library1(void) {}']))
        headers_with_library.add(
            name='library-2.c',
            entry=File(lines=['#include <headers-only-install/header-2.h>',
                              'void library2(void) {}']))

        exe.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['EXECUTABLE(exename="exe",',
                              '           center=C(filename="main.c"))',
                              ]))
        exe.add(
            name='main.c',
            entry=File(lines=['#include <headers-only-install/header-1.h>',
                              '#include <headers-only-install/header-2.h>',
                              '#include <headers-with-library-install/library-1.h>',
                              '#include <headers-with-library-install/library-2.h>',
                              'int main(void) {',
                              '    library1();',
                              '    library2();',
                              '}']))

        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=source)
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])
        commands.make(builddir=build.abspath(), args=[])

        scan.rescan_dir(build)

        # I doubt that this will hold under Windows :-) if it becomes
        # an issue we will skip this check
        self.failUnless(build.find(['exe', 'exe']))

        pass

    def test_explicit_no_public_visibility(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('blah')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='header.h', public=False)"]))
        source.add(
            name='header.h',
            entry=File())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(),
                                       C(),
                                       CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(builddir=build.abspath(), args=['install'])

        scan.rescan_dir(install)

        self.failIf(install.find(['include', 'header.h']))
        
        pass
    
    def test_auto_no_public_visibility(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('blah')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["SET_HEADER_PUBLIC(shellmatch='header.h', public=False)"]))
        source.add(
            name='header.h',
            entry=File())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(),
                                       AutoC(),
                                       CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(builddir=build.abspath(), args=['install'])

        scan.rescan_dir(install)

        self.failIf(install.find(['include', 'header.h']))
        pass

    # provided that the sourcefile does not change, local install must
    # not take place at every call to make.

    # I observed that this happens when having lots of header files in
    # a directory, so I use 200 for this test. finally it turned out
    # that the local-install rule's dependency on the local-install
    # directory's timestamp didn't work out right.
    def test_no_timestamp_clobber(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_no_timestamp_clobber')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                "for f in xrange(200):",
                "    H(filename='%s.h' % str(f), install=['subdir'])",
                ]))
        for f in xrange(200):
            source.add(
                name='%s.h' % str(f),
                entry=File())
            pass            

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])

        commands.make(builddir=build.abspath(), args=[])
        mtimes = {}
        for f in xrange(200):
            mtime = os.stat(os.sep.join(build.abspath()+['confix-include', 'subdir', '%s.h' % str(f)])).st_mtime
            mtimes[f] = mtime
            pass

        # wait a bit and then call 'make' again
        time.sleep(1)

        commands.make(builddir=build.abspath(), args=[])
        for f in xrange(200):
            mtime = os.stat(os.sep.join(build.abspath()+['confix-include', 'subdir', '%s.h' % str(f)])).st_mtime
            self.failIf(mtime != mtimes[f], f)
            pass
        pass

    # if the sourcefile changes it must be locally installed again.
    def test_sourcefile_dependency(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_sourcefile_dependency')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                "H(filename='h.h', install=['subdir'])",
                ]))
        h = source.add(
            name='h.h',
            entry=File())

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])

        commands.make(builddir=build.abspath(), args=[])
        before_mtime = os.stat(os.sep.join(build.abspath()+['confix-include', 'subdir', 'h.h'])).st_mtime

        # wait a bit. then touch the source file, call make again, and
        # check that the file was locally installed again.
        time.sleep(1)

        h.add_lines(['x'])
        fs.sync()

        commands.make(builddir=build.abspath(), args=[])

        self.failUnless(os.stat(os.sep.join(build.abspath()+['confix-include', 'subdir', 'h.h'])).st_mtime > before_mtime)

        pass
        
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LocalInstallBuildSuite())
    pass
