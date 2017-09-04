#coding=utf8

import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial
import model, control



class ControlBase:
    
    mayawin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    mainui = QtGui.QMainWindow()
    manageui = QtGui.QMainWindow()
    uiTreeWidget = QtGui.QWidget()
    
    infoBaseDir = cmds.about( pd=1 ) + "/pingowms"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    projectListPath = infoBaseDir+ '/projectList.json'
    defaultInfoPath = infoBaseDir + '/defaultInfo.json'
    
    labelServerPath = 'projPath'
    labelLocalPath = 'localPath'
    labelCurrentProject = 'currentProject'
    labelDefaultLocalFolder = "defaultLocalFolder"
    labelDefaultServerPath = 'defaultServerPath'
    labelDefaultTaskFolder = 'defaultTaskFolder'
    labelDefaultTaskType = 'defaultTaskType'
    labelTasks = 'tasks'
    labelTaskType = 'type'
    labelTaskPath = 'path'
    
    currentTaskInstances = []

    @staticmethod
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


    @staticmethod
    def makeFile( filePath ):
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        ControlBase.makeFolder( folder )
        f = open( filePath, "w" )
        json.dump( {}, f )
        f.close()
    
    
    @staticmethod
    def getFile( parent, defaultPath = '' ):
        dialog = QtGui.QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        fileName = dialog.getOpenFileName()[0]
        return fileName.replace( '\\', '/' )
    
    
    
    @staticmethod
    def getDirectory( parent, defaultPath = '' ):
        dialog = QtGui.QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        choosedFolder = dialog.getExistingDirectory()
        return choosedFolder.replace( '\\', '/' )



    @staticmethod
    def getDefaultProjectFolder():
        
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data.has_key( ControlBase.labelDefaultServerPath ): return None
        if os.path.exists( data[ControlBase.labelDefaultServerPath] ): return data[ControlBase.labelDefaultServerPath].replace( '\\', '/' )
        else: return ''



    @staticmethod
    def getDefaultLocalFolder():
        
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data.has_key( ControlBase.labelDefaultLocalFolder ): return None
        if os.path.exists( data[ControlBase.labelDefaultLocalFolder] ): return data[ControlBase.labelDefaultLocalFolder].replace( '\\', '/' )
        else: return ''
    


    @staticmethod
    def getCurrentProject():
    
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        try:currentProject = data[ControlBase.labelCurrentProject]
        except:return
        return currentProject
    
    
    @staticmethod
    def getCurrentServerPath():
        
        cuProject = ControlBase.getCurrentProject()
        projectListData = ControlBase.getProjectListData()
        return projectListData[cuProject][ControlBase.labelServerPath]
    
    
    @staticmethod
    def getCurrentLocalPath():
        
        cuProject = ControlBase.getCurrentProject()
        projectListData = ControlBase.getProjectListData()
        return projectListData[cuProject][ControlBase.labelLocalPath]



    @staticmethod
    def getDefaultTaskFolder():
        
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        currentServerPath = ControlBase.getCurrentServerPath()
        if not data.has_key( ControlBase.labelDefaultTaskFolder ):
            data[ControlBase.labelDefaultTaskFolder] = ''
        
        if os.path.exists( data[ControlBase.labelDefaultTaskFolder] ):
            if data[ControlBase.labelDefaultTaskFolder].find( currentServerPath ) != -1:
                return data[ControlBase.labelDefaultTaskFolder].replace( '\\', '/' )
        return ControlBase.getCurrentServerPath()


    @staticmethod
    def getProjectListData():
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        try: data = json.load( f )
        except: data = {}
        f.close()
        return data



    @staticmethod
    def setProjectListData( data ):
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()




class TreeWidgetCmds:
    
    
    @staticmethod
    def setTreeItemCondition( targetItem ):
        
        cuServerPath = ControlBase.getCurrentServerPath()
        cuLocalPath = ControlBase.getCurrentLocalPath()
        
        localUnitPath = cuLocalPath + targetItem.text(1)
        if not os.path.exists( localUnitPath ):
            brush = QtGui.QBrush( QtGui.QColor("gray" ) ) 
            targetItem.setForeground ( 0, brush )
        else:
            brush = QtGui.QBrush( QtGui.QColor("lightGray") ) 
            targetItem.setForeground ( 0, brush )


    @staticmethod
    def reloadTreeItems( treeWidget ):
        
        def getAllChildItems( targetItem ):
            children = [targetItem]
            for k in range( targetItem.childCount() ):
                children += getAllChildItems( targetItem.child( k ) )
            return children
        
        numItems = 0
        for i in range( treeWidget.topLevelItemCount() ):
            items = getAllChildItems( treeWidget.topLevelItem( i ) )
            for item in items:
                TreeWidgetCmds.setTreeItemCondition( item )
                numItems += 1
        print "numItems : ", numItems
    
    
    @staticmethod
    def updateTaskHierarcy( *args ):
        
        expandedItem = args[0]
        for i in range( expandedItem.childCount() ):
            expandedItem.takeChild( 0 )
        
        if expandedItem.isExpanded():
            serverPath = ControlBase.getCurrentServerPath()
            localPath   = ControlBase.getCurrentLocalPath()
            path = expandedItem.text(1)
            
            fullPath = serverPath + path
            if not os.path.exists( fullPath ): return
            
            enableFont  = QtGui.QFont( "", 9, QtGui.QFont.Bold )
            disableFont = QtGui.QFont( "", 9, QtGui.QFont.Light )
            
            numTasks = 0
            for root, dirs, names in os.walk( fullPath ):
                for dir in dirs:
                    newItem = QtGui.QTreeWidgetItem( expandedItem )
                    newItem.setText( 0, dir )
                    newItem.setText( 1, root.replace( serverPath, '' ) + '/' + dir )
                    emptyChild = QtGui.QTreeWidgetItem( newItem )
                    numTasks += 1
                for name in names:
                    newItem = QtGui.QTreeWidgetItem( expandedItem )
                    newItem.text
                    newItem.setText( 0, name )
                    newItem.setText( 1, root.replace( serverPath, '' ) + '/' + name )
                    numTasks += 1
                break
        else:
            QtGui.QTreeWidgetItem( expandedItem )
        
        treeWidget = expandedItem.treeWidget()
        
        TreeWidgetCmds.reloadTreeItems( treeWidget )
        treeWidget.resizeColumnToContents( 0 )




class ContextMenuCmds:
    
    @staticmethod
    def loadFile():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]
        elsePath = selItem.text( 1 )
        
        upperParent = selItem
        targetIndex = 0
        while upperParent:
            for i in range( ControlBase.uiTreeWidget.topLevelItemCount() ):
                if upperParent.text(1) == ControlBase.uiTreeWidget.topLevelItem( i ).text(1):
                    targetIndex = i
                    break
            upperParent = upperParent.parent()
        
        currentTaskInstance = ControlBase.currentTaskInstances[ targetIndex ]
        unitInst = model.Unit( currentTaskInstance, selItem.text(1) )

        control.loadFile( unitInst )
        TreeWidgetCmds.reloadTreeItems()


    @staticmethod
    def openFileBrowser():
    
        selItems = ControlBase.uiTreeWidget.selectedItems()
    
        cuServerUnitPath = ControlBase.getCurrentServerPath() + selItems[0].text( 1 )
        cuLocalUnitPath  = ControlBase.getCurrentLocalPath() + selItems[0].text( 1 )
    
        if not os.path.exists( cuServerUnitPath ):
            cmds.error( "%s Path is not exists" % cuServerUnitPath )
        if os.path.isfile( cuServerUnitPath ):
            targetPath = os.path.dirname( cuLocalUnitPath )
        else:
            targetPath = cuLocalUnitPath
        if not os.path.exists( targetPath ):
            ControlBase.makeFolder( targetPath )
        os.startfile( targetPath )
    
    
    @staticmethod
    def reloadTreeItems():
        
        TreeWidgetCmds.reloadTreeItems()





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
        
        verticalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical )
        self.setCentralWidget( verticalSplitter )

        widgetVLayoutProjects = QtGui.QWidget()
        vLayoutProjects = QtGui.QVBoxLayout( widgetVLayoutProjects )
        labelProjList = QtGui.QLabel( '프로젝트 리스트'.decode( 'utf-8' ) )
        projectTableView = QtGui.QTableView()
        tableModel = QtGui.QStandardItemModel( 0, 5, self )
        tableModel.setHorizontalHeaderItem( 0, QtGui.QStandardItem( '프로젝트 이름'.decode('utf-8') ) )
        tableModel.setHorizontalHeaderItem( 1, QtGui.QStandardItem( '로컬경로'.decode('utf-8') ) )
        tableModel.setHorizontalHeaderItem( 2, QtGui.QStandardItem( '서버경로'.decode('utf-8') ) )
        tableModel.setHorizontalHeaderItem( 3, QtGui.QStandardItem( '최근사용'.decode('utf-8') ) )
        tableModel.setHorizontalHeaderItem( 4, QtGui.QStandardItem( '생성날짜'.decode('utf-8') ) )
        projectTableView.setModel( tableModel )
        vLayoutProjects.addWidget( labelProjList )
        vLayoutProjects.addWidget( projectTableView )

        widgetVLayoutWorks = QtGui.QWidget()
        vLayoutWorks = QtGui.QVBoxLayout( widgetVLayoutWorks )
        WorkAreaGroupBox = QtGui.QGroupBox( '작업 리스트'.decode('utf-8') )
        WorkAreaGroupLayout = QtGui.QVBoxLayout()
        workTreeWidget = WorkTreeWidget()
        buttonDelWork = QtGui.QPushButton( "작업삭제".decode( 'utf-8' ) )
        WorkAreaGroupLayout.addWidget( workTreeWidget )
        WorkAreaGroupLayout.addWidget( buttonDelWork )
        WorkAreaGroupBox.setLayout( WorkAreaGroupLayout )
        buttonDelWork.setEnabled( False )
        WorkAreaGroupBox.setEnabled(False)
        
        projectButtonsLayout = QtGui.QHBoxLayout()
        buttonDelProject = QtGui.QPushButton( "프로젝트 삭제".decode('utf-8') )
        projectButtonsLayout.addWidget( buttonDelProject )
        buttonDelProject.setEnabled(False)
        vLayoutWorks.addWidget( WorkAreaGroupBox )
        vLayoutWorks.addLayout( projectButtonsLayout )
        
        verticalSplitter.addWidget( widgetVLayoutProjects )
        verticalSplitter.addWidget( widgetVLayoutWorks )
        
        self.projectTableView = projectTableView
        self.WorkAreaGroupBox = WorkAreaGroupBox
        self.buttonDelProject = buttonDelProject
        
        self.updateProjectList()
        
        self.buttonDelProject.clicked.connect( self.deleteProject )
        self.projectTableView.clicked.connect( self.showProjectInfo )
        self.projectTableView.doubleClicked.connect( self.editServerPath )
        QtCore.QObject.connect( self.projectTableView.model(), QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)' ), self.editProjectName )
    
        self.loadUIInfo()
    
    
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
            selectedDirectory = ControlBase.getDirectory( self, selectedPath )
            if selectedDirectory:selItem.setText(selectedDirectory)
            selectionModel.select( qIndex, QtGui.QItemSelectionModel.Select )
        elif columnIndex == 2:
            selectedPath = os.path.abspath(os.path.join(selItem.text(), os.pardir))
            selectedDirectory = ControlBase.getDirectory( self, selectedPath )
            if selectedDirectory:selItem.setText(selectedDirectory)
            selectionModel.select(  qIndex, QtGui.QItemSelectionModel.Select )
    
    
    def editProjectName(self, modelIndex1, modelIndex2 ):
        
        rowIndex = modelIndex1.row()
        columnIndex = modelIndex1.column()
        
        standardModel = self.projectTableView.model()
        
        if columnIndex != 0: return  
        if rowIndex >=len( self.projectRows ): return
        originalProjectName,localPath,serverPath,date1,date2 = self.projectRows[rowIndex]
        editedName = standardModel.item( rowIndex ).text()
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        if not data: 
            cmds.warning( "data is not exists" )
            return

        projectNames = data.keys()
        if editedName in projectNames:
            if editedName == originalProjectName: return
            QtGui.QMessageBox.warning( self, "Warning", "동일한 프로젝트 이름이 존제합니다.\n다른이름으로 설정해주세요.".decode( 'utf-8' ) )
            standardModel.item( rowIndex ).setText( originalProjectName )
            return
        
        originalProjectData = data[originalProjectName]
        data[ editedName ] = originalProjectData
        data.pop( originalProjectName )
        
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data , f )
        f.close()
        
        self.projectRows[rowIndex][0] = editedName
        try:ControlBase.mainui.updateProjectList()
        except:pass
        try:ControlBase.manageui.updateProjectList()
        except:pass
    
    
    
    def deleteProject(self):
        
        qIndices = self.projectTableView.selectionModel().selection().indexes()
        qIndex = qIndices[-1]
        selIndex = qIndex.row()
        
        projectName, serverPath, localPath, updateDate, startDate  = self.projectRows[selIndex]
        
        resultButton = QtGui.QMessageBox.warning(self, self.tr("Warning"),'"%s" 프로젝트를 삭제하시겠습니까?'.decode( 'utf-8' ) % projectName,
                           QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel )
        if resultButton == QtGui.QMessageBox.Cancel: return
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = None
        f.close()
        
        if not data: return
        data.pop( projectName )
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data, f )
        f.close()
        try:ControlBase.mainui.updateProjectList()
        except:pass
        try:ControlBase.manageui.updateProjectList()
        except:pass
    
    
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
        
    
    def updateProjectList(self):
        
        data = ControlBase.getProjectListData()
        
        keys = data.keys()
        keys.sort()
        
        model = self.projectTableView.model()
        #model = QtGui.QStandardItemModel( 0, 5, self )
        for i in range( model.rowCount() ):
            model.removeRow( 0 )
        
        self.projectRows = {}
        for i in range( len( keys ) ):
            projectName = keys[i]
            projectInfo = data[ projectName ]
            serverPath = projectInfo[ ControlBase.labelServerPath ]
            localPath   = projectInfo[ ControlBase.labelLocalPath ]
            standardModel = self.projectTableView.model()
            standardModel.insertRow( i )
            itemProjectName = QtGui.QStandardItem( projectName )
            itemLocalPath   = QtGui.QStandardItem( localPath ); itemLocalPath.setEditable(False)
            itemServerPath = QtGui.QStandardItem( serverPath ); itemServerPath.setEditable(False)
            standardModel.setItem(i, 0, itemProjectName)
            standardModel.setItem(i, 1, itemLocalPath)
            standardModel.setItem(i, 2, itemServerPath)
            self.projectRows[i] = [projectName,serverPath,localPath,'','' ]
    

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
            width, height = data['manageProjectWindow']['size']
            pWidth, pHeight = data['mainWindow']['size']
        except:
            return
        
        x = ControlBase.mainui.x() + ControlBase.mainui.width() + 5
        y = ControlBase.mainui.y()
        self.move( x, y )
        self.resize( width, pHeight )


    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()




class Dialog_addProject( QtGui.QDialog ):
    
    objectName = 'ui_pingowms_addProject'
    title = "프로젝트 추가".decode('utf-8')
    defaultWidth= 450
    defaultHeight = 50
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [ControlBase.mayawin] )
        
        QtGui.QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Dialog_addProject.title )
        self.resize( Dialog_addProject.defaultWidth, Dialog_addProject.defaultHeight )
        
        vlayout = QtGui.QVBoxLayout( self )
        projectNameLayout = QtGui.QHBoxLayout()
        serverPathLayout = QtGui.QHBoxLayout()
        localPathLayout   = QtGui.QHBoxLayout()
        buttonsLayout     = QtGui.QHBoxLayout()
        
        projectNameLabel = QtGui.QLabel( "프로젝트 명 : ".decode('utf-8') )
        projectNameEdit  = QtGui.QLineEdit()
        projectNameLayout.addWidget( projectNameLabel )
        projectNameLayout.addWidget( projectNameEdit )
        
        serverPathLabel = QtGui.QLabel( "프로젝트 경로 : ".decode('utf-8') )
        serverPathEdit  = QtGui.QLineEdit()
        serverPathButton = QtGui.QPushButton('...')
        serverPathLayout.addWidget( serverPathLabel )
        serverPathLayout.addWidget( serverPathEdit )
        serverPathLayout.addWidget( serverPathButton )
        
        localPathLocal = QtGui.QLabel( "로컬 경로 : ".decode('utf-8') )
        localPathEdit  = QtGui.QLineEdit()
        localPathButton = QtGui.QPushButton('...')
        localPathLayout.addWidget( localPathLocal )
        localPathLayout.addWidget( localPathEdit )
        localPathLayout.addWidget( localPathButton )
        
        buttonsFirst = QtGui.QPushButton( "생성".decode('utf-8') )
        buttonsSecond  = QtGui.QPushButton( "취소".decode('utf-8') )
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

        resultPath = ControlBase.getDirectory( self, ControlBase.getDefaultProjectFolder() )
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

        resultPath = ControlBase.getDirectory( self, ControlBase.getDefaultLocalFolder() )
        if os.path.exists( resultPath ):
            self.localPathEdit.setText( resultPath )
            f = open( ControlBase.defaultInfoPath, 'r' )
            data = json.load( f )
            f.close()
            data[ControlBase.labelDefaultLocalFolder] = '/'.join( resultPath.split( '/' )[:-1] )
            f = open( ControlBase.defaultInfoPath, 'w' )
            json.dump( data, f )
            f.close() 
    
    

    def createProject(self):
        
        projName = self.projectNameEdit.text()
        projPath = self.serverPathEdit.text()
        localPath = self.localPathEdit.text()
        
        ControlBase.makeFile( ControlBase.projectListPath )
        
        f = open( ControlBase.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        keyList = data.keys()
        
        if not projName:
            QtGui.QMessageBox.warning(self, self.tr("Warning"),"프로젝트 이름을 입력하세요.".decode( 'utf-8' ),
                               QtGui.QMessageBox.Ok )
            return
        
        if not projPath or not os.path.exists( projPath ):
            QtGui.QMessageBox.warning(self, self.tr("Warning"),'"%s"\n프로젝트 경로가 존재하지 않습니다.'.decode( 'utf-8' ) % projPath,
                               QtGui.QMessageBox.Ok )
            return
        
        if not localPath or not os.path.exists( localPath ):
            QtGui.QMessageBox.warning(self, self.tr("Warning"),'"%s"\n로컬 경로가 존재하지 않습니다.'.decode( 'utf-8' ) % localPath,
                               QtGui.QMessageBox.Ok )
            return
        
        if projName in keyList:
            resultButton = QtGui.QMessageBox.warning(self, self.tr("Warning"),'"%s" 프로젝트가 존재합니다.\n대치하시겠습니까?'.decode( 'utf-8' ) % projName,
                               QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel )
            if resultButton == QtGui.QMessageBox.Cancel: return
    
        data["%s" % projName] = { ControlBase.labelServerPath:"%s" % projPath, ControlBase.labelLocalPath:"%s" % localPath }
        ControlBase.setProjectListData(data)
        self.close()
        
        ControlBase.mainui.updateProjectList( projName )
        
        
    def closeUI(self):
        
        self.close()




class Dialog_addTask( QtGui.QDialog ):
    
    objectName = 'ui_pingowms_addTask'
    title = "작업영역추가".decode('utf-8')
    defaultWidth= 450
    defaultHeight = 50
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [ControlBase.mayawin] )
        
        QtGui.QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Dialog_addTask.title + ' - ' + ControlBase.getCurrentProject() )
        self.resize( Dialog_addTask.defaultWidth, Dialog_addTask.defaultHeight )
        
        self.setModal( True )
        
        vLayout       = QtGui.QVBoxLayout( self )
        typeLayout    = QtGui.QHBoxLayout()
        pathLayout    = QtGui.QHBoxLayout()
        taskNameLayout = QtGui.QHBoxLayout()
        buttonsLayout = QtGui.QHBoxLayout()
        
        typeLabel = QtGui.QLabel( "영역 타입".decode( 'utf-8' ) )
        typeComboBox = QtGui.QComboBox()
        typeComboBox.addItems( ['파일'.decode( 'utf-8' ),'폴더'.decode( 'utf-8' )] )
        typeLayout.addWidget( typeLabel )
        typeLayout.addWidget( typeComboBox )
        
        pathLabel = QtGui.QLabel( "경로 : ".decode( "utf-8" ) )
        pathLineEdit = QtGui.QLineEdit()
        pathButton = QtGui.QPushButton( "..." )
        pathLayout.addWidget( pathLabel )
        pathLayout.addWidget( pathLineEdit )
        pathLayout.addWidget( pathButton )
        
        taskNameLabel = QtGui.QLabel( "작업영역이름 : ".decode( 'utf-8' ) )
        taskNameLineEdit = QtGui.QLineEdit()
        taskNameLayout.addWidget( taskNameLabel )
        taskNameLayout.addWidget( taskNameLineEdit )
        
        buttonCreate = QtGui.QPushButton( "생성".decode( 'utf-8' ) )
        buttonClose  = QtGui.QPushButton( "닫기".decode( 'utf-8' ) )
        buttonsLayout.addWidget( buttonCreate )
        buttonsLayout.addWidget( buttonClose )
        
        vLayout.addLayout( typeLayout )
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
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        data[ControlBase.labelDefaultTaskType] = self.typeComboBox.currentIndex()
        
        f = open( ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close() 
        
        

    def loadDefaultTaskType(self):
        ControlBase.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        try: data = json.load( f )
        except: data = {}
        f.close()
        if not data.has_key( ControlBase.labelDefaultTaskType ): return 0
        self.typeComboBox.setCurrentIndex( data[ControlBase.labelDefaultTaskType] )


    
    def loadTaskPath(self):
        if self.typeComboBox.currentIndex() == 0:
            resultPath = ControlBase.getFile( self, ControlBase.getDefaultTaskFolder() )
        else:
            resultPath = ControlBase.getDirectory( self, ControlBase.getDefaultTaskFolder() )

        if os.path.exists( resultPath ):
            self.pathLineEdit.setText( resultPath )
            f = open( ControlBase.defaultInfoPath, 'r' )
            data = json.load( f )
            f.close()
            data[ControlBase.labelDefaultTaskFolder] = '/'.join( resultPath.split( '/' )[:-1] )
            f = open( ControlBase.defaultInfoPath, 'w' )
            json.dump( data, f )
            f.close() 
            self.taskNameLineEdit.setText( resultPath.split( '/' )[-1] )


    def createTask(self):
        currentProject = ControlBase.getCurrentProject()
        projectListData = ControlBase.getProjectListData()
        if not projectListData.has_key( currentProject ):
            cmds.warning( "프로젝트가 존제하지 않습니다.".decode( 'utf-8') )
            return
        projectDict = projectListData[currentProject]
        if not projectDict.has_key( ControlBase.labelTasks ):
            projectDict[ControlBase.labelTasks] = {}
        taskDict = projectDict[ControlBase.labelTasks]
        typeTask = self.typeComboBox.currentIndex()
        pathTask = self.pathLineEdit.text()
        nameTask = self.taskNameLineEdit.text()
        
        if not os.path.exists( pathTask ):
            cmds.warning( "%s 경로가 존재하지 않습니다.".decode( 'utf-8') % pathTask )
            return
        if not os.path.isfile( pathTask ) and typeTask == 0:
            cmds.warning( "'%s' 는 파일이 아닙니다.".decode( 'utf-8') % pathTask )
            return
        if not os.path.isdir( pathTask ) and typeTask == 1:
            cmds.warning( "'%s' 는 폴더가 아닙니다.".decode( 'utf-8') % pathTask )
            return
        
        serverPath = projectDict[ ControlBase.labelServerPath ]
        if pathTask.lower().find( serverPath.lower() ) == -1: 
            cmds.warning( "%s 가 프로젝트 경로에 존제하지 않습니다.".decode( 'utf-8') % serverPath )
            return

        addTaskPath = pathTask.replace( serverPath, '' )
        taskDict[nameTask] = { ControlBase.labelTaskType : typeTask, ControlBase.labelTaskPath : addTaskPath }
        
        ControlBase.setProjectListData(projectListData)
        self.close()
        ControlBase.mainui.updateTaskList()





class WorkTreeWidget( QtGui.QTreeWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QTreeWidget.__init__( self, *args, **kwargs )
        self.setColumnCount(4)
        headerItem = self.headerItem()
        headerItem.setText( 0, '작업이름'.decode('utf-8') )
        headerItem.setText( 1, '경로'.decode('utf-8') )
        headerItem.setText( 2, '업데이트날짜'.decode('utf-8') )
        headerItem.setText( 3, '생성날짜'.decode('utf-8') )
        self.itemExpanded.connect( TreeWidgetCmds.updateTaskHierarcy )
        self.itemCollapsed.connect( TreeWidgetCmds.updateTaskHierarcy )
        

    



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
        label = QtGui.QLabel( "프로젝트 명 : ".decode('utf-8') ); label.setMaximumWidth( 100 )
        comboBox = QtGui.QComboBox(); #comboBox.setMaximumWidth( 200 )
        addProject_button = QtGui.QPushButton( " + " ); addProject_button.setMaximumWidth( 30 )
        manageProject_button = QtGui.QPushButton( "프로젝트 관리".decode('utf-8') ); manageProject_button.setMaximumWidth( 100 )
        layout_project.addWidget( label )
        layout_project.addWidget( comboBox )
        layout_project.addWidget( addProject_button )
        layout_project.addWidget( manageProject_button )
        
        layoutWorkArea = QtGui.QVBoxLayout()
        treeWidget = WorkTreeWidget()
        addTaskArea_button = QtGui.QPushButton( '작업추가'.decode('utf-8') )
        layoutWorkArea.addWidget( treeWidget )
        layoutWorkArea.addWidget( addTaskArea_button )
        
        vLayout.addLayout( layout_project )
        vLayout.addLayout( layoutWorkArea )
        
        addProject_button.clicked.connect( self.show_addProject )
        manageProject_button.clicked.connect( self.show_manageProject )
        addTaskArea_button.clicked.connect( self.show_addTaskArea )
        comboBox.currentIndexChanged.connect( self.loadProject )
        
        self.comboBox = comboBox
        self.addTaskArea_button = addTaskArea_button
        ControlBase.uiTreeWidget = treeWidget
        self.updateProjectList()
        
        ControlBase.uiTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect( ControlBase.uiTreeWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),  self.loadContextMenu )
        
        if ControlBase.getCurrentProject():
            self.addTaskArea_button.setEnabled( True )
        else:
            self.addTaskArea_button.setEnabled( False )
        
        ControlBase.uiTreeWidget.setFont( QtGui.QFont( "", 9, QtGui.QFont.Light ) )
            
    
    def loadContextMenu(self, *args ):
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem = selItems[0]
        elsePath = selItem.text( 1 )
        
        serverPath = ControlBase.getCurrentServerPath()
        targetPath = serverPath + elsePath 
        
        menu = QtGui.QMenu( ControlBase.uiTreeWidget )
        
        if os.path.isfile( targetPath ):menu.addAction("파일열기".decode( 'utf-8'), ContextMenuCmds.loadFile )
        menu.addAction("폴더열기".decode( 'utf-8'), ContextMenuCmds.openFileBrowser )
        menu.addAction("리로드".decode( "utf-8"), ContextMenuCmds.reloadTreeItems )

        globalPosTreeWidget = ControlBase.uiTreeWidget.mapToGlobal( ControlBase.uiTreeWidget.pos() )        
        point = QtCore.QPoint( globalPosTreeWidget.x() + args[0].x(), globalPosTreeWidget.y() + args[0].y()-20 )
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
        
        self.updateTaskList()
    
    
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
        keys.sort()
        
        self.comboBox.clear()
        if data:
            self.comboBox.addItems( keys )
        
        if not selectProjectName:
            selectProjectName = ControlBase.getCurrentProject()
        
        if selectProjectName in keys:
            self.comboBox.setCurrentIndex( keys.index( selectProjectName ) )
        
        try:
            ControlBase.manageui.updateProjectList()
        except:
            pass
        
        if ControlBase.getCurrentProject():
            self.addTaskArea_button.setEnabled( True )
        else:
            self.addTaskArea_button.setEnabled( False )



    def updateTaskList( self ):
        
        projectName = ControlBase.getCurrentProject()
        ControlBase.uiTreeWidget.clear()
        projectData = ControlBase.getProjectListData()[ projectName ]
        if not projectData.has_key( ControlBase.labelTasks ): return
        tasksData = ControlBase.getProjectListData()[ projectName ][ControlBase.labelTasks]
        keys = tasksData.keys()
        #model = QtGui.QStandardItemModel( 0, 5, self )
        self.projectRows = {}
        
        def addHierarchy( parent ):
            itemDir = QtGui.QTreeWidgetItem()
            parent.addChild( itemDir )
        
        serverPath = ControlBase.getCurrentServerPath()
        localPath   = ControlBase.getCurrentLocalPath()
        
        ControlBase.currentTaskInstances = []
        for i in range( len( keys ) ):
            taskName = keys[i]
            taskData = tasksData[ taskName ]
            taskType = taskData[ ControlBase.labelTaskType ]
            taskPath = taskData[ ControlBase.labelTaskPath ]
            itemWidget = QtGui.QTreeWidgetItem( ControlBase.uiTreeWidget )
            itemWidget.setText( 0, taskName )
            itemWidget.setText( 1, taskPath )
            ControlBase.uiTreeWidget.resizeColumnToContents( i )
            addHierarchy( itemWidget )
            currentTaskInst = model.Task( serverPath, localPath, taskPath )
            ControlBase.currentTaskInstances.append( currentTaskInst )
            
            self.projectRows[i] = [projectName,taskPath,'','' ]
        ControlBase.uiTreeWidget.resizeColumnToContents( 0 )

    
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
