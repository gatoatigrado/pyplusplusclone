import os
from file_system_iter import files_iterator, folders_iterator
from clean_source_dir import to_be_deleted_file_exts, to_be_deleted_files

CURRENT_DIR = os.path.abspath( os.getcwd() )
if 'developer_scripts' != os.path.split( CURRENT_DIR )[1]:
    raise RuntimeError( "This script should be run from developer_scripts directory!" )

class manifest_creator_t:
    def __init__( self, root ):
        self.root = root

    def include_dir( self, dir_path ):
        raise NotImplementedError()
        
    def __proceed_files( self, dir_path, manifest ):
        for file_path in files_iterator( dir_path, is_recursive=False ):
            file_name = os.path.split( file_path )[1]
            if file_name in to_be_deleted_files:
                continue
            if file_name in [ 'www_configuration.py', 'MANIFEST.readme' ]:
                continue
            file_ext = os.path.splitext( file_name )[1]
            if file_ext in to_be_deleted_file_exts:
                continue
            if file_ext.endswith( '~' ):
                continue
            manifest.write( file_path[ len( self.root ) + 1 : ] + os.linesep )
        
    def __call__( self ):
        manifest = file( os.path.join( self.root, 'MANIFEST' ), 'w+b' )
        self.__proceed_files( self.root, manifest )
        for dir_path in folders_iterator( self.root ):
            dir_name = os.path.split( dir_path )[1]
            if '.svn' in dir_path:
                continue
            if dir_path == os.path.join( self.root, 'dist' ):
                continue #exlude directory built by distutils 
            if not self.include_dir( dir_path ):
                continue            
            self.__proceed_files( dir_path, manifest )
        manifest.close()

class pydsc_creator_t( manifest_creator_t ):
    def __init__( self ):
        global CURRENT_DIR
        root = os.path.normpath( os.path.join( CURRENT_DIR, '..', 'pydsc_dev' ) ) 
        manifest_creator_t.__init__( self, root )

    def include_dir( self, dir_path ):
        return True

class pygccxml_creator_t( manifest_creator_t ):
    def __init__( self ):
        global CURRENT_DIR
        root = os.path.normpath( os.path.join( CURRENT_DIR, '..', 'pygccxml_dev' ) ) 
        manifest_creator_t.__init__( self, root )

    def include_dir( self, dir_path ):
        return os.path.split( dir_path )[1] not in [ 'temp' ]

class pyplusplus_creator_t( manifest_creator_t ):
    def __init__( self ):
        global CURRENT_DIR
        root = os.path.normpath( os.path.join( CURRENT_DIR, '..', 'pyplusplus_dev' ) ) 
        manifest_creator_t.__init__( self, root )

    def include_dir( self, dir_path ):
        if os.path.split( dir_path )[1] in [ 'temp', 'osdc2006' ]:
            return False
        if 'pyboost' in dir_path and 'generated' in dir_path:
            return False
        return True
    
if __name__ == '__main__':
    print 'creating pydsc manifest'
    pydsc_creator_t()()
    print 'creating pydsc manifest - done'
    print 'creating pygccxml manifest'
    pygccxml_creator_t()()
    print 'creating pygccxml manifest - done'
    print 'creating Py++ manifest'
    pyplusplus_creator_t()()
    print 'creating Py++ manifest - done'
    
