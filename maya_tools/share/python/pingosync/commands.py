#coding=utf8

from maya import OpenMayaUI, cmds

from pymel import api

import os, sys
import json
import ntpath, ctypes

import Models
from __qtImport import *
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

        cuLocalFullPath  = FileControl.getCurrentLocalProjectPath() + targetItem.taskPath + targetItem.unitPath
        cuServerFullPath = FileControl.getCurrentServerProjectPath() + targetItem.taskPath + targetItem.unitPath
        
        compairTwoPath = Models.CompairTwoPath( cuServerFullPath, cuLocalFullPath )
        compairResult  = compairTwoPath.getCompairResult()
        
        if compairResult == compairTwoPath.targetOnly:
            brush = QBrush( Models.Colors.localOnly )
        elif compairResult == compairTwoPath.baseOnly:
            brush = QBrush( Models.Colors.serverOnly )
        elif compairResult == compairTwoPath.targetIsNew:
            brush = QBrush( Models.Colors.localModified )
        elif compairResult == compairTwoPath.baseIsNew:
            brush = QBrush( Models.Colors.serverModified )
        else:
            brush = QBrush( Models.Colors.equar )
        brushForPath = QBrush( Models.Colors.serverOnly )

        targetItem.setForeground( 0, brush )
        targetItem.setForeground( 1, brush )
        cuColor = brush.color()
        cuColor.setAlpha( 120 )
        brush = QBrush( cuColor )
        targetItem.setForeground( 1, brush )
        targetItem.setForeground( 3, brushForPath )

        cuLocalUnitPath  = FileControl.getArrangedPathString( cuLocalFullPath )
        currentScenePath = cmds.file( q=1, sceneName=1 )

        currentScenePath = FileControl.getArrangedPathString( currentScenePath )
        localFullPath = FileControl.getArrangedPathString( cuLocalUnitPath )

        if currentScenePath and FileControl.hasPath( currentScenePath, localFullPath ):
            targetItem.setText( 2, "Opened".decode( 'utf-8' ) )
            targetItem.setForeground( 2, brush )
        else:
            targetItem.setText( 2, "" )
        targetItem.setSelected( False )


    @staticmethod
    def setTreeItemsCondition( treeWidget=None ):
        
        if not treeWidget:
            treeWidget = Models.ControlBase.uiTreeWidget
        
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
        
        treeWidget.resizeColumnToContents( 0 )
        treeWidget.resizeColumnToContents( 1 )
        treeWidget.setColumnWidth( 2, 50 )



    @staticmethod
    def updateTaskList( targetTreeWidget = None, addChild=True ):

        if not targetTreeWidget:
            targetTreeWidget = Models.ControlBase.uiTreeWidget

        projectName = ProjectControl.getCurrentProjectName()
        try:targetTreeWidget.clear()
        except:pass

        if not projectName: return None
        if not ProjectControl.getProjectListData()[projectName]: return None
        projectData = ProjectControl.getProjectListData()[ projectName ]
        if not projectData.has_key( Models.ControlBase.labelTasks ): return
        tasksData = projectData[Models.ControlBase.labelTasks]
        keys = tasksData.keys()
        #classes = QStandardItemModel( 0, 5, self )

        def addHierarchy( parent ):
            itemDir = QTreeWidgetItem()
            parent.addChild( itemDir )

        keys.sort()
        for i in range( len( keys ) ):
            taskName = keys[i]
            taskData = tasksData[ taskName ]
            taskPath = taskData[ Models.ControlBase.labelTaskPath ]
            itemWidget = QTreeWidgetItem( targetTreeWidget )
            itemWidget.taskPath = taskPath
            itemWidget.unitPath = ""
            if addChild :addHierarchy( itemWidget )
            itemWidget.setText( 0, taskName )
            itemWidget.setText( 3, taskPath )
            
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

            numTasks = 0

            unitDirs  = []
            unitFiles = []

            for root, dirs, names in os.walk( serverFullPath ):
                for directory in dirs:
                    unitDirs.append( root[len(serverPath):] + '/' + directory )
                for name in [ name for name in names if os.path.splitext( name )[-1] != '.' + Models.ControlBase.editorInfoExtension]:
                    unitFiles.append( root[len(serverPath):] + '/' + name )
                break
            
            for root, dirs, names in os.walk( localFullPath ):
                for directory in dirs:
                    unitDirs.append( root[len(localPath):] + '/' + directory )
                for name in [ name for name in names if os.path.splitext( name )[-1] != '.' + Models.ControlBase.editorInfoExtension ]:
                    unitFiles.append( root[len(localPath):] + '/' + name )
                break

            unitDirs  = list( set( unitDirs ) )
            unitFiles = list( set( unitFiles ) )

            unitDirs.sort()
            unitFiles.sort()

            for unitDir in unitDirs:
                newItem = QTreeWidgetItem( expandedItem )
                newItem.taskPath = expandedItem.taskPath
                newItem.unitPath = unitDir[ len( expandedItem.taskPath ): ]
                emptyChild = QTreeWidgetItem( newItem )
                newItem.setText( 0, unitDir.split( '/' )[-1] )
                newItem.setText( 3, unitDir )
                numTasks += 1
                
            for unitFile in unitFiles:
                newItem = QTreeWidgetItem( expandedItem )
                newItem.taskPath = expandedItem.taskPath
                newItem.unitPath = unitFile[ len( expandedItem.taskPath ): ]
                newItem.setText( 0, unitFile.split( '/' )[-1] )
                newItem.setText( 3, unitFile )
                
                serverUnitFile = serverPath + unitFile
                localUnitFile  = localPath  + unitFile
                
                targetTime = None
                if os.path.exists( serverUnitFile ) and os.path.exists( localUnitFile ):
                    serverTime = Models.FileTime( serverUnitFile )
                    localTime  = Models.FileTime( localUnitFile )
                    targetTime = serverTime if serverTime > localTime else localTime
                elif os.path.exists( serverUnitFile ) and not os.path.exists( localUnitFile ):
                    targetTime = Models.FileTime( serverUnitFile )
                elif os.path.exists( localUnitFile ):
                    targetTime = Models.FileTime( localUnitFile )
                if targetTime:
                    newItem.setText( 1, targetTime.getStrFromMTime( targetTime.mtime() ) + " "*3 )
                
                numTasks += 1
        else:
            QTreeWidgetItem( expandedItem )

        treeWidget = expandedItem.treeWidget()

        TreeWidgetCmds.setTreeItemsCondition( treeWidget )


    @staticmethod
    def updateFamily():

        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return None
        selItems[0].setSelected( False )
        TreeWidgetCmds.updateTaskHierarchy( selItems[0].parent() )
    
    
    @staticmethod
    def selectPath( inputPath, treeWidget ):
        
        path = FileControl.getArrangedPathString( inputPath )
        serverProjectPath = FileControl.getArrangedPathString( FileControl.getCurrentServerProjectPath() )
        localProjectPath  = FileControl.getArrangedPathString( FileControl.getCurrentLocalProjectPath() )
        
        if path.find( serverProjectPath ) == -1 and path.find( localProjectPath ) == -1: return None
        
        basePath = localProjectPath if FileControl.hasPath( path, localProjectPath ) else serverProjectPath
        
        resultItem = None
        for i in range( treeWidget.topLevelItemCount() ):
            resultItem = treeWidget.topLevelItem( i )
            resultPath = basePath + resultItem.taskPath + resultItem.unitPath
            
            if not FileControl.hasPath( path, resultPath ): continue
            
            whileCount = 0
            while len( resultPath ) < len( path ):
                treeWidget.expandItem( resultItem )
                TreeWidgetCmds.updateTaskHierarchy( resultItem )
                
                for j in range( resultItem.childCount() ):
                    childItem = resultItem.child( j )
                    resultPath = basePath + childItem.taskPath + childItem.unitPath
                    if not FileControl.hasPath( path, resultPath ): continue
                    resultItem = childItem
                    break
                whileCount += 1
                if whileCount > 10: break
            if resultPath == path: break
            
        resultItem.setSelected( True ) 
        
        
    




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
        return True
        


    @staticmethod
    def isEnableFileDownload( serverPath ):
        if not os.path.exists( serverPath ): return False
        if os.path.isdir( serverPath ): return False
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
    
    
    @staticmethod
    def isEnableBackup( targetPath ):
        
        if not os.path.exists(targetPath): return False
        return True
    
    
    @staticmethod
    def isEnableDownloadHierarchy( targetPath ):
        if not os.path.isdir( targetPath ): return False
        return True
        




class ProjectControl:


    @staticmethod
    def getAllProjectNames():
        
        FileControl.makeFile( Models.ControlBase.projectListPath )
        f = open( Models.ControlBase.projectListPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        return data.keys()
    


    @staticmethod
    def getCurrentProjectName():
    
        FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        try:currentProject = data[Models.ControlBase.labelCurrentProject]
        except:return
        return currentProject
    
    
    
    @staticmethod
    def setCurrentProjectName( projectName ):
        
        FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        if not data: data = {}
        data[ Models.ControlBase.labelCurrentProject ] = projectName
        f = open( Models.ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f )
        f.close()

    
    
    @staticmethod
    def getProjectListData():
        
        FileControl.makeFile( Models.ControlBase.projectListPath )
        f = open( Models.ControlBase.projectListPath, 'r' )
        try: data = json.load( f )
        except: data = {}
        f.close()
        return data



    @staticmethod
    def setProjectListData( data ):
        
        FileControl.makeFile( Models.ControlBase.projectListPath )
        f = open( Models.ControlBase.projectListPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()
    


    @staticmethod
    def renameProject( targetProjectName, editedProjectName ):
        
        FileControl.makeFile( Models.ControlBase.projectListPath )
        f = open( Models.ControlBase.projectListPath, 'r' )
        data = json.load( f )
        f.close()
        
        cuProjectData = data[targetProjectName]
        del data[targetProjectName]
        data[editedProjectName] = cuProjectData
        
        f = open( Models.ControlBase.projectListPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()
        
        currentProjectName = ProjectControl.getCurrentProjectName()
        Models.ControlBase.mainui.updateProjectList( currentProjectName )


    
    @staticmethod
    def resetServerPath():

        resultPath = FileControl.getFolderFromBrowser( Models.ControlBase.mainui, FileControl.getDefaultProjectFolder() )
        if not os.path.exists( resultPath ): return
        
        cuProject = ProjectControl.getCurrentProjectName()
        data = ProjectControl.getProjectListData()
        projectData = data[cuProject]
        if projectData.has_key( Models.ControlBase.labelServerPath ):
            projectData[Models.ControlBase.labelServerPath] = resultPath
            ProjectControl.setProjectListData( data )
            Models.ControlBase.mainui.loadProject()
        
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        data[Models.ControlBase.labelDefaultServerPath] = '/'.join( resultPath.split( '/' )[:-1] )
        f = open( Models.ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()



    @staticmethod
    def resetLocalPath():

        resultPath = FileControl.getFolderFromBrowser( Models.ControlBase.mainui, FileControl.getDefaultLocalFolder() )
        if not os.path.exists( resultPath ): return
        
        cuProject = ProjectControl.getCurrentProjectName()
        data = ProjectControl.getProjectListData()
        projectData = data[cuProject]
        if projectData.has_key( Models.ControlBase.labelLocalPath ):
            projectData[Models.ControlBase.labelLocalPath] = resultPath
            ProjectControl.setProjectListData( data )
            Models.ControlBase.mainui.loadProject()
        
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        data[Models.ControlBase.labelDefaultLocalPath] = '/'.join( resultPath.split( '/' )[:-1] )
        f = open( Models.ControlBase.defaultInfoPath, 'w' )
        json.dump( data, f, indent=2 )
        f.close()





class FileControl:
    
    
    @staticmethod
    def hasPath( inputBasePath, inputTargetPath ):
        
        basePath = inputBasePath.replace( '\\', '/' )
        targetPath = inputTargetPath.replace( '\\', '/' )
        
        baseSplits   = basePath.split( '/' )
        targetSplits = targetPath.split( '/' )
        
        if len( targetSplits ) > len( baseSplits ): return False
        
        for i in range( len( targetSplits ) ):
            if targetSplits[i].lower() != baseSplits[i].lower(): return False
        
        return True
        
        
    
    
    @staticmethod
    def isMayaFile( targetPath ):
        
        extension = os.path.splitext( targetPath )[-1]
        if not extension in ['.mb', '.ma', '.fbx', '.obj']: 
            return False
        return True
    

    @staticmethod
    def getArrangedPathString( path ):
        try:return path[:2] + path[2:].replace( '\\', '/' ).replace( '//', '/' ).replace( '//', '/' )
        except:return ""



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
        
        dialog = QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        fileName = dialog.getOpenFileName()[0]
        return fileName.replace( '\\', '/' )
    
    
    
    @staticmethod
    def getFolderFromBrowser( parent, defaultPath = '' ):
        
        dialog = QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        choosedFolder = dialog.getExistingDirectory()
        return choosedFolder.replace( '\\', '/' )



    @staticmethod
    def getDefaultProjectFolder():
        
        FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data.has_key( Models.ControlBase.labelDefaultServerPath ): return None
        if os.path.exists( data[ Models.ControlBase.labelDefaultServerPath ] ): return data[Models.ControlBase.labelDefaultServerPath].replace( '\\', '/' )
        else: return ''



    @staticmethod
    def getDefaultLocalFolder():
        
        FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        if not data.has_key( Models.ControlBase.labelDefaultLocalPath ): return None
        if os.path.exists( data[Models.ControlBase.labelDefaultLocalPath] ): return data[Models.ControlBase.labelDefaultLocalPath].replace( '\\', '/' )
        else: return ''
    
    

    @staticmethod
    def getCurrentServerProjectPath():
        
        cuProject = ProjectControl.getCurrentProjectName()
        projectListData = ProjectControl.getProjectListData()
        if not cuProject: return None
        if not projectListData[cuProject]: return None
        try:
            return projectListData[cuProject][Models.ControlBase.labelServerPath]
        except:
            FileControl.makeFile( Models.ControlBase.projectListPath )
            f = open( Models.ControlBase.projectListPath, 'r' )
            try:data = json.load( f )
            except:data = None
            f.close()
            try:
                if not data: return
                data.pop( cuProject )
                f = open( Models.ControlBase.projectListPath, 'w' )
                json.dump( data, f, indent=2 )
                f.close()
                try:Models.ControlBase.mainui.updateProjectList()
                except:pass
            except:
                pass
    


    @staticmethod
    def getCurrentLocalProjectPath():
        
        cuProject = ProjectControl.getCurrentProjectName()
        projectListData = ProjectControl.getProjectListData()
        if not cuProject: return None
        if not projectListData[cuProject]: return None
        return projectListData[cuProject][Models.ControlBase.labelLocalPath]



    @staticmethod
    def getDefaultTaskFolder():
        
        FileControl.makeFile( Models.ControlBase.defaultInfoPath )
        f = open( Models.ControlBase.defaultInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        currentServerPath = FileControl.getCurrentServerProjectPath()
        if not data.has_key( Models.ControlBase.labelDefaultTaskFolder ):
            data[Models.ControlBase.labelDefaultTaskFolder] = ''
        
        if os.path.exists( data[Models.ControlBase.labelDefaultTaskFolder] ):
            if data[Models.ControlBase.labelDefaultTaskFolder].find( currentServerPath ) != -1:
                return data[Models.ControlBase.labelDefaultTaskFolder].replace( '\\', '/' )
        return FileControl.getCurrentServerProjectPath()
    
    
    
    @staticmethod
    def getBackupPath( filePath, timeTarget = None ):
        
        if not timeTarget: timeTarget = filePath
        
        filename = ntpath.split( filePath )[-1]
        stringtime = Models.FileTime( timeTarget ).stringTime()
        dirpath = os.path.dirname( filePath ) + '/' + Models.ControlBase.backupDirName + '/' + filename + '/' + stringtime
        FileControl.makeFolder( dirpath )
        return dirpath + '/' + filename
    
    
    @staticmethod
    def isBackupFile( filePath ):
        return Models.ControlBase.backupDirName in FileControl.getArrangedPathString( filePath ).split( '/' )
    
    
    
    @staticmethod
    def isEditorInfoFile( filePath ):
        return os.path.splitext( filePath )[-1] == '.' + Models.ControlBase.editorInfoExtension
    
    
    @staticmethod
    def downloadFile( srcFullPath, dstFullPath ):
        
        import shutil
        FileControl.makeFolder( os.path.dirname( dstFullPath ) )
        if os.path.exists( dstFullPath ):
            shutil.copy2( dstFullPath, FileControl.getBackupPath( dstFullPath ) )
        shutil.copy2( srcFullPath, dstFullPath )
        shutil.copy2( srcFullPath, FileControl.getBackupPath( dstFullPath, srcFullPath ) )
    


    @staticmethod
    def uploadFile( srcFullPath, dstFullPath ):
        
        import shutil
        import ntpath
        
        srcFolder, srcName = ntpath.split( srcFullPath )
        dstFolder, dstName = ntpath.split( dstFullPath ) 
        
        FileControl.makeFolder( os.path.dirname( dstFullPath ) )
        if os.path.exists( dstFullPath ):
            shutil.copy2( dstFullPath, FileControl.getBackupPath( srcFullPath, dstFullPath ) )
        shutil.copy2( srcFullPath, dstFullPath )
        shutil.copy2( srcFullPath, FileControl.getBackupPath( srcFullPath ) )
    

    
    @staticmethod
    def loadFile( fullPath ):
        
        from maya import mel
        extension = os.path.splitext( fullPath )[-1]
        try:
            if extension == '.mb':
                mel.eval( 'file -f -options "v=0;p=17;f=0"  -ignoreVersion  -typ "mayaBinary" -o "%s";' % fullPath )
                mel.eval( 'addRecentFile("%s", "mayaBinary");' % fullPath )
            elif extension == ".ma":
                mel.eval( 'file -f -options "v=0;p=17;f=0"  -ignoreVersion  -typ "mayaAscii" -o "%s";' % fullPath )
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
        
        compairResult = Models.CompairTwoPath( serverPath, localPath ).getCompairResult()
        
        if compairResult == Models.CompairTwoPath.baseOnly or\
           compairResult == Models.CompairTwoPath.baseIsNew:
            return True
        
        return False
        
    
    




class EditorCmds:
    
    
    @staticmethod
    def getEditorInfoFromFile( filePath ):
        
        if not os.path.exists( filePath ):
            return Models.EditorInfo(filePath)
        
        import ntpath
        filename = ntpath.split( filePath )[-1]
        editorInfoPath = Models.EditorInfo.getEditorInfoPath( filePath )
        FileControl.makeFile( editorInfoPath )
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 0)
        f = open( editorInfoPath, 'r' )
        data = json.load( f )
        f.close()
        newInstance = Models.EditorInfo(filePath)
        if data.has_key( filename ):
            newInstance.setDict( data[filename] )
        else:
            data[filename] = Models.EditorInfo.getMyInfo(filePath).getDict()
            newInstance.setDict( data[filename] )
            f = open( editorInfoPath, 'w' )
            json.dump( data, f, indent=2 )
            f.close()
        return newInstance
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 2)


    @staticmethod
    def setEditorInfoToFile( editorInfo, filePath ):
        
        import ntpath
        fileName = ntpath.split( filePath )[-1]
        editorInfoPath = Models.EditorInfo.getEditorInfoPath( filePath )
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
        return Models.EditorInfo.getMyInfo(localPath)



    @staticmethod
    def fixEditorInfo( filePath ):
        
        if os.path.isfile(filePath):
            dirpath = os.path.dirname( filePath )
        else:
            dirpath = filePath
        
        editorInfoPath = Models.EditorInfo.getEditorInfoPath( filePath )
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 0)
        
        data = {}
        if not os.path.exists( editorInfoPath ):
            for root, dirs, names in os.walk( dirpath ):
                for name in names:
                    if os.path.splitext( name )[-1] == '.' + Models.ControlBase.editorInfoExtension: continue
                    data[ name ] = Models.EditorInfo( root + '/' + name ).getDict()
                break
        else:
            f = open( editorInfoPath, 'r' )
            data = json.load( f )
            f.close()
            
            for root, dirs, names in os.walk( dirpath ):
                for name in names:
                    if os.path.splitext( name )[-1] == '.' + Models.ControlBase.editorInfoExtension: continue
                    if data.has_key( name ):
                        data[ name ][ 'mtime' ] = Models.FileTime( root + '/' + name ).mtime()
                    else:
                        data[ name ] = Models.EditorInfo( root + '/' + name ).getDict()
                break
            
            f = open( editorInfoPath, 'w' )
            json.dump( data, f, indent=2 )
            f.close()
        #ctypes.windll.kernel32.SetFileAttributesW(editorInfoPath, 2)




class SceneControl:
    
    @staticmethod
    def getNeedDownloadTextureFileList( serverUnit, localUnit ):
        
        def afterCmds():
            for fileNode in pymel.core.ls( type='file' ):
                try:mel.eval( "AEfileTextureReloadCmd %s" % fileNode.fileTextureName.name() )
                except:pass
        
        import pymel.core
        from maya import mel
        from functools import partial
        
        nodeAndAttrList = [('file', 'fileTextureName'), ('mesh', 'miProxyFile'),
                           ('RedshiftProxyMesh','fileName'), ('gpuCache','cacheFileName')]
        
        nodeAndElsePathsList = []
        for nodeType, attr in nodeAndAttrList:
            targetNodes = pymel.core.ls( type=nodeType )
            
            serverProjectPath = serverUnit.projectPath
            localProjectPath  = FileControl.getArrangedPathString( localUnit.projectPath )
            
            elsePaths = []
            for targetNode in targetNodes:
                if not pymel.core.attributeQuery( attr, node=targetNode, ex=1 ): continue
                textureLocalPath  = FileControl.getArrangedPathString( targetNode.attr( attr ).get() )
                if textureLocalPath.lower().find( localProjectPath.lower() ) != -1:
                    textureServerPath = serverProjectPath + textureLocalPath[len(localProjectPath):]
                else:
                    continue
                if not os.path.exists( textureServerPath ): continue
                else:
                    pass
                    print nodeType, textureServerPath
                
                if FileControl.isUpdateRequired( textureServerPath, textureLocalPath ):
                    elsePaths.append( textureLocalPath[ len( localProjectPath ): ] )
            
            if elsePaths:
                nodeAndElsePathsList.append( [nodeType, elsePaths] )

        if nodeAndElsePathsList:
            ui_updateFileList = Dialog_downloadFileList( Models.ControlBase.mayawin )
            ui_updateFileList.setServerPath( serverProjectPath )
            ui_updateFileList.setLocalPath( localProjectPath )
            ui_updateFileList.addDownloadCmd(afterCmds)
            for nodeType, elsePaths in nodeAndElsePathsList:
                for elsePath in elsePaths:
                    ui_updateFileList.appendFilePath( elsePath, nodeType )
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
            ui_updateFileList = Dialog_downloadFileList( Models.ControlBase.mayawin )
            ui_updateFileList.setServerPath( serverProjectPath )
            ui_updateFileList.setLocalPath( localProjectPath )
            for elsePath in elsePaths:
                ui_updateFileList.appendFilePath( elsePath, "reference" )
            ui_updateFileList.updateUI()
            ui_updateFileList.addDownloadCmd( afterCmd )
            ui_updateFileList.show()
        else:
            afterCmd()





class ContextMenuCmds:
    

    @staticmethod
    def loadFile_local():
        
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]

        serverUnitInst = Models.FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )
        localUnitInst  = Models.FileUnit( FileControl.getCurrentLocalProjectPath(), selItem.taskPath, selItem.unitPath )
        
        serverFullPath = serverUnitInst.fullPath()
        localFullPath  = localUnitInst.fullPath()
        
        isMayaFile = True
        for path in [serverFullPath, localFullPath]:
            if not os.path.exists( path ): continue
            if not FileControl.isMayaFile( path ): isMayaFile = False

        if isMayaFile and cmds.file( modified=1, q=1 ):
            txSaveAndOpen = '저장하고 열기'.decode( 'utf-8' )
            txJustOpen = '그냥열기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            confirmResult = cmds.confirmDialog( title='Confirm', message='씬이 저장되지 않았습니다. 그대로 진행할까요?'.decode( 'utf-8' ), 
                                                button=[txSaveAndOpen,txJustOpen,txCancel], 
                                                defaultButton=txCancel, parent= Models.ControlBase.mainui.objectName )
            if confirmResult == txSaveAndOpen:
                cmds.file( save=1 )
            elif confirmResult == txCancel:
                return
        
        if not os.path.exists( serverFullPath ) and os.path.exists( localFullPath ):
            pass
        elif os.path.exists( serverFullPath ) and not os.path.exists( localFullPath ):
            serverEditor = EditorCmds.getEditorInfoFromFile( serverFullPath )
            FileControl.downloadFile( serverFullPath, localFullPath )
            EditorCmds.setEditorInfoToFile( serverEditor, localFullPath )
            EditorCmds.setEditorInfoToFile( serverEditor, serverFullPath )
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
                                                        parent= Models.ControlBase.mainui.objectName )
                    if confirmResult == txDownload:
                        FileControl.downloadFile( serverFullPath, localFullPath )
                        EditorCmds.setEditorInfo( serverEditor, localFullPath )
            else:
                pass
        
        def afterCmd():
            if isMayaFile:
                FileControl.loadFile( localFullPath )
                SceneControl.getNeedDownloadTextureFileList( serverUnitInst, localUnitInst )
                TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )
            else:
                os.startfile( localFullPath )
                TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )
        
        SceneControl.getNeedDownloadReferenceFileList( serverUnitInst, localUnitInst, afterCmd )
        TreeWidgetCmds.updateFamily()
        TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )
        

    
    @staticmethod
    def reference():
        
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]

        serverUnitInst = Models.FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )
        localUnitInst  = Models.FileUnit( FileControl.getCurrentLocalProjectPath(), selItem.taskPath, selItem.unitPath )

        if cmds.file( modified=1, q=1 ):
            txSaveAndOpen = '저장하고 불러오기'.decode( 'utf-8' )
            txJustOpen = '그냥 불러오기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            confirmResult = cmds.confirmDialog( title='Confirm', message='레퍼런스를 불러오기 전에 씬을 저장하시겠습니까?'.decode( 'utf-8' ), 
                                                button=[txSaveAndOpen,txJustOpen,txCancel], 
                                                defaultButton=txCancel, parent= Models.ControlBase.mainui.objectName )
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
        TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )
    
    
    
    @staticmethod
    def backup():
        
        import shutil
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return None
        selItem  = selItems[0]
    
        localUnitInst = Models.FileUnit( FileControl.getCurrentLocalProjectPath(), selItem.taskPath, selItem.unitPath )
        if not os.path.exists( localUnitInst.fullPath() ): return None
        
        backupPath = FileControl.getBackupPath( localUnitInst.fullPath() )
        txBackup = '백업'.decode( 'utf-8' )
        txCancel = '취소'.decode( 'utf-8' )
        confirmResult = cmds.confirmDialog( title='백업'.decode( 'utf-8' ), message="%s\n위 경로로 백업을 진행하시겠습니까?".decode( 'utf-8' ) % backupPath, 
                                            button=[txBackup,txCancel], 
                                            parent= Models.ControlBase.mainui.objectName )
        if confirmResult == txBackup:
            FileControl.makeFolder( os.path.dirname( backupPath ) )
            shutil.copy2( localUnitInst.fullPath(), backupPath )
            cmds.confirmDialog( title = "백업완료".decode( 'utf-8' ), message="백업이 완료되었습니다.".decode( 'utf-8'),
                                button = ['확인'.decode( 'utf-8') ],
                                parent = Models.ControlBase.mainui.objectName )
        else:
            return None
            
        
    
    
    @staticmethod
    def exportReferenceInfo():
        
        pass


    @staticmethod
    def loadFile_server():
        
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        if not selItems: return
        selItem  = selItems[0]
        
        serverUnitInst = Models.FileUnit( FileControl.getCurrentServerProjectPath(), selItem.taskPath, selItem.unitPath )

        if cmds.file( modified=1, q=1 ):
            txSaveAndOpen = '저장하고 열기'.decode( 'utf-8' )
            txJustOpen = '그냥열기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            confirmResult = cmds.confirmDialog( title='Confirm', message='씬이 저장되지 않았습니다. 그대로 진행할까요?'.decode( 'utf-8' ),
                                                button=[txSaveAndOpen,txJustOpen,txCancel],
                                                defaultButton=txCancel, parent= Models.ControlBase.mainui.objectName )
            if confirmResult == txSaveAndOpen:
                cmds.file( save=1 )
            elif confirmResult == txCancel:
                return
        
        FileControl.loadFile( serverUnitInst.fullPath() )
        TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )



    @staticmethod
    def openFileBrowser_server():
    
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        cuServerUnitPath = FileControl.getCurrentServerProjectPath() + selItems[0].taskPath + selItems[0].unitPath

        if os.path.isfile( cuServerUnitPath ):
            targetDir = os.path.dirname( cuServerUnitPath )
        else:
            targetDir = cuServerUnitPath
            
        if not os.path.exists( targetDir ):
            cmds.confirmDialog( title='Confirm', message='해댱 폴더가 존재하지 않습니다.'.decode( 'utf-8' ),
                                                        button=["확인".decode('utf-8')], parent= Models.ControlBase.mainui.objectName )
            return
            
        import subprocess
        subprocess.call( 'explorer /object, "%s"' % targetDir.replace( '/', '\\' ).encode( 'cp949' ) )



    @staticmethod
    def openFileBrowser_local():

        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
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
                                                        button=["확인".decode('utf-8')], parent= Models.ControlBase.mainui.objectName )
            return
        
        import subprocess
        subprocess.call( 'explorer /object, "%s"' % targetDir.replace( '/', '\\' ).encode( 'cp949' ) )

    
    
    @staticmethod
    def download():
        
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        serverUnit = Models.FileUnit( FileControl.getCurrentServerProjectPath(), selItems[0].taskPath, selItems[0].unitPath )
        localUnit  = Models.FileUnit( FileControl.getCurrentLocalProjectPath(),  selItems[0].taskPath, selItems[0].unitPath )
        
        if os.path.isfile( serverUnit.fullPath() ):
            txDownload = '덮어 씌우기'.decode( 'utf-8' )
            txCancel = '취소'.decode( 'utf-8' )
            
            if not os.path.exists( localUnit.fullPath() ):
                serverEditorInfo = EditorCmds.getEditorInfoFromFile( serverUnit.fullPath() )
                FileControl.downloadFile( serverUnit.fullPath(), localUnit.fullPath() )
                EditorCmds.setEditorInfoToFile( serverEditorInfo, localUnit.fullPath() )
                EditorCmds.setEditorInfoToFile( serverEditorInfo, serverUnit.fullPath() )
            else:
                recentEditor = EditorCmds.getEditorInfoFromFile( serverUnit.fullPath() )
                myEditor     = EditorCmds.getEditorInfoFromFile( localUnit.fullPath() )
                
                serverFileTime = Models.FileTime( serverUnit.fullPath() )
                localFileTime  = Models.FileTime( localUnit.fullPath() )

                if recentEditor == myEditor:
                    confirmResult = txDownload
                else:
                    hostAddString = ""
                    if recentEditor.host:
                        hostAddString = "%s에 의해 ".decode( 'utf-8' ) % recentEditor.host
                    
                    localIsRecentString= ""
                    if serverFileTime < localFileTime:
                        localIsRecentString += "( 경고 : 로컬이 더 최신입니다. )".decode("utf-8")
                    
                    filename = ntpath.split( localUnit.fullPath() )[-1]
                    confirmResult = cmds.confirmDialog( title='Confirm', 
                                                        message='%s는\n%s%s 에 변경된 파일입니다.\n로컬에 덮어씌울까요?%s'.decode( 'utf-8' ) % (filename, 
                                                                                                                                hostAddString, Models.FileTime.getStrFromMTime( recentEditor.mtime ),
                                                                                                                                localIsRecentString ),
                                                        button=[txDownload,txCancel],
                                                        defaultButton=txCancel, parent = Models.ControlBase.mainui.objectName )

                if confirmResult == txDownload:
                    FileControl.downloadFile( serverUnit.fullPath(), localUnit.fullPath() )
                    EditorCmds.setEditorInfoToFile( recentEditor, serverUnit.fullPath() )
                    EditorCmds.setEditorInfoToFile( recentEditor, localUnit.fullPath() )
        elif os.path.isdir( serverUnit.fullPath() ):
            EditorCmds.fixEditorInfo( localUnit.fullPath()  )
            EditorCmds.fixEditorInfo( serverUnit.fullPath() )
            targetPaths = []
            for root, dirs, names in os.walk( localUnit.fullPath() ):
                for name in names:
                    targetPath = FileControl.getArrangedPathString( root + '/' + name )[ len( localUnit.projectPath ): ]
                    if FileControl.isBackupFile( targetPath ): continue
                    if FileControl.isEditorInfoFile( targetPath ): continue
                    serverEditorInfo = EditorCmds.getEditorInfoFromFile( serverUnit.projectPath + targetPath )
                    localEditorInfo  = EditorCmds.getEditorInfoFromFile( localUnit.projectPath  + targetPath )
                    if serverEditorInfo <= localEditorInfo: continue
                    targetPaths.append( targetPath )
            
            confirmResult = cmds.confirmDialog( title='Confirm',
                                                message='%s는\n%s%s 에 변경된 파일입니다.\n로컬에 덮어씌울까요?%s'.decode( 'utf-8' ) % (filename, 
                                                                                                                        hostAddString, Models.FileTime.getStrFromMTime( recentEditor.mtime ),
                                                                                                                        localIsRecentString ),
                                                button=[txDownload,txCancel],
                                                defaultButton=txCancel, parent = Models.ControlBase.mainui.objectName )
            
            ui_downloadFileList = Dialog_downloadFileList( Models.ControlBase.mayawin )
            ui_downloadFileList.setServerPath( serverUnit.projectPath )
            ui_downloadFileList.setLocalPath( localUnit.projectPath )
            for targetPath in targetPaths:
                ui_downloadFileList.appendFilePath( targetPath, "paths" )
            ui_downloadFileList.updateUI()
            ui_downloadFileList.show()
        
        TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )
        
    
    
    @staticmethod
    def downloadHierarchy( extensionList = [] ):
        
        selItems = Models.ControlBase.uiTreeWidget.selectedItems()
        serverUnit = Models.FileUnit( FileControl.getCurrentServerProjectPath(), selItems[0].taskPath, selItems[0].unitPath )
        localUnit  = Models.FileUnit( FileControl.getCurrentLocalProjectPath(),  selItems[0].taskPath, selItems[0].unitPath )
        
        serverPath = serverUnit.fullPath()
        localPath  = localUnit.fullPath()
        
        FileControl.makeFolder( localPath )
        
        copyList = []
        for root, dirs, names in os.walk( serverPath ):
            for name in names:
                extension = os.path.splitext( name )[-1]
                if extensionList and not extension in extensionList: continue
                serverFullPath = ( root + '\\' + name ).replace( '\\', '/' )
                copyList.append( [serverFullPath[ len( serverUnit.projectPath ): ], extension] )
        
        ui_updateFileList = Dialog_downloadFileList( Models.ControlBase.mayawin )
        ui_updateFileList.setServerPath( serverUnit.projectPath )
        ui_updateFileList.setLocalPath( localUnit.projectPath )
        for serverElsePath, extension in copyList:
            ui_updateFileList.appendFilePath( serverElsePath, extension )
        ui_updateFileList.updateUI()
        ui_updateFileList.show()
    
    
    
    @staticmethod
    def refresh():
        TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )



    @staticmethod
    def upload():
        
        selItems   = Models.ControlBase.uiTreeWidget.selectedItems()
        serverUnit = Models.FileUnit( FileControl.getCurrentServerProjectPath(), selItems[0].taskPath, selItems[0].unitPath )
        localUnit  = Models.FileUnit( FileControl.getCurrentLocalProjectPath(),  selItems[0].taskPath, selItems[0].unitPath )
        
        if os.path.isfile( localUnit.fullPath() ):
            scenePath = cmds.file( q=1, sceneName=1 )
            txSave = "저장하기".decode( 'utf-8' )
            txDoNotSave = "저장하기 않고 업로드".decode( "utf-8" )
            txCancel = "취소".decode( 'utf-8' )
            if os.path.normpath( scenePath ) == os.path.normpath( localUnit.fullPath() ) and cmds.file( q=1, amf=1 ):
                confirmResult = cmds.confirmDialog( title='Confirm', message='업로드하기전에 Scene을 저장하시겠습니까?'.decode( 'utf-8' ),
                                                        button=[txSave,txDoNotSave,txCancel],
                                                        defaultButton=txCancel, parent= Models.ControlBase.mainui.objectName )
                if confirmResult == txCancel:
                    return
                elif confirmResult == txSave:
                    cmds.file( save=1, f=1 )
                else:
                    pass
            
            if not os.path.exists( serverUnit.fullPath() ):
                myEditor = EditorCmds.getMyEditorInfo( localUnit.fullPath() )
                FileControl.uploadFile( localUnit.fullPath(), serverUnit.fullPath() )
                EditorCmds.setEditorInfoToFile( myEditor, localUnit.fullPath() )
                EditorCmds.setEditorInfoToFile( myEditor, serverUnit.fullPath() )
            else:
                txUpload = '덮어 씌우기'.decode( 'utf-8' )
                txCancel = '취소'.decode( 'utf-8' )
                
                recentEditor = EditorCmds.getEditorInfoFromFile( serverUnit.fullPath() )
                myEditor     = EditorCmds.getMyEditorInfo( localUnit.fullPath() )
                if recentEditor == myEditor:
                    confirmResult = txUpload
                else:
                    serverFileTime = Models.FileTime( serverUnit.fullPath() )
                    localFileTime  = Models.FileTime( localUnit.fullPath() )
                    
                    hostAddString = ""
                    if recentEditor.host:
                        hostAddString = "%s에 의해 ".decode( 'utf-8' ) % recentEditor.host
                    
                    localIsRecentString= ""
                    if serverFileTime > localFileTime:
                        localIsRecentString += "( 경고 : 서버가 더 최신입니다. )".decode("utf-8")
                    
                    filename = ntpath.split( localUnit.fullPath() )[-1]
                    confirmResult = cmds.confirmDialog( title='Confirm', message='%s는\n%s%s 에 변경된 파일입니다.\n서버에 덮어씌울까요?%s'.decode( 'utf-8' ) % (filename, 
                                                                                                                                hostAddString, Models.FileTime.getStrFromMTime( recentEditor.mtime ),
                                                                                                                                localIsRecentString ),
                                                        button=[txUpload,txCancel],
                                                        defaultButton=txCancel, parent= Models.ControlBase.mainui.objectName )

                if confirmResult == txUpload:
                    FileControl.uploadFile( localUnit.fullPath(), serverUnit.fullPath() )
                    EditorCmds.setEditorInfoToFile( myEditor, serverUnit.fullPath() )
                    EditorCmds.setEditorInfoToFile( myEditor, localUnit.fullPath() )

        elif os.path.isdir( localUnit.fullPath() ):
            
            scenePath = cmds.file( q=1, sceneName=1 )
            txSave = "저장하고 업로드".decode( 'utf-8' )
            txDoNotSave = "저장하기 않고 업로드".decode( "utf-8" )
            txCancel = "취소".decode( 'utf-8' )
            
            for root, dirs, names in os.walk( localUnit.fullPath() ):
                for name in names:
                    targetPath = root + '/' + name
                    
                    if os.path.normpath( scenePath ) == os.path.normpath( targetPath ) and cmds.file( q=1, amf=1 ):
                        confirmResult = cmds.confirmDialog( title='Confirm', message='업로드할 파일들 중 현제 Scene이 존재합니다.\n업로드하기전에 Scene을 저장하시겠습니까?'.decode( 'utf-8' ),
                                                                button=[txSave,txDoNotSave,txCancel],
                                                                defaultButton=txCancel, parent= Models.ControlBase.mainui.objectName )
                        if confirmResult == txCancel:
                            return
                        elif confirmResult == txSave:
                            cmds.file( save=1, f=1 )
                        else:
                            pass
                        break
            
            EditorCmds.fixEditorInfo( localUnit.fullPath() )
            EditorCmds.fixEditorInfo( serverUnit.fullPath() )
            targetPaths = []
            
            for root, dirs, names in os.walk( localUnit.fullPath() ):
                for name in names:
                    targetPath = FileControl.getArrangedPathString( root + '/' + name )[ len( localUnit.projectPath ): ]
                    if FileControl.isBackupFile( targetPath ): continue
                    if FileControl.isEditorInfoFile( targetPath ): continue
                    serverEditorInfo = EditorCmds.getEditorInfoFromFile( serverUnit.projectPath + targetPath )
                    localEditorInfo  = EditorCmds.getEditorInfoFromFile( localUnit.projectPath  + targetPath )
                    if os.path.normpath( cmds.file( q=1, sceneName=1 ) ) == os.path.normpath( localUnit.projectPath + '/' + targetPath ) and cmds.file( q=1, amf=1 ):
                        targetPaths.append( targetPath )
                        continue
                    elif serverEditorInfo >= localEditorInfo:
                        continue
                    targetPaths.append( targetPath )
            
            if not targetPaths:
                cmds.confirmDialog( title='Notice', message='업로드할 파일이 없습니다.'.decode( 'utf-8' ),
                                    button=["확인".decode( 'utf-8' )], parent= Models.ControlBase.mainui.objectName )
                return

            ui_updateFileList = Dialog_uploadFileList( Models.ControlBase.mayawin )
            ui_updateFileList.setServerPath( serverUnit.projectPath )
            ui_updateFileList.setLocalPath( localUnit.projectPath )
            for targetPath in targetPaths:
                ui_updateFileList.appendFilePath( targetPath )
            ui_updateFileList.updateUI()
            ui_updateFileList.show()

        TreeWidgetCmds.setTreeItemsCondition( Models.ControlBase.uiTreeWidget )

