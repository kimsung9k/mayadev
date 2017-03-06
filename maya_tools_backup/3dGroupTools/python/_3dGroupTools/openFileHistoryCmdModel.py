import maya.cmds as cmds
import maya.OpenMaya as om
import os, sys
import functions.path as pathFunctions
import datetime
import socket


class Model:
    
    mayaDocPath = pathFunctions.getMayaDocPath()
    fileHistoryPath = mayaDocPath + '/LocusCommPackagePrefs/fileHistory'
    
    callbackId = None



def writeRecentFilePath( *args ):
    
    nowtime = datetime.datetime.now()
    
    fileName = '%04d%02d%02d.txt' %( nowtime.year, nowtime.month, nowtime.day )
    filePath = Model.fileHistoryPath+'/'+fileName
    pathFunctions.makeFile( filePath )
    
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