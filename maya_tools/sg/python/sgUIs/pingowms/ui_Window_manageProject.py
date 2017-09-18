#coding=utf8

from ui_ControlBase import *


class Window_manageProject( QtGui.QMainWindow ):
    
    objectName = 'ui_pingowms_manageProject'
    title = "프로젝트 관리".decode('utf-8')
    defaultWidth  = 450
    defaultHeight = 500
    
    def __init__(self, *args, **kwargs ):
        
        args = tuple( [ControlBase.mayawin] )
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window_manageProject.title )
        self.resize( Window_manageProject.defaultWidth, Window_manageProject.defaultHeight )

        widgetVLayoutWorks = QtGui.QWidget()
        self.setCentralWidget(widgetVLayoutWorks)
        
        vLayoutWorks = QtGui.QVBoxLayout( widgetVLayoutWorks )
        
        layout_projectName = QtGui.QHBoxLayout()
        label_projectName = QtGui.QLabel( "프로젝트 : ".decode( 'utf8' ) )
        lineEdit_projectName   = QtGui.QLineEdit()
        button_projectName = QtGui.QPushButton( "이름변경".decode( 'utf8' ) )
        lineEdit_projectName.setReadOnly( True )
        layout_projectName.addWidget( label_projectName )
        layout_projectName.addWidget( lineEdit_projectName )
        layout_projectName.addWidget( button_projectName )
        
        WorkAreaGroupBox = QtGui.QGroupBox( '작업 리스트'.decode('utf-8') )
        WorkAreaGroupLayout = QtGui.QVBoxLayout()
        workTreeWidget = WorkTreeWidget()
        buttonDelWork = QtGui.QPushButton( "작업삭제".decode( 'utf-8' ) )
        WorkAreaGroupLayout.addWidget( workTreeWidget )
        WorkAreaGroupLayout.addWidget( buttonDelWork )
        WorkAreaGroupBox.setLayout( WorkAreaGroupLayout )
        
        projectButtonsLayout = QtGui.QHBoxLayout()
        buttonDelProject = QtGui.QPushButton( "프로젝트 삭제".decode('utf-8') )
        projectButtonsLayout.addWidget( buttonDelProject )
        
        vLayoutWorks.addLayout( layout_projectName )
        vLayoutWorks.addWidget( WorkAreaGroupBox )
        vLayoutWorks.addLayout( projectButtonsLayout )

        buttonDelWork.clicked.connect( self.deleteWork )
        buttonDelProject.clicked.connect( self.deleteProject )
        button_projectName.clicked.connect( self.setNameEditable )
        QtCore.QObject.connect( lineEdit_projectName, QtCore.SIGNAL('returnPressed()'),  self.renameProject )
        QtCore.QObject.connect( workTreeWidget, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'),  self.updateButtonCondition )

        buttonDelWork.setEnabled(False)
    
        self.currentProjectName = ControlBase.getCurrentProjectName()
        
        self.lineEdit_projectName = lineEdit_projectName
        self.workTreeWidget = workTreeWidget
        self.buttonDelProject = buttonDelProject
        self.buttonDelWork = buttonDelWork
        
        self.loadUIInfo()
    

    
    def deleteWork(self, *args):
        
        data = ControlBase.getProjectListData()
        cuProjectData = data[ self.currentProjectName ]
        
        selItems = self.workTreeWidget.selectedItems()
        del cuProjectData[ ControlBase.labelTasks ][ selItems[0].text(0) ]
        
        ControlBase.setProjectListData( data )
        
        self.loadUIInfo()
        ControlBase.mainui.updateProjectList( self.currentProjectName )
        



    def updateButtonCondition(self, *args ):
        
        selItems = self.workTreeWidget.selectedItems()
        if not selItems: 
            self.buttonDelWork.setEnabled( False )
            return None
        self.buttonDelWork.setEnabled( True )




    def renameProject(self):
        
        editedProjectName  = self.lineEdit_projectName.text()
        
        self.lineEdit_projectName.setReadOnly( True )
        
        if editedProjectName == self.currentProjectName: return
        projectNames = ControlBase.getAllProjectNames()
        
        if editedProjectName in projectNames:
            QtGui.QMessageBox.warning( self, "Warning", "동일한 프로젝트 이름이 존제합니다.\n다른이름으로 설정해주세요.".decode( 'utf-8' ) )
            self.lineEdit_projectName.setReadOnly( False )
            self.lineEdit_projectName.selectAll()
            return
        
        ControlBase.renameProject( self.currentProjectName, editedProjectName )
        self.currentProjectName = editedProjectName




    def setNameEditable(self):
        
        self.lineEdit_projectName.setReadOnly( False )
        self.lineEdit_projectName.setFocus( QtCore.Qt.MouseFocusReason )
        self.lineEdit_projectName.selectAll()
        



    def editServerPath(self):
        
        standardModel = self.projectTableView.model()
        selectionModel = self.projectTableView.selectionModel()
        qIndices = selectionModel.selection().indexes()
        qIndex = qIndices[-1]
        rowIndex = qIndex.row()
        columnIndex = qIndex.column()
        
        selItem = standardModel.itemFromIndex( qIndex )
        
        targetProjectRow = self.projectRows[rowIndex]
        
        if columnIndex == 0:
            pass
        elif columnIndex == 1:
            selectedPath = os.path.abspath(os.path.join(selItem.text(), os.pardir))
            selectedDirectory = ControlBase.getFolderFromBrowser( self, selectedPath )
            if selectedDirectory:selItem.setText(selectedDirectory)
            selectionModel.select( qIndex, QtGui.QItemSelectionModel.Select )
        elif columnIndex == 2:
            selectedPath = os.path.abspath(os.path.join(selItem.text(), os.pardir))
            selectedDirectory = ControlBase.getFolderFromBrowser( self, selectedPath )
            if selectedDirectory:selItem.setText(selectedDirectory)
            selectionModel.select(  qIndex, QtGui.QItemSelectionModel.Select )



    def deleteProject(self):
        
        resultButton = QtGui.QMessageBox.warning(self, self.tr("Warning"),'"%s" 프로젝트를 삭제하시겠습니까?'.decode( 'utf-8' ) % self.currentProjectName,
                           QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel )
        if resultButton == QtGui.QMessageBox.Cancel: return
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = None
        f.close()
        
        if not data: return
        data.pop( self.currentProjectName )
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data, f )
        f.close()
        try:ControlBase.mainui.updateProjectList()
        except:pass
        try:ControlBase.manageui.updateProjectList()
        except:pass
        self.close()
    



    def showProjectInfo( self ):
        
        qIndices = self.projectTableView.selectionModel().selection().indexes()
        if not qIndices: 
            self.WorkAreaGroupBox.setEnabled( False )
            self.buttonDelProject.setEnabled( False )
            return None
        qIndex = qIndices[-1]
        selIndex = qIndex.row()
        
        projectName, serverPath, localPath, updateDate, startDate  = self.projectRows[selIndex]
        self.WorkAreaGroupBox.setTitle( '작업 리스트 - %s'.decode('utf-8') % projectName )
        self.WorkAreaGroupBox.setEnabled( True )
        self.buttonDelProject.setEnabled( True )
    



    def saveUIInfo( self ):
        ControlBase.makeFile( ControlBase.uiInfoPath )
        f = open( ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        manageProjectWindowDict = {}
        manageProjectWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'manageProjectWindow' ] = manageProjectWindowDict
        
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
            width,  height = data['manageProjectWindow']['size']
            pWidth, pHeight = data['mainWindow']['size']
        except:
            return
        
        x = ControlBase.mainui.x() + ControlBase.mainui.width() + 5
        y = ControlBase.mainui.y()
        self.move( x, y )
        self.resize( width, pHeight )
        
        self.lineEdit_projectName.setText( ControlBase.getCurrentProjectName() )
        TreeWidgetCmds.updateTaskList(self.workTreeWidget, False)
        


    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()



