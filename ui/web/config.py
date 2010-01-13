import os
import sys
import getpass
import tempfile

this_module_dir_path = os.path.abspath ( os.path.dirname( sys.modules[__name__].__file__) )
projects_root_dir = os.path.dirname( os.path.dirname( this_module_dir_path ) )

#~ sys.path.insert( 0, os.path.join( this_module_dir_path, 'web.zip' ) )

if os.path.exists( os.path.join( projects_root_dir, 'pygccxml_dev' ) ):
    sys.path.append( os.path.join( projects_root_dir, 'pygccxml_dev' ) )
if os.path.exists( os.path.join( projects_root_dir, 'pyplusplus_dev' ) ):
    sys.path.append( os.path.join( projects_root_dir, 'pyplusplus_dev' ) )
#else use installed modules

import pygccxml

gccxml = pygccxml.parser.load_gccxml_configuration( os.path.join( this_module_dir_path, 'gccxml.cfg' )
                                                    , gccxml_path=os.path.join( projects_root_dir, 'gccxml_bin', 'v09', sys.platform, 'bin' )
                                                    , compiler=pygccxml.utils.native_compiler.get_gccxml_compiler() )

temp_dir = tempfile.gettempdir()
