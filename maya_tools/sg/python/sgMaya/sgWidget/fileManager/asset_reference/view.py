import maya.cmds as cmds
import cmdModel
import uiModel
import os
from functools import partial



class Model:
    targetExtensions = ['mb', 'ma', 'fbx', 'obj']



class SaveCheckUI:
    
    def __init__(self, afterCmd ):
        
        self._winName = uiModel.Info._winName+'_saveCheck'
        self._title   = uiModel.Info._title  +' - Save Check'
        self._width   = uiModel.Info._width
        self._height  = uiModel.Info._height
    
        self._afterCmd = afterCmd
    
        
    def cmdSave(self, *args ):
        
        cmds.deleteUI( self._winName, wnd=1 )
        cmds.file( save=1 )
        self._afterCmd()
        
        
    def cmdDoNotSave(self, *args):
        
        cmds.deleteUI( self._winName, wnd=1 )
        self._afterCmd()
        
        
    def cmdCancel(self, *args):
        
        cmds.deleteUI( self._winName, wnd=1 )
        
    
    def create(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title=self._title )
        
        columnWidth = self._width - 2
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        cmds.text( l='Scene is not saveed !', h=25 )
        cmds.setParent( '..' )
        
        firstWidth = (columnWidth ) / 3.0
        secondWidth = ( columnWidth )/ 3.0
        thirdWidth = ( columnWidth ) - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)])
        cmds.button( l='Save', c=self.cmdSave )
        cmds.button( l='Do not save', c=self.cmdDoNotSave )
        cmds.button( l='Cancel', c=self.cmdCancel )
        cmds.setParent( '..' )
        
        top, left = cmds.window( uiModel.Info._winName, q=1, tlc=1 )
        height  = cmds.window( uiModel.Info._winName, q=1, h=1 )
        
        cmds.showWindow( self._winName )
        
        cmds.window( self._winName, e=1,
                     tlc=[ top+height+37, left ], w = self._width, h = self._height )
        



class ImportAndExportFileUI:
    
    def __init__(self):
        
        self._winName = uiModel.Info._winName
        self._title   = uiModel.Info._title
        self._width   = uiModel.Info._width
        self._height  = uiModel.Info._height
        
        
    def updatePopupMenu( self, textField, popupMenu ):
    
        cmds.popupMenu( popupMenu, e=1, dai=1 )
        cmds.setParent( popupMenu, menu=1 )
        path = cmds.textFieldGrp( textField, q=1, tx=1 )
        
        if not cmdModel.isFile(path) and not cmdModel.isFolder(path): return None
        
        cmds.menuItem( l='Open File Browser', c=partial( cmdModel.openFileBrowser, path ) )
        cmds.menuItem( d=1 )
        
        def backToUpfolder( path, *args ):
            path = path.replace( '\\', '/' )
            path = '/'.join( path.split( '/' )[:-1] )
            cmds.textFieldGrp( textField, e=1, tx=path )
            self.cmdCheckImportPathAndEditButtonCondition()
            self.cmdCheckServerPathAndEditButtonCondition()
            
        if cmdModel.isFile(path) or cmdModel.isFolder(path):
            splitPath = path.replace( '\\', '/' ).split( '/' )
            if splitPath and splitPath[-1] != '':
                cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
        cmds.menuItem( d=1 )
        
        path = path.replace( '\\', '/' )
        if cmdModel.isFile(path):
            path = '/'.join( path.split( '/')[:-1] )
        
        def updateTextField( path, *args ):
            cmds.textFieldGrp( textField, e=1, tx=path )
            self.cmdCheckImportPathAndEditButtonCondition()
            self.cmdCheckServerPathAndEditButtonCondition()
        
        for root, dirs, names in os.walk( path ):
            dirs.sort()
            for dir in dirs:
                cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
            names.sort()
            for name in names:
                extension = name.split( '.' )
                if len( extension ) == 1: continue
                extension = extension[1]
                if not extension.lower() in Model.targetExtensions:continue
                cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )
            break
        
        
        
    def editServerPathFieldFromfile(self):
        
        serverPath = cmdModel.PathToFile.getLastServerPathFromFile()
        cmds.textFieldGrp( self._tf_server, e=1, tx=serverPath )
        

    def cmdCheckImportPathAndEditButtonCondition( self, *args ):

        self.updatePopupMenu( self._tf_import, self._pu_import )
        
        importPathStr = cmds.textFieldGrp( self._tf_import, q=1, tx=1 )
        if cmdModel.isFile( importPathStr ):
            cmds.button( self._bt_import, e=1, en=1 )
        else:
            cmds.button( self._bt_import, e=1, en=0 )
            
        

    def cmdCheckServerPathAndEditButtonCondition( self, *args ):

        self.updatePopupMenu( self._tf_server, self._pu_server )
        
        serverPathStr = cmds.textFieldGrp( self._tf_server, q=1, tx=1 )
        backupPath, backupFileName = cmdModel.getBackupPath(serverPathStr)
        cmds.textField( self._tf_backup, e=1, tx=backupPath )
        
        if cmdModel.isFile( serverPathStr ):
            cmds.button( self._bt_open, e=1, en=1 )
        else:
            cmds.button( self._bt_open, e=1, en=0 )
            
            
    def cmdImport(self, *args ):
        
        importPath = cmds.textFieldGrp( self._tf_import, q=1, tx=1 )
        cmdModel.importFile( importPath )
        cmdModel.PathToFile.setLastImportPathToFile( importPath )
        
    
    def cmdCopyFromServerAndOpen(self, *args ):
        
        def afterCmd():
            serverPath = cmds.textFieldGrp( self._tf_server, q=1, tx=1 )
            serverPath = serverPath.replace( '\\', '/' )
            cmdModel.copyFromServerAndOpen( serverPath )
            cmdModel.PathToFile.setLastServerPathToFile( serverPath )
            scenePath = cmdModel.getCurrentScenePath()
            cmds.textField( self._tf_current, e=1, tx=scenePath )
            backupPath, backupFileName = cmdModel.getBackupPath(serverPath)
            cmds.textField( self._tf_backup, e=1, tx=backupPath )
            
        SaveCheckUI( afterCmd ).create()
    
    
    def cmdSaveAndUpdate(self, *args ):
        
        currentPath = cmds.textField( self._tf_current, q=1, tx=1 )
        serverPath = cmds.textFieldGrp( self._tf_server, q=1, tx=1 )
        cmdModel.saveAndUpdate( currentPath, serverPath )
        self.cmdCheckImportPathAndEditButtonCondition()
        self.cmdCheckServerPathAndEditButtonCondition()
        cmdModel.PathToFile.setLastServerPathToFile( serverPath )
        
        
        
    def setInit(self, *args ):
        
        importPath = cmdModel.PathToFile.getLastImportPathFromFile()
        serverPath = cmdModel.PathToFile.getLastServerPathFromFile()
        currentPath = cmdModel.getCurrentScenePath()
        
        cmds.textFieldGrp( self._tf_import, e=1, tx=importPath )
        cmds.textFieldGrp( self._tf_server, e=1, tx=serverPath )
        cmds.textField( self._tf_current, e=1, tx=currentPath )
        
        
        
    def openFileBrowser(self, textField, *args ):
        
        path = cmds.textField( textField, q=1, tx=1 )
        cmdModel.openFileBrowser( path )
        
        
    
    def create(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title = self._title )

        cmds.columnLayout()
        
        columnWidth = self._width-4
        rowColumnWidth = columnWidth - 2
        textWidth = rowColumnWidth * 0.25
        fieldWidth = rowColumnWidth - textWidth
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        tf_import = cmds.textFieldGrp( l='Import Path : ', cw=[(1,textWidth),(2,fieldWidth)],
                                       cc = self.cmdCheckImportPathAndEditButtonCondition )
        pu_import = cmds.popupMenu()
        cmds.text( l='', h=5 )
        bt_import = cmds.button( l='Import', c=self.cmdImport )
        cmds.setParent( '..' )
        
        cmds.text( l='', h=5 )
        cmds.separator( w=self._width )
        cmds.text( l='', h=5 )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,textWidth),(2,fieldWidth)])
        pu_current = cmds.popupMenu()
        mi_current = cmds.menuItem( l='Open File Browser' )
        cmds.text( l='Current Path :  ', al='right' )
        tf_current = cmds.textField( en=0 )
        cmds.menuItem( mi_current, e=1, c= partial( self.openFileBrowser, tf_current ) )
        cmds.setParent( '..' )
        
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        tf_server = cmds.textFieldGrp( l='Server Path : ',  cw=[(1,textWidth),(2,fieldWidth)],
                                       cc = self.cmdCheckServerPathAndEditButtonCondition )
        pu_server = cmds.popupMenu() 
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,textWidth),(2,fieldWidth)])
        pu_backup = cmds.popupMenu()
        mi_backup = cmds.menuItem( l='Open File Browser' )
        cmds.text( l='Backup Path :  ', al='right' )
        tf_backup = cmds.textField( en=0 )
        cmds.menuItem( mi_backup, e=1, c= partial( self.openFileBrowser, tf_backup ) )
        cmds.setParent( '..' )
        
        cmds.text( l='', h=5 )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        bt_open   = cmds.button( l = 'Copy From Server and Open', 
                                 c = self.cmdCopyFromServerAndOpen )
        bt_update = cmds.button( l='Back up', w=rowColumnWidth, en=1,
                                 c = self.cmdSaveAndUpdate )
        cmds.setParent( '..' )

        cmds.showWindow( self._winName )
        uiTopLeft = cmdModel.getUIPosition( self._width )
        cmds.window( self._winName, e=1,
                     w= self._width, h= self._height )
        
        self._tf_import = tf_import
        self._bt_import = bt_import
        self._tf_server = tf_server
        self._tf_current= tf_current
        self._tf_backup = tf_backup
        self._bt_open   = bt_open
        self._bt_update = bt_update
        self._pu_server = pu_server
        self._pu_import = pu_import
        
        self.setInit()
        self.cmdCheckImportPathAndEditButtonCondition()
        self.cmdCheckServerPathAndEditButtonCondition()