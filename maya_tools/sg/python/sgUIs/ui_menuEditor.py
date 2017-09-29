import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken


class Window( QtGui.QMainWindow ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    objectName = "sg_menuEditor"
    title = "UI - Menu Editor"
    width = 600
    height = 300

    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget( self.centralWidget )
        
        self.layoutBase = QtGui.QVBoxLayout( self.centralWidget )
        
        layout_menuPath   = QtGui.QHBoxLayout()
        label_menuPath    = QtGui.QLabel( "Menu path" )
        lineEdit_menuPath = QtGui.QLineEdit()
        button_menuPath = QtGui.QPushButton( '...' )
        [ layout_menuPath.addWidget( widget ) for widget in [label_menuPath,lineEdit_menuPath,button_menuPath] ]
        scrollArea = QtGui.QScrollArea()
        
        listWidgetSizePolicy = QtGui.QSizePolicy()
        listWidgetSizePolicy.setVerticalPolicy( QtGui.QSizePolicy.Preferred )
        listWidgetSizePolicy.setHorizontalPolicy( QtGui.QSizePolicy.Maximum )
        
        layoutSpliterWidget = QtGui.QWidget()
        layoutSpliter = QtGui.QHBoxLayout(layoutSpliterWidget)
        layoutSpliter.setContentsMargins(1,1,1,1)
        listWidgetBase  = QtGui.QListWidget();listWidgetBase.setSizePolicy( listWidgetSizePolicy )
        toolButton = QtGui.QPushButton('||')
        listWidgetBase2 = QtGui.QListWidget();listWidgetBase2.setSizePolicy( listWidgetSizePolicy )
        label_empty = QtGui.QLabel()
        layoutSpliter.addWidget( listWidgetBase )
        layoutSpliter.addWidget( toolButton )
        layoutSpliter.addWidget( listWidgetBase2 )
        layoutSpliter.addWidget( label_empty )
        
        scrollArea.setWidget( layoutSpliterWidget )
        scrollArea.setWidgetResizable( True )
        
        self.layoutBase.addLayout( layout_menuPath )
        self.layoutBase.addWidget( scrollArea )
        
        listWidgetBase.setFixedWidth( 200 )
        listWidgetBase2.setFixedWidth( 200 )
        toolButton.setFixedWidth( 20 )
        


def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mainui = Window(Window.mayaWin)
    mainui.setObjectName( Window.objectName )
    mainui.setWindowTitle( Window.title )
    mainui.resize( Window.width, Window.height )
    mainui.show()