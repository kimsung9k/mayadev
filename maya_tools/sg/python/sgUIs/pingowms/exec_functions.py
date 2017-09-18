from maya import cmds
import os


def fileCmp( first, second ):
    import time
    projectTaskState = os.stat(first)
    if os.path.exists( second ):
        localTaskState   = os.stat(second)
        mTimeProjectTask = time.localtime( projectTaskState.st_mtime )
        mTimeLocalTask   = time.localtime( localTaskState.st_mtime )
    else:
        mTimeProjectTask = time.localtime( projectTaskState.st_mtime )
        mTimeLocalTask   = time.localtime( 0 )

        return mTimeProjectTask <= mTimeLocalTask



def makeFolder( pathName ):
    pathName = pathName.replace( '\\\\', '/' )
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



def updateFile( srcPath, trgPath ):
    import shutil
    if not fileCmp( srcPath, trgPath ):
        trgDir = os.path.dirname( trgPath )
        makeFolder( trgDir )
        shutil.copy2( srcPath, trgPath )
        return True
    return False



def setTextureFileServerToLocal( baseProjectPath, targetProjectPath, taskPath ):
    
    import pymel.core
    files = pymel.core.ls( type='file' )
    for textureFile in files:
        if pymel.core.referenceQuery( textureFile, inr=1 ): continue
        origPath = textureFile.fileTextureName.get()
        if origPath.find( baseProjectPath ) == -1:
            mapPath = targetProjectPath + taskPath + '/map'
            makeFolder( mapPath )
            replacedPath = mapPath + '/' + origPath.split( '/' )[-1]
        else:
            replacedPath = origPath.replace( baseProjectPath, targetProjectPath )
        
        if not os.path.exists( origPath ): continue
        
        updateFile( origPath, replacedPath )
        textureFile.fileTextureName.set( replacedPath )



def upload( srcProjectPath, dstProjectPath, taskPath, unitPath ):

    srcFullPath = srcProjectPath + taskPath + unitPath
    dstFullPath = dstProjectPath + taskPath + unitPath

    cmds.file( srcFullPath, force=True, open=True )
    cmds.refresh()
    cmds.file( rename = dstFullPath )
    setTextureFileServerToLocal( srcProjectPath, dstProjectPath, taskPath )
    cmds.file( f=1, save=1, options="v=0;" )