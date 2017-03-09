import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial


lineEditName = "sgui_putObjectAtGround_lineEdit"
listWidgetName = "sgui_putObjectAtGround_listWidget"




def appendPluginPath():

    putenvStr = mel.eval( 'getenv "MAYA_PLUG_IN_PATH"' )
    
    if os.name == 'posix':
        sepChar = ':'
    else:
        sepChar = ';'
    
    pythonPathName = sepChar + os.path.dirname( __file__.replace( '\\', '/' ) ) + '/pluginRoot'
    
    version = cmds.about(version=True)[:4]
    cppPathName = sepChar + os.path.dirname( __file__.replace( '\\', '/' ) ) + '/pluginRoot/' + version
    
    putenvStr = putenvStr.replace( pythonPathName, '' )
    putenvStr += pythonPathName
    putenvStr = putenvStr.replace( cppPathName, '' )
    putenvStr += cppPathName
    
    mel.eval( 'putenv "MAYA_PLUG_IN_PATH" "%s"' % putenvStr )
    putenvStr = mel.eval( 'getenv "MAYA_PLUG_IN_PATH"' )




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
    objectName = "sgui_putObjectAtGround"
    title = "Put Object At Ground"
    width = 300
    height = 300
    
    infoPath = cmds.about(pd=True) + "/sg/putObjectAtGround/uiInfo.txt"
    makeFile( infoPath )
    
    mainGui = QtGui.QMainWindow()
    listItems = []

    @staticmethod
    def saveInfo( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath
        
        posX = Window_global.mainGui.pos().x()
        posY = Window_global.mainGui.pos().y()
        width  = Window_global.mainGui.width()
        height = Window_global.mainGui.height()
        
        f = open( filePath, "w" )
        json.dump( [posX, posY, width, height], f, True, False, False )
        f.close()
    
    
    @staticmethod
    def loadInfo( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath
        
        f = open( filePath, 'r')
        try:data = json.load( f )
        except: f.close(); return None
        f.close()
    
        if not data: return None
        
        try:
            posX = data[0]
            posY = data[1]
            width = data[2]
            height = data[3]
            
            Window_global.mainGui.resize( width, height )
            
            desktop = QtGui.QApplication.desktop()
            desktopWidth = desktop.width()
            desktopHeight = desktop.height()
            if posX + width > desktopWidth: posX = desktopWidth - width
            if posY + height > desktopWidth: posY = desktopHeight - height
            if posX < 0 : posX = 0
            if posY < 0 : posY = 0
            
            Window_global.mainGui.move( posX, posY )
        except:
            pass





class Window_cmd:
    
    @staticmethod
    def addObject( evt=0 ):
        
        listItems = cmds.textScrollList( Window_global.scrollList, q=1, ai=1 )
        if not listItems: listItems = []
            
        sels = cmds.ls( sl=1 )
        for sel in sels:
            listItems.append( sel )
        
        targetItems = []
        for item in listItems:
            if not cmds.objExists( item ): continue
            if item in targetItems: continue
            targetItems.append( item )
        
        cmds.textScrollList( Window_global.scrollList, e=1, ra=1 )
        for item in targetItems:
            cmds.textScrollList( Window_global.scrollList, e=1, append=item )
    

    
    @staticmethod
    def loadGround( evt=0 ):
        sels = cmds.ls( sl=1 )
        if not sels: return None
        cmds.textField( Window_global.txf_ground, e=1, tx= sels[-1] )
    

    @staticmethod
    def removeObject( evt=0 ):
        selItems = cmds.textScrollList( Window_global.scrollList, q=1, si=1 )
        for item in selItems:
            cmds.textScrollList( Window_global.scrollList, e=1, ri=item )
    
    
    @staticmethod
    def setObjectBySelection( evt=0 ):
        pass
    
    
    @staticmethod
    def setTool_putObjectAtGround( evt=0 ):
        ground = cmds.textField( Window_global.txf_ground, q=1, tx=1 )
        cmds.select( ground )
        if not cmds.pluginInfo( 'sgPutObjectAtGround', q=1, l=1 ):
            appendPluginPath()
            cmds.loadPlugin( 'sgPutObjectAtGround' )
        cmds.setToolTo( 'sgPutObjectAtGroundContext1' )
        cmds.select( d=1 )
        




class UI_ground:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        txf_ground = cmds.textField( lineEditName, h=25 )
        bt_ground  = cmds.button( l='Load ground', h=25 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(txf_ground, 'top', 0), (txf_ground, 'left', 0),
                               (bt_ground, 'top', 0 ), ( bt_ground, 'right', 0 )],
                         ac = [ (txf_ground, 'right', 5, bt_ground) ] )
        
        
        Window_global.txf_ground = txf_ground
        Window_global.bt_ground = bt_ground
        
        return form




class UI_buttons:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        bt_add = cmds.button( l='Add Objects' )
        bt_remove = cmds.button( l='Remove Object' )
        bt_tool   = cmds.button( l='Put Object' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( bt_add, 'top', 0 ), ( bt_add, 'left', 0 ),
                               ( bt_remove, 'top', 0 ), ( bt_remove, 'right', 0 ),
                               ( bt_tool, 'left', 0 ), ( bt_tool, 'right', 0 )],
                         ap = [(bt_add, 'right', 3, 50 ), (bt_remove, 'left', 3, 50 )],
                         ac = [(bt_tool, 'top', 5, bt_add )])
        
        
        Window_global.bt_add = bt_add
        Window_global.bt_remove = bt_remove
        Window_global.bt_tool = bt_tool
        
        return form






class Window:
    
    def __init__(self):
        
        self.ui_ground = UI_ground()
        self.ui_buttons = UI_buttons()
    
    
    def create(self):
        
        if cmds.window( Window_global.objectName, q=1, ex=1 ):
            cmds.deleteUI( Window_global.objectName )
        cmds.window( Window_global.objectName, title= Window_global.title )
        
        form = cmds.formLayout()
        ui_ground = self.ui_ground.create()
        scrollList = cmds.textScrollList( listWidgetName )
        ui_buttons = self.ui_buttons.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[(ui_ground, 'top', 5), (ui_ground, 'left', 5), (ui_ground, 'right', 5),
                             (scrollList, 'left', 5), (scrollList, 'right', 5),
                             (ui_buttons, 'bottom', 5), (ui_buttons, 'left', 5), (ui_buttons, 'right', 5) ],
                         ac = [( scrollList, 'top', 5, ui_ground), ( scrollList, 'bottom', 5, ui_buttons)])
        
        #cmds.window( Window_global.objectName, e=1, w= Window_global.width, h= Window_global.height )
        cmds.showWindow( Window_global.objectName )
        Window_global.scrollList = scrollList
        
        cmds.button( Window_global.bt_ground, e=1, c=Window_cmd.loadGround )
        cmds.button( Window_global.bt_add,    e=1, c=Window_cmd.addObject )
        cmds.button( Window_global.bt_remove, e=1, c=Window_cmd.removeObject )
        cmds.button( Window_global.bt_tool,   e=1, c=Window_cmd.setTool_putObjectAtGround )
    
    
    
def show():
    
    Window().create()
