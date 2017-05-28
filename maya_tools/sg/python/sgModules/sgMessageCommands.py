from maya import OpenMaya
from maya import cmds
import os


def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()



def copyShader( srcObj, dstObj ):
    
    import pymel.core
    srcObj = pymel.core.ls( srcObj )[0]
    dstObj = pymel.core.ls( dstObj )[0]
    
    if srcObj.type() == 'transform':
        srcObj = srcObj.getShape()
    if dstObj.type() == 'transform':
        dstObj = dstObj.getShape()
    
    shadingEngine = srcObj.listConnections( s=0, d=1, type='shadingEngine' )
    if not shadingEngine:
        cmds.warning( "%s has no shading endgine" % srcObj.name )
        return None
    cmds.sets( dstObj.name(), e=1, forceElement = shadingEngine[0].name() )






