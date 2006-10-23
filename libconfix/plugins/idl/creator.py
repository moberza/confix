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

from libconfix.core.builder import Builder
from libconfix.core.filesys.file import File

import builder

class Creator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.handled_entries_ = set()
        pass

    def shortname(self):
        return 'IDL.Creator'

    def enlarge(self):
        super(Creator, self).enlarge()
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, File):
                continue
            if name in self.handled_entries_:
                continue
            if not name.endswith('.idl'):
                continue

            self.handled_entries_.add(name)
            self.parentbuilder().add_builder(builder.Builder(file=entry))
            pass
        pass
    pass
