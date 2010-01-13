# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import unittest
import autoconfig
import parser_test_case

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations


class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)

    def test1(self):
        code = 'int aaaa[2][3][4][5];'
        src_reader = parser.source_reader_t( self.config )
        global_ns = declarations.get_global_namespace( src_reader.read_string( code ) )
        aaaa_type = global_ns.var('aaaa').type
        self.failUnless( 'int[2][3][4][5]' == aaaa_type.decl_string, aaaa_type.decl_string )

    def test2(self):
        code = 'int* aaaa[2][3][4][5];'
        src_reader = parser.source_reader_t( self.config )
        global_ns = declarations.get_global_namespace( src_reader.read_string( code ) )
        aaaa_type = global_ns.var('aaaa').type
        self.failUnless( 'int *[2][3][4][5]' == aaaa_type.decl_string, aaaa_type.decl_string )

    def test3(self):
        code = 'int aaaa[2];'
        src_reader = parser.source_reader_t( self.config )
        global_ns = declarations.get_global_namespace( src_reader.read_string( code ) )
        aaaa_type = global_ns.var('aaaa').type
        self.failUnless( 'int[2]' == aaaa_type.decl_string, aaaa_type.decl_string )

    def test4(self):
        code = 'struct xyz{}; xyz aaaa[2][3];'
        src_reader = parser.source_reader_t( self.config )
        global_ns = declarations.get_global_namespace( src_reader.read_string( code ) )
        aaaa_type = global_ns.var('aaaa').type
        self.failUnless( '::xyz[2][3]' == aaaa_type.decl_string, aaaa_type.decl_string )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
