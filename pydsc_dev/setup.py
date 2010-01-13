# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

from distutils.core import setup
from distutils.cmd import Command

setup( name="pydsc"
       , version = "0.4"
       , description="Python documentation and comments spell checker"
       , author="Roman Yakovenko"
       , author_email="roman.yakovenko@gmail.com"
       , url='http://www.language-binding.net'
       , py_modules=[ 'pydsc' ]
)
