#coding=utf8

from ui_ControlBase import *

from ui_Dialog_addProject import *
from ui_Dialog_addTask import *
from ui_Window_manageProject import *


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
        treeWidget = WorkTreeWidget()
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
        button_serverPath.clicked.connect( ControlBase.resetServerPath )
        button_localPath.clicked.connect( ControlBase.resetLocalPath )
        
        treeWidget.setFont( QtGui.QFont( "", 9, QtGui.QFont.Light ) )
        
        if ControlBase.getCurrentProjectName():
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
            

    
    def show( self, *args, **kwargs):
        
        self.loadProject()
        QtGui.QMainWindow.show( self, *args, **kwargs )



    def loadContextMenu(self, *args ):
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem = selItems[0]
        elsePath = selItem.taskPath + selItem.unitPath
        
        serverPath = ControlBase.getCurrentServerPath()
        localPath  = ControlBase.getCurrentLocalPath()
        targetPath_inServer = serverPath + elsePath
        targetPath_inLocal  = localPath  + elsePath
        
        menu = QtGui.QMenu( ControlBase.uiTreeWidget )
        
        downloadRequired = control.isDownloadRequired( targetPath_inServer, targetPath_inLocal )
        uploadRequired   = control.isUploadRequired( targetPath_inServer, targetPath_inLocal )
        
        if os.path.isfile( targetPath_inServer ) or os.path.isfile( targetPath_inLocal ):menu.addAction("파일열기".decode( 'utf-8'), ContextMenuCmds.loadFile_local )
        menu.addAction("폴더열기".decode( 'utf-8'), ContextMenuCmds.openFileBrowser_local )
        if uploadRequired:
            separator = QtGui.QAction( self ); separator.setSeparator( True );menu.addAction( separator )
            menu.addAction("업로드".decode( 'utf-8'), ContextMenuCmds.upload )
        separator = QtGui.QAction( self ); separator.setSeparator( True );menu.addAction( separator )
        if os.path.isfile( targetPath_inServer ):menu.addAction("파일열기( 서버 )".decode( 'utf-8'), ContextMenuCmds.loadFile_server )
        menu.addAction("폴더열기( 서버 )".decode( 'utf-8'), ContextMenuCmds.openFileBrowser_server )
        separator = QtGui.QAction( self ); separator.setSeparator( True );menu.addAction( separator )
        menu.addAction("리로드".decode( "utf-8"), ContextMenuCmds.setTreeItemsCondition )

        pos = QtGui.QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        menu.exec_( point )




    def loadProject(self):
        
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data: data = {}
        
        currentText = self.comboBox.currentText()
        data[ ControlBase.labelCurrentProject ] = currentText
        
        f = open( ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        
        self.lineEdit_serverPath.setText( ControlBase.getCurrentServerPath() )
        self.lineEdit_localPath.setText( ControlBase.getCurrentLocalPath() )
        
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
        ControlBase.makeFile( ControlBase.projectListPath )
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
            selectProjectName = ControlBase.getCurrentProjectName()
        
        if selectProjectName in keys:
            self.comboBox.setCurrentIndex( keys.index( selectProjectName ) )
        
        try:
            ControlBase.manageui.updateProjectList()
        except:
            pass
        
        if ControlBase.getCurrentProjectName():
            self.addTaskArea_button.setEnabled( True )
        else:
            self.addTaskArea_button.setEnabled( False )


    
    def saveUIInfo( self ):
        ControlBase.makeFile( ControlBase.uiInfoPath )
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
        
        ControlBase.makeFile( ControlBase.uiInfoPath )
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
    
    ControlBase.mainui.loadUIInfo()
    ControlBase.mainui.show()


