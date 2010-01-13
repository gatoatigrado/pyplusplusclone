#! /usr/bin/python
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""Py++ user interface runner

The main purpose of this module is to run ui.py from development tree, so the
only work it does is adding new paths to sys.path variable.
"""

import os
import sys

this_module_dir_path = os.path.abspath ( os.path.dirname( sys.modules[__name__].__file__) )
projects_root_dir = os.path.dirname( os.path.dirname( this_module_dir_path ) )

sys.path.insert( 0, os.path.join( this_module_dir_path, 'web.zip' ) )

if os.path.exists( os.path.join( projects_root_dir, 'pygccxml_dev' ) ):
    sys.path.append( os.path.join( projects_root_dir, 'pygccxml_dev' ) )
if os.path.exists( os.path.join( projects_root_dir, 'pyplusplus_dev' ) ):    
    sys.path.append( os.path.join( projects_root_dir, 'pyplusplus_dev' ) )
#else use installed modules 


import ui
if __name__ == '__main__':
    ui.show_demo()
