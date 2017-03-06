import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial



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
    objectName = "sg_Tool_createAnimCurve"
    title = "SG Tool Create AnimCurve"
    width = 300
    height = 10
    
    infoPath = cmds.about(pd=True) + "/sg_toolInfo/createAnimCurve.txt"
    makeFile( infoPath )
    
    mainGui = QtGui.QMainWindow()




class Commands:
    
    @staticmethod
    def connectCommand( uiInstance ):
        
        sels = cmds.ls( sl=1 )
        selChannels = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
        
        numItems = uiInstance.layout.count()
        animNode = cmds.createNode( 'animCurveUU' )
        
        for i in range( 1, numItems-1 ):
            targetWidget = uiInstance.layout.itemAt( i ).widget()
            
            key = targetWidget.lineEdit_key.text()
            value = targetWidget.lineEdit_value.text()
            
            cmds.setKeyframe( animNode, f=float(key), v=float(value) )
            cmds.keyTangent( animNode, f=(float(key),float(key)), itt='linear', ott = 'linear' )
        
        if sels and selChannels:
            cmds.connectAttr( sels[0] + '.' + selChannels[0], animNode + '.input' )
            addString = ''
            if float(key) > 0:
                addString = 'positive'
            else:
                addString = 'negative'
            animNode = cmds.rename( animNode, selChannels[0] + '_' + addString + '_from_' + sels[0] )
        
        cmds.select( animNode )




class UI_labels( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.text_key = QtGui.QLabel('Float')
        self.text_value = QtGui.QLabel('Value')
        
        self.text_key.setAlignment( QtCore.Qt.AlignCenter )
        self.text_value.setAlignment( QtCore.Qt.AlignCenter )
        
        self.layout.addWidget( self.text_key )
        self.layout.addWidget( self.text_value )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass




class UI_attrlist( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.lineEdit_key = QtGui.QLineEdit()
        self.lineEdit_value = QtGui.QLineEdit()
        
        self.layout.addWidget( self.lineEdit_key )
        self.layout.addWidget( self.lineEdit_value )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass



class UI_buttons( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.button_connect = QtGui.QPushButton("Create")
        self.button_addLine = QtGui.QPushButton("Add Line")
        self.lineEdit_value = QtGui.QLineEdit()
        self.layout.addWidget( self.button_connect )
        self.layout.addWidget( self.button_addLine )
        
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass
    




class Window( QtGui.QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowFlags(QtCore.Qt.Drawer)
    
        self.layoutWidget = QtGui.QWidget()
        self.setCentralWidget( self.layoutWidget )
        
        self.layout = QtGui.QVBoxLayout( self.layoutWidget )
        self.layout.setContentsMargins( 5,5,5,5 )
        
        self.ui_labels     = UI_labels()
        self.ui_driverAttr1 = UI_attrlist()
        self.ui_driverAttr2 = UI_attrlist()
        self.ui_buttons    = UI_buttons()
        self.layout.addWidget( self.ui_labels )
        self.layout.addWidget( self.ui_driverAttr1 )
        self.layout.addWidget( self.ui_driverAttr2 )
        self.layout.addWidget( self.ui_buttons )
        
        self.ui_driverAttr1.lineEdit_key.setText( '0' )
        self.ui_driverAttr1.lineEdit_value.setText( '0' )
        self.ui_driverAttr2.lineEdit_key.setText( '1' )
        self.ui_driverAttr2.lineEdit_value.setText( '1' )
        
        
        def addLineCommand():
            
            numItems = self.layout.count()
            attrlist = UI_attrlist()
            self.layout.insertWidget( numItems-1, attrlist )
        
        self.ui_buttons.button_connect.clicked.connect( partial( Commands.connectCommand, self ) )
        self.ui_buttons.button_addLine.clicked.connect( addLineCommand )
    
    
    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass



def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.mainGui.show()
