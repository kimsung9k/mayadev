#coding=utf8

from ControlBase import *



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



class Dialog_updateFileList( QtGui.QDialog ):
    
    objectName = 'ui_pingowms_updateFileList'
    title = "다운로드 리스트".decode('utf-8')
    defaultWidth= 300
    defaultHeight = 300
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [ControlBase.mayawin] )
        
        if cmds.window( Dialog_updateFileList.objectName, ex=1 ):
            cmds.deleteUI( Dialog_updateFileList.objectName, wnd=1 )
        
        QtGui.QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Dialog_updateFileList.objectName )
        self.setWindowTitle( Dialog_updateFileList.title )
        self.resize( Dialog_updateFileList.defaultWidth, Dialog_updateFileList.defaultHeight )
        
        self.setModal( True )
        
        vLayout = QtGui.QVBoxLayout( self )
        label_download = QtGui.QLabel( "다음항목들이 서버에서 로컬로 다운로드 됩니다.".decode( 'utf-8' ) )
        label_download.setMaximumHeight( 30 )
        label  = QtGui.QLabel( "" )
        hLayout_buttons = QtGui.QHBoxLayout()
        buttonDownload = QtGui.QPushButton( "다운로드하기".decode( 'utf-8' ) )
        buttonCanel    = QtGui.QPushButton( "다운로드 하지 않기".decode( 'utf-8' ) )
        hLayout_buttons.addWidget( buttonDownload )
        hLayout_buttons.addWidget( buttonCanel )
        vLayout.addWidget( label_download )
        vLayout.addWidget( label )
        vLayout.addLayout( hLayout_buttons )
        
        self.label = label
        self.serverPath = ""
        self.localPath   = ""
        self.files = []
        self.cmds = []
        
        QtCore.QObject.connect( buttonDownload, QtCore.SIGNAL('clicked()'),  self.cmd_download )
        QtCore.QObject.connect( buttonCanel, QtCore.SIGNAL('clicked()'),   self.cmd_deleteUI )
        
    

    def setServerPath(self, serverPath ):
        
        self.serverPath = serverPath
    

    def setLocalPath(self, localPath ):
        
        self.localPath = localPath


    def appendFilePath(self, path ):
        
        self.files.append( path )
    
    
    def updateUI(self):
        
        labelString = "Server Work Area : \n    %s\n\nLocal Work Area : \n    %s\n"
        for i in range( len( self.files ) ):
            labelString += "\n    " + self.files[i]
        
        self.label.setText( labelString %( self.serverPath, self.localPath ) )
    
    
    def cmd_download(self):
        
        import shutil
        import pymel.core
        from maya import mel
        
        for filePath in self.files:
            serverPath = self.serverPath + filePath
            localPath  = self.localPath + filePath
            makeFolder( os.path.dirname(localPath) )
            
            if os.path.exists( serverPath ):
                shutil.copy2( serverPath, localPath )
        
        for fileNode in pymel.core.ls( type='file' ):
            #print "AEfileTextureReloadCmd %s" % fileNode.fileTextureName.name()
            mel.eval( "AEfileTextureReloadCmd %s" % fileNode.fileTextureName.name() )
        
        cmds.deleteUI( Dialog_updateFileList.objectName, wnd=1 )
        
                

    def cmd_deleteUI(self):
        
        cmds.deleteUI( Dialog_updateFileList.objectName, wnd=1 )
    
    



