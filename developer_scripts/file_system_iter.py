# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
from types import *

##If you want include files that doesn't have extension then use filter like '*.'

def _make_list( argument ):
    if type(argument) in StringTypes:
        if argument:
            return [argument]
        else:
            return []
    elif type(argument) is ListType:
        return argument
    else:
        raise TypeError( 'Argument "%s" must be or list of strings or string.' % argument )
        
class base_files_iterator:
    def __init__(self, file_exts, is_include_exts = True):
        self.__file_exts = _make_list( file_exts )
        self.__is_include_exts = is_include_exts

    def _is_to_skip(self, file_path):     
        if not self.__file_exts:
            return 0
        file_ext = os.path.splitext( file_path )[1]
        if not file_ext:
            file_ext = '.' + file_ext
        file_ext = '*' + file_ext 
        if file_ext.lower() in self.__file_exts:
            return not self.__is_include_exts
        else:
            return self.__is_include_exts

    def _subfolders_and_files(self, folder_path):
        files, folders = [], []
        folder_contents = os.listdir(folder_path)
        for object_name in folder_contents:
            object_path = os.path.join(folder_path, object_name)
            if os.path.isfile( object_path ) and not self._is_to_skip( object_path ):
                files.append( object_path )
            elif os.path.isdir( object_path ):
                folders.append( object_path )
            else:
                pass
        return folders, files

    def __iter__(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError

class files_iterator_generator(base_files_iterator):
    def __init__(self, folders, file_ext_filter = '', is_include_filter = True, is_recursive = True):
        base_files_iterator.__init__(self, file_ext_filter, is_include_filter)
        self.__folders = _make_list( folders )
        self.__is_recursive = is_recursive
        self.__file_generator = None

    def __walk(self):
        folders = self.__folders[:]
        while folders:
            sub_folders, files = self._subfolders_and_files( folders.pop(0) )
            if self.__is_recursive:
                for folder in sub_folders:
                    folders.append( folder )
            for file_os in files:
                yield file_os

    def __iter__(self):
        self.__file_generator = self.__walk()
        return self

    def next(self):
        return self.__file_generator.next()

    def restart(self):
        self.__file_generator = None


class folders_iterator_generator:
    def __init__(self, folders, is_recursive = 1):
        self.__folders = []
        for root in _make_list( folders ):
            self.__folders.extend( self.__sub_folders( root ) )
        self.__is_recursive = is_recursive
        self.__folder_generator = None
        
    def __sub_folders(self, folder_path):
        sub_folders = []
        folder_contains = os.listdir(folder_path)
        for object_in_folder in folder_contains:
            full_path = os.path.join(folder_path, object_in_folder)
            if os.path.isdir( full_path ):
                sub_folders.append( full_path )
        return sub_folders

    def __walk(self):
        folders = self.__folders[:]
        for curr_folder in folders:
            yield curr_folder
            if self.__is_recursive:
                for f in folders_iterator_generator( [curr_folder], True ):
                    yield f
                
    def __iter__(self):
        self.__folder_generator = self.__walk()
        return self

    def next(self):
        return self.__folder_generator.next()

    def restart(self):
        self.__folder_generator = None

#preserving backward computability names
file_iter = files_iterator_generator
folder_iter = folders_iterator_generator
#new names
files_iterator = files_iterator_generator
folders_iterator = folders_iterator_generator

if '__main__' == __name__:
    #lFileCount = 0
    #for file_os in files_iterator( r'C:\Program Files\Microsoft Visual Studio\VC98\Include\stlport', ['*.h', '*.'], True, False):
        #print file_os
        #lFileCount += 1
    #print lFileCount

    for folder in folders_iterator( '/home/roman/language-binding', False ):
        print folder
    for folder in folders_iterator( '/home/roman/language-binding', True ):
        print folder