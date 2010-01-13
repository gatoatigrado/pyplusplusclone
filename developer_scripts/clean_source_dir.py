# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
from file_system_iter import files_iterator, folders_iterator

to_be_deleted_file_exts = [
      '*.pyc'
    , '*.py~'
    , '*.so'
    , '*.os'
    , '*.cpp~'
    , '*.hpp~'
    , '*.dll'
    , '*.rest~'
    , '*.obj'
    , '*.a'
    , '*.def'
    , '*.exp'
    , '*.lib'
    , '*.scons'
    , '*.bak'
    , '*.pdb'
    , '*.htm'
    , '*.idb'
    , '*.pdb'
    , '*.dat'
    , '*.ncb'
    , '*.out'
    , '*.dblite'
]

to_be_deleted_files = [ '.sconsign' ]

if __name__ == '__main__':
    sources_dir = os.path.join( os.path.abspath( os.curdir ), '..' )

    for file in files_iterator( sources_dir, to_be_deleted_file_exts ):
        if 'gccxml_bin' in file:
            continue
        print 'removing : ', file
        os.remove( file )

    for file in files_iterator( sources_dir ):
        if os.path.split( file )[1] in to_be_deleted_files:
            print 'removing : ', file
            os.remove( file )
