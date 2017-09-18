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
        
    
def isUpdateRequired( first, second ):
    import time
    
    if not os.path.exists( first ):
        return False
    if not os.path.exists( second ):
        return True
    
    projectTaskState = os.stat(first)
    localTaskState   = os.stat(second)
    
    mTimeProjectTask = time.localtime( projectTaskState.st_mtime )
    mTimeLocalTask   = time.localtime( localTaskState.st_mtime )

    return mTimeProjectTask > mTimeLocalTask



def getTextureFileToLocalList( srcPath, localPath, fileNode ):
   
    def getFixedPath( path ):
        return path.replace( '\\', '/' ).replace( '///', '/' ).replace( '//', '/' )
    
    filePathAttr = 'fileTextureName'    
    srcPath = getFixedPath( srcPath )
    localPath = getFixedPath( srcPath )
    texturePath = getFixedPath(  fileNode.attr( filePathAttr ).get() )
    
    textureDirName = os.path.dirname( texturePath ).split( '/' )[-1]
    textureName = texturePath.split( '/' )[-1]
    sceneDir = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
    localMapPath = sceneDir + '/' + textureDirName + '/' + textureName
    
    if texturePath == localMapPath:
        return ['', '']
    
    return [texturePath, localMapPath]




def setPathsServerToLocal( basePath, targetPath, taskPath ):
    
    files = pymel.core.ls( type='file' )
    for textureFile in files:
        if pymel.core.referenceQuery( textureFile, inr=1 ): continue
        origPath = textureFile.fileTextureName.get()
        if origPath.find( basePath ) == -1:
            mapPath = targetPath + '/' + taskPath + '/map'
            FileControl.makeFolder( mapPath )
            replacedPath = mapPath + '/' + origPath.split( '/' )[-1]
        else:
            replacedPath = origPath.replace( basePath, targetPath )
        FileControl.updateFile( origPath, replacedPath )
        textureFile.fileTextureName.set( replacedPath )




def loadFile_local( instServerUnit, instLocalUnit ):
    
    serverPath  = instServerUnit.projectPath
    localPath   = instLocalUnit.projectPath
    taskPath    = instServerUnit.taskPath
    unitPath    = instServerUnit.unitPath

    projectUnitPath = serverPath + taskPath + unitPath
    localUnitPath   = localPath + taskPath + unitPath
    
    if os.path.exists( projectUnitPath ):
        FileControl.updateFile( projectUnitPath, localUnitPath )

    cmds.file( localUnitPath, o=1, f=1, options="v=0;", ignoreVersion=1, typ="mayaBinary" )

    setPathsServerToLocal( serverPath, localPath, taskPath )
    cmds.file( s=1 )




def loadFile_server( instServerUnit ):
    
    serverPath  = instServerUnit.projectPath
    taskPath    = instServerUnit.taskPath
    unitPath    = instServerUnit.unitPath
        
    projectUnitPath = serverPath + '/' + taskPath + '/' + unitPath
    cmds.file( projectUnitPath, o=1, f=1, options="v=0;", ignoreVersion=1, typ="mayaBinary" )
    cmds.file( s=1 )



def isUploadRequired( basePath, targetPath ):
    
    compairTwoPath  = model.CompairTwoPath( basePath, targetPath )
    compairResult   = compairTwoPath.getCompairResult()
    return compairResult in [compairTwoPath.targetIsNew, compairTwoPath.targetOnly]



def isDownloadRequired( basePath, targetPath ):
    
    compairTwoPath  = model.CompairTwoPath( basePath, targetPath )
    compairResult   = compairTwoPath.getCompairResult()
    return compairResult in [compairTwoPath.baseOnly, compairTwoPath.baseIsNew]



def upload( instUnitSrc, instUnitDst ):
    
    from maya import mel
    mayapyPath = mel.eval( 'getenv MAYA_LOCATION' ) + '/bin/mayapy.exe'
    launchPath = cmds.about( pd=1 ) + "/pingowms/launch.py"
    
    srcProjectPath = instUnitSrc.projectPath
    dstProjectPath = instUnitDst.projectPath
    taskPath   = instUnitDst.taskPath
    unitPath   = instUnitDst.unitPath
    
    srcUnitPath = srcProjectPath + taskPath + unitPath
    dstUnitPath = dstProjectPath + taskPath + unitPath
    
    FileControl.makeFile( launchPath )
    FileControl.makeFolder( os.path.dirname( dstUnitPath ) )

    standalonCommands = """
import maya.standalone

maya.standalone.initialize( name='python' )

import maya.cmds as cmds
import pymel.core
import time, os
import sys, shutil

execFunctionPaths = '%EXECFUNCTIONPATHS%'
execfile( execFunctionPaths )

srcProjectPath = '%SRCPROJECTPATH%'
dstProjectPath = '%DSTPROJECTPATH%'
dstBackupProjectPath = dstProjectPath + '/backup' 
taskPath       = '%TASKPATH%'
unitPath       = '%UNITPATH%'

srcUnitPath = srcProjectPath + taskPath + unitPath
dstUnitPath = dstProjectPath + taskPath + unitPath

upload( srcProjectPath, dstProjectPath, taskPath, unitPath )
"""
    exec_functionPath = os.path.dirname( __file__.replace( '\\', '/' ) ) + '/exec_functions.py'
    standalonCommands = standalonCommands.replace( '%EXECFUNCTIONPATHS%', exec_functionPath )
    standalonCommands = standalonCommands.replace( '%SRCPROJECTPATH%', srcProjectPath )
    standalonCommands = standalonCommands.replace( '%DSTPROJECTPATH%', dstProjectPath )
    standalonCommands = standalonCommands.replace( '%TASKPATH%', taskPath )
    standalonCommands = standalonCommands.replace( '%UNITPATH%', unitPath )

    print standalonCommands

    f = open( launchPath, 'w' )
    f.write( standalonCommands )
    f.close()

    mel.eval( 'system( "start %s %s" )' %( mayapyPath, launchPath ) )




