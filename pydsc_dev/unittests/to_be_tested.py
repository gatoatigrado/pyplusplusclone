# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import types

class code_creator_t(object):
    """
    code_creator_t is the base class for all code creators.
    This class defines interface that every code creator should implement.
    Also it provides few convenience functions.


    qeqerqwerqwerqwer
    """
    PYPLUSPLUS_NS_NAME = 'pyplusplus'
    __INDENTATION = '    '
    LINE_LENGTH = 80
    def __init__(self, parent=None):
        object.__init__(self)
        if parent:
            assert isinstance( parent, code_creator_t )
        self._parent = parent
        self._target_configuration = None

    def _get_parent( self ):
        return self._parent
    def _set_parent( self, new_parent ):
        if new_parent:
            assert isinstance( new_parent, code_creator_t )
        self._parent = new_parent
    """parent - reference to parent code creator"""
    parent = property( _get_parent, _set_parent )

    def _get_target_configuration( self ):
        return self._target_configuration
    def _set_target_configuration( self, config ):
        self._target_configuration = config
    """target_configuration - reference to target_configuration_t class instance"""
    target_configuration = property( _get_target_configuration, _set_target_configuration )

    def _get_top_parent(self):
        parent = self.parent
        me = self
        while True:
            if not parent:
                return me
            else:
                me = parent
                parent = me.parent
    """top_parent - reference to top parent code creator"""
    top_parent = property( _get_top_parent )

    def _create_impl(self):
        """
        function that all derived classes should implement. This function
        actually creates code and returns it. Return value of this function is
        string.
        """
        raise NotImplementedError()

    def create(self):
        """
        this function should be used in order to get code that should be
        generated.
        """
        code = self._create_impl()
        assert isinstance( code, types.StringTypes )
        return self.beautify( code )

    def beautify( self, code ):
        """
        function that returns code without leading and trailing whitespaces.
        """
        assert isinstance( code, types.StringTypes )
        return code.strip()

    @staticmethod
    def indent( code, size=1 ):
        """
        function that implements code indent algorithm.
        """
        assert isinstance( code, types.StringTypes )
        return code_creator_t.__INDENTATION * size\
               + code.replace( os.linesep
                               , os.linesep + code_creator_t.__INDENTATION * size )

    @staticmethod
    def unindent( code ):
        """
        function that implements code unindent algorithm.
        """
        assert isinstance( code, types.StringTypes )
        if code.startswith(code_creator_t.__INDENTATION):
            code = code[ len( code_creator_t.__INDENTATION ):]
        return code.replace( os.linesep + code_creator_t.__INDENTATION
                               , os.linesep )

    @staticmethod
    def is_comment( line ):
        """
        function that returns true if content of the line is comment, otherwise
        false.
        """
        assert isinstance( line, types.StringTypes )
        l = line.lstrip()
        #1q2w3e4r--------------
        return l.startswith( '//' ) or l.startswith( '/*' )


    def do_nothing( self ):
        """abracadabra"""
        pass

