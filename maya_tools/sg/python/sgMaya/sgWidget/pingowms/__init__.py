#coding=utf8

from commands import *
from maya import OpenMayaUI

from ui_Dialog_addProject import *
from ui_Dialog_addTask import *
from ui_Dialog_help_fileCondition import *
from ui_Window_manageProject import *



class Window_Login( QDialog ):
    
    objectName = 'ui_pingowms_login'
    title = 'Login'
    defaultWidth = 350
    defaultHeight = 150

    
    def __init__(self, *args, **kwargs ):
        
        QDialog.__init__( self, *args, **kwargs )
        self.setWindowFlags(QtCore.Qt.Drawer)
        self.installEventFilter( self )
        self.setObjectName( Window_Login.objectName )
        self.setWindowTitle( Window_Login.title )
        
        hLayout = QHBoxLayout( self )
        
        gridWidget = QWidget()
        gridWidget.setMaximumWidth( 250 )
        grid = QGridLayout(gridWidget)
        label_id = QLabel( "아이디".decode( 'utf-8' ) )
        lineEdit_id = QLineEdit()
        label_pass = QLabel( "비밀번호".decode( "utf-8" ) )
        lineEdit_pass = QLineEdit()
        lineEdit_pass.setEchoMode( QLineEdit.Password )
        button_login = QPushButton( "로그인".decode( "utf-8" ) )
        label_makeId = QPushButton( "아이디 만들기".decode("utf-8") )
        grid.addWidget( label_id, 0, 0 )
        grid.addWidget( lineEdit_id, 0, 1 )
        grid.addWidget( label_pass, 1, 0 )
        grid.addWidget( lineEdit_pass, 1, 1 )
        grid.addWidget( button_login, 2, 0, 1, 2 )
        grid.addWidget( label_makeId, 3, 0, 1, 2 )
        
        hLayout.addWidget( gridWidget )
        
        self.setMinimumSize( Window_Login.defaultWidth, Window_Login.defaultHeight )

        QtCore.QObject.connect( label_makeId, QtCore.SIGNAL('clicked()'),  self.createAcount )
    
    
    
    def createAcount(self):
        
        self.close()
        
        if cmds.window( Window_CreateAcount.objectName, ex=1 ):
            cmds.deleteUI( Window_CreateAcount.objectName )
        
        createAcount = Window_CreateAcount( ControlBase.mayawin )
        createAcount.show()



    def getIdAndPass(self):
        
        if False:
            if cmds.window( Window.objectName, ex=1 ):
                cmds.deleteUI( Window.objectName )
            
            ControlBase.mainui = Window( ControlBase.mayawin )
            ControlBase.mainui.show()
        




class Window_CreateAcount( QDialog ):
    
    objectName = 'ui_pingowms_createAcount'
    title = 'Create Acount'
    defaultWidth = 350
    defaultHeight = 150

    
    def __init__(self, *args, **kwargs ):

        QDialog.__init__( self, *args, **kwargs )
        self.setWindowFlags(QtCore.Qt.Drawer)
        self.installEventFilter( self )
        self.setObjectName( Window_CreateAcount.objectName )
        self.setWindowTitle( Window_CreateAcount.title )
        
        label_name = QLabel( "사용자명".decode( 'utf-8' ) )
        lineEdit_name = QLineEdit()
        label_company = QLabel( "회사코드".decode( 'utf-8' ) )
        lineEdit_company = QLineEdit()
        grid = QGridLayout( self )
        label_id = QLabel( "아이디".decode( 'utf-8' ) )
        lineEdit_id = QLineEdit()
        label_pass = QLabel( "비밀번호".decode( 'utf-8' ) )
        lineEdit_pass = QLineEdit()
        lineEdit_pass.setEchoMode( QLineEdit.Password )
        label_passConfirm = QLabel( "비밀번호 확인".decode( 'utf-8' ) )
        lineEdit_passConfirm = QLineEdit()
        lineEdit_passConfirm.setEchoMode( QLineEdit.Password )
        label_email = QLabel( "이메일 주소".decode( 'utf-8' ) )
        lineEdit_email = QLineEdit()
        button_request = QPushButton( "인증코드요청".decode('utf-8') )
        label_code = QLabel( "인증코드입력".decode( 'utf-8' ) )
        lineEdit_code = QLineEdit()
        button_create = QPushButton( "아이디 생성".decode( 'utf-8' ) )
        
        grid.addWidget( label_name, 0,0 )
        grid.addWidget( lineEdit_name, 0,1,1,2 )
        grid.addWidget( label_company, 1,0 )
        grid.addWidget( lineEdit_company, 1,1,1,2 )
        grid.addWidget( label_id, 2,0 )
        grid.addWidget( lineEdit_id, 2,1,1,2 )
        grid.addWidget( label_pass, 3,0 )
        grid.addWidget( lineEdit_pass, 3,1,1,2 )
        grid.addWidget( label_passConfirm, 4,0 )
        grid.addWidget( lineEdit_passConfirm, 4,1,1,2 )
        grid.addWidget( label_email, 5,0 )
        grid.addWidget( lineEdit_email, 5,1 )
        grid.addWidget( button_request, 5,2 )
        grid.addWidget( label_code,6,0 )
        grid.addWidget( lineEdit_code, 6,1,1,2 )
        grid.addWidget( button_create, 7,0,1,3)
        
        self.setMinimumWidth( Window_CreateAcount.defaultWidth )
        
        



class Window( QMainWindow ):
    
    objectName = 'ui_pingowms'
    title = "Pingo SYNC for Maya - v1.0"
    defaultWidth = 550
    defaultHeight = 300


    def __init__(self, *args, **kwargs ):

        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )
        
        baseWidget = QWidget()
        self.setCentralWidget( baseWidget )
        
        vLayout = QVBoxLayout( baseWidget )
        layout_project = QHBoxLayout()
        label_projectName = QLabel( "프로젝트 명 : ".decode('utf-8') ); label_projectName.setMinimumWidth( 90 ); label_projectName.setMaximumWidth( 90 )
        comboBox = QComboBox(); #comboBox.setMaximumWidth( 200 )
        addProject_button = QPushButton( " + " ); addProject_button.setMaximumWidth( 30 )
        manageProject_button = QPushButton( "프로젝트 관리".decode('utf-8') ); manageProject_button.setMaximumWidth( 100 )
        layout_project.addWidget( label_projectName )
        layout_project.addWidget( comboBox )
        layout_project.addWidget( addProject_button )
        layout_project.addWidget( manageProject_button )
        
        layout_serverPath = QHBoxLayout()
        label_serverPath = QLabel( "서버경로 : ".decode( 'utf-8' ) ); label_serverPath.setMinimumWidth( 90 )
        lineEdit_serverPath = QLineEdit()
        button_serverPath = QPushButton( "경로변경".decode('utf-8') ); button_serverPath.setMinimumWidth( 100 )
        layout_serverPath.addWidget( label_serverPath )
        layout_serverPath.addWidget( lineEdit_serverPath )
        layout_serverPath.addWidget( button_serverPath )
        
        layout_localPath = QHBoxLayout()
        label_localPath = QLabel( "로컬경로 : ".decode( 'utf-8' ) ); label_localPath.setMinimumWidth( 90 )
        lineEdit_localPath = QLineEdit()
        button_localPath = QPushButton( "경로변경".decode('utf-8') ); button_localPath.setMinimumWidth( 100 )
        layout_localPath.addWidget( label_localPath )
        layout_localPath.addWidget( lineEdit_localPath )
        layout_localPath.addWidget( button_localPath )
        
        treeWidget = WorkTreeWidget()
        addTaskArea_button = QPushButton( '작업영역 추가'.decode('utf-8') )
        
        vLayout.addLayout( layout_project )
        vLayout.addLayout( layout_serverPath )
        vLayout.addLayout( layout_localPath )
        vLayout.addWidget( treeWidget )
        vLayout.addWidget( addTaskArea_button )
        
        addProject_button.clicked.connect( self.show_addProject )
        manageProject_button.clicked.connect( self.show_manageProject )
        addTaskArea_button.clicked.connect( self.show_addTaskArea )
        comboBox.currentIndexChanged.connect( self.loadProject )
        
        lineEdit_serverPath.setReadOnly( True )
        lineEdit_localPath.setReadOnly( True )
        
        treeWidget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        QtCore.QObject.connect( treeWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),  self.loadContextMenu )
        
        treeWidget.itemExpanded.connect( TreeWidgetCmds.updateTaskHierarchy )
        treeWidget.itemCollapsed.connect( TreeWidgetCmds.updateTaskHierarchy )
        button_serverPath.clicked.connect( ProjectControl.resetServerPath )
        button_localPath.clicked.connect( ProjectControl.resetLocalPath )
        
        treeWidget.setFont( QFont( "", 9, QFont.Light ) )
        
        if ProjectControl.getCurrentProjectName():
            addTaskArea_button.setEnabled( True )
        else:
            addTaskArea_button.setEnabled( False )
        
        self.comboBox = comboBox
        self.addTaskArea_button = addTaskArea_button
        self.lineEdit_localPath   = lineEdit_localPath
        self.lineEdit_serverPath = lineEdit_serverPath
        ControlBase.uiTreeWidget = treeWidget
        self.button_serverPath = button_serverPath
        self.button_localPath   = button_localPath
        
        self.updateProjectList()
        self.addMainMenu()


    
    def show(self, *args, **kwangs ):
        
        self.loadUIInfo()
        QMainWindow.show( self, *args, **kwangs )
    
    
    
    def addMainMenu(self):
        
        def check():
            print "check"
        
        infoMenu = self.menuBar().addMenu("정보".decode( 'utf-8' ) )
        infoMenu.addAction( "파일상태정보".decode( 'utf-8' ), self.show_help_fileCondition )
    


    def loadContextMenu(self, *args ):
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem = selItems[0]
        elsePath = selItem.taskPath + selItem.unitPath
        
        serverPath = FileControl.getCurrentServerProjectPath()
        localPath  = FileControl.getCurrentLocalProjectPath()
        targetPath_inServer = serverPath + elsePath
        targetPath_inLocal  = localPath  + elsePath
        
        menu = QMenu( ControlBase.uiTreeWidget )
        
        enableOpenFile = QueryCmds.isEnableOpen( targetPath_inServer, targetPath_inLocal )
        enableReference = QueryCmds.isEnableReference( targetPath_inServer, targetPath_inLocal )
        enableExportReferenceInfo = QueryCmds.isEnableExportReferneceInfo( targetPath_inLocal )
        enableFileDownload = QueryCmds.isEnableFileDownload( targetPath_inServer )
        
        if enableOpenFile: 
            menu.addAction("파일열기".decode( 'utf-8'), ContextMenuCmds.loadFile_local )
        if enableReference:
            menu.addAction( "레퍼런스".decode( "utf-8" ), ContextMenuCmds.reference )
        menu.addAction("폴더열기".decode( 'utf-8'), ContextMenuCmds.openFileBrowser_local )
        separator = QAction( self ); separator.setSeparator( True );menu.addAction( separator )
        if enableFileDownload:
            menu.addAction("다운로드".decode( 'utf-8'), ContextMenuCmds.download )
        if enableExportReferenceInfo:
            menu.addAction("업로드( +레퍼런스 정보 )".decode( 'utf-8'), ContextMenuCmds.upload )
        else:
            menu.addAction("업로드".decode( 'utf-8'), ContextMenuCmds.upload )
        separator = QAction( self ); separator.setSeparator( True );menu.addAction( separator )
        #if enableOpenFile: menu.addAction("파일열기( 서버 )".decode( 'utf-8'), ContextMenuCmds.loadFile_server )
        menu.addAction("폴더열기( 서버 )".decode( 'utf-8'), ContextMenuCmds.openFileBrowser_server )
        separator = QAction( self ); separator.setSeparator( True );menu.addAction( separator )

        pos = QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        menu.exec_( point )




    def loadProject(self):
        
        currentText = self.comboBox.currentText()
        ProjectControl.setCurrentProjectName( currentText )
        self.lineEdit_serverPath.setText( FileControl.getCurrentServerProjectPath() )
        self.lineEdit_localPath.setText( FileControl.getCurrentLocalProjectPath() )
        
        TreeWidgetCmds.updateTaskList()




    def show_help_fileCondition(self):
        
        try:self.dialog.close()
        except:pass
        self.dialog = Dialog_help_fileCondition( self )
        self.dialog.show()




    def show_addProject( self ):
        
        try:self.dialog.close()
        except:pass
        self.dialog = Dialog_addProject( self )
        self.dialog.show()
    



    def show_addTaskArea(self):
        
        try: self.dialog.close()
        except:pass
        self.dialog = Dialog_addTask( self )
        self.dialog.show()
        
    


    def show_manageProject(self):
        
        try:self.window_manageProject.close()
        except:pass
        self.window_manageProject = Window_manageProject( self )
        self.window_manageProject.show()
        ControlBase.manageui = self.window_manageProject
    
    


    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()
        elif event.type() in [ QtCore.QEvent.Close ]:
            try: self.dialog.close()
            except:pass
            try: self.window_manageProject.close()
            except:pass




    def updateProjectList( self, selectProjectName='' ):
        
        FileControl.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        keys = data.keys()
        self.comboBox.clear()
        
        currentProject = ProjectControl.getCurrentProjectName()
        if data:
            self.comboBox.addItems( keys )
        if not selectProjectName:
            selectProjectName = currentProject
        if selectProjectName in keys:
            self.comboBox.setCurrentIndex( keys.index( selectProjectName ) )
        
        if ProjectControl.getCurrentProjectName():
            self.addTaskArea_button.setEnabled( True )
        else:
            self.addTaskArea_button.setEnabled( False )


    
    
    def saveUIInfo( self ):
        
        FileControl.makeFile( ControlBase.uiInfoPath )
        f = open( ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        mainWindowDict = {}
        mainWindowDict['position'] = [ self.x(), self.y() ]
        mainWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'mainWindow' ] = mainWindowDict
        
        f = open( ControlBase.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        



    def loadUIInfo( self ):
        
        FileControl.makeFile( ControlBase.uiInfoPath )
        f = open( ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            ControlBase.mainui.resize( self.defaultWidth, self.defaultHeight )
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
        
        ControlBase.mainui.move( posX, posY )
        ControlBase.mainui.resize( width, height )
        



def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )

    ControlBase.mainui = Window( ControlBase.mayawin )
    ControlBase.mainui.show()


