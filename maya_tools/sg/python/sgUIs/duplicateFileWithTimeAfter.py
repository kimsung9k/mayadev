import maya.cmds as cmds
import maya.OpenMayaUI
from __qtImprot import *
import os, sys
import json
from functools import partial



def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
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
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "sgui_duplicateFileWithTimeAfter"
    title = "Get Image From Object"
    width = 300
    height = 300




class Functions:
    
    pass

        
        

class Window( QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window_global.title )
        
        self.mainWidget = QWidget()
        self.setCentralWidget( self.mainWidget )
        
        
        


    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [QtCore.QEvent.LayoutRequest,QtCore.QEvent.Move,QtCore.QEvent.Resize] :
            pass



def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.mainGui.show()

