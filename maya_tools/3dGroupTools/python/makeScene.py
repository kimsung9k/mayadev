import sys
import cPickle
import maya.standalone
import maya.cmds as cmds

sysPathInfoPath = 'C:/Users/skkim/Documents/maya/LocusCommPackagePrefs/sysPath.txt'
makeScenePath = 'C:/Users/skkim/Documents/maya/LocusCommPackagePrefs/sgStandalone/makeScenePath.txt'
addCommandPath = 'C:/Users/skkim/Documents/maya/LocusCommPackagePrefs/sgStandalone/makeSceneAddCommand.txt'


f = open( sysPathInfoPath, 'r' )
sysPaths = cPickle.load( f )
f.close()

f = open( makeScenePath, 'r' )
scenePath = f.read()
f.close()

f = open( addCommandPath, 'r' )
addCommand = f.read()
f.close()


for path in sysPaths:
    if not path in sys.path:
        sys.path.append( path )

import sgFunctionFileAndPath

maya.standalone.initialize( name='python' )
sgFunctionFileAndPath.makeFile( scenePath, False )


cmds.file( rename=scenePath )
try:
    exec( addCommand )
except:
    print "--------------------------------------"
    print "AddCommand is not acceptable"
    print "--------------------------------------"
cmds.file( f=1, save=1,  options="v=0;", type="mayaBinary" )