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


    @staticmethod
    def copyAndPast( copyTarget, pastTarget, copyTargetSrcsString, pastTargetSrcsString ):
        
        from sgMaya import sgCmds
        
        pastTargetSrcDict = {}
        copyTargetSrcs = [ copyTargetSrcString.strip() for copyTargetSrcString in copyTargetSrcsString.split( ',' ) ]
        pastTargetSrcs = [ pastTargetSrcString.strip() for pastTargetSrcString in pastTargetSrcsString.split( ',' ) ]
        for i in range( len( copyTargetSrcs ) ):
            pastTargetSrcDict[ copyTargetSrcs[i] ] = pastTargetSrcs[i]
        
        cmds.undoInfo( ock=1 )
        sgCmds.copyAndPastRig( copyTarget, pastTarget, pastTargetSrcDict )
        cmds.undoInfo( cck=1 )






class ContextMenu( QMenu ):
    
    def __init__(self, *args, **kwargs ):
        
        self.parentUi = args[0]
        loadType = None
        if kwargs.has_key( 'loadTypes' ):
            loadType = kwargs['loadTypes']
            del kwargs['loadTypes']
        
        QMenu.__init__( self, *args, **kwargs )
        
        self.parentUi.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect( self.parentUi, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
                                self.loadContextMenu )
        
        if loadType and loadType == 'multi':
            self.addAction( "Load Objects", self.cmd_loadObjects )
        else:
            self.addAction( "Load Object", self.cmd_loadObject )


    def cmd_loadObject(self):

        import pymel.core
        sels = pymel.core.ls( sl=1 )
        self.parentUi.setText( sels[0].name() )
    
    
    def cmd_loadObjects(self):

        import pymel.core
        sels = pymel.core.ls( sl=1 )
        self.parentUi.setText( ','.join( [ sel.name() for sel in sels ] ) )


    def loadContextMenu(self):

        pos = QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        self.exec_( point )





class Window( QMainWindow ):
    
    objectName = 'ui_copyAndPastRig'
    title = "UI - Copy And Past Rig"
    defaultWidth = 400
    defaultHeight = 50
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/ui_copyAndPastRig"
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
        label_src = QLabel("Copy Target")
        label_dst = QLabel("Past Target")
        label_src.setAlignment( QtCore.Qt.AlignCenter )
        label_dst.setAlignment( QtCore.Qt.AlignCenter )
        layout_labels.addWidget( label_src )
        layout_labels.addWidget( label_dst )
        
        layout_lineEdits = QHBoxLayout()
        lineEdit_src = QLineEdit()
        lineEdit_dst = QLineEdit()
        layout_lineEdits.addWidget( lineEdit_src )
        layout_lineEdits.addWidget( lineEdit_dst )
        
        separator = QFrame(); separator.setFrameShape( QFrame.HLine )
        
        layout_buttons = QHBoxLayout()
        button_copyAndPast = QPushButton( "Copy And Past" )
        button_close  = QPushButton( "Close" )
        layout_buttons.addWidget( button_copyAndPast )
        layout_buttons.addWidget( button_close )
        
        layout_labelsSecond = QHBoxLayout()
        label_src = QLabel("Source transforms from copy target")
        label_dst = QLabel("Source transforms from cast target")
        label_src.setAlignment( QtCore.Qt.AlignCenter )
        label_dst.setAlignment( QtCore.Qt.AlignCenter )
        layout_labelsSecond.addWidget( label_src )
        layout_labelsSecond.addWidget( label_dst )
        
        layout_lineEditsSecond = QHBoxLayout()
        lineEdit_srcSecond = QLineEdit()
        lineEdit_dstSecond = QLineEdit()
        layout_lineEditsSecond.addWidget( lineEdit_srcSecond )
        layout_lineEditsSecond.addWidget( lineEdit_dstSecond )
        
        vLayout.addLayout( layout_labels )
        vLayout.addLayout( layout_lineEdits )
        vLayout.addWidget( separator )
        vLayout.addLayout( layout_labelsSecond )
        vLayout.addLayout( layout_lineEditsSecond )
        vLayout.addLayout( layout_buttons )


        #---------- Connect to self------------------
        self.lineEdit_src = lineEdit_src
        self.lineEdit_dst = lineEdit_dst
        self.lineEdit_srcSecond = lineEdit_srcSecond
        self.lineEdit_dstSecond = lineEdit_dstSecond
        
        
        #------------Connect context menu---------------
        ContextMenu( lineEdit_src )
        ContextMenu( lineEdit_dst )
        ContextMenu( lineEdit_srcSecond, loadTypes='multi' )
        ContextMenu( lineEdit_dstSecond, loadTypes='multi' )

        #-----------Connect Command------------------
        QtCore.QObject.connect( button_copyAndPast, QtCore.SIGNAL('clicked()'),  self.cmd_copyAndPast )
        QtCore.QObject.connect( button_close, QtCore.SIGNAL('clicked()'),  self.cmd_close )


    def cmd_copyAndPast(self):
        
        copyTarget = self.lineEdit_src.text()
        pastTarget = self.lineEdit_dst.text()
        copySources = self.lineEdit_srcSecond.text()
        pastTargets = self.lineEdit_dstSecond.text()
        Commands.copyAndPast( copyTarget, pastTarget, copySources, pastTargets )
    
    
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

