# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from libconfix.core.machinery.require import Require
from libconfix.core.machinery.provide import Provide
from libconfix.core.machinery.repo import update_marshalling_data, Marshallable, MarshalledVersionUnknownError

class RequireRelocatedHeader(Require):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Require.get_marshalling_data(self),
            generating_class=RequireRelocatedHeader,
            attributes={},
            version={'RequireRelocatedHeader': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['RequireRelocatedHeader']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Require.set_marshalling_data(self, data)
        pass

    def __init__(self, filename, source_directory):
        Require.__init__(
            self,
            string='.'.join(source_directory+[filename]),
            found_in=[],
            urgency=Require.URGENCY_ERROR)
        pass
    pass

class ProvideRelocatedHeader(Provide):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide.get_marshalling_data(self),
            generating_class=ProvideRelocatedHeader,
            attributes={},
            version={'ProvideRelocatedHeader': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['ProvideRelocatedHeader']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Provide.set_marshalling_data(self, data)
        pass

    MATCH_CLASSES = [RequireRelocatedHeader]
    def __init__(self, filename, source_directory):
        Provide.__init__(
            self,
            string='.'.join(source_directory+[filename]))
        pass
    def can_match_classes(self):
        return self.MATCH_CLASSES
    pass
