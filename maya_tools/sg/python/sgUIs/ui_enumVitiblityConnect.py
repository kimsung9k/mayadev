import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken
import os, sys
import json
from functools import partial
import pymel.core



def addAttr( target, **options ):
    
    items = options.items()
    
    attrName = ''
    channelBox = False
    keyable = False
    for key, value in items:
        if key in ['ln', 'longName']:
            attrName = value
        elif key in ['cb', 'channelBox']:
            channelBox = True
            options.pop( key )
        elif key in ['k', 'keyable']:
            keyable = True 
            options.pop( key )
    
    if pymel.core.attributeQuery( attrName, node=target, ex=1 ): return None
    
    pymel.core.addAttr( target, **options )
    
    if channelBox:
        pymel.core.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        pymel.core.setAttr( target+'.'+attrName, e=1, k=1 )



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
    objectName = "sg_ui_enumVisibilityConnect"
    title = "UI - Enum Visibility Connect"
    width = 300
    height = 10
    
    infoPath = cmds.about(pd=True) + "/sg/sg_ui_enumVisibilityConnect.txt"
    makeFile( infoPath )
    
    mainGui = QtGui.QMainWindow()





class UI_AttributeName( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs ):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )





class UI_labels( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.text_srcAttr = QtGui.QLabel('Enum Name')
        self.text_dstAttr = QtGui.QLabel('Target')
        
        self.text_srcAttr.setAlignment( QtCore.Qt.AlignCenter )
        self.text_dstAttr.setAlignment( QtCore.Qt.AlignCenter )
        
        self.layout.addWidget( self.text_srcAttr )
        self.layout.addWidget( self.text_dstAttr )

    
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
        
        self.lineEdit_srcAttr = QtGui.QLineEdit()
        self.lineEdit_dstAttr = QtGui.QLineEdit()
        
        self.layout.addWidget( self.lineEdit_srcAttr )
        self.layout.addWidget( self.lineEdit_dstAttr )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass





class UI_options( QtGui.QWidget ):
    
    def __init__( self, *args, **kwargs ):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QVBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.checkBox = QtGui.QCheckBox( "To Parent" )
        self.layout.addWidget( self.checkBox )        
        
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
        
        self.button_connect = QtGui.QPushButton("Connect")
        self.button_addLine = QtGui.QPushButton("Add Line")
        self.lineEdit_dstAttr = QtGui.QLineEdit()
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
        self.ui_driverAttr = UI_attrlist()
        #self.ui_options    = UI_options()
        self.ui_buttons    = UI_buttons()
        self.layout.addWidget( self.ui_labels )
        self.layout.addWidget( self.ui_driverAttr )
        #self.layout.addWidget( self.ui_options )
        self.layout.addWidget( self.ui_buttons )


        def addLineCommand():
            
            numItems = self.layout.count()
            attrlist = UI_attrlist()
            self.layout.insertWidget( numItems-2, attrlist )
        
        
        def connectCommand():
            
            import pymel.core
            cmds.undoInfo( ock=1 )
            sels = pymel.core.ls( sl=1 )
            numItems = self.layout.count()
            
            enumNames     = []
            targetObjects = []
            
            attrName = 'mode'
            
            for i in range( 1, numItems-1 ):
                targetWidget = self.layout.itemAt( i ).widget()
                eachEnumName = targetWidget.lineEdit_srcAttr.text()
                targetObject = pymel.core.ls( targetWidget.lineEdit_dstAttr.text() )[0]
                if not eachEnumName: continue
                enumNames.append( eachEnumName )
                targetObjects.append( targetObject )
            
            enumName = ':'.join( enumNames ) + ':'
            addAttr( sels[-1], ln=attrName, at='enum', enumName = enumName, k=1 )
            
            for i in range( len( targetObjects ) ):
                if not targetObjects[i]: continue
                condition = pymel.core.createNode( 'condition' )
                sels[-1].attr( attrName ) >> condition.firstTerm
                condition.secondTerm.set( i )
                condition.colorIfTrueR.set( 1 )
                condition.colorIfFalseR.set( 0 )
                condition.outColorR >> targetObjects[i].v
                
            
            cmds.undoInfo( cck=1 )
            
        self.ui_buttons.button_connect.clicked.connect( connectCommand )
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
    Window_global.mainGui.setWindowTitle( Window_global.title )
    
    pos = Window_global.mainGui.mapFromGlobal( QtGui.QCursor.pos() )
    
    Window_global.mainGui.move( pos.x()-25, pos.y()-63 )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.mainGui.show()
