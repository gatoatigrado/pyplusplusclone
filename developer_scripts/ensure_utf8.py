# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import codecs
from file_system_iter import files_iterator, folders_iterator

to_be_validated_file_exts = [
      '*.rest'
]

def ensure_utf8( fpath ):
    def read_content( fpath ):
        last_error = None
        for encoding in [ 'ascii', 'UTF8', 'UTF16' ]:
            try:
                f = codecs.open( fpath, 'rb', encoding )
                fcontent = f.read()
                f.close()
                return fcontent
            except UnicodeDecodeError, err:
                last_error = err
        else:
            raise last_error

    def write_content( fpath, content ):
        fcontent_new = content #unicode( content, 'UTF8' )
        fcontent_new = fcontent_new.lstrip( unicode( codecs.BOM_UTF8, "utf8" ) )
        f = codecs.open( fpath, 'w+b', 'UTF8' )
        f.write( fcontent_new )
        f.close()

    write_content( fpath, read_content( fpath ) )


if __name__ == '__main__':
    sources_dir = os.path.join( os.path.abspath( os.curdir ), '..' )
    dirs_to_go = [ os.path.join( sources_dir, 'pydsc_dev' )
                   , os.path.join( sources_dir, 'pygccxml_dev' )
                   , os.path.join( sources_dir, 'pyplusplus_dev' ) ]

    for fpath in files_iterator( dirs_to_go, to_be_validated_file_exts ):

        print 'converting %s' % fpath
        ensure_utf8( fpath )
        print 'converting %s - done' % fpath
