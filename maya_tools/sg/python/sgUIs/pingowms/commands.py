#coding=utf8

import maya.cmds as cmds
from maya import OpenMayaUI
from PySide import QtGui, QtCore
import shiboken
import os, sys
import json
import ntpath, ctypes

from Models import *
from ui_Dialog_updateFileList import Dialog_downloadFileList, Dialog_uploadFileList



class UICmds:
    
    @staticmethod
    def getStyleSheetFromColor( qcolor ):
        
        rValue = qcolor.red()
        gValue = qcolor.green()
        bValue = qcolor.blue()
        aValue = qcolor.alpha()
        
        return "color:rgba( %d, %d, %d, %d );" %( rValue, gValue, bValue, aValue )



class TreeWidgetCmds:


    @staticmethod
    def setTreeItemCondition( targetItem ):
        
        cuLocalUnitPath  = FileControl.getCurrentLocalProjectPath() + targetItem.taskPath + targetItem.unitPath
        cuServerUnitPath = FileControl.getCurrentServerProjectPath() + targetItem.taskPath + targetItem.unitPath
        
        compairTwoPath = CompairTwoPath( cuServerUnitPath, cuLocalUnitPath )
        compairResult  = compairTwoPath.getCompairResult()
        
        if compairResult == compairTwoPath.targetOnly:
            brush = QtGui.QBrush( Colors.localOnly )
        elif compairResult == compairTwoPath.baseOnly:
            brush = QtGui.QBrush( Colors.serverOnly )
        elif compairResult == compairTwoPath.targetIsNew:
            brush = QtGui.QBrush( Colors.localModified )
        elif compairResult == compairTwoPath.baseIsNew:
            brush = QtGui.QBrush( Colors.serverModified )
        else:
            brush = QtGui.QBrush( Colors.equar )
        
        targetItem.setForeground( 0, brush )
        
        cuLocalUnitPath  = FileControl.getArrangedPathString( cuLocalUnitPath )
        currentScenePath = cmds.file( q=1, sceneName=1 )
        
        currentScenePath = FileControl.getArrangedPathString( currentScenePath )
        localFullPath = FileControl.getArrangedPathString( cuLocalUnitPath )
        
        if currentScenePath and currentScenePath.find( localFullPath ) != -1:
            targetItem.setText( 1, "Opened".decode( 'utf-8' ) )
            cuColor = brush.color()
            cuColor.setAlpha( 100 )
            targetItem.setForeground( 1, QtGui.QBrush( cuColor ) )
        else:
            targetItem.setText( 1, "" )



    @staticmethod
    def setTreeItemsCondition( treeWidget=None ):
        
        if not treeWidget:
            treeWidget = ControlBase.uiTreeWidget
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
        #classes = QtGui.QStandardItemModel( 0, 5, self )

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
                for name in [ name for name in names if os.path.splitext( name )[-1] != '.' + ControlBase.editorInfoExtension]:
                    unitFiles.append( root.replace( serverPath, '' ) + '/' + name )
                break
            
            for root, dirs, names in os.walk( localFullPath ):
                for directory in dirs:
                    unitDirs.append( root.replace( localPath, '' ) + '/' + directory )
                for name in [ name for name in names if os.path.splitext( name )[-1] != '.' + ControlBase.editorInfoExtension ]:
                    unitFiles.append( root.replace( localPath, '' ) + '/' + name )
                break
            
            unitDirs  = list( set( unitDirs ) )
            unitFiles = list( set( unitFiles ) )

            unitDirs.sort()
            unitFiles.sort()

            for unitDir in unitDirs:
                newItem = QtGui.QTreeWidgetItem( expandedItem )
                newItem.setText( 0, unitDir.split( '/' )[-1] )
                newItem.taskPath = expandedItem.taskPath
                newItem.unitPath = unitDir.replace( expandedItem.taskPath, '' )
                emptyChild = QtGui.QTreeWidgetItem( newItem )
                numTasks += 1
            for unitFile in unitFiles:
                newItem = QtGui.QTreeWidgetItem( expandedItem )
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
    
    
    
    @staticmethod
    def isEnableReference( targetPath_inServer, targetPath_inLocal ):
        
        existPath = None
        if os.path.exists( targetPath_inServer ):
            existPath = targetPath_inServer
        elif os.path.exists( targetPath_inLocal ):
            existPath = targetPath_inLocal
        
        if not existPath: return False
        if not os.path.isfile( existPath ): return False
        
        extension = os.path.splitext( existPath )[-1]
        if not extension in ['.mb', '.ma', '.fbx', '.obj']: return False
        return True
        
        
    
    @staticmethod
    def isEnableExportReferneceInfo( targetPath ):
        
        scenePath = FileControl.getArrangedPathString( cmds.file( q=1, sceneName=1 ) )
        targetPath = FileControl.getArrangedPathString( targetPath )
        
        if scenePath != targetPath: return False
        if not cmds.ls( type='reference' ): return False
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
        json.dump( data, f, indent=2 )
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
        json.dump( data, f, indent=2 )
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
        json.dump( data, f, indent=2 )
        f.close()





class FileControl:

    @staticmethod
    def getArrangedPathString( path ):
        return path[:2] + path[2:].replace( '\\', '/' ).replace( '//', '/' ).replace( '//', '/' )



    @staticmethod
    def makeFolder( pathName ):
        
        if os.path.exists( pathName ):return None
        os.makedirs( pathName )
        return pathName



    @staticmethod
    def makeFile( filePath ):
        
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        FileControl.makeFolder( folder )
        f = open( filePath, "w" )
        json.dump( {}, f, indent=2 )
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
                json.dump( data, f, indent=2 )
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
    def getBackupPath( filePath ):
        
        filename = ntpath.split( filePath )[-1]
        dirpath = os.path.dirname( filePath ) + '/' + ControlBase.backupDirName + '/' + filename
        FileControl.makeFolder( dirpath )
        stringtime = FileTime( filePath ).stringTime()
        ext = os.path.splitext( filePath )[-1]
        return dirpath + '/' + ControlBase.backupFileName + '_' + stringtime + ext
    
    
    @staticmethod
    def isBackupFile( filePath ):
        
        filename = ntpath.split( filePath )[-1]
        if len( filename ) <= len( ControlBase.backupFileName ): return False
        if filename[:len( ControlBase.backupFileName )] == ControlBase.backupFileName: return True
        return False
    
    
    
    @staticmethod
    def downloadFile( srcFullPath, dstFullPath ):
        
        import shutil
        FileControl.makeFolder( os.path.dirname( dstFullPath ) )
        shutil.copy2( srcFullPath, dstFullPath )
        shutil.copy2( srcFullPath, FileControl.getBackupPath( dstFullPath ) )
    


    @staticmethod
    def uploadFile( srcFullPath, dstFullPath ):
        
        import shutil
        FileControl.makeFolder( os.path.dirname( dstFullPath ) )
        shutil.copy2( srcFullPath, dstFullPath )
        shutil.copy2( srcFullPath, FileControl.getBackupPath( srcFullPath ) )
    

    
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
    def referenceFile( fullPath ):
        filename = ntpath.split( fullPath )[-1]
        filename, extension = os.path.splitext( filename )
        try:
            if extension == '.mb':
                cmds.file( fullPath, r=1, type='mayaBinary', ignoreVersion=1, gl=1, mergeNamespacesOnClash=False, ns=filename, options='v=0' )
            elif extension == ".ma":
                cmds.file( fullPath, r=1, type='mayaAscii', ignoreVersion=1, gl=1, mergeNamespacesOnClash=False, ns=filename, options='v=0' )
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
    def getEditorInfoFromFile( filePath ):
        
        if not os.path.exists( filePath ):
            return EditorInfo(filePath)
        
        import ntpath
        filename = ntpath.split( filePath )[-1]
        editorInfoPath = EditorInfo.getEditorInfoPath( filePath )
        FileControl.makeFile( editorInfoPath )
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 0)
        newInstance = EditorInfo(filePath)
        f = open( editorInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if data.has_key( filename ):
            newInstance.setDict( data[filename] )
        else:
            data[filename] = newInstance.getDict()
            f = open( editorInfoPath, 'w' )
            json.dump( data, f, indent=2 )
            f.close()
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 2)
        return newInstance


    @staticmethod
    def setEditorInfoToFile( editorInfo, filePath ):
        
        import ntpath
        fileName = ntpath.split( filePath )[-1]
        editorInfoPath = EditorInfo.getEditorInfoPath( filePath )
        FileControl.makeFile( editorInfoPath )
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 0)
        
        f = open( editorInfoPath, 'r' )
        data = json.load( f )
        f.close()
        data[fileName] = editorInfo.getDict()
        f = open( editorInfoPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 2)
    
    
    
    @staticmethod
    def getMyEditorInfo( localPath ):
        return EditorInfo.getMyInfo(localPath)


    @staticmethod
    def fixEditorInfo( filePath ):
        
        if os.path.isfile(filePath):
            dirpath = os.path.dirname( filePath )
        else:
            dirpath = filePath
        
        editorInfoPath = EditorInfo.getEditorInfoPath( filePath )
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 0)
        
        data = {}
        if not os.path.exists( editorInfoPath ):
            for root, dirs, names in os.walk( dirpath ):
                for name in names:
                    if os.path.splitext( name )[-1] == '.' + ControlBase.editorInfoExtension: continue
                    data[ name ] = EditorInfo( root + '/' + name ).getDict()
                break
        else:
            f = open( editorInfoPath, 'r' )
            data = json.load( f )
            f.close()
            
            for root, dirs, names in os.walk( dirpath ):
                for name in names:
                    if os.path.splitext( name )[-1] == '.' + ControlBase.editorInfoExtension: continue
                    if data.has_key( name ):
                        data[ name ][ 'mtime' ] = FileTime( root + '/' + name ).mtime()
                    else:
                        data[ name ] = EditorInfo( root + '/' + name ).getDict()
                break
            
            f = open( editorInfoPath, 'w' )
            json.dump( data, f, indent=2 )
            f.close()
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 2)




class SceneControl:
    
    @staticmethod
    def getNeedDownloadTextureFileList( serverUnit, localUnit ):
        
        import pymel.core
        from maya import mel
        from functools import partial
        
        fileNodes = pymel.core.ls( type='file' )
        
        serverProjectPath = serverUnit.projectPath
        localProjectPath  = FileControl.getArrangedPathString( localUnit.projectPath )
        
        elsePaths = []
        for fileNode in fileNodes:
            textureLocalPath  = FileControl.getArrangedPathString( fileNode.fileTextureName.get() )
            if textureLocalPath.lower().find( localProjectPath.lower() ) != -1:
                textureServerPath = serverProjectPath + textureLocalPath[len(localProjectPath):]
            else:
                continue
            if not os.path.exists( textureServerPath ): continue
            
            if FileControl.isUpdateRequired( textureServerPath, textureLocalPath ):
                elsePaths.append( textureLocalPath[ len( localProjectPath ): ] )
        
        if elsePaths:
            elsePaths = list( set( elsePaths ) )
            ui_updateFileList = Dialog_downloadFileList( ControlBase.mayawin )
            ui_updateFileList.setServerPath( serverProjectPath )
            ui_updateFileList.setLocalPath( localProjectPath )
            for elsePath in elsePaths:
                ui_updateFileList.appendFilePath( elsePath )
            ui_updateFileList.updateUI()
            ui_updateFileList.show()


    @staticmethod
    def getNeedDownloadReferenceFileList( serverUnit, localUnit, afterCmd ):
        
        serverProjectPath = serverUnit.projectPath
        localProjectPath  = FileControl.getArrangedPathString( localUnit.projectPath )
        
        editorInfo = EditorCmds.getEditorInfoFromFile( localUnit.fullPath() )
        
        referenceFilePaths = editorInfo.getDict()['references']
        
        elsePaths = []
        for referecePath_local in [ FileControl.getArrangedPathString( filePath ) for filePath in referenceFilePaths ]:
            if referecePath_local.lower().find( localProjectPath.lower() ) != -1:
                referencePath_server = serverProjectPath + referecePath_local[len(localProjectPath):]
            else:
                continue
            if not os.path.exists( referencePath_server ): continue
            
            if FileControl.isUpdateRequired( referencePath_server, referecePath_local ):
                elsePaths.append( referecePath_local[ len( localProjectPath ): ] )
        
        if elsePaths:
            elsePaths = list( set( elsePaths ) )
            ui_updateFileList = Dialog_downloadFileList( ControlBase.mayawin )
            ui_updateFileList.setServerPath( serverProjectPath )
            ui_updateFileList.setLocalPath( localProjectPath )
            for elsePath in elsePaths:
                ui_updateFileList.appendFilePath( elsePath )
            ui_updateFileList.updateUI()
            ui_updateFileList.addDownloadCmd( afterCmd )
            ui_updateFileList.show()
    



class ContextMenuCmds:

    @staticmethod
    def loadFile_local():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]

        serverUnitInst = FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )
        localUnitInst  = FileUnit( FileControl.getCurrentLocalProjectPath(), selItem.taskPath, selItem.unitPath )

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
            serverEditor = EditorCmds.getEditorInfoFromFile( serverFullPath )
            FileControl.downloadFile( serverFullPath, localFullPath )
            EditorCmds.setEditorInfoToFile( serverEditor, localFullPath )
        else:
            serverEditor = EditorCmds.getEditorInfoFromFile( serverFullPath )
            localEditor  = EditorCmds.getEditorInfoFromFile( localFullPath )
            
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
                confirmResult = cmds.confirmDialog( title='Confirm', message='%s에 의해 %s에 변경되었습니다.\n다운받으시겠습니까?'.decode( 'utf-8' ) % (serverEditor.host, FileTime.getStrFromMTime( serverEditor.mtime )), 
                                                        button=[txDownload,txJustOpen], 
                                                        defaultButton=txJustOpen, 
                                                        parent= ControlBase.mainui.objectName )
                if confirmResult == txDownload:
                    FileControl.downloadFile( serverFullPath, localFullPath )
                    EditorCmds.setEditorInfoToFile( serverEditor, localFullPath )
        
        def afterCmd():
            FileControl.loadFile( localFullPath )
            SceneControl.getNeedDownloadTextureFileList( serverUnitInst, localUnitInst )
            TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )
        
        SceneControl.getNeedDownloadReferenceFileList( serverUnitInst, localUnitInst, afterCmd )

    
    @staticmethod
    def reference():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]

        serverUnitInst = FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )
        localUnitInst  = FileUnit( FileControl.getCurrentLocalProjectPath(), selItem.taskPath, selItem.unitPath )

        if cmds.file( modified=1, q=1 ):
            txSaveAndOpen = '저장하고 불러오기'.decode( 'utf-8' )
            txJustOpen = '그냥 불러오기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            confirmResult = cmds.confirmDialog( title='Confirm', message='레퍼런스를 불러오기 전에 씬을 저장하시겠습니까?'.decode( 'utf-8' ), 
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
            serverEditor = EditorCmds.getEditorInfoFromFile( serverFullPath )
            EditorCmds.setEditorInfoToFile( serverEditor, localFullPath )
            FileControl.downloadFile( serverFullPath, localFullPath )
        else:
            serverEditor = EditorCmds.getEditorInfoFromFile( serverFullPath )
            localEditor  = EditorCmds.getEditorInfoFromFile( localFullPath )
            
            if serverEditor > localEditor:
                FileControl.downloadFile( serverFullPath, localFullPath )
                EditorCmds.setEditorInfo( serverEditor, localFullPath )
        
        FileControl.referenceFile( localFullPath )
        SceneControl.getNeedDownloadTextureFileList( serverUnitInst, localUnitInst )
        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )
    
    
    @staticmethod
    def exportReferenceInfo():
        
        pass


    @staticmethod
    def loadFile_server():
        
        selItems = ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]
        
        serverUnitInst = FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )

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
            cmds.confirmDialog( title='Confirm', message='해댱 폴더가 존재하지 않습니다.'.decode( 'utf-8' ),
                                                        button=["확인".decode('utf-8')], parent= ControlBase.mainui.objectName )
            return
            
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
            cmds.confirmDialog( title='Confirm', message='해댱 폴더가 존재하지 않습니다.'.decode( 'utf-8' ),
                                                        button=["확인".decode('utf-8')], parent= ControlBase.mainui.objectName )
            return
        
        import subprocess
        subprocess.call( 'explorer /object, "%s"' % targetDir.replace( '/', '\\' ) )

    
    
    @staticmethod
    def upload():
        
        selItems   = ControlBase.uiTreeWidget.selectedItems()
        serverUnit = FileUnit( FileControl.getCurrentServerProjectPath(), selItems[0].taskPath, selItems[0].unitPath )
        localUnit  = FileUnit( FileControl.getCurrentLocalProjectPath(),  selItems[0].taskPath, selItems[0].unitPath )
        
        if os.path.isfile( localUnit.fullPath() ):
            txUpload = '덮어 씌우기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            
            if not os.path.exists( serverUnit.fullPath() ):
                myEditor = EditorCmds.getMyEditorInfo( localUnit.fullPath() )
                FileControl.uploadFile( localUnit.fullPath(), serverUnit.fullPath() )
                EditorCmds.setEditorInfoToFile( myEditor, localUnit.fullPath() )
                EditorCmds.setEditorInfoToFile( myEditor, serverUnit.fullPath() )
            else:
                recentEditor = EditorCmds.getEditorInfoFromFile( serverUnit.fullPath() )
                myEditor     = EditorCmds.getMyEditorInfo( localUnit.fullPath() )
                if recentEditor == myEditor:
                    confirmResult = txUpload
                else:
                    filename = ntpath.split( localUnit.fullPath() )[-1]
                    confirmResult = cmds.confirmDialog( title='Confirm', message='%s는 %s에 의해 %s에 변경되었습니다. 덮어씌울까요?'.decode( 'utf-8' ) % (filename, recentEditor.host, FileTime.getStrFromMTime( recentEditor.mtime ) ),
                                                        button=[txUpload,txCancel],
                                                        defaultButton=txCancel, parent= ControlBase.mainui.objectName )

                if confirmResult == txUpload:
                    FileControl.uploadFile( localUnit.fullPath(), serverUnit.fullPath() )
                    EditorCmds.setEditorInfoToFile( myEditor, serverUnit.fullPath() )
                    EditorCmds.setEditorInfoToFile( myEditor, localUnit.fullPath() )
        elif os.path.isdir( localUnit.fullPath() ):
            EditorCmds.fixEditorInfo( localUnit.fullPath() )
            EditorCmds.fixEditorInfo( serverUnit.fullPath() )
            targetPaths = []
            for root, dirs, names in os.walk( localUnit.fullPath() ):
                for name in names:
                    targetPath = FileControl.getArrangedPathString( root + '/' + name )[ len( localUnit.projectPath ): ]
                    if FileControl.isBackupFile( targetPath ): continue
                    if os.path.splitext( targetPath )[-1] == '.' + ControlBase.editorInfoExtension: continue
                    serverEditorInfo = EditorCmds.getEditorInfoFromFile( serverUnit.projectPath + targetPath )
                    localEditorInfo  = EditorCmds.getEditorInfoFromFile( localUnit.projectPath + targetPath )
                    if serverEditorInfo >= localEditorInfo: continue
                    targetPaths.append( targetPath )
            
            if not targetPaths:
                cmds.confirmDialog( title='Notice', message='업로드할 파일이 없습니다.'.decode( 'utf-8' ),
                                    button=["확인".decode( 'utf-8' )], parent= ControlBase.mainui.objectName )
                return
            
            ui_updateFileList = Dialog_uploadFileList( ControlBase.mayawin )
            ui_updateFileList.setServerPath( serverUnit.projectPath )
            ui_updateFileList.setLocalPath( localUnit.projectPath )
            for targetPath in targetPaths:
                ui_updateFileList.appendFilePath( targetPath )
            ui_updateFileList.updateUI()
            ui_updateFileList.show()

        TreeWidgetCmds.setTreeItemsCondition( ControlBase.uiTreeWidget )

