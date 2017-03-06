import maya.cmds as cmds
import maya.OpenMaya as om
import os, sys
import datetime
import socket


class Model:
    
    fileHistoryPath = cmds.about( pd=1 ) + '/sg/fileHistory'
    
    callbackId = None


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



def writeRecentFilePath( *args ):
    
    nowtime = datetime.datetime.now()
    
    fileName = '%04d%02d%02d.txt' %( nowtime.year, nowtime.month, nowtime.day )
    filePath = Model.fileHistoryPath+'/'+fileName
    makeFile( filePath )
    
    f = open( filePath, 'r' )
    data = f.read()
    f.close()
    
    redata = ''
    for path in data.split( '\n' ):
        path = path.strip()
        if not path: continue
        redata += path+'\n'
    sceneName = cmds.file( q=1, sceneName=1 )
    redata += '%02d%02d%02d-' %( nowtime.hour, nowtime.minute, nowtime.second ) + sceneName
    
    f = open( filePath, 'w' )
    f.write( redata )
    f.close()



def createOpenSceneCallback():
    
    Model.callbackId1 = om.MSceneMessage.addCallback( om.MSceneMessage.kAfterOpen, writeRecentFilePath )
    Model.callbackId2 = om.MSceneMessage.addCallback( om.MSceneMessage.kAfterSave, writeRecentFilePath )