import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial
from pymel.core.uitypes import Layout



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
    objectName = "sgui_createPointOnCurve"
    title = "Create Point On Curve"
    width = 350
    height = 50
    
    infoPath = cmds.about(pd=True) + "/sg/createPointOnCurve/uiInfo.txt"
    infoPath2 = cmds.about( pd=True ) + '/sg/createPointOnCurve/uiInfo2.txt'
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
        json.dump( [posX, posY, width, height ], f, True, False, False )
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



class Functions:
    
    @staticmethod
    def setButtonEnabled( evt=0 ):
        
        curveExists = False
        
        sels = cmds.ls( sl=1 )
        for sel in sels:
            if cmds.nodeType( sel ) in ['transform', 'joint']:
                selShape = cmds.listRelatives( sel, s=1, type='nurbsCurve' )
                if not selShape: continue
                curveExists = True
            elif cmds.nodeType( sel ) == 'nurbsCurve':
                curveExists = True
        Window_global.button.setEnabled( curveExists )
    
    
    @staticmethod
    def createPointOnCurve( evt=0 ):
        
        sliderValue = Window_global.slider.value()
        
        sels = cmds.ls( sl=1 )
        
        curveShapes = []
        for sel in sels:
            if cmds.nodeType( sel ) in ['transform', 'joint']:
                selShapes = cmds.listRelatives( sel, s=1, f=1, type='nurbsCurve' )
                if not selShapes: continue
                for selShape in selShapes:
                    if cmds.getAttr( selShape + '.io' ): continue
                    curveShapes.append( selShape )
            elif cmds.nodeType( sel ) == 'nurbsCurve':
                curveShapes.append( sel )
        
        eachParamValue = 1.0
        if sliderValue == 1:
            addParamValue = 0.5
        else:
            addParamValue = 0.0
            eachParamValue = 1.0/(sliderValue-1)

        cmds.undoInfo( ock=1 )
        for curveShape in curveShapes:
            for i in range( sliderValue ):
                curveInfo = cmds.createNode( 'pointOnCurveInfo' )
                cmds.connectAttr( curveShape + '.worldSpace', curveInfo+'.inputCurve' )
                cmds.setAttr( curveInfo + '.top', 1 )
                trNode = cmds.createNode( 'transform' )
                cmds.addAttr( trNode, ln='param', min=0, max=100, dv=(eachParamValue * i + addParamValue)*100 )
                cmds.setAttr( trNode + '.param', e=1, k=1 )
                cmds.setAttr( trNode + '.dh', 1 )
                cmds.connectAttr( curveInfo + '.position', trNode + '.t' )
                cmds.setAttr( trNode + '.inheritsTransform', 0 )
                multDouble = cmds.createNode( 'multDoubleLinear' )
                cmds.setAttr( multDouble + '.input2', 0.01 )
                cmds.connectAttr( trNode + '.param', multDouble + '.input1' )
                cmds.connectAttr( multDouble + '.output', curveInfo + '.parameter' )
        cmds.undoInfo( cck=1 )
    
        




class Window( QtGui.QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        
        self.minimum = 1
        self.maximum = 100
        self.lineEditMaximum = 10000
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        #self.setWindowFlags( QtCore.Qt.Drawer )
        self.setWindowTitle( Window_global.title )
        
        widgetMain = QtGui.QWidget()
        layoutVertical = QtGui.QVBoxLayout( widgetMain )
        self.setCentralWidget( widgetMain )
        
        layoutSlider = QtGui.QHBoxLayout()
        lineEdit     = QtGui.QLineEdit(); lineEdit.setFixedWidth( 100 )
        lineEdit.setText( str( 1 ) )
        validator    = QtGui.QIntValidator(self.minimum, self.lineEditMaximum, self)
        lineEdit.setValidator( validator )
        slider       = QtGui.QSlider(); slider.setOrientation( QtCore.Qt.Horizontal )
        slider.setMinimum( self.minimum )
        slider.setMaximum( self.maximum )
        layoutSlider.addWidget( lineEdit )
        layoutSlider.addWidget( slider )
        button       = QtGui.QPushButton( 'Create' )
        
        layoutVertical.addLayout( layoutSlider )
        layoutVertical.addWidget( button )
        
        QtCore.QObject.connect( slider, QtCore.SIGNAL('valueChanged(int)'),   self.sliderValueChanged )
        QtCore.QObject.connect( lineEdit, QtCore.SIGNAL('textEdited(QString)'), self.lineEditValueChanged )
        QtCore.QObject.connect( button, QtCore.SIGNAL('clicked()'), Functions.createPointOnCurve )
        self.slider = slider
        self.lineEdit = lineEdit
        
        Window_global.slider = slider
        Window_global.button = button
        
        Functions.setButtonEnabled()
        
    
    def sliderValueChanged( self, value, evt=0 ):
        
        self.lineEdit.setText( str(value) )
    
    
    def lineEditValueChanged(self, value, evt=0 ):
        
        if value:
            self.slider.setValue( int( value ) )
    
    

    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [QtCore.QEvent.LayoutRequest,QtCore.QEvent.Move,QtCore.QEvent.Resize] :
            Window_global.saveInfo()



def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    #cmds.scriptJob( e=['SelectionChanged', Functions.setButtonEnabled ], p=Window_global.mainGui.objectName() )
    
    Window_global.loadInfo()
    Window_global.mainGui.show()


