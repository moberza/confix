# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

from libconfix.core.automake import helper_automake
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

class InterixSetup(Setup):
    def initial_builders(self):
        ret = super(InterixSetup, self).initial_builders()
        ret.add_builder(InterixMacroDefiner())
        return ret
    pass

class InterixMacroDefiner(Builder):
    def __init__(self):
        Builder.__init__(self)
        # tell everyone who's interested
        pass

    def shortname(self):
        return 'C.InterixMacroDefiner'

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def enlarge(self):
        self.parentbuilder().directory().set_property('INTERIX_SHARED_COMPILING_MACRO', self.__macroname())
        pass

    def output(self):
        super(InterixMacroDefiner, self).output()
        self.parentbuilder().makefile_am().add_cmdlinemacro(self.__macroname(), '1')
        pass

    def __macroname(self):
        return '_COMPILING_'+helper_automake.automake_name('_'.join(
            [self.package().name()]+\
            self.parentbuilder().directory().relpath(self.package().rootdirectory())))
    pass
