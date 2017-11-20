#coding=utf8
from commands import *


class Dialog_addProject( QDialog ):
    
    objectName = 'ui_pingowms_addProject'
    title = "프로젝트 추가".decode('utf-8')
    defaultWidth= 450
    defaultHeight = 50
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [ControlBase.mayawin] )
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Dialog_addProject.title )
        self.resize( Dialog_addProject.defaultWidth, Dialog_addProject.defaultHeight )
        
        vlayout = QVBoxLayout( self )
        projectNameLayout = QHBoxLayout()
        serverPathLayout = QHBoxLayout()
        localPathLayout   = QHBoxLayout()
        buttonsLayout     = QHBoxLayout()
        
        projectNameLabel = QLabel( "프로젝트 명 : ".decode('utf-8') )
        projectNameEdit  = QLineEdit()
        projectNameLayout.addWidget( projectNameLabel )
        projectNameLayout.addWidget( projectNameEdit )
        
        serverPathLabel = QLabel( "프로젝트 경로 : ".decode('utf-8') )
        serverPathEdit  = QLineEdit()
        serverPathButton = QPushButton('...')
        serverPathLayout.addWidget( serverPathLabel )
        serverPathLayout.addWidget( serverPathEdit )
        serverPathLayout.addWidget( serverPathButton )
        
        localPathLocal = QLabel( "로컬 경로 : ".decode('utf-8') )
        localPathEdit  = QLineEdit()
        localPathButton = QPushButton('...')
        localPathLayout.addWidget( localPathLocal )
        localPathLayout.addWidget( localPathEdit )
        localPathLayout.addWidget( localPathButton )
        
        buttonsFirst = QPushButton( "생성".decode('utf-8') )
        buttonsSecond  = QPushButton( "취소".decode('utf-8') )
        buttonsLayout.addWidget( buttonsFirst )
        buttonsLayout.addWidget( buttonsSecond )
        
        vlayout.addLayout( projectNameLayout )
        vlayout.addLayout( serverPathLayout )
        vlayout.addLayout( localPathLayout )
        vlayout.addLayout( buttonsLayout )
    
        serverPathButton.clicked.connect( self.getServerPath )
        localPathButton.clicked.connect( self.getLocalPath )
        buttonsFirst.clicked.connect( self.createProject )
        buttonsSecond.clicked.connect( self.closeUI )
        
        self.projectNameEdit = projectNameEdit
        self.serverPathEdit = serverPathEdit
        self.localPathEdit = localPathEdit
    
    

    def getServerPath(self):

        resultPath = FileControl.getFolderFromBrowser( self, FileControl.getDefaultProjectFolder() )
        if os.path.exists( resultPath ):
            self.serverPathEdit.setText( resultPath )
            f = open( ControlBase.defaultInfoPath, 'r' )
            data = json.load( f )
            f.close()
            data[ControlBase.labelDefaultServerPath] = '/'.join( resultPath.split( '/' )[:-1] )
            f = open( ControlBase.defaultInfoPath, 'w' )
            json.dump( data, f )
            f.close()
    


    def getLocalPath(self):

        resultPath = FileControl.getFolderFromBrowser( self, FileControl.getDefaultLocalFolder() )
        if os.path.exists( resultPath ):
            self.localPathEdit.setText( resultPath )
            f = open( ControlBase.defaultInfoPath, 'r' )
            data = json.load( f )
            f.close()
            data[ControlBase.labelDefaultLocalPath] = '/'.join( resultPath.split( '/' )[:-1] )
            f = open( ControlBase.defaultInfoPath, 'w' )
            json.dump( data, f )
            f.close()
    
    

    def createProject(self):
        
        projName = self.projectNameEdit.text()
        projPath = self.serverPathEdit.text()
        localPath = self.localPathEdit.text()
        
        FileControl.makeFile( ControlBase.projectListPath )
        
        f = open( ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        keyList = data.keys()
        
        if not projName:
            QMessageBox.warning(self, self.tr("Warning"),"프로젝트 이름을 입력하세요.".decode( 'utf-8' ),
                               QMessageBox.Ok )
            return
        
        if not projPath or not os.path.exists( projPath ):
            QMessageBox.warning(self, self.tr("Warning"),'"%s"\n프로젝트 경로가 존재하지 않습니다.'.decode( 'utf-8' ) % projPath,
                               QMessageBox.Ok )
            return
        
        if not localPath or not os.path.exists( localPath ):
            QMessageBox.warning(self, self.tr("Warning"),'"%s"\n로컬 경로가 존재하지 않습니다.'.decode( 'utf-8' ) % localPath,
                               QMessageBox.Ok )
            return
        
        if projName in keyList:
            resultButton = QMessageBox.warning(self, self.tr("Warning"),'"%s" 프로젝트가 존재합니다.\n대치하시겠습니까?'.decode( 'utf-8' ) % projName,
                               QMessageBox.Ok|QMessageBox.Cancel )
            if resultButton == QMessageBox.Cancel: return
    
        data["%s" % projName] = { ControlBase.labelServerPath:"%s" % projPath, ControlBase.labelLocalPath:"%s" % localPath }
        ProjectControl.setProjectListData(data)
        self.close()
        
        ControlBase.mainui.updateProjectList( projName )
        
        

    def closeUI(self):
        
        self.close()


