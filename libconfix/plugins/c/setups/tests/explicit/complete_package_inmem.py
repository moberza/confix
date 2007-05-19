# Copyright (C) 2007 Joerg Faschingbauer

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

import complete_package

from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.testutils import find

import unittest

class CompletePackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CompletePackageInMemoryTest('test'))
        pass
    pass

class CompletePackageInMemoryTest(unittest.TestCase):
    def test(self):
        package = LocalPackage(rootdirectory=complete_package.make_package_source(package_name=self.__class__.__name__),
                               setups=[ExplicitCSetup(use_libtool=False),
                                       ExplicitDirectorySetup()])
        package.boil(external_nodes=[])

        # see if we have got the directories right
        found_lodir_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['lolibrary'])
        self.failIf(found_lodir_builder is None)
        found_hidir_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['hilibrary'])
        self.failIf(found_hidir_builder is None)
        found_exedir_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['executable'])
        self.failIf(found_exedir_builder is None)

        # lodirectory has lolibrary has H(lo.h), C(lo1.c), C(lo2.c)
        # ---------------------------------------------------------

        # we called H() and C() in the directory's Confix2.dir, as
        # arguments of LIBRARY(). the side effect of this must have
        # been to add the corresponding source files to the directory.
        found_lo_lo_h = None
        found_lo_lo1_c = None
        found_lo_lo2_c = None
        for b in found_lodir_builder.builders():
            if type(b) is HeaderBuilder and b.file().name() == 'lo.h':
                found_lo_lo_h = b
                pass
            if type(b) is CBuilder and b.file().name() == 'lo1.c':
                found_lo_lo1_c = b
                pass
            if type(b) is CBuilder and b.file().name() == 'lo2.c':
                found_lo_lo2_c = b
                pass
            pass
        self.failIf(found_lo_lo_h is None)
        self.failIf(found_lo_lo1_c is None)
        self.failIf(found_lo_lo2_c is None)

        # find the library itself and see if it has the right
        # properties.
        found_lolib_builder = None
        for b in found_lodir_builder.builders():
            if type(b) is LibraryBuilder:
                self.failUnless(found_lolib_builder is None, str(b)) # we build only one library
                found_lolib_builder = b
                pass
            pass
        self.failIf(found_lolib_builder is None)
        self.failUnless(found_lolib_builder.basename() == 'hansi')

        # see if it has the right members
        found_lo_lo_h = None
        found_lo_lo1_c = None
        found_lo_lo2_c = None
        for b in found_lolib_builder.members():
            if type(b) is HeaderBuilder and b.file().name() == 'lo.h':
                found_lo_lo_h = b
                continue
            if type(b) is CBuilder and b.file().name() == 'lo1.c':
                found_lo_lo1_c = b
                continue
            if type(b) is CBuilder and b.file().name() == 'lo2.c':
                found_lo_lo2_c = b
                continue
            pass
        self.failIf(found_lo_lo_h is None)
        self.failIf(found_lo_lo1_c is None)
        self.failIf(found_lo_lo2_c is None)
        
                

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CompletePackageInMemorySuite())
    pass
