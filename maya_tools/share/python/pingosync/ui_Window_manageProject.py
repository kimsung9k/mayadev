#coding=utf8

import commands
import Models
from __qtImport import *
import json, os


class Window_manageProject( QMainWindow ):
    
    objectName = 'ui_pingowms_manageProject'
    title = "프로젝트 관리".decode('utf-8')
    defaultWidth  = 450
    defaultHeight = 500
    
    def __init__(self, *args, **kwargs ):
        
        args = tuple( [Models.ControlBase.mayawin] )
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.setObjectName( Window_manageProject.objectName )
        self.installEventFilter( self )
        self.setWindowTitle( Window_manageProject.title )
        self.resize( Window_manageProject.defaultWidth, Window_manageProject.defaultHeight )

        widgetVLayoutWorks = QWidget()
        self.setCentralWidget(widgetVLayoutWorks)
        
        vLayoutWorks = QVBoxLayout( widgetVLayoutWorks )
        
        layout_projectName = QHBoxLayout()
        label_projectName = QLabel( "프로젝트 : ".decode( 'utf8' ) )
        lineEdit_projectName   = QLineEdit()
        button_projectName = QPushButton( "이름변경".decode( 'utf8' ) )
        lineEdit_projectName.setReadOnly( True )
        layout_projectName.addWidget( label_projectName )
        layout_projectName.addWidget( lineEdit_projectName )
        layout_projectName.addWidget( button_projectName )
        
        WorkAreaGroupBox = QGroupBox( '작업 리스트'.decode('utf-8') )
        WorkAreaGroupLayout = QVBoxLayout()
        workTreeWidget = Models.WorkTreeWidget()
        WorkAreaGroupLayout.addWidget( workTreeWidget )
        WorkAreaGroupBox.setLayout( WorkAreaGroupLayout )
        
        projectButtonsLayout = QHBoxLayout()
        buttonDelProject = QPushButton( "프로젝트 삭제".decode('utf-8') )
        projectButtonsLayout.addWidget( buttonDelProject )
        
        vLayoutWorks.addLayout( layout_projectName )
        vLayoutWorks.addWidget( WorkAreaGroupBox )
        vLayoutWorks.addLayout( projectButtonsLayout )

        buttonDelProject.clicked.connect( self.deleteProject )
        button_projectName.clicked.connect( self.setProjectNameEditable )
        QtCore.QObject.connect( lineEdit_projectName, QtCore.SIGNAL('returnPressed()'),  self.renameProject )
        
        workTreeWidget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        QtCore.QObject.connect( workTreeWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),  self.loadContextMenu )
        workTreeWidget.doubleClicked.connect( self.renameWorkArea )
    
        self.currentProjectName = commands.ProjectControl.getCurrentProjectName()
        
        self.lineEdit_projectName = lineEdit_projectName
        self.workTreeWidget = workTreeWidget
        self.buttonDelProject = buttonDelProject
        
        self.loadUIInfo()
        
    
    
    
    def loadContextMenu(self, *args ):
        
        menu = QMenu( self.workTreeWidget )
        menu.addAction( "이름변경".decode( "utf-8" ), self.renameWorkArea )
        menu.addAction( "삭제".decode( 'utf-8' ), self.deleteWorkArea )
        pos = QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        menu.exec_( point )
        
    
    


    def renameWorkArea(self ):
        
        objectName = "dialog_renameWorkArea_pingowms"
        selItems = self.workTreeWidget.selectedItems()
        if not selItems: return
        selItem = selItems[0]
        
        dialog = QDialog( self )
        dialog.setObjectName( objectName )
        dialog.setWindowFlags(QtCore.Qt.Drawer)
        dialog.setWindowTitle( "이름변경".decode( 'utf-8' ) )
        dialog.resize( 200, 50 )
        dialog.setModal(True )
        
        layout = QVBoxLayout( dialog )
        lineEdit = QLineEdit( selItem.text(0) )
        button = QPushButton("이름변경".decode( 'utf-8' ) )
        layout.addWidget( lineEdit )
        layout.addWidget( button )
        
        dialog.show()

        def rename():
            dialog.close()
            
            cuText = lineEdit.text()
            
            data = commands.ProjectControl.getProjectListData()
            cuProjectData = data[ self.currentProjectName ]
            
            selItems = self.workTreeWidget.selectedItems()
            cuProjectData[ Models.ControlBase.labelTasks ][ cuText ] = cuProjectData[ Models.ControlBase.labelTasks ][ selItems[0].text(0) ]
            cuProjectData[ Models.ControlBase.labelTasks ].pop(selItems[0].text(0))
            
            commands.ProjectControl.setProjectListData( data )
            
            self.loadUIInfo()
            Models.ControlBase.mainui.updateProjectList( self.currentProjectName )
        
        QtCore.QObject.connect( lineEdit, QtCore.SIGNAL( "returnPressed()" ), rename )
        QtCore.QObject.connect( button, QtCore.SIGNAL( "clicked()" ), rename )
    
    
    
    
    def deleteWorkArea(self, *args):
        
        selItems = self.workTreeWidget.selectedItems()
        if not selItems: return
        selItem = selItems[0]
        
        objectName = "dialog_deleteWorkArea_pingowms"
        dialog = QDialog( self )
        dialog.setWindowFlags( QtCore.Qt.Drawer )
        dialog.setObjectName( objectName )
        dialog.setWindowTitle( "작업영역삭제".decode( 'utf-8' ) )
        dialog.resize( 200, 50 )
        dialog.setModal(True )
        
        layout = QVBoxLayout( dialog )
        label = QLabel( "'%s'를 삭제하시겠습니까?".decode( 'utf-8' ) % selItem.text( 0 ) )
        layoutButtons = QHBoxLayout()
        buttonDelete = QPushButton( "삭제".decode( 'utf-8' ) )
        buttonCancel = QPushButton( "취소".decode( 'utf-8' ) )
        layoutButtons.addWidget( buttonDelete )
        layoutButtons.addWidget( buttonCancel )
        layout.addWidget( label )
        layout.addLayout( layoutButtons )
        dialog.show()

        def delete():
            
            dialog.close()
            
            data = commands.ProjectControl.getProjectListData()
            cuProjectData = data[ self.currentProjectName ]
            
            selItems = self.workTreeWidget.selectedItems()
            print cuProjectData[ Models.ControlBase.labelTasks ]
            print selItems[0].text(0)
            print cuProjectData[ Models.ControlBase.labelTasks ].pop( selItems[0].text(0) )
            
            commands.ProjectControl.setProjectListData( data )
            
            self.loadUIInfo()
            Models.ControlBase.mainui.updateProjectList( self.currentProjectName )
    
        def cancel():
            dialog.close()

        QtCore.QObject.connect( buttonDelete, QtCore.SIGNAL( "clicked()" ), delete )
        QtCore.QObject.connect( buttonCancel, QtCore.SIGNAL( "clicked()" ), cancel )
        



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
        projectNames = commands.ProjectControl.getAllProjectNames()
        
        if editedProjectName in projectNames:
            QMessageBox.warning( self, "Warning", "동일한 프로젝트 이름이 존제합니다.\n다른이름으로 설정해주세요.".decode( 'utf-8' ) )
            self.lineEdit_projectName.setReadOnly( False )
            self.lineEdit_projectName.selectAll()
            return
        
        commands.ProjectControl.renameProject( self.currentProjectName, editedProjectName )
        self.currentProjectName = editedProjectName



    def setProjectNameEditable(self):
        
        self.lineEdit_projectName.setReadOnly( False )
        self.lineEdit_projectName.setFocus( QtCore.Qt.MouseFocusReason )
        self.lineEdit_projectName.selectAll()



    def deleteProject(self):
        
        resultButton = QMessageBox.warning(self, self.tr("Warning"),'"%s" 프로젝트를 삭제하시겠습니까?'.decode( 'utf-8' ) % self.currentProjectName,
                           QMessageBox.Ok|QMessageBox.Cancel )
        if resultButton == QMessageBox.Cancel: return
        
        commands.FileControl.makeFile( Models.ControlBase.projectListPath )
        f = open( Models.ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = None
        f.close()
        
        if not data: return
        data.pop( self.currentProjectName )
        f = open( Models.ControlBase.projectListPath, 'w' )
        json.dump( data, f )
        f.close()
        try:Models.ControlBase.mainui.updateProjectList()
        except:pass
        try:Models.ControlBase.manageui.updateProjectList()
        except:pass
        self.close()
    



    def saveUIInfo( self ):
        commands.FileControl.makeFile( Models.ControlBase.uiInfoPath )
        f = open( Models.ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        manageProjectWindowDict = {}
        manageProjectWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'manageProjectWindow' ] = manageProjectWindowDict
        
        f = open( Models.ControlBase.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        



    def loadUIInfo( self ):
        commands.FileControl.makeFile( Models.ControlBase.uiInfoPath )
        f = open( Models.ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            Models.ControlBase.mainui.resize( self.defaultWidth, self.defaultHeight )
            return
        
        try:
            width,  height = data['manageProjectWindow']['size']
            pWidth, pHeight = data['mainWindow']['size']
        except:
            return
        
        x = Models.ControlBase.mainui.x() + Models.ControlBase.mainui.width() + 5
        y = Models.ControlBase.mainui.y()
        self.move( x, y )
        self.resize( width, pHeight )
        
        self.lineEdit_projectName.setText( commands.ProjectControl.getCurrentProjectName() )
        commands.TreeWidgetCmds.updateTaskList(self.workTreeWidget, False)
        


    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()



