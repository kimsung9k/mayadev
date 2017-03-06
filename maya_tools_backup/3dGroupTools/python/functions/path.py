import os
import maya.cmds as cmds


def getMayaDocPath():
    
    mayaDocPath = os.path.expanduser('~\\maya').replace( '\\', '/' )
    return mayaDocPath


def isFile( path ):
    
    return os.path.isfile( path )



def isFolder( path ):
    
    return os.path.isdir( path )



def openFileBrowser( path='', *args ):
    
    if not isFile( path ) and not isFolder( path ):
        cmds.warning( 'Path is not Exists' )
    
    path = path.replace( '\\', '/' )
    if isFile( path ):
        path = '/'.join( path.split( '/' )[:-1] )
        
    os.startfile( path )


def makePath( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath



def makeFolder( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath
        
        
        
def makeFile( pathName ):
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makeFolder( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()
        
        


def deletePathHierarchy( pathName ):
    pathName = pathName.replace( '\\', '/' )
    
    deleteDirTargets = []
    for root, dirs, names in os.walk( pathName ):
        for name in names:
            os.remove( root+'/'+name )
        if root == pathName: continue
        deleteDirTargets.append( root )
    
    deleteDirTargets.reverse()
    for deleteDirTarget in deleteDirTargets:
        if os.path.exists( deleteDirTarget ):
            os.rmdir( deleteDirTarget )