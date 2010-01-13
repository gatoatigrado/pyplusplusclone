"""generates Py++ code from the user data"""
import os
from pygccxml import parser

BP_FILE_CODE_TEMPLATE = \
"""
import os
from pyplusplus import module_builder

#Creating an instance of class that will help you to expose your declarations
mb = module_builder.module_builder_t( [r"%(file_name)s"]
                                      , gccxml_path=r"%(gccxml_path)s"
                                      , include_paths=%(include_paths)s
                                      , define_symbols=%(define_symbols)s )

#print all parsed declarations and some information about them
mb.print_declarations()

#Py++ has smart algorithm, which automaticly selects what declarations should be
#exported, but of course you can change that.

#building code creator. After this step you should not modify declarations.
mb.build_code_creator( module_name='pyplusplus' )

#writing code to file.
mb.write_module( './bindings.cpp' )
"""

BP_TEXT_CODE_TEMPLATE = \
r'''
import os
import tempfile
from pygccxml import parser
from pyplusplus import module_builder

code = \
"""
%(text)s
"""


#Creating an instance of class that will help you to expose your declarations
mb = module_builder.module_builder_t( [parser.create_text_fc(code)]
                                      , gccxml_path=r"%(gccxml_path)s"
                                      , include_paths=%(include_paths)s
                                      , define_symbols=%(define_symbols)s )

#print all parsed declarations and some information about them
mb.print_declarations()

#select all declarations from the code fragment and export them
mb.decls( header_dir=tempfile.tempdir ).include()

mb.add_declaration_code( code, tail=False )

#building code creator. After this step you should not modify declarations.
mb.build_code_creator( module_name='pyplusplus' )

#writing code to file.
mb.write_module( './bindings.cpp' )
'''

class wizard_t( object ):
    """code generator that creates Py++ code"""
    def __init__( self ):
        object.__init__( self )

    def create_bpl_code( self, gccxml_cfg, file_configuration ):
        tmpl = None
        substitute_dict = dict( gccxml_path=gccxml_cfg.gccxml_path
                                , include_paths=`gccxml_cfg.include_paths`
                                , define_symbols=`gccxml_cfg.define_symbols` )
        if file_configuration.content_type == file_configuration.CONTENT_TYPE.TEXT:
            global BP_TEXT_CODE_TEMPLATE
            tmpl = BP_TEXT_CODE_TEMPLATE
            substitute_dict['text'] = '\n'.join( [ line.rstrip() for line in file_configuration.data.split('\n') ] )
        else:
            global BP_FILE_CODE_TEMPLATE
            tmpl = BP_FILE_CODE_TEMPLATE
            substitute_dict['file_name'] = file_configuration.data
        return tmpl % substitute_dict
