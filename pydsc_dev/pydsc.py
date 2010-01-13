# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
The pydsc module checks documentation strings and comments for spelling errors.

Usage example:

.. code-block:: python

   import pydsc
   pydsc.include_paths( r'D:\pygccxml_dev\pygccxml' ) #check only pygccxml package
   pydsc.ignore_words([ 'Yakovenko', 'www', 'org', 'py' ])
   #if you use sphinx as a documentation tool:
   pydsc.set_text_preprocessor( pydsc.sphinx_preprocessor )
"""

__version__ = '0.3' #current version
__author__ = 'Roman Yakovenko <roman.yakovenko@gmail.com>'
__url__ = 'http://www.language-binding.net'
__license__ = 'Boost Software License <http://boost.org/more/license_info.html>'

import os
import re
import sys
import pprint
import atexit
import inspect
import __builtin__
import enchant
import enchant.checker

def normalize_path( some_path ):
    """return os.path.normcase( os.path.normpath( some_path ) )"""
    return os.path.normcase( os.path.normpath( some_path ) )

def contains_parent_dir( path, dirs ):
    """
    returns true if one of the directories is root directory for the `path`, false otherwise

    :param path: path to be checked
    :type path: str

    :param dirs: list of directories and\\or files
    :type dirs: [ str ]

    :rtype: bool
    """
    #precondition: dirs and fpath should be normalize_path'ed before calling this function
    return bool( filter( lambda dir: path.startswith( dir ), dirs ) )


def is_identifier( word ):
    """
    returns `True` is the word represents an identifier, constructed from two or more words, `False` otherwise.

    This function is used to filter out some errors, reported by spell checker.
    """
    if not word:
        return False
    if '_' in word:
        return True
    rest_of_word = word[1:]
    for ch in rest_of_word:
        if ch == ch.upper():
            return True
    return False


class checker_t( object ):
    """
    Applies spell check process on every imported module.

    Every documentation string within the imported modules will be checked.
    Some comments will be checked too. The :mod:`inspect` module is used to
    extract documentation strings and comments
    """

    def __init__( self
                  , speller
                  , writer=sys.stdout
                  , ignore_identifiers=True
                  , text_preprocessor=lambda t: t ):
        """
        initialization method

        replaces :func:`__builtin__.__import__` function with :meth:`checker_t.import_`

        :param speller: reference to enchant.checker.SpellChecker object
        :type speller: enchant.checker.SpellChecker

        :param writer: reference to instance of class that has write method.
                       By default sys.stdout will be used.

        :param ignore_identifiers: often comments/documentation strings contains
                                   class\\method\\function names. Those names,
                                   usually introduce spell error. If ignore_identifiers
                                   set to True, those names will be ignored.
        :type ignore_identifiers: bool

        :param text_preprocessor: a callable, which takes a text before it is passed to
                                  the spell checker. The result will be passed to the spell checker.
        """
        object.__init__( self )
        self.__checked = set()
        self.__orig_import = __builtin__.__import__
        __builtin__.__import__ = self.import_
        self.__already_imported = set( sys.modules.keys() )
        self.__checked = set()
        self.__reported_errors = set()
        self.speller = speller
        self.writer = writer
        self.__include_paths = set()
        self.ignored_words = set()
        self.add_include_paths( '.')
        self.ignore_identifiers = ignore_identifiers
        self.text_preprocessor = text_preprocessor
        atexit.register( self.report_statistics )

    def add_include_paths( self, path ):
        np = lambda p: normalize_path( os.path.abspath( p ) )
        if isinstance( path, str ):
            self.__include_paths.add( np( path ) )
        else:
            for pi in path:
                self.__include_paths.add( np( pi ) )

    def should_be_checked( self, obj, module=None ):
        """returns True, if obj should be checked, False otherwise"""
        if id(obj) in self.__checked:
            return False
        if inspect.isbuiltin( obj ):
            return False
        if inspect.ismodule( obj ):
            if obj.__name__ in self.__already_imported:
                return False #do not check already imported modules
            source_file = self.getsourcefile(obj)
            if source_file:
                return contains_parent_dir( source_file, self.__include_paths )
            else:
                return False
        obj_module = inspect.getmodule( obj )
        if not obj_module is module:
            return False
        if inspect.isclass( obj ) \
           or inspect.ismethod( obj ) \
           or inspect.isfunction( obj ) \
           or inspect.isroutine( obj ) \
           or inspect.ismethoddescriptor( obj ) \
           or inspect.isdatadescriptor( obj ):
            return True
        return False

    def import_( self, name, globals=None, locals=None, fromlist=None, level=-1 ):
        """Hook to import functionality"""
        pymodule = self.__orig_import( name, globals, locals, fromlist, level )
        if self.should_be_checked(pymodule):
            self.__already_imported.add( name )
            self.__check( pymodule )
        return pymodule

    @staticmethod
    def getsourcefile( obj ):
        try:
            fpath = inspect.getsourcefile( obj )
            if fpath is None:
                fpath = inspect.getfile( obj )
            if fpath:
                fpath = os.path.abspath( fpath )
                fpath = normalize_path( fpath )
            return fpath
        except TypeError:
            pass

    def __get_local_ignored_words( self, obj ):
        names = set()
        if inspect.ismethod( obj ) or inspect.isfunction( obj ):
            args_desc = inspect.getargspec( obj )
            names.update( args_desc[0] )
            if args_desc[1]:
                names.add( args_desc[1] )
            if args_desc[2]:
                names.add( args_desc[2] )
        return names

    def __check_text_impl( self, obj, text_, text_type ):
        text = self.text_preprocessor( text_ )

        if not text:
            return

        if self.ignore_identifiers and hasattr( obj, '__name__' ) and obj.__name__:
            self.ignored_words.add( obj.__name__ )

        local_ignored_words = self.__get_local_ignored_words( obj )

        errors = {}
        self.speller.set_text( text )
        for error in self.speller:
            if error.word in self.ignored_words or error.word in local_ignored_words:
                continue
            if is_identifier( error.word ):
                continue
            fpath = self.getsourcefile( inspect.getmodule( obj ) )
            if fpath:
                error_id = "%s:%s:%d" % ( error.word, fpath, inspect.getsourcelines( obj )[1] )
                if error_id in self.__reported_errors:
                    continue
                else:
                    self.__reported_errors.add( error_id )
            errors[ error.word ] = self.speller.suggest()

        if not errors:
            return

        write = self.writer.write
        if self.getsourcefile( inspect.getmodule( obj ) ):
            write( '  error details: %s' % os.linesep )
            write( '    location        : %s:%d%s' % ( self.getsourcefile( inspect.getmodule( obj ) ), 1 + inspect.getsourcelines( obj )[1], os.linesep ) )
            write( '    text type       : %s%s' % ( text_type, os.linesep ) )
        else:
            write( '  error details: %s' % os.linesep )
            write( '    text type       : %s%s' % ( text_type, os.linesep ) )
        for word, suggestions in errors.items():
            write( '    misspelled word : %s%s' % ( word, os.linesep ) )
            write( '    suggestions     : %s%s' % ( `suggestions`, os.linesep ) )
        if 0: #debug code
            clean = lambda t: t.replace( '\n', ' ' ).replace( '\r', '' )
            write( '    source file text: %s\n' % clean( text_ ) )
            write( '    checked text    : %s\n' % clean( text ) )
            write( '    object          : %s\n' % str(obj) )

    def __check_text( self, obj):
        self.__check_text_impl( obj, inspect.getdoc( obj ), 'documentation string' )
        try:
            if self.getsourcefile( obj ):
                self.__check_text_impl( obj, inspect.getcomments( obj ), 'comment' )
        except TypeError:
            pass

    def __check( self, module ):
        self.__check_text( module )
        to_be_checked = map( lambda x: x[1], inspect.getmembers( module ) )
        while to_be_checked:
            member = to_be_checked.pop(0)
            if not self.should_be_checked( member, module ):
                continue
            self.__check_text( member )
            to_be_checked.extend( map( lambda x: x[1], inspect.getmembers( member ) ) )
            self.__checked.add( id(member) )

    def report_statistics( self ):
        words = {}
        print '\n'
        print 'pydsc report'
        print '  errors found: ', len( self.__reported_errors )
        for error_id in self.__reported_errors:
            word = error_id.split( ':' )[0]
            if word not in words:
                words[ word ] = []
            words[ word ].append( error_id[ len(word) + 1: ] )
        for word, occurs in words.iteritems():
            print '    ', word, ' - ', len( occurs )
            occurs.sort()
            for location in occurs:
                print '      ', location
        print 'pydsc report - end'


"""documentation spell checker instance"""
doc_checker = None
if not( ('PYDSC' in os.environ) and ('sphinx' in os.environ['PYDSC']) ):
    doc_checker = checker_t( enchant.checker.SpellChecker( "en_US"
                                                            , filters=[ enchant.tokenize.EmailFilter
                                                                        , enchant.tokenize.URLFilter
                                                                        , enchant.tokenize.WikiWordFilter ] ) )


def include_paths( what ):
    """
    includes all modules, to the check process, that are lying in *what* directory(ies)

    *what* - a path or list of paths, could be or contain file and/or directory names
    """
    doc_checker.add_include_paths( what )

def ignore_words( what, case_sensitive=False ):
    """
    adds *what*, word or list of words, to the ignore list.

    what - word(string) or list of words(strings) to be ignored.
    """
    if isinstance( what, str ):
        if not case_sensitive:
            what = what.lower()
        doc_checker.ignored_words.add( what )
    else:
        for word in what:
            if case_sensitive:
                word = word.lower()
            doc_checker.ignored_words.add( word )

def ignore_dictionary( path, case_sensitive=False ):
    """
    adds all words from file to the "ignore" list

    The file should contain one word per line

    :param path: path to dictionary file
    :type path: str
    """
    for w in file( path, 'r' ).readlines():
        w = w.strip()
        if case_sensitive:
            w = w.lower()
        if w:
            doc_checker.ignored_words.add( w )

def set_text_preprocessor( preprocessor ):
    doc_checker.text_preprocessor = preprocessor

class sphinx_preprocessor_t:
    __ref_def = re.compile( r':[_a-zA-Z]+(\s+[_a-zA-Z0-9]+)?:' )
    __ref_no_title = re.compile( r'`(\:\:)?[_a-zA-Z]+[_a-zA-Z0-9\.\:\+]*`' )
    __ref_with_title = re.compile( r'`(?P<text>.+)?\s(\<.*\>)`' )


    def __replace_via_re( self, text ):
        def replace( m ):
            if 'text' in m.groupdict():
                return ' ' * ( m.start( 'text' ) - m.start() ) +  m.group( 'text' ) + ' ' * ( m.end() - m.end( 'text' ) )
            else:
                return ' ' * ( m.end() - m.start() )
        if not text:
            return text
        result = text
        result = self.__ref_no_title.sub( replace, result )
        result = self.__ref_def.sub( replace, result )
        result = self.__ref_with_title.sub( replace, result )
        return result

    #~ def __remove_code_block( self, text ):
        #~ lines = map( lambda line: line.rstrip(), text.split( '\n' ) )

        #~ no_code_lines = []

        #~ index = 0
        #~ within_block = False
        #~ indent_level = 0
        #~ while index < len( lines ):

    def __call__( self, text ):
        return self.__replace_via_re( text )

#sphinx_preprocessor, instance of :class:`sphinx_preprocessor_t` allows to remove
#some special words and code from the text.
sphinx_preprocessor = sphinx_preprocessor_t()
