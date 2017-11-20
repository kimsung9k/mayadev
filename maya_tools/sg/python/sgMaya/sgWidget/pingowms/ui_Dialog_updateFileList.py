#coding=utf8

from sgUIs.pingowms.Models import *
from sgUIs.__qtImprot import *
import commands



class Dialog_downloadFileList( QDialog ):
    
    objectName = 'ui_pingowms_updateFileList'
    title = "다운로드 리스트".decode('utf-8')
    defaultWidth= 300
    defaultHeight = 300
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [ControlBase.mayawin] )
        
        if cmds.window( Dialog_downloadFileList.objectName, ex=1 ):
            cmds.deleteUI( Dialog_downloadFileList.objectName, wnd=1 )
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Dialog_downloadFileList.objectName )
        self.setWindowTitle( Dialog_downloadFileList.title )
        self.resize( Dialog_downloadFileList.defaultWidth, Dialog_downloadFileList.defaultHeight )
        
        self.setModal( True )
        
        vLayout = QVBoxLayout( self )
        label_download = QLabel( "다음항목들이 서버에서 로컬로 다운로드 됩니다.".decode( 'utf-8' ) )
        label_download.setMaximumHeight( 30 )
        labelBaseWidget = QWidget()
        scrollArea = QScrollArea( labelBaseWidget )
        label  = QLabel( "" )
        scrollArea.setWidget( label )
        scrollArea.setWidgetResizable( True )
        hLayout_buttons = QHBoxLayout()
        buttonDownload = QPushButton( "다운로드하기".decode( 'utf-8' ) )
        buttonCanel    = QPushButton( "다운로드 하지 않기".decode( 'utf-8' ) )
        hLayout_buttons.addWidget( buttonDownload )
        hLayout_buttons.addWidget( buttonCanel )
        vLayout.addWidget( label_download )
        vLayout.addWidget( labelBaseWidget )
        vLayout.addLayout( hLayout_buttons )
        
        self.label = label
        self.serverPath = ""
        self.localPath   = ""
        self.files = []
        self.downloadCmds = []
        
        QtCore.QObject.connect( buttonDownload, QtCore.SIGNAL('clicked()'),  self.cmd_download )
        QtCore.QObject.connect( buttonCanel, QtCore.SIGNAL('clicked()'),   self.cmd_deleteUI )
        
    

    def setServerPath(self, serverPath ):
        
        self.serverPath = serverPath
    

    def setLocalPath(self, localPath ):
        
        self.localPath = localPath


    def addDownloadCmd(self, targetCmd ):
        self.downloadCmds.append( targetCmd )


    def appendFilePath(self, path ):
        
        self.files.append( path )
    
    
    def updateUI(self):
        
        labelString = "Server Work Area : \n    %s\n\nLocal Work Area : \n    %s\n"
        for i in range( len( self.files ) ):
            labelString += "\n    " + self.files[i]
        
        self.label.setText( labelString %( self.serverPath, self.localPath ) )
    
    
    def cmd_download(self):
        
        import shutil
        import pymel.core, os
        from maya import mel
        
        for filePath in self.files:
            serverPath = self.serverPath + filePath
            localPath  = self.localPath + filePath
            
            if os.path.exists( serverPath ):
                editorInfo = commands.EditorCmds.getEditorInfoFromFile( serverPath )
                commands.EditorCmds.setEditorInfoToFile( editorInfo, localPath )
                commands.FileControl.downloadFile( serverPath, localPath )
        
        for fileNode in pymel.core.ls( type='file' ):
            #print "AEfileTextureReloadCmd %s" % fileNode.fileTextureName.name()
            try:mel.eval( "AEfileTextureReloadCmd %s" % fileNode.fileTextureName.name() )
            except:pass
        cmds.deleteUI( Dialog_downloadFileList.objectName, wnd=1 )
        commands.TreeWidgetCmds.setTreeItemsCondition()
        
        for cmd in self.downloadCmds:
            cmd()
    

    def cmd_deleteUI(self):
        
        cmds.deleteUI( Dialog_downloadFileList.objectName, wnd=1 )
    



class Dialog_uploadFileList( QDialog ):
    
    objectName = 'ui_pingowms_updateFileList'
    title = "업로드 리스트".decode('utf-8')
    defaultWidth= 300
    defaultHeight = 300
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [ControlBase.mayawin] )
        
        if cmds.window( Dialog_uploadFileList.objectName, ex=1 ):
            cmds.deleteUI( Dialog_uploadFileList.objectName, wnd=1 )
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Dialog_uploadFileList.objectName )
        self.setWindowTitle( Dialog_uploadFileList.title )
        self.resize( Dialog_uploadFileList.defaultWidth, Dialog_uploadFileList.defaultHeight )
        
        self.setModal( True )
        
        vLayout = QVBoxLayout( self )
        label_download = QLabel( "다음항목들이 로컬에서 서버로 업로드 됩니다.".decode( 'utf-8' ) )
        label_download.setMaximumHeight( 30 )
        labelBaseWidget = QWidget()
        scrollArea = QScrollArea( labelBaseWidget )
        label  = QLabel( "" )
        scrollArea.setWidget( label )
        scrollArea.setWidgetResizable( True )
        hLayout_buttons = QHBoxLayout()
        buttonUpload = QPushButton( "업로드하기".decode( 'utf-8' ) )
        buttonCanel    = QPushButton( "업로드 하지 않기".decode( 'utf-8' ) )
        hLayout_buttons.addWidget( buttonUpload )
        hLayout_buttons.addWidget( buttonCanel )
        vLayout.addWidget( label_download )
        vLayout.addWidget( labelBaseWidget )
        vLayout.addLayout( hLayout_buttons )
        
        self.label = label
        self.serverPath = ""
        self.localPath   = ""
        self.files = []
        self.cmds = []
        
        QtCore.QObject.connect( buttonUpload, QtCore.SIGNAL('clicked()'),  self.cmd_upload )
        QtCore.QObject.connect( buttonCanel, QtCore.SIGNAL('clicked()'),   self.cmd_deleteUI )
        
    

    def setServerPath(self, serverPath ):
        
        self.serverPath = serverPath
    


    def setLocalPath(self, localPath ):
        
        self.localPath = localPath



    def appendFilePath(self, path ):
        
        self.files.append( path )



    def updateUI(self):
        
        labelString = "Local Work Area : \n    %s\n\nServer Work Area : \n    %s\n\nFiles:"
        for i in range( len( self.files ) ):
            labelString += "\n    " + self.files[i]
        
        self.label.setText( labelString %( self.localPath, self.serverPath ) )
    


    def cmd_upload(self):
        
        import shutil
        import pymel.core, os
        from maya import mel
        
        for filePath in self.files:
            serverPath = self.serverPath + filePath
            localPath  = self.localPath + filePath
            
            if os.path.exists( localPath ):
                editorInfoLocal  = commands.EditorCmds.getEditorInfoFromFile( localPath )
                commands.FileControl.uploadFile( localPath, serverPath )
                commands.EditorCmds.setEditorInfoToFile( editorInfoLocal, serverPath )
        cmds.deleteUI( Dialog_uploadFileList.objectName, wnd=1 )
        commands.TreeWidgetCmds.setTreeItemsCondition()
    


    def cmd_deleteUI(self):
        
        cmds.deleteUI( Dialog_uploadFileList.objectName, wnd=1 )



