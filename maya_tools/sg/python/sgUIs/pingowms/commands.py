#coding=utf8

import maya.cmds as cmds
from maya import OpenMayaUI
from PySide import QtGui, QtCore
import shiboken
import os, sys
import json
import model, ntpath

from ControlBase import *
from sgUIs.pingowms.model import CompairTwoPath



class TreeWidgetCmds:


    @staticmethod
    def setTreeItemCondition( targetItem ):
        
        cuLocalUnitPath  = FileControl.getCurrentLocalProjectPath() + targetItem.taskPath + targetItem.unitPath
        cuServerUnitPath = FileControl.getCurrentServerProjectPath() + targetItem.taskPath + targetItem.unitPath
        
        compairTwoPath = model.CompairTwoPath( cuServerUnitPath, cuLocalUnitPath )
        compairResult  = compairTwoPath.getCompairResult()
        
        if compairResult == compairTwoPath.targetOnly:
            brush = QtGui.QBrush( QtGui.QColor("LightBlue") )
        elif compairResult == compairTwoPath.baseOnly:
            brush = QtGui.QBrush( QtGui.QColor("Gray") )
        elif compairResult == compairTwoPath.targetIsNew:
            brush = QtGui.QBrush( QtGui.QColor("LightBlue") )
        elif compairResult == compairTwoPath.baseIsNew:
            brush = QtGui.QBrush( QtGui.QColor("Pink") )
        elif compairResult == compairTwoPath.baseIsNew:
            brush = QtGui.QBrush( QtGui.QColor("lightGray") )
        else:
            brush = QtGui.QBrush( QtGui.QColor( 'lightGray' ) )
        
        targetItem.setForeground( 0, brush )
        
        cuLocalUnitPath  = FileControl.getArrangedPathString( cuLocalUnitPath )
        currentScenePath = cmds.file( q=1, sceneName=1 )



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

        projectName = ProjectControl.getCurrentProjectName()
        targetTreeWidget.clear()

        if not projectName: return None
        if not ProjectControl.getProjectListData()[projectName]: return None
        projectData = ProjectControl.getProjectListData()[ projectName ]
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
            serverPath = FileControl.getCurrentServerProjectPath()
            localPath   = FileControl.getCurrentLocalProjectPath()
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




class QueryCmds:
    
    @staticmethod
    def isEnableOpen( targetPath_inServer, targetPath_inLocal ):
        
        existPath = None
        if os.path.exists( targetPath_inServer ):
            existPath = targetPath_inServer
        elif os.path.exists( targetPath_inLocal ):
            existPath = targetPath_inLocal

        if not existPath: return False
        if not os.path.isfile( existPath ): return False 
        
        extension = os.path.splitext( existPath )[-1]
        if not extension in ['.mb', '.ma', '.fbx', '.obj' ]: return False
        return True
        
        
    
    
    @staticmethod
    def isEnableUpload( targetPath ):
    
        if not os.path.exists( targetPath ): return False
        if os.path.isdir( targetPath ): return False
        sceneName = FileControl.getArrangedPathString( cmds.file( q=1, sceneName=1 ) )
        targetPath = FileControl.getArrangedPathString( targetPath )
        if sceneName != targetPath: return False
        return True




class ProjectControl:


    @staticmethod
    def getAllProjectNames():
        
        FileControl.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        return data.keys()
    


    @staticmethod
    def getCurrentProjectName():
    
        FileControl.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        try:currentProject = data[ControlBase.labelCurrentProject]
        except:return
        return currentProject

    
    
    @staticmethod
    def getProjectListData():
        
        FileControl.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        try: data = json.load( f )
        except: data = {}
        f.close()
        return data



    @staticmethod
    def setProjectListData( data ):
        
        FileControl.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()
    


    @staticmethod
    def renameProject( targetProjectName, editedProjectName ):
        
        FileControl.makeFile( ControlBase.projectListPath )
        f = open( ControlBase.projectListPath, 'r' )
        data = json.load( f )
        f.close()
        
        cuProjectData = data[targetProjectName]
        del data[targetProjectName]
        data[editedProjectName] = cuProjectData
        
        f = open( ControlBase.projectListPath, 'w' )
        json.dump( data, f )
        f.close()
        
        currentProjectName = ProjectControl.getCurrentProjectName()
        ControlBase.mainui.updateProjectList( currentProjectName )


    
    @staticmethod
    def resetServerPath():

        resultPath = FileControl.getFolderFromBrowser( ControlBase.mainui, FileControl.getDefaultProjectFolder() )
        if not os.path.exists( resultPath ): return
        
        cuProject = ProjectControl.getCurrentProjectName()
        data = ProjectControl.getProjectListData()
        projectData = data[cuProject]
        if projectData.has_key( ControlBase.labelServerPath ):
            projectData[ControlBase.labelServerPath] = resultPath
            ProjectControl.setProjectListData( data )
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

        resultPath = FileControl.getFolderFromBrowser( ControlBase.mainui, FileControl.getDefaultLocalFolder() )
        if not os.path.exists( resultPath ): return
        
        cuProject = ProjectControl.getCurrentProjectName()
        data = ProjectControl.getProjectListData()
        projectData = data[cuProject]
        if projectData.has_key( ControlBase.labelLocalPath ):
            projectData[ControlBase.labelLocalPath] = resultPath
            ProjectControl.setProjectListData( data )
            ControlBase.mainui.loadProject()
        
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        data[ControlBase.labelDefaultLocalPath] = '/'.join( resultPath.split( '/' )[:-1] )
        f = open( ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close()





class FileControl:

    @staticmethod
    def getArrangedPathString( path ):
        return path.replace( '\\', '/' ).replace( '//', '/' ).replace( '//', '/' )



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
        
        FileControl.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data.has_key( ControlBase.labelDefaultServerPath ): return None
        if os.path.exists( data[ControlBase.labelDefaultServerPath] ): return data[ControlBase.labelDefaultServerPath].replace( '\\', '/' )
        else: return ''



    @staticmethod
    def getDefaultLocalFolder():
        
        FileControl.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data.has_key( ControlBase.labelDefaultLocalPath ): return None
        if os.path.exists( data[ControlBase.labelDefaultLocalPath] ): return data[ControlBase.labelDefaultLocalPath].replace( '\\', '/' )
        else: return ''
    
    

    @staticmethod
    def getCurrentServerProjectPath():
        
        cuProject = ProjectControl.getCurrentProjectName()
        projectListData = ProjectControl.getProjectListData()
        if not cuProject: return None
        if not projectListData[cuProject]: return None
        try:
            return projectListData[cuProject][ControlBase.labelServerPath]
        except:
            FileControl.makeFile( ControlBase.projectListPath )
            f = open( ControlBase.projectListPath, 'r' )
            try:data = json.load( f )
            except:data = None
            f.close()
            try:
                if not data: return
                data.pop( cuProject )
                f = open( ControlBase.projectListPath, 'w' )
                json.dump( data, f )
                f.close()
                try:ControlBase.mainui.updateProjectList()
                except:pass
            except:
                pass
    


    @staticmethod
    def getCurrentLocalProjectPath():
        
        cuProject = ProjectControl.getCurrentProjectName()
        projectListData = ProjectControl.getProjectListData()
        if not cuProject: return None
        if not projectListData[cuProject]: return None
        return projectListData[cuProject][ControlBase.labelLocalPath]



    @staticmethod
    def getDefaultTaskFolder():
        
        FileControl.makeFile( ControlBase.defaultInfoPath )
        f = open( ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        currentServerPath = FileControl.getCurrentServerProjectPath()
        if not data.has_key( ControlBase.labelDefaultTaskFolder ):
            data[ControlBase.labelDefaultTaskFolder] = ''
        
        if os.path.exists( data[ControlBase.labelDefaultTaskFolder] ):
            if data[ControlBase.labelDefaultTaskFolder].find( currentServerPath ) != -1:
                return data[ControlBase.labelDefaultTaskFolder].replace( '\\', '/' )
        return FileControl.getCurrentServerProjectPath()
    
    
    @staticmethod
    def downloadFile( srcFullPath, dstFullPath ):
        
        import shutil
        FileControl.makeFolder( os.path.dirname( dstFullPath ) )
        shutil.copy2( srcFullPath, dstFullPath )
    


    @staticmethod
    def uploadFile( srcFullPath, dstFullPath ):
        
        import shutil
        try:FileControl.makeFolder( os.path.dirname( dstFullPath ) )
        except:pass
        shutil.copy2( srcFullPath, dstFullPath )
    

    
    @staticmethod
    def loadFile( fullPath ):
        
        from maya import mel
        extension = os.path.splitext( fullPath )[-1]
        try:
            if extension == '.mb':
                cmds.file( fullPath, f=1, options = "v=0;",  typ = "mayaBinary", o=1 )
                mel.eval( 'addRecentFile("%s", "mayaBinary");' % fullPath )
            elif extension == ".ma":
                cmds.file( fullPath, f=1, options = "v=0;",  typ = "mayaAscii", o=1 )
                mel.eval( 'addRecentFile("%s", "mayaAscii");' % fullPath )
        except:
            pass
    
    
    @staticmethod
    def isUpdateRequired( serverPath, localPath ):
        
        compairResult = CompairTwoPath( serverPath, localPath ).getCompairResult()
        
        if compairResult == CompairTwoPath.baseOnly or\
           compairResult == CompairTwoPath.baseIsNew:
            return True
        
        return False
        
    
    




class EditorCmds:


    @staticmethod
    def getEditorInfoPath( filePath ):
        
        dirPath, fileName = ntpath.split( filePath )
        onlyFileName, extension = os.path.splitext( fileName )
        return dirPath + '/' + onlyFileName + '.' + ControlBase.fileInfoExtension
    
    
    
    @staticmethod
    def getMyEditorInfo( localPath ):
        return model.EditorInfo.getMyInfo(localPath)
    
    
    @staticmethod
    def getEditorInfo( serverPath ):
        
        editorInfoPath = EditorCmds.getEditorInfoPath( serverPath )
        return model.EditorInfo.getFromFile( serverPath, editorInfoPath )
    
    
    @staticmethod
    def setEditorInfo( editorInst, dstPath ):
        
        editorInfoPath= EditorCmds.getEditorInfoPath( dstPath )
        model.EditorInfo.setToFile( editorInst, editorInfoPath )
            



class SceneControl:
    
    @staticmethod
    def getNeedDownloadTextureFileList( serverUnit, localUnit ):
        
        import pymel.core
        from maya import mel
        from ui_Dialog_updateFileList import *
        
        fileNodes = pymel.core.ls( type='file' )
        
        serverTaskFullPath = serverUnit.projectPath + serverUnit.taskPath
        localTaskFullPath  = FileControl.getArrangedPathString( localUnit.projectPath + localUnit.taskPath )
        
        elsePaths = []
        for fileNode in fileNodes:
            textureLocalPath  = FileControl.getArrangedPathString( fileNode.fileTextureName.get() )
            if textureLocalPath.lower().find( localTaskFullPath.lower() ) != -1:
                textureServerPath = serverTaskFullPath + textureLocalPath[len(localTaskFullPath):]
            else:
                continue
            if not os.path.exists( textureServerPath ): continue
            
            if FileControl.isUpdateRequired( textureServerPath, textureLocalPath ):
                elsePaths.append( textureLocalPath[ len( localTaskFullPath ): ] )
        
        if elsePaths:
            elsePaths = list( set( elsePaths ) )
            ui_updateFileList = Dialog_updateFileList()
            ui_updateFileList.setServerPath( serverTaskFullPath )
            ui_updateFileList.setLocalPath( localTaskFullPath )
            for elsePath in elsePaths:
                ui_updateFileList.appendFilePath( elsePath )
            ui_updateFileList.updateUI()
            ui_updateFileList.show()
    
    


class ContextMenuCmds:

    @staticmethod
    def loadFile_local():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]

        serverUnitInst = model.FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )
        localUnitInst  = model.FileUnit( FileControl.getCurrentLocalProjectPath(), selItem.taskPath, selItem.unitPath )

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
        
        serverFullPath = serverUnitInst.fullPath()
        localFullPath  = localUnitInst.fullPath()
        
        if not os.path.exists( serverFullPath ) and os.path.exists( localFullPath ):
            pass
        elif os.path.exists( serverFullPath ) and not os.path.exists( localFullPath ):
            FileControl.downloadFile( serverFullPath, localFullPath )
        else:
            serverEditor = EditorCmds.getEditorInfo( serverFullPath )
            localEditor  = EditorCmds.getEditorInfo( localFullPath )
            
            if serverEditor == localEditor:
                if serverEditor.mtime > localEditor.mtime:
                    txDownload = "다운받고 열기".decode( "utf-8" )
                    txJustOpen = "그냥열기".decode( "utf-8" )
                    confirmResult = cmds.confirmDialog( title='Confirm', message='서버에 있는 파일이 더 최신입니다.\n다운받으시겠습니까?'.decode( 'utf-8' ), 
                                                        button=[txDownload,txJustOpen], 
                                                        defaultButton=txJustOpen, 
                                                        parent= ControlBase.mainui.objectName )
                    if confirmResult == txDownload:
                        FileControl.downloadFile( serverFullPath, localFullPath )
                        EditorCmds.setEditorInfo( serverEditor, localFullPath )
            else:
                txDownload = "다운받고 열기".decode( "utf-8" )
                txJustOpen = "그냥열기".decode( "utf-8" )
                confirmResult = cmds.confirmDialog( title='Confirm', message='%s에 의해 %s에 변경되었습니다.\n다운받으시겠습니까?'.decode( 'utf-8' ) % (serverEditor.host, model.FileTime.getStrFromMTime( serverEditor.mtime )), 
                                                        button=[txDownload,txJustOpen], 
                                                        defaultButton=txJustOpen, 
                                                        parent= ControlBase.mainui.objectName )
                if confirmResult == txDownload:
                    FileControl.downloadFile( serverFullPath, localFullPath )
                    EditorCmds.setEditorInfo( serverEditor, localFullPath )
        
        FileControl.loadFile( localFullPath )
        SceneControl.getNeedDownloadTextureFileList( serverUnitInst, localUnitInst )
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )



    @staticmethod
    def loadFile_server():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]
        
        serverUnitInst = model.FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )

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
        
        FileControl.loadFile( serverUnitInst.fullPath() )
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )



    @staticmethod
    def openFileBrowser_server():
    
        selItems = ControlBase.uiTreeWidget.selectedItems()
        cuServerUnitPath = FileControl.getCurrentServerProjectPath() + selItems[0].taskPath + selItems[0].unitPath

        if os.path.isfile( cuServerUnitPath ):
            targetDir = os.path.dirname( cuServerUnitPath )
        else:
            targetDir = cuServerUnitPath
            
        if not os.path.exists( targetDir ):
            cmds.error( "%s Path is not exists" % cuServerUnitPath )
            
        import subprocess
        subprocess.call( 'explorer /object, "%s"' % targetDir.replace( '/', '\\' ) )



    @staticmethod
    def openFileBrowser_local():

        selItems = ControlBase.uiTreeWidget.selectedItems()
        cuLocalUnitPath  = FileControl.getCurrentLocalProjectPath() + selItems[0].taskPath + selItems[0].unitPath

        compairPath = cuLocalUnitPath
        if not os.path.exists( cuLocalUnitPath ):
            compairPath = FileControl.getCurrentServerProjectPath() + selItems[0].taskPath + selItems[0].unitPath

        if os.path.isfile( compairPath ):
            targetDir = os.path.dirname( cuLocalUnitPath ) 
        else:
            targetDir = cuLocalUnitPath

        if not os.path.exists( targetDir ):
            FileControl.makeFolder( targetDir )
        
        import subprocess
        subprocess.call( 'explorer /object, "%s"' % targetDir.replace( '/', '\\' ) )

    
    
    @staticmethod
    def upload():
        
        selItems   = ControlBase.uiTreeWidget.selectedItems()
        serverUnit = model.FileUnit( FileControl.getCurrentServerProjectPath(), selItems[0].taskPath, selItems[0].unitPath )
        localUnit  = model.FileUnit( FileControl.getCurrentLocalProjectPath(),  selItems[0].taskPath, selItems[0].unitPath )
        
        txUpload = '덮어 씌우기'.decode( 'utf-8' )
        txCancel = '취소'.decode( 'utf-8' )
        
        if not os.path.exists( serverUnit.fullPath() ):
            FileControl.makeFolder( os.path.dirname( serverUnit.fullPath()) )
            FileControl.uploadFile( localUnit.fullPath(), serverUnit.fullPath() )
        else:
            recentEditor = EditorCmds.getEditorInfo( serverUnit.fullPath() )
            myEditor     = EditorCmds.getEditorInfo( localUnit.fullPath() )
            if recentEditor == myEditor:
                confirmResult = txUpload
            else:
                #print recentEditor.host, model.FileTime.getStrFromMTime( recentEditor.mtime )
                confirmResult = cmds.confirmDialog( title='Confirm', message='%s에 의해 %s에 변경되었습니다. 덮어씌울까요?'.decode( 'utf-8' ) % (recentEditor.host, model.FileTime.getStrFromMTime( recentEditor.mtime ) ),
                                                    button=[txUpload,txCancel],
                                                    defaultButton=txCancel, parent= ControlBase.mainui.objectName )
        
            if confirmResult == txUpload:
                try:FileControl.makeFolder( os.path.dirname(serverUnit.fullPath()) )
                except:pass
                FileControl.uploadFile( localUnit.fullPath(), serverUnit.fullPath() )

        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )

