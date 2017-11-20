#coding=utf8

from maya import OpenMayaUI, cmds
from __qtImprot import *
import os, json



class Commands:
    
    @staticmethod
    def makeFolder( pathName ):
        if os.path.exists( pathName ):return None
        os.makedirs( pathName )
        return pathName



    @staticmethod
    def makeFile( filePath ):
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        Commands.makeFolder( folder )
        f = open( filePath, "w" )
        json.dump( {}, f )
        f.close()



class Window( QMainWindow ):
    
    objectName = 'ui_renameBySourceObject'
    title = "UI - Rename By Source Object"
    defaultWidth = 400
    defaultHeight = 50
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/ui_renameBySourceObject"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    
    def __init__(self, *args, **kwargs ):
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )
        
        #-----------ui setting-----------------
        baseWidget = QWidget()
        self.setCentralWidget( baseWidget )
        vLayout = QVBoxLayout( baseWidget )
        
        layout_labels = QHBoxLayout()
        lineEdit_src = QLabel("Source Str")
        lineEdit_dst = QLabel("Replace Str")
        lineEdit_src.setAlignment( QtCore.Qt.AlignCenter )
        lineEdit_dst.setAlignment( QtCore.Qt.AlignCenter )
        layout_labels.addWidget( lineEdit_src )
        layout_labels.addWidget( lineEdit_dst )
        
        layout_lineEdits = QHBoxLayout()
        lineEdit_src = QLineEdit()
        lineEdit_dst = QLineEdit()
        layout_lineEdits.addWidget( lineEdit_src )
        layout_lineEdits.addWidget( lineEdit_dst )
        
        layout_buttons = QHBoxLayout()
        button_rename = QPushButton( "Rename" )
        button_close  = QPushButton( "Close" )
        layout_buttons.addWidget( button_rename )
        layout_buttons.addWidget( button_close )
        
        vLayout.addLayout( layout_labels )
        vLayout.addLayout( layout_lineEdits )
        vLayout.addLayout( layout_buttons )
        
        #---------------connect width commands----------------
        QtCore.QObject.connect( button_rename, QtCore.SIGNAL('clicked()'),  self.cmd_rename )
        QtCore.QObject.connect( button_close, QtCore.SIGNAL('clicked()'),  self.cmd_close )
        
        #---------------assign to self----------------------
        self.lineEdit_src = lineEdit_src
        self.lineEdit_dst = lineEdit_dst
        
        

    def cmd_rename(self):
    
        import pymel.core
        srcStr = self.lineEdit_src.text()
        dstStr = self.lineEdit_dst.text()
        sels = pymel.core.ls( sl=1 )
        src = sels[-2]
        dst = sels[-1]
        dst.rename( src.shortName().replace( srcStr, dstStr ) )
        
    
    
    def cmd_close(self):
        
        cmds.deleteUI( Window.objectName )
    
        
        
    def show( self, *args, **kwargs):
        
        self.loadUIInfo()
        QMainWindow.show( self, *args, **kwargs )
    
    
    
    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()

    
    
    def saveUIInfo( self ):
        Commands.makeFile( Window.uiInfoPath )
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
        
        Commands.makeFile( Window.uiInfoPath )
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
        desktop = QApplication.desktop()
        desktopWidth = desktop.width()
        desktopHeight = desktop.height()
        
        if posX + width > desktopWidth: posX = desktopWidth - width
        if posY + height > desktopWidth: posY = desktopHeight - height
        if posX < 0 : posX = 0
        
        self.move( posX, posY )
        self.resize( width, height )



def show():
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mayawin = shiboken.wrapInstance( long( OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    win = Window( mayawin )
    win.show()