import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial
from PySide.QtGui import QFileDialog


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



class Window_global:
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    winName = 'test_fileDialog'
    infoPath = cmds.about( pd=1 ) + "/" + __name__.replace( '.', '/' ) + '.info'
    makeFile( infoPath )
    
    @staticmethod
    def saveUpperFolder( path ):
        
        path = path.replace( '\\', '/' )
        upperFolder = '/'.join( path.split( '/' )[:-1] )
        f = open( Window_global.infoPath, 'w' )
        f.write( upperFolder )
        f.close()
    
    @staticmethod
    def getDefaultFolder():
        
        f = open( Window_global.infoPath, 'r' )
        path = f.read()
        f.close()
        if os.path.exists( path ): return path
        else: return ''
    


def getDirectory( evt=0 ):
    
    if cmds.window( Window_global.winName, ex=1 ):
        cmds.deleteUI( Window_global.winName )
    dialog = QtGui.QFileDialog(Window_global.mayaWin)
    dialog.setObjectName( Window_global.winName )
    dialog.setDirectory( Window_global.getDefaultFolder() )
    choosedFolder = dialog.getExistingDirectory()
    
    if choosedFolder: Window_global.saveUpperFolder( choosedFolder )
    
    return choosedFolder


