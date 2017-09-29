#coding=utf8

from commands import *
import model
from maya import OpenMayaUI

from ui_Dialog_addProject import *
from ui_Dialog_addTask import *
from ui_Window_manageProject import *



class Window_Login( QtGui.QDialog ):
    
    objectName = 'ui_pingowms_login'
    title = 'Login'
    defaultWidth = 350
    defaultHeight = 150

    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QDialog.__init__( self, *args, **kwargs )
        self.setWindowFlags(QtCore.Qt.Drawer)
        self.installEventFilter( self )
        self.setObjectName( Window_Login.objectName )
        self.setWindowTitle( Window_Login.title )
        
        hLayout = QtGui.QHBoxLayout( self )
        
        gridWidget = QtGui.QWidget()
        gridWidget.setMaximumWidth( 250 )
        grid = QtGui.QGridLayout(gridWidget)
        label_id = QtGui.QLabel( "아이디".decode( 'utf-8' ) )
        lineEdit_id = QtGui.QLineEdit()
        label_pass = QtGui.QLabel( "비밀번호".decode( "utf-8" ) )
        lineEdit_pass = QtGui.QLineEdit()
        lineEdit_pass.setEchoMode( QtGui.QLineEdit.Password )
        button_login = QtGui.QPushButton( "로그인".decode( "utf-8" ) )
        label_makeId = QtGui.QPushButton( "아이디 만들기".decode("utf-8") )
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
        
        cmds.deleteUI( Window_Login.objectName )
        
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
        




class Window_CreateAcount( QtGui.QDialog ):
    
    objectName = 'ui_pingowms_createAcount'
    title = 'Create Acount'
    defaultWidth = 350
    defaultHeight = 150

    
    def __init__(self, *args, **kwargs ):

        QtGui.QDialog.__init__( self, *args, **kwargs )
        self.setWindowFlags(QtCore.Qt.Drawer)
        self.installEventFilter( self )
        self.setObjectName( Window_CreateAcount.objectName )
        self.setWindowTitle( Window_CreateAcount.title )
        
        label_name = QtGui.QLabel( "사용자명".decode( 'utf-8' ) )
        lineEdit_name = QtGui.QLineEdit()
        label_company = QtGui.QLabel( "회사코드".decode( 'utf-8' ) )
        lineEdit_company = QtGui.QLineEdit()
        grid = QtGui.QGridLayout( self )
        label_id = QtGui.QLabel( "아이디".decode( 'utf-8' ) )
        lineEdit_id = QtGui.QLineEdit()
        label_pass = QtGui.QLabel( "비밀번호".decode( 'utf-8' ) )
        lineEdit_pass = QtGui.QLineEdit()
        lineEdit_pass.setEchoMode( QtGui.QLineEdit.Password )
        label_passConfirm = QtGui.QLabel( "비밀번호 확인".decode( 'utf-8' ) )
        lineEdit_passConfirm = QtGui.QLineEdit()
        lineEdit_passConfirm.setEchoMode( QtGui.QLineEdit.Password )
        label_email = QtGui.QLabel( "이메일 주소".decode( 'utf-8' ) )
        lineEdit_email = QtGui.QLineEdit()
        button_request = QtGui.QPushButton( "인증코드요청".decode('utf-8') )
        label_code = QtGui.QLabel( "인증코드입력".decode( 'utf-8' ) )
        lineEdit_code = QtGui.QLineEdit()
        button_create = QtGui.QPushButton( "아이디 생성".decode( 'utf-8' ) )
        
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
        
        



class Window( QtGui.QMainWindow ):
    
    objectName = 'ui_pingowms'
    title = "Pingo WMS for Maya - v1.0"
    defaultWidth = 550
    defaultHeight = 300


    def __init__(self, *args, **kwargs ):

        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )
        
        baseWidget = QtGui.QWidget()
        self.setCentralWidget( baseWidget )
        
        vLayout = QtGui.QVBoxLayout( baseWidget )
        layout_project = QtGui.QHBoxLayout()
        label_projectName = QtGui.QLabel( "프로젝트 명 : ".decode('utf-8') ); label_projectName.setMinimumWidth( 90 ); label_projectName.setMaximumWidth( 90 )
        comboBox = QtGui.QComboBox(); #comboBox.setMaximumWidth( 200 )
        addProject_button = QtGui.QPushButton( " + " ); addProject_button.setMaximumWidth( 30 )
        manageProject_button = QtGui.QPushButton( "프로젝트 관리".decode('utf-8') ); manageProject_button.setMaximumWidth( 100 )
        layout_project.addWidget( label_projectName )
        layout_project.addWidget( comboBox )
        layout_project.addWidget( addProject_button )
        layout_project.addWidget( manageProject_button )
        
        layout_serverPath = QtGui.QHBoxLayout()
        label_serverPath = QtGui.QLabel( "서버경로 : ".decode( 'utf-8' ) ); label_serverPath.setMinimumWidth( 90 )
        lineEdit_serverPath = QtGui.QLineEdit()
        button_serverPath = QtGui.QPushButton( "경로변경".decode('utf-8') ); button_serverPath.setMinimumWidth( 100 )
        layout_serverPath.addWidget( label_serverPath )
        layout_serverPath.addWidget( lineEdit_serverPath )
        layout_serverPath.addWidget( button_serverPath )
        
        layout_localPath = QtGui.QHBoxLayout()
        label_localPath = QtGui.QLabel( "로컬경로 : ".decode( 'utf-8' ) ); label_localPath.setMinimumWidth( 90 )
        lineEdit_localPath = QtGui.QLineEdit()
        button_localPath = QtGui.QPushButton( "경로변경".decode('utf-8') ); button_localPath.setMinimumWidth( 100 )
        layout_localPath.addWidget( label_localPath )
        layout_localPath.addWidget( lineEdit_localPath )
        layout_localPath.addWidget( button_localPath )
        
        layoutWorkArea = QtGui.QVBoxLayout()
        treeWidget = model.WorkTreeWidget()
        addTaskArea_button = QtGui.QPushButton( '작업영역 추가'.decode('utf-8') )
        layoutWorkArea.addWidget( treeWidget )
        layoutWorkArea.addWidget( addTaskArea_button )
        
        vLayout.addLayout( layout_project )
        vLayout.addLayout( layout_serverPath )
        vLayout.addLayout( layout_localPath )
        vLayout.addLayout( layoutWorkArea )
        
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
        
        treeWidget.setFont( QtGui.QFont( "", 9, QtGui.QFont.Light ) )
        
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


    
    def show(self, *args, **kwangs ):
        
        self.loadUIInfo()
        QtGui.QMainWindow.show( self, *args, **kwangs )
        
    


    def loadContextMenu(self, *args ):
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem = selItems[0]
        elsePath = selItem.taskPath + selItem.unitPath
        
        serverPath = FileControl.getCurrentServerProjectPath()
        localPath  = FileControl.getCurrentLocalProjectPath()
        targetPath_inServer = serverPath + elsePath
        targetPath_inLocal  = localPath  + elsePath
        
        menu = QtGui.QMenu( ControlBase.uiTreeWidget )
        
        enableOpenFile = QueryCmds.isEnableOpen( targetPath_inServer, targetPath_inLocal )
        enableUpload   = QueryCmds.isEnableUpload( targetPath_inLocal )
        
        if enableOpenFile: menu.addAction("파일열기".decode( 'utf-8'), ContextMenuCmds.loadFile_local )
        menu.addAction("폴더열기".decode( 'utf-8'), ContextMenuCmds.openFileBrowser_local )
        separator = QtGui.QAction( self ); separator.setSeparator( True );menu.addAction( separator )
        if enableUpload: menu.addAction("업로드".decode( 'utf-8'), ContextMenuCmds.upload )
        separator = QtGui.QAction( self ); separator.setSeparator( True );menu.addAction( separator )
        if enableOpenFile: menu.addAction("파일열기( 서버 )".decode( 'utf-8'), ContextMenuCmds.loadFile_server )
        menu.addAction("폴더열기( 서버 )".decode( 'utf-8'), ContextMenuCmds.openFileBrowser_server )
        separator = QtGui.QAction( self ); separator.setSeparator( True );menu.addAction( separator )

        pos = QtGui.QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        menu.exec_( point )




    def loadProject(self):
        
        FileControl.makeFile( ControlBase.defaultInfoPath )
        
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data: data = {}
        
        currentText = self.comboBox.currentText()
        data[ ControlBase.labelCurrentProject ] = currentText
        
        f = open( ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        
        self.lineEdit_serverPath.setText( FileControl.getCurrentServerProjectPath() )
        self.lineEdit_localPath.setText( FileControl.getCurrentLocalProjectPath() )
        
        TreeWidgetCmds.updateTaskList()




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
        #keys.sort()
        
        self.comboBox.clear()
        if data:
            self.comboBox.addItems( keys )
        
        if not selectProjectName:
            selectProjectName = ProjectControl.getCurrentProjectName()
        
        if selectProjectName in keys:
            self.comboBox.setCurrentIndex( keys.index( selectProjectName ) )
        
        try:
            ControlBase.manageui.updateProjectList()
        except:
            pass
        
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
        desktop = QtGui.QApplication.desktop()
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


