import maya.mel as mel
import sys, os


class Info:
    
    _melFilePath = ''
    
    for j in sys.path:
        if not os.path.isdir( j ):
            continue
        dirList = os.listdir( j )
        if 'animation' in dirList:
            _melFilePath = j+'/animation/importCache/importCacheUi.mel'



mel.eval( 'source "%s"' % Info._melFilePath )


def openImportCacheUI( *args ):
    
    mel.eval( 'cacheConnect' )