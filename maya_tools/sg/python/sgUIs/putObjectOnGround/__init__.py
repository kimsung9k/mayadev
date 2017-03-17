import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial



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
    title = "Put Object On Ground"
    width = 300
    height = 300
    
    infoPath = cmds.about(pd=True) + "/sg/putObjectOnGround/uiInfo.txt"
    makeFile( infoPath )
    
    mainGui = QtGui.QMainWindow()
    listItems = []

    objectName = 'sgui_putObjectOnGround'
    listWidgetPutName     =  objectName + "_listPut"
    listWidgetGroundName  =  objectName + "_listGround"
    randomOptionRotName   =  objectName + "_randomRot"
    randomOptionScaleName =  objectName + "_randomScale"
    randomOptionRotAName   = objectName + "_randomRotAll"
    randomOptionScaleAName = objectName + "_randomScaleAll"
    offsetByObjectName     = objectName + '_offsetObject'
    offsetByGroundName     = objectName + '_offsetGround'
    checkNormalOrientName  = objectName + '_checkNormalOrient'
    orientEditModeName     = objectName + '_orientEditMode'
    duGroupListName        = objectName + '_duGroupList'
    componentCheckName         = objectName + '_componentCheck'
    
    
    @staticmethod
    def saveInfo2( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath2
        
        rotateChecked = ''
        
        '''
        f = open( filePath, "w" )
        json.dump( , f, True, False, False )
        f.close()
        '''
    
    @staticmethod
    def loadInfo2( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath2
        
        f = open( filePath, 'r')
        try:data = json.load( f )
        except: f.close(); return None
        f.close()
    
    

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
    def setTool_putObjectOnGround( evt=0 ):

        if not cmds.pluginInfo( 'sgPutObjectOnGround', q=1, l=1 ):
            appendPluginPath()
            cmds.loadPlugin( 'sgPutObjectOnGround' )
        cmds.setToolTo( 'sgPutObjectOnGroundContext1' )
        cmds.select( d=1 )
        



class UI_objectList( QtGui.QWidget ):
    
    def __init__(self ):
        
        QtGui.QWidget.__init__( self )
        layout = QtGui.QVBoxLayout( self )
        
        label = QtGui.QLabel()
        listWidget = QtGui.QListWidget()
        listWidget.setSelectionMode( QtGui.QAbstractItemView.ExtendedSelection )
        hLayout = QtGui.QHBoxLayout()
        buttonLoad   = QtGui.QPushButton( "LOAD")
        buttonRemove = QtGui.QPushButton( "REMOVE")
        hLayout.addWidget( buttonLoad )
        hLayout.addWidget( buttonRemove )
        
        layout.addWidget( label )
        layout.addWidget( listWidget )
        layout.addLayout( hLayout )
        
        self.label = label
        self.listWidget = listWidget
        self.buttonLoad = buttonLoad
        self.buttonRemove = buttonRemove
        
        QtCore.QObject.connect( self.buttonLoad, QtCore.SIGNAL( 'clicked()' ), self.loadCommand )
        QtCore.QObject.connect( self.buttonRemove, QtCore.SIGNAL( 'clicked()' ), self.removeCommand )
        

    def loadCommand(self, evt=0 ):

        count = self.listWidget.count()
        existItems = []
        for i in range( count ):
            existItem = self.listWidget.item( i ).text()
            existItems.append( existItem )

        sels = cmds.ls( sl=1 )
        for sel in sels:
            if cmds.nodeType( sel ) != 'transform': continue
            if sel in existItems: continue
            self.listWidget.addItem( sel )
        
    
    
    def removeCommand(self, evt=0 ):
        
        selItems = self.listWidget.selectedItems()
        
        for selItem in selItems:
            self.listWidget.takeItem( self.listWidget.row( selItem ) )
        
    



class UI_radomLabel( QtGui.QWidget ):
    
    def __init__(self):
        
        QtGui.QWidget.__init__( self )
        layout = QtGui.QHBoxLayout( self )
        
        label = QtGui.QLabel()
        label.setFixedWidth( 120 )
        
        layout.addWidget( label )
        labelX = QtGui.QLabel( 'X Range' )
        labelY = QtGui.QLabel( 'Y Range' )
        labelZ = QtGui.QLabel( 'Z Range' )
        labelX.setAlignment( QtCore.Qt.AlignCenter )
        labelY.setAlignment( QtCore.Qt.AlignCenter )
        labelZ.setAlignment( QtCore.Qt.AlignCenter )
        layout.addWidget( labelX )
        layout.addWidget( labelY )
        layout.addWidget( labelZ )






class UI_randomOption( QtGui.QWidget ):
    
    def __init__(self, text, validator, minValue, maxValue ):
    
        QtGui.QWidget.__init__( self )
        layout = QtGui.QHBoxLayout( self )
        
        checkBox = QtGui.QCheckBox()
        checkBox.setFixedWidth( 115 )
        checkBox.setText( text )
        
        layout.addWidget( checkBox )
        
        hLayoutX = QtGui.QHBoxLayout()
        lineEditXMin = QtGui.QLineEdit()
        lineEditXMax = QtGui.QLineEdit()
        hLayoutX.addWidget( lineEditXMin )
        hLayoutX.addWidget( lineEditXMax )
        lineEditXMin.setValidator( validator )
        lineEditXMax.setValidator( validator )
        lineEditXMin.setText( str( minValue ) )
        lineEditXMax.setText( str( maxValue ) )
        
        layout.addLayout( hLayoutX )
        
        self.checkBox      = checkBox
        self.lineEditX_min = lineEditXMin
        self.lineEditX_max = lineEditXMax
        self.lineEdits = [ lineEditXMin, lineEditXMax ]

        QtCore.QObject.connect( checkBox, QtCore.SIGNAL( "clicked()" ), self.updateEnabled )
        self.updateEnabled()
    
    
    def updateEnabled(self, *args, **kwargs ):

        enabledValue = False
        if self.checkBox.isChecked():
            enabledValue = True
        
        for lineEdit in self.lineEdits:
            lineEdit.setEnabled( enabledValue )


    def eventFilter(self, *args, **kwargs):
        
        return QtGui.QWidget.eventFilter(self, *args, **kwargs)
    






class UI_randomOption2( QtGui.QWidget ):
    
    def __init__(self, text, validator, minValue, maxValue ):
        
        QtGui.QWidget.__init__( self )
        layout = QtGui.QHBoxLayout( self )
        
        checkBox = QtGui.QCheckBox()
        checkBox.setFixedWidth( 115 )
        checkBox.setText( text )
        
        layout.addWidget( checkBox )
        
        hLayoutX = QtGui.QHBoxLayout()
        lineEditXMin = QtGui.QLineEdit()
        lineEditXMax = QtGui.QLineEdit()
        hLayoutX.addWidget( lineEditXMin )
        hLayoutX.addWidget( lineEditXMax )
        lineEditXMin.setValidator( validator )
        lineEditXMax.setValidator( validator )
        lineEditXMin.setText( str( minValue ) )
        lineEditXMax.setText( str( maxValue ) )
        
        hLayoutY = QtGui.QHBoxLayout()
        lineEditYMin = QtGui.QLineEdit()
        lineEditYMax = QtGui.QLineEdit()
        hLayoutY.addWidget( lineEditYMin )
        hLayoutY.addWidget( lineEditYMax )
        lineEditYMin.setValidator( validator )
        lineEditYMax.setValidator( validator )
        lineEditYMin.setText( str( minValue ) )
        lineEditYMax.setText( str( maxValue ) )
        
        hLayoutZ = QtGui.QHBoxLayout()
        lineEditZMin = QtGui.QLineEdit()
        lineEditZMax = QtGui.QLineEdit()
        hLayoutZ.addWidget( lineEditZMin )
        hLayoutZ.addWidget( lineEditZMax )
        lineEditZMin.setValidator( validator )
        lineEditZMax.setValidator( validator )
        lineEditZMin.setText( str( minValue ) )
        lineEditZMax.setText( str( maxValue ) )
        
        layout.addLayout( hLayoutX )
        layout.addLayout( hLayoutY )
        layout.addLayout( hLayoutZ )
        
        self.checkBox      = checkBox
        self.lineEditX_min = lineEditXMin
        self.lineEditX_max = lineEditXMax
        self.lineEditY_min = lineEditYMin
        self.lineEditY_max = lineEditYMax
        self.lineEditZ_min = lineEditZMin
        self.lineEditZ_max = lineEditZMax
        self.lineEdits = [ lineEditXMin, lineEditXMax, lineEditYMin, lineEditYMax, lineEditZMin, lineEditZMax ]

        QtCore.QObject.connect( checkBox, QtCore.SIGNAL( "clicked()" ), self.updateEnabled )
        self.updateEnabled()


    def updateEnabled(self, *args, **kwargs ):

        enabledValue = False
        if self.checkBox.isChecked():
            enabledValue = True
        
        for lineEdit in self.lineEdits:
            lineEdit.setEnabled( enabledValue )


    def eventFilter(self, *args, **kwargs):
        
        return QtGui.QWidget.eventFilter(self, *args, **kwargs)






class UI_OffsetSlider( QtGui.QWidget ):
    
    def __init__(self, text, minValue, maxValue, defaultValue ):
        
        QtGui.QWidget.__init__( self )
        
        validator = QtGui.QDoubleValidator(minValue, maxValue, 2, self )
        mainLayout = QtGui.QHBoxLayout( self )
        
        checkBox = QtGui.QCheckBox()
        checkBox.setFixedWidth( 115 )
        checkBox.setText( text )
        
        lineEdit = QtGui.QLineEdit()
        lineEdit.setValidator( validator )
        lineEdit.setText( str(defaultValue) )
        
        slider = QtGui.QSlider( QtCore.Qt.Horizontal )
        slider.setMinimum( minValue*100 )
        slider.setMaximum( maxValue*100 )
        slider.setValue( defaultValue )
        
        mainLayout.addWidget( checkBox )
        mainLayout.addWidget( lineEdit )
        mainLayout.addWidget( slider )
        
        QtCore.QObject.connect( slider, QtCore.SIGNAL( 'valueChanged(int)' ), self.syncWidthLineEdit )
        QtCore.QObject.connect( lineEdit, QtCore.SIGNAL( 'textChanged(QString)' ), self.syncWidthSlider )
        QtCore.QObject.connect( checkBox, QtCore.SIGNAL( "clicked()" ), self.updateEnabled )
        
        self.checkBox = checkBox
        self.slider = slider
        self.lineEdit = lineEdit
        
        self.updateEnabled()
    
    
    
    def updateEnabled(self, *args, **kwargs ):

        enabledValue = False
        if self.checkBox.isChecked():
            enabledValue = True
        self.lineEdit.setEnabled( enabledValue )
        self.slider.setEnabled( enabledValue )
    


    def syncWidthLineEdit(self, *args ):
        
        self.lineEdit.setText( str(args[0]/100.0) )
    
    
    
    def syncWidthSlider(self, *args ):
        
        try:self.slider.setValue( float( self.lineEdit.text() )*100 )
        except:pass



    def eventFilter(self, *args, **kwargs):
        return QtGui.QWidget.eventFilter(self, *args, **kwargs)





class Window( QtGui.QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window_global.title )
        
        mainWidget = QtGui.QWidget()
        self.setCentralWidget( mainWidget )
        
        vLayout = QtGui.QVBoxLayout( mainWidget )
        
        hLayoutListWidget = QtGui.QHBoxLayout()
        widgetPutList  = UI_objectList()
        widgetBaseList = UI_objectList()
        widgetPutList.label.setText( 'Put Object List' )
        widgetBaseList.label.setText( 'Ground Object List' )
        buttonPut = QtGui.QPushButton( 'Put Object' )
        widgetPutList.listWidget.setObjectName( Window_global.listWidgetPutName )
        widgetBaseList.listWidget.setObjectName( Window_global.listWidgetGroundName )
        
        widgetGroupList = UI_objectList()
        widgetGroupList.label.setText( 'Duplicate Group List' )
        widgetGroupList.listWidget.setObjectName( Window_global.duGroupListName )
        widgetGroupList.listWidget.setSelectionMode( QtGui.QAbstractItemView.SingleSelection )
        
        hLayoutListWidget.addWidget( widgetPutList )
        hLayoutListWidget.addWidget( widgetBaseList )
        
        randomGroupBox = QtGui.QGroupBox( 'Random' )
        vLayoutRandom = QtGui.QVBoxLayout( randomGroupBox )
        
        rotateValidator = QtGui.QDoubleValidator(-1000000, 1000000, 2, self )
        scaleValidator  = QtGui.QDoubleValidator( 0.0, 100, 2, self )
        
        randomOptionR = UI_randomOption2( 'Rotate', rotateValidator, -45, 45 )
        randomOptionS = UI_randomOption2( 'Scale', scaleValidator, 0.8, 1.2 )
        randomOptionRA = UI_randomOption( 'Rotate All', rotateValidator, -45, 45 )
        randomOptionSA = UI_randomOption( 'Scale All', scaleValidator, 0.8, 1.2 )
        randomOptionR.setObjectName( Window_global.randomOptionRotName )
        randomOptionS.setObjectName( Window_global.randomOptionScaleName )
        randomOptionRA.setObjectName( Window_global.randomOptionRotAName )
        randomOptionSA.setObjectName( Window_global.randomOptionScaleAName )
        
        vLayoutRandom.addWidget( randomOptionR )
        vLayoutRandom.addWidget( randomOptionS )
        vLayoutRandom.addWidget( randomOptionRA )
        vLayoutRandom.addWidget( randomOptionSA )
        
        offsetGroupBox = QtGui.QGroupBox( 'Offset' )
        vLayoutOffset = QtGui.QVBoxLayout( offsetGroupBox )
        
        componentCheck    = QtGui.QCheckBox( "Component check" )
        offsetSlider1 = UI_OffsetSlider( "Offset By Object",  -1, 1, 0 )
        offsetSlider2 = UI_OffsetSlider( "Offset By Ground",  -100, 100, 0 )
        componentCheck.setObjectName( Window_global.componentCheckName )
        offsetSlider1.setObjectName( Window_global.offsetByObjectName )
        offsetSlider2.setObjectName( Window_global.offsetByGroundName )
        
        vLayoutOffset.addWidget( componentCheck )
        vLayoutOffset.addWidget( offsetSlider1 )
        vLayoutOffset.addWidget( offsetSlider2 )
        
        orientGroupBox = QtGui.QGroupBox( 'Orient Option' )
        vLayoutOrient = QtGui.QVBoxLayout( orientGroupBox )
        orientNormalCheck  = QtGui.QCheckBox("Ground Normal Affects")
        hLayoutCombobox = QtGui.QHBoxLayout()
        orientTypeText = QtGui.QLabel( 'Orient Edit Type : ' )
        orientTypeComboBox = QtGui.QComboBox()
        orientTypeComboBox.addItem( 'All' )
        orientTypeComboBox.addItem( 'Only Y' )
        hLayoutCombobox.addWidget( orientTypeText )
        hLayoutCombobox.addWidget( orientTypeComboBox )
        vLayoutOrient.addWidget( orientNormalCheck )
        vLayoutOrient.addLayout( hLayoutCombobox )
        orientNormalCheck.setObjectName( Window_global.checkNormalOrientName )
        orientTypeComboBox.setObjectName( Window_global.orientEditModeName )
        
        vLayout.addLayout( hLayoutListWidget )
        vLayout.addWidget( widgetGroupList )
        vLayout.addWidget( randomGroupBox )
        vLayout.addWidget( offsetGroupBox )
        vLayout.addWidget( orientGroupBox )
        vLayout.addWidget( buttonPut )
        Window_global.loadInfo()
        
        QtCore.QObject.connect( buttonPut, QtCore.SIGNAL( 'clicked()' ), Window_cmd.setTool_putObjectOnGround )
        
        
    
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
    
    Window_global.loadInfo()
    Window_global.mainGui.show()



