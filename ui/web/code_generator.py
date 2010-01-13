import os
import config
from pygccxml import parser
from pyplusplus import _logging_
from pygccxml import declarations
from pyplusplus import module_builder
from pyplusplus.module_builder import ctypes_module_builder_t
import xml.sax.saxutils

class manager_t:
    def __init__( self ):
        pass

    def show_xml( self, file_configuration, compiler_config ):
        try:
            reader = parser.project_reader_t( config=compiler_config )
            content = reader.read_xml( file_configuration )
            return content, ''
            #return xml.sax.saxutils.escape( content ), ''
        except Exception, error:
            user_msg = [ 'Error occured during code generation process!' ]
            user_msg.append( 'Error:' )
            user_msg.append( str( error ) )
            return '', '\n'.join( user_msg )

    def show_declarations( self, file_configuration, compiler_config ):
        try:
            reader = parser.project_reader_t( config=compiler_config )
            decls = reader.read_files( [file_configuration] )
            global_ns = declarations.get_global_namespace( decls )
            tmp = []
            declarations.print_declarations( decls, verbose=False, writer=lambda x: tmp.append( x.rstrip() ) )
            return os.linesep.join( tmp ), ''
        except Exception, error:
            user_msg = [ 'Error occured during code generation process!' ]
            user_msg.append( 'Error:' )
            user_msg.append( str( error ) )
            return '', '\n'.join( user_msg )

    def generate_bpl_code( self, file_configuration, compiler_config ):
        try:
            _logging_.loggers.make_inmemory()

            mb = module_builder.module_builder_t( [ file_configuration ]
                                                   , gccxml_path=compiler_config.gccxml_path
                                                   , compiler=compiler_config.compiler)
            mb.decls( header_dir=config.temp_dir ).include()
            mb.build_code_creator( "pyplusplus" )
            code = mb.code_creator.create()
            code = code.replace( '\n\r', '\n' )
            code = code.replace( '\r\n', '\n' )
            warnings = _logging_.loggers.stream.getvalue()
            _logging_.loggers.stream.close()
            return code, warnings
        except Exception, error:
            user_msg = [ 'Error occured during code generation process!' ]
            user_msg.append( 'Error:' )
            user_msg.append( str( error ) )
            return '', '\n'.join( user_msg )

    def generate_ctypes_code( self, file_configuration, symbols_file, compiler_config ):
        try:
            _logging_.loggers.make_inmemory()
            mb = ctypes_module_builder_t( [ file_configuration ], symbols_file, compiler_config )
            mb.build_code_creator( symbols_file )
            code = mb.code_creator.create()
            code = code.replace( '\n\r', '\n' )
            code = code.replace( '\r\n', '\n' )
            warnings = _logging_.loggers.stream.getvalue()
            _logging_.loggers.stream.close()
            return code, warnings
        except Exception, error:
            user_msg = [ 'Error occured during code generation process!' ]
            user_msg.append( 'Error:' )
            user_msg.append( str( error ) )
            return '', '\n'.join( user_msg )
