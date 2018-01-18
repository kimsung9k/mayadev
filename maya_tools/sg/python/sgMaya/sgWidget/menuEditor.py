import maya.cmds as cmds
import maya.OpenMayaUI
from __qtImprot import *


class Window( QMainWindow ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "sg_menuEditor"
    title = "UI - Menu Editor"
    width = 600
    height = 300

    def __init__(self, *args, **kwargs ):
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.centralWidget = QWidget()
        self.setCentralWidget( self.centralWidget )
        
        self.layoutBase = QVBoxLayout( self.centralWidget )
        
        layout_menuPath   = QHBoxLayout()
        label_menuPath    = QLabel( "Menu path" )
        lineEdit_menuPath = QLineEdit()
        button_menuPath = QPushButton( '...' )
        [ layout_menuPath.addWidget( widget ) for widget in [label_menuPath,lineEdit_menuPath,button_menuPath] ]
        scrollArea = QScrollArea()
        
        listWidgetSizePolicy = QSizePolicy()
        listWidgetSizePolicy.setVerticalPolicy( QSizePolicy.Preferred )
        listWidgetSizePolicy.setHorizontalPolicy( QSizePolicy.Maximum )
        
        layoutSpliterWidget = QWidget()
        layoutSpliter = QHBoxLayout(layoutSpliterWidget)
        layoutSpliter.setContentsMargins(1,1,1,1)
        listWidgetBase  = QListWidget();listWidgetBase.setSizePolicy( listWidgetSizePolicy )
        toolButton = QPushButton('||')
        listWidgetBase2 = QListWidget();listWidgetBase2.setSizePolicy( listWidgetSizePolicy )
        label_empty = QLabel()
        layoutSpliter.addWidget( listWidgetBase )
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
    
    
if __name__ == '__main__':
    show()


