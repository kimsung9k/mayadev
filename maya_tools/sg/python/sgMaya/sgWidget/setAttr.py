import maya.OpenMayaUI
import os


from maya import cmds

if int( cmds.about( v=1 ) ) < 2017:
    from PySide import QtGui, QtCore
    import shiboken
    from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu,QCursor, QMessageBox, QBrush, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, QIntValidator,\
    QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction,\
    QFont, QGridLayout
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken
    from PySide2.QtWidgets import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QVBoxLayout, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QMessageBox, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QSlider,\
    QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction, QGridLayout
    
    from PySide2.QtGui import QColor, QCursor, QBrush, QDoubleValidator, QIntValidator, QImage, QPixmap, QTransform,\
    QPaintEvent, QFont



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
    objectName = "sg_ui_setAttr"
    title = "UI - Set attr"
    width = 300
    height = 10
    
    infoPath = cmds.about(pd=True) + "/sg/ui_setAttrInfo.txt"
    makeFile( infoPath )
    
    mainGui = QMainWindow()





class UI_labels( QWidget ):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.text_srcAttr = QLabel('Attribute Name')
        self.text_dstAttr = QLabel('Attribute Value')
        
        self.text_srcAttr.setAlignment( QtCore.Qt.AlignCenter )
        self.text_dstAttr.setAlignment( QtCore.Qt.AlignCenter )
        
        self.layout.addWidget( self.text_srcAttr )
        self.layout.addWidget( self.text_dstAttr )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass





class UI_attrlist( QWidget ):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.lineEdit_srcAttr = QLineEdit()
        self.lineEdit_dstAttr = QLineEdit()
        
        self.layout.addWidget( self.lineEdit_srcAttr )
        self.layout.addWidget( self.lineEdit_dstAttr )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass




class UI_options( QWidget ):
    
    def __init__( self, *args, **kwargs ):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QVBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.checkBox = QCheckBox( "To Parent" )
        self.layout.addWidget( self.checkBox )        
        
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass
        




class UI_buttons( QWidget ):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.button_connect = QPushButton("SET")
        self.button_addLine = QPushButton("Add Line")
        self.lineEdit_dstAttr = QLineEdit()
        self.layout.addWidget( self.button_connect )
        self.layout.addWidget( self.button_addLine )
        
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass
    




class Window( QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowFlags(QtCore.Qt.Drawer)

        self.layoutWidget = QWidget()
        self.setCentralWidget( self.layoutWidget )
        
        self.layout = QVBoxLayout( self.layoutWidget )
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
        
        
        def setAttrCommand():
            
            import pymel.core
            cmds.undoInfo( ock=1 )
            sels = pymel.core.ls( sl=1 )
            numItems = self.layout.count()
            
            for i in range( 1, numItems-1 ):
                targetWidget = self.layout.itemAt( i ).widget()
                
                attrName = targetWidget.lineEdit_srcAttr.text()
                attrValue = targetWidget.lineEdit_dstAttr.text()
                
                if not attrName or not attrValue: continue

                for sel in sels:
                    attrType = sel.attr( attrName ).type()
                    if attrType == 'string':
                        sel.attr( attrName ).set( attrValue )
                    else:
                        print "attr value : ", attrValue
                        if attrValue.find( ',' ) != -1:
                            values = [ float( value ) for value in attrValue.split( ',' ) ]
                            sel.attr( attrName ).set( values )
                        else:
                            sel.attr( attrName ).set( float( attrValue ) ) 

            cmds.undoInfo( cck=1 )
            
        self.ui_buttons.button_connect.clicked.connect( setAttrCommand )
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
    
    pos = Window_global.mainGui.mapFromGlobal( QCursor.pos() )
    
    Window_global.mainGui.move( pos.x()-25, pos.y()-63 )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.mainGui.show()
