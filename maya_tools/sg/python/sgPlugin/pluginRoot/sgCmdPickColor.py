import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial
from maya import OpenMayaMPx
from maya import OpenMaya



kPluginCmdName="sgCmdPickColor"


class Window_global:
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    objectName = 'sgui_colorPicker'
    width = 100
    height = 100



class Window( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QWidget.__init__( self, *args, **kwargs )
        
    
    
    @staticmethod
    def show():
        
        if cmds.window( Window_global.objectName, ex=1 ):
            cmds.deleteUI( Window_global.objectName )
        
        Window_global.mainGui = Window( Window_global.mayaWin )
        Window_global.mainGui.setObjectName( Window_global.objectName )
        Window_global.mainGui.resize( Window_global.width, Window_global.height )
        Window_global.mainGui.show()
        
        
    
    
    



# command
class SGCmdSkinCluster(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)


    def doIt(self, *args):
        Window.show()
    
    
    
    def isUndoable(self):
        return False
        
        
        

# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( SGCmdSkinCluster() )


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    try:mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except:sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName);raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:mplugin.deregisterCommand(kPluginCmdName)
    except:sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName);raise


