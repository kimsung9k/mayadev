import cPickle
import sys
import maya.standalone

maya.standalone.initialize( name='python' )


import maya.mel as mel
mayaDocPath = mel.eval( 'getenv MAYA_APP_DIR' )


sysPathInfoPath = mayaDocPath + '/LocusCommPackagePrefs/sysPath.txt'
standaloneInfoPath = mayaDocPath + '/LocusCommPackagePrefs/sgStandalone/moveFile.txt'


f = open( sysPathInfoPath, 'r' )
sysPaths = cPickle.load( f )
f.close()

for path in sysPaths:
    if not path in sys.path:
        sys.path.append( path )


f = open( standaloneInfoPath, 'r' )
srcPath, destPath = cPickle.load( f )
f.close()

import sgFunctionFileAndPath

sgFunctionFileAndPath.moveDefulatCacheFilesToCurrentCacheFiles( srcPath, destPath )
