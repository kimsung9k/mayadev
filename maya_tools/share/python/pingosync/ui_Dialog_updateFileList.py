#coding=utf8

import commands
import Models
from __qtImport import *
import json, os



class Dialog_downloadFileList( QDialog ):
    
    objectName = 'ui_pingowms_updateFileList'
    title = "다운로드 리스트".decode('utf-8')
    defaultWidth= 300
    defaultHeight = 300
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [Models.ControlBase.mayawin] )
        
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
        scrollArea = QScrollArea()
        label  = QLabel( "" )
        scrollArea.setWidget( label )
        scrollArea.setWidgetResizable(True)
        hLayout_buttons = QHBoxLayout()
        buttonDownload = QPushButton( "다운로드하기".decode( 'utf-8' ) )
        buttonCanel    = QPushButton( "다운로드 하지 않기".decode( 'utf-8' ) )
        hLayout_buttons.addWidget( buttonDownload )
        hLayout_buttons.addWidget( buttonCanel )
        vLayout.addWidget( label_download )
        vLayout.addWidget( scrollArea )
        vLayout.addLayout( hLayout_buttons )
        
        self.label = label
        self.serverPath = ""
        self.localPath   = ""
        self.downloadCmds = []
        self.typeAndFiles = {}
        
        QtCore.QObject.connect( buttonDownload, QtCore.SIGNAL('clicked()'),  self.cmd_download )
        QtCore.QObject.connect( buttonCanel, QtCore.SIGNAL('clicked()'),   self.cmd_deleteUI )
        
        scrollArea.resize( scrollArea.sizeHint() )
        
    

    def setServerPath(self, serverPath ):
        
        self.serverPath = serverPath
    

    def setLocalPath(self, localPath ):
        
        self.localPath = localPath


    def addDownloadCmd(self, targetCmd ):
        self.downloadCmds.append( targetCmd )


    def appendFilePath(self, path, inputType ):
        
        if not self.typeAndFiles.has_key( inputType ):
            self.typeAndFiles[inputType] = [path]
        else:
            if path in self.typeAndFiles[inputType]: return None
            self.typeAndFiles[inputType].append( path )
    
    
    def updateUI(self):
        
        labelString = "Server Work Area : \n    %s\n\nLocal Work Area : \n    %s\n"
        
        print "self.typeAndFiles : ",self.typeAndFiles
        
        for nodeType in self.typeAndFiles.keys():
            paths = self.typeAndFiles[ nodeType ]
            labelString += "\nTarget Node type : %s" % nodeType
            for i in range( len( paths ) ):
                labelString += "\n    " + paths[i]
        
        self.label.setText( labelString %( self.serverPath, self.localPath ) )
    
    
    def cmd_download(self):
        
        import shutil
        import pymel.core, os
        from maya import mel
        
        for nodeType in self.typeAndFiles.keys():
            paths = self.typeAndFiles[ nodeType ]
            for path in paths:
                serverPath = self.serverPath + path
                localPath  = self.localPath + path
                
                if os.path.exists( serverPath ):
                    editorInfo = commands.EditorCmds.getEditorInfoFromFile( serverPath )
                    commands.EditorCmds.setEditorInfoToFile( editorInfo, localPath )
                    commands.FileControl.downloadFile( serverPath, localPath )
                
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
        
        if not args: args = tuple( [Models.ControlBase.mayawin] )
        
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
        scrollArea = QScrollArea()
        label  = QLabel( "" )
        scrollArea.setWidget( label )
        scrollArea.setWidgetResizable( True )
        hLayout_buttons = QHBoxLayout()
        buttonUpload = QPushButton( "업로드하기".decode( 'utf-8' ) )
        buttonCanel    = QPushButton( "업로드 하지 않기".decode( 'utf-8' ) )
        hLayout_buttons.addWidget( buttonUpload )
        hLayout_buttons.addWidget( buttonCanel )
        vLayout.addWidget( label_download )
        vLayout.addWidget( scrollArea )
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



