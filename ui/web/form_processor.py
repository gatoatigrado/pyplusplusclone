import config
import web
from pygccxml import parser
import wizard

class generator_t:
    def __init__( self, code_generator, input ):
        self.__input = input
        self.__code_generator = code_generator
        self.__handlers = {
            "VIEW_XML" : self.on_view_xml
            , "VIEW_DECLS" : self.on_view_decls
            , "GENERATE_BP_CODE" : self.on_generate_bpl_code
            , "GENERATE_BP_PYPP_CODE" : self.on_generate_bpl_pypp_code
            , "GENERATE_CTYPES_CODE" : self.on_generate_ctypes_code
            , "GENERATE_CTYPES_PYPP_CODE" : self.on_generate_ctypes_pypp_code
        }

    def __create_fc( self, prefix ):
        fto_key = prefix + '_TAKE_CODE_FROM'
        code_key = prefix + '_SOURCE_CODE'
        file_key = prefix + '_FILE_NAME'
        if self.__input[fto_key] == 'text':
            return parser.create_text_fc( self.__input[ code_key ] )
        else:
            return parser.create_source_fc( self.__input[ file_key ] )

    def __create_gccxml_cfg( self ):
        #in real web mode this functionality should be disabled
        cfg = config.gccxml.clone()

        include_dirs = self.__input['COMPILER_INCLUDE_DIRECTORIES']
        include_dirs = include_dirs.split('\n')
        include_dirs = filter( None, [ idir.strip() for idir in include_dirs ] )
        cfg.include_paths.extend(include_dirs)

        preprocessor_defs = self.__input['COMPILER_PREPROCESSOR_DEFINITIONS']
        cfg.append_cflags( preprocessor_defs.replace( '\n', ' ' ) )

        additional_args = self.__input['COMPILER_CMD_ARGS']
        cfg.append_cflags( additional_args.replace( '\n', ' ' ) )
        return cfg

    def on_view_xml( self ):
        fc = self.__create_fc( 'GCCXML' )
        decls_tree, warnings = self.__code_generator.show_xml( fc, compiler_config=self.__create_gccxml_cfg() )
        return decls_tree, warnings

    def on_view_decls( self ):
        fc = self.__create_fc( 'GCCXML' )
        decls_tree, warnings = self.__code_generator.show_declarations( fc, compiler_config=self.__create_gccxml_cfg() )
        return decls_tree, warnings

    def on_generate_bpl_code( self ):
        fc = self.__create_fc( 'BPL' )
        code, warnings = self.__code_generator.generate_bpl_code( fc, compiler_config=self.__create_gccxml_cfg() )
        return code, warnings

    def on_generate_bpl_pypp_code( self ):
        w = wizard.wizard_t()
        code = w.create_bpl_code( self.__create_gccxml_cfg(), self.__create_fc( 'BPL' ) )
        return code, ''

    def on_generate_ctypes_code( self ):
        fc = parser.create_source_fc( self.__input[ "CTYPES_FILE_NAME" ] )
        symbols_file = self.__input[ "CTYPES_SHLIB_FILE_NAME" ]
        code, warnings = self.__code_generator.generate_ctypes_code( fc, symbols_file, compiler_config=self.__create_gccxml_cfg() )
        return code, warnings

    def on_generate_ctypes_pypp_code( self ):
        pass

    def not_found_handler( self ):
        raise RuntimeError( 'Error - unknown submit action' )

    def __select_handler( self ):
        for key, handler in self.__handlers.iteritems():
            if key in self.__input:
                return handler
        else:
            return self.not_found_handler

    def process( self ):
        handler = self.__select_handler()
        return handler()
