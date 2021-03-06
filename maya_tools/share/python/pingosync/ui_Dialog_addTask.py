#coding=utf8
import commands
import Models
from __qtImport import *
import json, os


class Dialog_addTask( QDialog ):
    
    objectName = 'ui_pingowms_addTask'
    title = "작업영역추가".decode('utf-8')
    defaultWidth= 450
    defaultHeight = 50
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [Models.ControlBase.mayawin] )
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Dialog_addTask.title + ' - ' + commands.ProjectControl.getCurrentProjectName() )
        self.resize( Dialog_addTask.defaultWidth, Dialog_addTask.defaultHeight )
        
        self.setModal( True )
        
        vLayout       = QVBoxLayout( self )
        typeLayout    = QHBoxLayout()
        pathLayout    = QHBoxLayout()
        taskNameLayout = QHBoxLayout()
        buttonsLayout = QHBoxLayout()
        
        typeLabel = QLabel( "영역 타입".decode( 'utf-8' ) )
        typeComboBox = QComboBox()
        typeComboBox.addItems( ['파일'.decode( 'utf-8' ),'폴더'.decode( 'utf-8' )] )
        typeLayout.addWidget( typeLabel )
        typeLayout.addWidget( typeComboBox )
        
        pathLabel = QLabel( "경로 : ".decode( "utf-8" ) )
        pathLineEdit = QLineEdit()
        pathButton = QPushButton( "..." )
        pathLayout.addWidget( pathLabel )
        pathLayout.addWidget( pathLineEdit )
        pathLayout.addWidget( pathButton )
        
        taskNameLabel = QLabel( "작업영역이름 : ".decode( 'utf-8' ) )
        taskNameLineEdit = QLineEdit()
        taskNameLayout.addWidget( taskNameLabel )
        taskNameLayout.addWidget( taskNameLineEdit )
        
        buttonCreate = QPushButton( "생성".decode( 'utf-8' ) )
        buttonClose  = QPushButton( "닫기".decode( 'utf-8' ) )
        buttonsLayout.addWidget( buttonCreate )
        buttonsLayout.addWidget( buttonClose )
        
        #vLayout.addLayout( typeLayout )
        vLayout.addLayout( pathLayout )
        vLayout.addLayout( taskNameLayout )
        vLayout.addLayout( buttonsLayout )
        
        typeComboBox.currentIndexChanged.connect( self.setTaskType )
        pathButton.clicked.connect( self.loadTaskPath )
        buttonCreate.clicked.connect( self.createTask )
        buttonClose.clicked.connect( self.close )

        self.typeComboBox = typeComboBox
        self.pathLineEdit = pathLineEdit
        self.taskNameLineEdit = taskNameLineEdit
        self.loadDefaultTaskType()


    def setTaskType(self):
        commands.FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        data[Models.ControlBase.labelDefaultTaskType] = self.typeComboBox.currentIndex()
        
        f = open( Models.ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close() 
        
        

    def loadDefaultTaskType(self):
        commands.FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        try: data = json.load( f )
        except: data = {}
        f.close()
        if not data.has_key( Models.ControlBase.labelDefaultTaskType ): return 0
        self.typeComboBox.setCurrentIndex( data[Models.ControlBase.labelDefaultTaskType] )



    def loadTaskPath(self):
        
        resultPath = commands.FileControl.getFolderFromBrowser( self, commands.FileControl.getDefaultTaskFolder() )

        if os.path.exists( resultPath ):
            self.pathLineEdit.setText( resultPath )
            f = open( Models.ControlBase.defaultInfoPath, 'r' )
            data = json.load( f )
            f.close()
            data[Models.ControlBase.labelDefaultTaskFolder] = '/'.join( resultPath.split( '/' )[:-1] )
            f = open( Models.ControlBase.defaultInfoPath, 'w' )
            json.dump( data, f )
            f.close() 
            self.taskNameLineEdit.setText( resultPath.split( '/' )[-1] )



    def createTask(self):
        
        currentProject = commands.ProjectControl.getCurrentProjectName()
        projectListData = commands.ProjectControl.getProjectListData()
        if not projectListData.has_key( currentProject ):
            cmds.warning( "프로젝트가 존제하지 않습니다.".decode( 'utf-8') )
            return
        projectDict = projectListData[currentProject]
        if not projectDict.has_key( Models.ControlBase.labelTasks ):
            projectDict[Models.ControlBase.labelTasks] = {}
        taskDict = projectDict[Models.ControlBase.labelTasks]
        typeTask = self.typeComboBox.currentIndex()
        pathTask = self.pathLineEdit.text()
        nameTask = self.taskNameLineEdit.text()
        
        if not os.path.exists( pathTask ):
            cmds.warning( "%s 경로가 존재하지 않습니다.".decode( 'utf-8') % pathTask )
            return
        if not os.path.isdir( pathTask ):
            cmds.warning( "'%s'는 폴더가 아닙니다.".decode( 'utf-8') % pathTask )
            return
        
        serverPath = projectDict[ Models.ControlBase.labelServerPath ]
        if pathTask.lower().find( serverPath.lower() ) == -1: 
            cmds.warning( "%s 가 프로젝트 경로에 존제하지 않습니다.".decode( 'utf-8') % serverPath )
            return

        addTaskPath = pathTask.replace( serverPath, '' )
        taskDict[nameTask] = { Models.ControlBase.labelTaskType : typeTask, Models.ControlBase.labelTaskPath : addTaskPath }
        
        commands.ProjectControl.setProjectListData(projectListData)
        self.close()
        commands.TreeWidgetCmds.updateTaskList()
    
    
