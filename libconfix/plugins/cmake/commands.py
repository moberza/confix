# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.utils import external_cmd
from libconfix.core.utils.error import Error

import os

def cmake(packageroot, builddir, args=None, prefix=None, path=None):
    cmake_prog = external_cmd.search_program('cmake', path)
    if cmake_prog is None:
        raise Error('cmake not found along path')
    the_args = []
    if args is not None:
        the_args.extend(args)
        pass
    if prefix is not None:
        assert type(prefix) in (list, tuple)
        the_args.append('-DCMAKE_INSTALL_PREFIX='+'/'.join(prefix))
        pass
    the_args.append(os.sep.join(packageroot))
    external_cmd.exec_program(
        program=cmake_prog,
        dir=os.path.join(builddir),
        args=the_args,
        path=path,
        print_cmdline=True)
    pass

def make(builddir, args=None, env=None):
    if args is None:
        the_args = []
    else:
        the_args = args
        pass
    external_cmd.exec_program(program='make', dir=builddir, args=the_args, env=env)
    pass
