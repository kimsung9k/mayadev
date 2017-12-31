import pymel.core
from maya import cmds
from sgMaya import sgCmds
import ntpath

sels = pymel.core.ls( type='file' )

for sel in sels:
    path = sel.fileTextureName.get()
    fileName = ntpath.split( path )[-1]
    if pymel.core.referenceQuery( sel, inr=1 ):
        mapFolder = ntpath.split( pymel.core.referenceQuery( sel, filename=1 ) )[0] + '/map'
        if not os.path.exists( mapFolder ):
            mapFolder = ntpath.split( pymel.core.referenceQuery( sel, filename=1 ) )[0] + '/maps'
    else:
        mapFolder = ntpath.split( cmds.file( q=1, sceneName=1 ) )[0] + '/map'
        if not os.path.exists( mapFolder ):
            mapFolder = ntpath.split( cmds.file( q=1, sceneName=1 ) )[0] + '/maps'
        if not os.path.exists( mapFolder ):
            os.mkdir( mapFolder )

    mapPath = mapFolder + '/' + fileName
    print "before path : ", path
    print "after path : ", mapPath
    if not os.path.exists( mapPath ):
        print "%s is not exists" % mapPath
    else:
        sel.fileTextureName.set( mapPath )