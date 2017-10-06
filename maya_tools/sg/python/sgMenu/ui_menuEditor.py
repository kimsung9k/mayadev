#coding=utf8

import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
from commands import *



class Window( QtGui.QMainWindow ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    objectName = "sg_menuEditor"
    title = "UI - Menu Editor"
    defaultWidth = 600
    defaultHeight = 600
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/menuEditor"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    defaultMenuPath = infoBaseDir + '/defaultMenuPath.txt'
    defaultSearchPath = infoBaseDir + '/defaultSearchPath.txt'


    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget( self.centralWidget )
        self.setWindowFlags(QtCore.Qt.Dialog)
        
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
        layoutSpliterAneDisplay = QtGui.QHBoxLayout( layoutSpliterWidget )
        layoutSpliterAneDisplay.setContentsMargins(1,1,1,1)
        layoutSpliter = QtGui.QHBoxLayout()
        layoutSpliter.setContentsMargins(1,1,1,1)
        label_forDisplay = QtGui.QLabel()
        layoutSpliterAneDisplay.addLayout( layoutSpliter )
        layoutSpliterAneDisplay.addWidget( label_forDisplay )
        
        scrollArea.setWidget( layoutSpliterWidget )
        scrollArea.setWidgetResizable( True )
        
        self.layoutBase.addLayout( layout_menuPath )
        self.layoutBase.addWidget( scrollArea )
        
        QtCore.QObject.connect( button_menuPath, QtCore.SIGNAL( 'clicked()'), self.getMenuPath )
    
        self.layoutSpliter     = layoutSpliter
        self.lineEdit_menuPath = lineEdit_menuPath
        self.listWidgetSizePolicy = listWidgetSizePolicy



    def show(self, *args, **kwangs ):
        
        self.loadUIInfo()
        self.lineEdit_menuPath.setText( FileAndPaths.getStringDataFromFile( Window.defaultMenuPath ) )
        self.loadFirstMenuList()
        QtGui.QMainWindow.show( self, *args, **kwangs )



    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()



    def getMenuPath(self):
        
        FileAndPaths.makeFile( Window.defaultSearchPath )
        defaultPath = FileAndPaths.getStringDataFromFile( Window.defaultSearchPath )
        
        menuPath = FileAndPaths.getFolderFromBrowser( self, defaultPath )
        if not menuPath: return None
        if not filter( lambda x : menuPath.find( x ) != -1 , ['_MAINMENU_','_POPUPMENU_','_MENU_'] ):
            QtGui.QMessageBox.critical( self, "Error", "_MAINMENU_, '_MENU_', _POPUPMENU_ 중 하나라도 포함하는 이름의 폴더를 선택하십시요.".decode( 'utf-8' ) )
            return None 
        self.lineEdit_menuPath.setText( menuPath )
        
        FileAndPaths.setStringDataToFile( os.path.dirname( menuPath ), Window.defaultSearchPath )
        FileAndPaths.makeFile( Window.defaultMenuPath )
        FileAndPaths.setStringDataToFile( menuPath, Window.defaultMenuPath )
        self.loadFirstMenuList()
    


    def loadFirstMenuList(self):
        
        menuPath = self.lineEdit_menuPath.text()
        if not os.path.exists( menuPath ): return None
        
        for i in range( self.layoutSpliter.count() ):
            self.layoutSpliter.takeAt(0)
        
        listWidget = QtGui.QListWidget()
        listWidget.setSizePolicy( self.listWidgetSizePolicy )
        listWidget.setFixedWidth( 200 )
        self.layoutSpliter.addWidget( listWidget )
        
        items = []
        for root, dirs, names in os.walk( menuPath ):
            if dirs:items += [ [dirname, root + '/' + dirname] for dirname in dirs ]
            if names:items += [ [filename, root + '/' + filename] for filename in names ]
            break
        items.sort()
        items = filter( lambda x:x[0], [ [StringEdit.convertFilenameToMenuname(shortname), fullname] for shortname, fullname in items] )
        
        convertedStrings = [ shortname for shortname, fullname in items ]
        listWidget.addItems( convertedStrings )


    
    def saveUIInfo( self ):
        
        FileAndPaths.makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        mainWindowDict = {}
        mainWindowDict['position'] = [ self.x(), self.y() ]
        mainWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'mainWindow' ] = mainWindowDict
        
        f = open( Window.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        



    def loadUIInfo( self ):
        
        FileAndPaths.makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            self.resize( self.defaultWidth, self.defaultHeight )
            return
        try:
            posX, posY = data['mainWindow']['position']
            width, height = data['mainWindow']['size']
        except:
            return
        desktop = QtGui.QApplication.desktop()
        desktopWidth = desktop.width()
        desktopHeight = desktop.height()
        
        if posX + width > desktopWidth: posX = desktopWidth - width
        if posY + height > desktopWidth: posY = desktopHeight - height
        if posX < 0 : posX = 0
        
        self.move( posX, posY )
        self.resize( width, height )
        
        



def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mainui = Window(Window.mayaWin)
    mainui.setObjectName( Window.objectName )
    mainui.setWindowTitle( Window.title )
    mainui.resize( Window.defaultWidth, Window.defaultHeight )
    mainui.show()


