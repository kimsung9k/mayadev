import pymel.core
import model
from maya import cmds
import os, time
import shutil


class FileControl:
    
    @staticmethod
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


    @staticmethod
    def makeFile( filePath ):
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        FileControl.makeFolder( folder )
        f = open( filePath, "w" )
        f.close()
        
    
    @staticmethod
    def fileCmp( first, second ):
        projectTaskState = os.stat(first)
        if os.path.exists( second ):
            localTaskState   = os.stat(second)
            mTimeProjectTask = time.localtime( projectTaskState.st_mtime )
            mTimeLocalTask   = time.localtime( localTaskState.st_mtime )
        else:
            mTimeProjectTask = time.localtime( projectTaskState.st_mtime )
            mTimeLocalTask   = time.localtime( 0 )

        return mTimeProjectTask <= mTimeLocalTask


    @staticmethod
    def updateFile( srcPath, trgPath ):
        if not FileControl.fileCmp( srcPath, trgPath ):
            trgDir = os.path.dirname( trgPath )
            FileControl.makeFolder( trgDir )
            shutil.copy2( srcPath, trgPath )
            return True
        return False




def setPathsServerToLocal( serverPath, localPath ):
    
    files = pymel.core.ls( type='file' )
    for textureFile in files:
        if pymel.core.referenceQuery( textureFile, inr=1 ): continue
        origPath = textureFile.fileTextureName.get()
        if origPath.find( serverPath ) == -1: continue
        replacedPath = origPath.replace( serverPath, localPath )
        FileControl.updateFile( origPath, replacedPath )
        textureFile.fileTextureName.set( replacedPath )
        



def loadFile( instUnit ):
    serverPath  = instUnit.projectPath
    localPath   = instUnit.localPath
    unitPath    = instUnit.unitPath
    
    projectUnitPath = serverPath + unitPath
    localUnitPath   = localPath + unitPath
    
    FileControl.updateFile( projectUnitPath, localUnitPath )
    cmds.file( localUnitPath, o=1, f=1, options="v=0;", ignoreVersion=1, typ="mayaBinary" )

    setPathsServerToLocal( serverPath, localPath )
    cmds.file( s=1 )

