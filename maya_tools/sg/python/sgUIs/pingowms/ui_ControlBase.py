#coding=utf8

import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
import model, control




class WorkTreeWidget( QtGui.QTreeWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QTreeWidget.__init__( self, *args, **kwargs )
        self.setColumnCount(2)
        headerItem = self.headerItem()
        headerItem.setText( 0, '작업이름'.decode('utf-8') )
        headerItem.setText( 1, '상태'.decode('utf-8') )




class ControlBase:
    
    mayawin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    mainui = QtGui.QMainWindow()
    manageui = QtGui.QMainWindow()
    uiTreeWidget = QtGui.QWidget()
    
    infoBaseDir = cmds.about( pd=1 ) + "/pingowms"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    projectListPath = infoBaseDir + '/projectList.json'
    defaultInfoPath = infoBaseDir + '/defaultInfo.json'
    
    labelServerPath = 'serverPath'
    labelLocalPath = 'localPath'
    labelCurrentProject = 'currentProject'
    labelDefaultLocalPath = "defaultLocalFolder"
    labelDefaultServerPath = 'defaultServerPath'
    labelDefaultTaskFolder = 'defaultTaskFolder'
    labelDefaultTaskType = 'defaultTaskType'
    labelTasks    = 'tasks'
    labelTaskType = 'type'
    labelTaskPath = 'path'



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
    def getFileFromBrowser( parent, defaultPath = '' ):
        dialog = QtGui.QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        fileName = dialog.getOpenFileName()[0]
        return fileName.replace( '\\', '/' )
    
    
    
    @staticmethod
    def getFolderFromBrowser( parent, defaultPath = '' ):
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
        if not data.has_key( ControlBase.labelDefaultLocalPath ): return None
        if os.path.exists( data[ControlBase.labelDefaultLocalPath] ): return data[ControlBase.labelDefaultLocalPath].replace( '\\', '/' )
        else: return ''
    


    @staticmethod
    def getAllProjectNames():
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        return data.keys()
    


    @staticmethod
    def getCurrentProjectName():
    
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
        
        cuProject = ControlBase.getCurrentProjectName()
        projectListData = ControlBase.getProjectListData()
        if not cuProject: return None
        if not projectListData[cuProject]: return None
        return projectListData[cuProject][ControlBase.labelServerPath]
    


    @staticmethod
    def getCurrentLocalPath():
        
        cuProject = ControlBase.getCurrentProjectName()
        projectListData = ControlBase.getProjectListData()
        if not cuProject: return None
        if not projectListData[cuProject]: return None
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
    


    @staticmethod
    def renameProject( targetProjectName, editedProjectName ):
        
        ControlBase.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        data = json.load( f )
        f.close()
        
        cuProjectData = data[targetProjectName]
        del data[targetProjectName]
        data[editedProjectName] = cuProjectData
        
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data, f )
        f.close()
        
        currentProjectName = ControlBase.getCurrentProjectName()
        ControlBase.mainui.updateProjectList( currentProjectName )


    
    @staticmethod
    def resetServerPath():

        resultPath = ControlBase.getFolderFromBrowser( ControlBase.mainui, ControlBase.getDefaultProjectFolder() )
        if not os.path.exists( resultPath ): return
        
        cuProject = ControlBase.getCurrentProjectName()
        data = ControlBase.getProjectListData()
        projectData = data[cuProject]
        if projectData.has_key( ControlBase.labelServerPath ):
            projectData[ControlBase.labelServerPath] = resultPath
            ControlBase.setProjectListData( data )
            ControlBase.mainui.loadProject()
        
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        data[ControlBase.labelDefaultServerPath] = '/'.join( resultPath.split( '/' )[:-1] )
        f = open( ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close()



    @staticmethod
    def resetLocalPath():

        resultPath = ControlBase.getFolderFromBrowser( ControlBase.mainui, ControlBase.getDefaultLocalFolder() )
        if not os.path.exists( resultPath ): return
        
        cuProject = ControlBase.getCurrentProjectName()
        data = ControlBase.getProjectListData()
        projectData = data[cuProject]
        if projectData.has_key( ControlBase.labelLocalPath ):
            projectData[ControlBase.labelLocalPath] = resultPath
            ControlBase.setProjectListData( data )
            ControlBase.mainui.loadProject()
        
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        data[ControlBase.labelDefaultLocalPath] = '/'.join( resultPath.split( '/' )[:-1] )
        f = open( ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close()


    



class TreeWidgetCmds:
    
    @staticmethod
    def setTreeItemCondition( targetItem ):
        
        cuLocalUnitPath  = ControlBase.getCurrentLocalPath() + targetItem.taskPath + targetItem.unitPath
        cuServerUnitPath = ControlBase.getCurrentServerPath() + targetItem.taskPath + targetItem.unitPath
        
        compairTwoPath = model.CompairTwoPath( cuServerUnitPath, cuLocalUnitPath )
        compairResult  = compairTwoPath.getCompairResult()
        
        if compairResult == compairTwoPath.targetOnly:
            brush = QtGui.QBrush( QtGui.QColor("lightGreen") )
        elif compairResult == compairTwoPath.baseOnly:
            brush = QtGui.QBrush( QtGui.QColor("Gray") )
        elif compairResult == compairTwoPath.targetIsNew:
            brush = QtGui.QBrush( QtGui.QColor("lightBlue") )
        elif compairResult == compairTwoPath.baseIsNew:
            brush = QtGui.QBrush( QtGui.QColor("Pink") )
        elif compairResult == compairTwoPath.baseIsNew:
            brush = QtGui.QBrush( QtGui.QColor("lightGray") )
        else:
            brush = QtGui.QBrush( QtGui.QColor( 'lightGray' ) )
            
        targetItem.setForeground( 0, brush )


    @staticmethod
    def setTreeItemsCondition( treeWidget ):
        
        def getAllChildItems( targetItem ):
            children = [targetItem]
            for k in range( targetItem.childCount() ):
                children += getAllChildItems( targetItem.child( k ) )
            return children
        
        for i in range( treeWidget.topLevelItemCount() ):
            items = getAllChildItems( treeWidget.topLevelItem( i ) )
            for item in items:
                if not item.text(0): continue
                TreeWidgetCmds.setTreeItemCondition( item )
    
    
    @staticmethod
    def updateTaskList( targetTreeWidget = None, addChild=True ):

        if not targetTreeWidget:
            targetTreeWidget = ControlBase.uiTreeWidget

        projectName = ControlBase.getCurrentProjectName()
        targetTreeWidget.clear()

        if not projectName: return None
        if not ControlBase.getProjectListData()[projectName]: return None
        projectData = ControlBase.getProjectListData()[ projectName ]
        if not projectData.has_key( ControlBase.labelTasks ): return
        tasksData = projectData[ControlBase.labelTasks]
        keys = tasksData.keys()
        #model = QtGui.QStandardItemModel( 0, 5, self )

        def addHierarchy( parent ):
            itemDir = QtGui.QTreeWidgetItem()
            parent.addChild( itemDir )

        keys.sort()
        for i in range( len( keys ) ):
            taskName = keys[i]
            taskData = tasksData[ taskName ]
            taskPath = taskData[ ControlBase.labelTaskPath ]
            itemWidget = QtGui.QTreeWidgetItem( targetTreeWidget )
            itemWidget.setText( 0, taskName )
            itemWidget.taskPath = taskPath
            itemWidget.unitPath = ""
            targetTreeWidget.resizeColumnToContents( i )
            if addChild :addHierarchy( itemWidget )

        targetTreeWidget.resizeColumnToContents( 0 )
        TreeWidgetCmds.setTreeItemsCondition( targetTreeWidget )



    @staticmethod
    def updateTaskHierarchy( *args ):
        
        expandedItem = args[0]
        for i in range( expandedItem.childCount() ):
            expandedItem.takeChild( 0 )
        
        if expandedItem.isExpanded():
            serverPath = ControlBase.getCurrentServerPath()
            localPath   = ControlBase.getCurrentLocalPath()
            path = expandedItem.taskPath + expandedItem.unitPath
            
            serverFullPath = serverPath + path
            localFullPath  = localPath  + path
            if not os.path.exists( serverFullPath ) and not os.path.exists( localFullPath ): return
            
            enableFont  = QtGui.QFont( "", 9, QtGui.QFont.Bold )
            disableFont = QtGui.QFont( "", 9, QtGui.QFont.Light )
            numTasks = 0
            
            unitDirs  = []
            unitFiles = []
            
            for root, dirs, names in os.walk( serverFullPath ):
                for directory in dirs:
                    unitDirs.append( root.replace( serverPath, '' ) + '/' + directory )
                for name in names:
                    unitFiles.append( root.replace( serverPath, '' ) + '/' + name )
                break
            
            for root, dirs, names in os.walk( localFullPath ):
                for directory in dirs:
                    unitDirs.append( root.replace( localPath, '' ) + '/' + directory )
                for name in names:
                    unitFiles.append( root.replace( localPath, '' ) + '/' + name )
                break
            
            unitDirs  = list( set( unitDirs ) )
            unitFiles = list( set( unitFiles ) )

            for unitDir in unitDirs:
                newItem = QtGui.QTreeWidgetItem( expandedItem )
                newItem.setText( 0, unitDir.split( '/' )[-1] )
                newItem.taskPath = expandedItem.taskPath
                newItem.unitPath = unitDir.replace( expandedItem.taskPath, '' )
                emptyChild = QtGui.QTreeWidgetItem( newItem )
                numTasks += 1
            for unitFile in unitFiles:
                newItem = QtGui.QTreeWidgetItem( expandedItem )
                newItem.text
                newItem.setText( 0, unitFile.split( '/' )[-1] )
                newItem.taskPath = expandedItem.taskPath
                newItem.unitPath = unitFile.replace( expandedItem.taskPath, '' )
                numTasks += 1
        else:
            QtGui.QTreeWidgetItem( expandedItem )
        
        treeWidget = expandedItem.treeWidget()
        
        TreeWidgetCmds.setTreeItemsCondition( treeWidget )
        treeWidget.resizeColumnToContents( 0 )




class ContextMenuCmds:

    @staticmethod
    def loadFile_local():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]

        serverUnitInst = model.FileUnit( ControlBase.getCurrentServerPath(), selItem.taskPath, selItem.unitPath )
        localUnitInst  = model.FileUnit( ControlBase.getCurrentLocalPath(), selItem.taskPath, selItem.unitPath )

        if cmds.file( modified=1, q=1 ):
            txSaveAndOpen = '저장하고 열기'.decode( 'utf-8' )
            txJustOpen = '그냥열기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            confirmResult = cmds.confirmDialog( title='Confirm', message='씬이 저장되지 않았습니다. 그대로 진행할까요?'.decode( 'utf-8' ), 
                                                button=[txSaveAndOpen,txJustOpen,txCancel], 
                                                defaultButton=txCancel, parent= ControlBase.mainui.objectName )
            if confirmResult == txSaveAndOpen:
                cmds.file( save=1 )
            elif confirmResult == txCancel:
                return
            
        control.loadFile_local( serverUnitInst, localUnitInst )
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )



    @staticmethod
    def loadFile_server():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]
        
        serverUnitInst = model.FileUnit( ControlBase.getCurrentServerPath(), selItem.taskPath, selItem.unitPath )

        if cmds.file( modified=1, q=1 ):
            txSaveAndOpen = '저장하고 열기'.decode( 'utf-8' )
            txJustOpen = '그냥열기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            confirmResult = cmds.confirmDialog( title='Confirm', message='씬이 저장되지 않았습니다. 그대로 진행할까요?'.decode( 'utf-8' ), 
                                                button=[txSaveAndOpen,txJustOpen,txCancel], 
                                                defaultButton=txCancel, parent= ControlBase.mainui.objectName )
            if confirmResult == txSaveAndOpen:
                cmds.file( save=1 )
            elif confirmResult == txCancel:
                return
            
        control.loadFile_server( serverUnitInst )
        
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )



    @staticmethod
    def openFileBrowser_server():
    
        selItems = ControlBase.uiTreeWidget.selectedItems()
        cuServerUnitPath = ControlBase.getCurrentServerPath() + selItems[0].taskPath + selItems[0].unitPath
    
        if os.path.isfile( cuServerUnitPath ):
            targetDir = os.path.dirname( cuServerUnitPath )
        else:
            targetDir = cuServerUnitPath
            
        if not os.path.exists( targetDir ):
            cmds.error( "%s Path is not exists" % cuServerUnitPath )
        os.startfile( targetDir )



    @staticmethod
    def openFileBrowser_local():

        selItems = ControlBase.uiTreeWidget.selectedItems()
        cuLocalUnitPath  = ControlBase.getCurrentLocalPath() + selItems[0].taskPath + selItems[0].unitPath

        if os.path.isfile( cuLocalUnitPath ):
            targetDir = os.path.dirname( cuLocalUnitPath )
        else:
            targetDir = cuLocalUnitPath

        if not os.path.exists( targetDir ):
            ControlBase.makeFolder( targetDir )
        os.startfile( targetDir )



    @staticmethod
    def setTreeItemsCondition():
        
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )
    
    
    
    @staticmethod
    def upload():
        
        selItems         = ControlBase.uiTreeWidget.selectedItems()
        instUnitServer = model.FileUnit( ControlBase.getCurrentServerPath(), selItems[0].taskPath, selItems[0].unitPath )
        instUnitLocal  = model.FileUnit( ControlBase.getCurrentLocalPath(), selItems[0].taskPath, selItems[0].unitPath )
        
        control.upload( instUnitLocal, instUnitServer )
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )
    
    


