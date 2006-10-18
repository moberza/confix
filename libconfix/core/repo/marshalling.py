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

import pickle

from libconfix.core.utils.error import Error

# use this like debug.trace([marshalling.REPOVERSION_TRACENAME], 'Upgrading class XXX from version 3 to version 100')
REPOVERSION_TRACENAME = 'repoversion'

class Marshallable:

    """ Provides support for versioned marshalling and unmarshalling
    of objects. Its functionality is a bit intrusive in that it
    requires every class that want to take part in this game to derive
    from it.

    The functionality is based on `pickle`'s __setstate__ and
    __getstate__ which is provided by `Marshallable`. Derived classes
    must implement two methods, `get_marshalling_data` and
    `set_marshalling_data`, to be able to operate meaningfully."""

    GENERATING_CLASS = 'generating_class'
    VERSIONS = 'versions'
    ATTRIBUTES = 'attributes'

    def get_marshalling_data(self):

        """ Return marshalling data for my attributes.

        To be implemented by derived classes.
        
        The returned marshalling data is a dictionary object that
        contains relatively anonymous data which represents the object
        to be marshalled. The dictionary is composed by derived
        classes and must look as follows:

        ::
        
           {
              'generating_class': <class object of generating object>,
              'versions': <versions of contributions>,
              'attributes': <dictionary with direct attributes key/value pairs>,
           }

        Called indirectly by `__getstate__`.
   
        """

        assert 0, 'abstract'
        pass

    def set_marshalling_data(self, data):

        """ (To be documented) """

        assert 0, 'abstract'
        pass
    
    def __getstate__(self):
        md = self.get_marshalling_data()

        # see if marshalling data are ok.

        assert md.has_key(Marshallable.GENERATING_CLASS)
        assert md.has_key(Marshallable.VERSIONS)
        assert md.has_key(Marshallable.ATTRIBUTES)

        # see if marshalling data have been generated by the concrete
        # class of the object. this can happen if there is some new
        # class derived from an already-marshalled class, and the
        # implementor forgot to overload get_marshalling_data().

        # delete the member since it is only to catch errors during
        # the marshalling phase, and thus need not be marshalled.

        assert md[Marshallable.GENERATING_CLASS] is self.__class__, \
               'Generating class: '+str(md[Marshallable.GENERATING_CLASS])+\
               ', self\'s class: '+str(self.__class__)+\
               ' (maybe the latter forgot to overload get_marshalling_data()?)'
        del md[Marshallable.GENERATING_CLASS]

        return md

    def __setstate__(self, data):
        return self.set_marshalling_data(data)

    pass

class Unmarshallable(Marshallable):
    def get_marshalling_data(self):
        assert 0, self.__class__.__name__+' is not meant to be marshalled'
    def set_marshalling_data(self, data):
        assert 0, self.__class__.__name__+' is not meant to be marshalled'

class MarshalledVersionTooHighError(Error):
    def __init__(self, klass, marshalled_version, highest_version):
        Error.__init__('Unmarshalling error in '+klass.__name__+': '
                       'persistent version (%d) higher than highest version (%d)' \
                       % (marshalled_version, highest_version))
        pass

class MarshalledVersionUnknownError(Error):
    def __init__(self, klass, marshalled_version, current_version):
        Error.__init__('Unmarshalling error in '+klass.__name__+': '
                       'persistent version (%d) unknown; highest version (%d)' \
                       % (marshalled_version, current_version))
        pass
    pass

def update_marshalling_data(marshalling_data,
                            generating_class,
                            attributes,
                            version):
    # don't let attribute conflicts get through
    lhs_attr_keys = set(marshalling_data[Marshallable.ATTRIBUTES].keys())
    rhs_attr_keys = set(attributes.keys())
    assert len(lhs_attr_keys & rhs_attr_keys) == 0

    # same for version conflicts
    lhs_version_keys = set(marshalling_data[Marshallable.VERSIONS].keys())
    rhs_version_keys = set(version.keys())
    assert len(lhs_version_keys & rhs_version_keys) == 0

    marshalling_data[Marshallable.GENERATING_CLASS] = generating_class
    marshalling_data[Marshallable.ATTRIBUTES].update(attributes)
    marshalling_data[Marshallable.VERSIONS].update(version)

    return marshalling_data
