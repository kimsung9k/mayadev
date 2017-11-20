import maya.cmds as cmds
import maya.mel as mel

import uiModel
import cmdModel
import functions.ui as uiFunctions
import functions.path as pathFunctions


class Model:
    targetExtensions = ['mb', 'ma', 'fbx', 'obj']



class SaveCheckUI:
    
    def __init__(self, afterCmd ):
        
        self._winName = uiModel.winName+'_saveCheck'
        self._title   = uiModel.title  +' - Save Check'
        self._width   = uiModel.width
        self._height  = uiModel.height
    
        self._afterCmd = afterCmd
    
        
    def cmdSave(self, *args ):
        
        cmds.deleteUI( self._winName, wnd=1 )
        try:
            cmds.file( save=1 )
            self._afterCmd()
        except: cmds.error( 'Set Scene Name File First !' )
        
        
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
        
        top, left = cmds.window( uiModel.winName, q=1, tlc=1 )
        height  = cmds.window( uiModel.winName, q=1, h=1 )
        
        cmds.showWindow( self._winName )
        
        cmds.window( self._winName, e=1,
                     tlc=[ top+height+37, left ], w = self._width, h = self._height )
        
        
class FileExistsCheckUI:
    
    def __init__(self, afterCmd ):
        
        self._winName = uiModel.winName+'_fileExists'
        self._title   = uiModel.title  +' - File Exists'
        self._width   = uiModel.width
        self._height  = uiModel.height
    
        self._afterCmd = afterCmd
    
        
    def cmdWrite(self, *args ):
        
        cmds.deleteUI( self._winName, wnd=1 )
        try:
            cmds.file( save=1 )
            self._afterCmd()
        except: cmds.error( 'Set Scene Name File First !' )
        
        
    def cmdCancel(self, *args):
        
        cmds.deleteUI( self._winName, wnd=1 )
        
    
    def create(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title=self._title )
        
        columnWidth = self._width - 2
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        cmds.text( l='File aleady exists !', h=25 )
        cmds.setParent( '..' )
        
        firstWidth = (columnWidth ) / 2.0
        secondWidth = ( columnWidth ) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Write', c=self.cmdWrite )
        cmds.button( l='Cancel', c=self.cmdCancel )
        cmds.setParent( '..' )
        
        top, left = cmds.window( uiModel.winName, q=1, tlc=1 )
        height  = cmds.window( uiModel.winName, q=1, h=1 )
        
        cmds.showWindow( self._winName )
        
        cmds.window( self._winName, e=1,
                     tlc=[ top+height+37, left ], w = self._width, h = self._height )


class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdTextFieldChange(self, *args ):
        
        uiFunctions.updatePathPopupMenu( self.tf_targetPath, self.pu_targetPath )
        path = cmds.textFieldGrp( self.tf_targetPath, q=1, tx=1 )
        if pathFunctions.isFile( path ):
            cmds.button( self.bt_open, e=1, en=1 )
            cmds.button( self.bt_openAtLocal, e=1,  en=1 )
            cmds.button( self.bt_import, e=1,  en=1 )
        else:
            cmds.button( self.bt_open, e=1,  en=0 )
            cmds.button( self.bt_openAtLocal, e=1,  en=0 )
            cmds.button( self.bt_import, e=1,  en=0 )
    
    
    def cmdSelectScrollList(self, *args ):
        
        selItems = cmds.textScrollList( self.sl_paths, q=1, si=1 )
        if not selItems: return None
        selItem = selItems[0]
        cmds.textFieldGrp( self.tf_targetPath, e=1, tx= selItem )
        self.cmdTextFieldChange()
    
    
    def cmdOpen(self, *args ):
        
        def cmdMain( *args ):
            path = cmds.textFieldGrp( self.tf_targetPath, q=1, tx=1 )
            if path.endswith( '.mb' ):
                cmds.file( path, f=1, options="v=0;", ignoreVersion=True, esn=False,  typ="mayaBinary", o=1 )
                mel.eval( 'addRecentFile("%s", "mayaBinary")' % path )
            elif path.endswith( '.ma' ):
                cmds.file( path, f=1, options="v=0;", ignoreVersion=True, esn=False,  typ="mayaAscii", o=1 )
                mel.eval( 'addRecentFile("%s", "mayaAscii")' % path )

        SaveCheckUI( cmdMain ).create()
    
    
    def cmdOpenAtLocal(self, *args ):
        
        def cmdMain( *args ):
            path = cmds.textFieldGrp( self.tf_targetPath, q=1, tx=1 )
            cmdModel.copyFromServerAndOpen( path )
        SaveCheckUI( cmdMain ).create()
        
    
    
    def cmdImport(self, *args ):
        
        path = cmds.textFieldGrp( self.tf_targetPath, q=1, tx=1 )
        cmdModel.importFile( path )
    
    
    def cmdSaveAs(self, *args ):
        
        targetPath = cmds.textFieldGrp( self.tf_targetPath, q=1, tx=1 )
        if not pathFunctions.isFile( targetPath ): return None
        def cmdMain( *args ):
            cmds.file( rename=targetPath )
            cmds.file( f=1, save=1, options='v=0', type='mayaBinary' )
        FileExistsCheckUI( cmdMain ).create()
    
    
    def cmdBackup(self, *args ):
        
        targetPath = cmds.textFieldGrp( self.tf_targetPath, q=1, tx=1 )
        currentPath = cmds.file( self.tf_targetPath, q=1, sceneName=1 )
        if not pathFunctions.isFile( currentPath ): return None
        if not pathFunctions.isFile( targetPath ): return None
        def cmdMain( *args ):
            cmdModel.saveAndUpdate( currentPath, targetPath )
        FileExistsCheckUI( cmdMain ).create()
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        columnWidth = self.width-4
        rowColumnWidth = columnWidth - 2
        textWidth = rowColumnWidth * 0.25
        fieldWidth = rowColumnWidth - textWidth
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        tf_targetPath = cmds.textFieldGrp( l='Target Path : ', cw=[(1,textWidth),(2,fieldWidth)], h=25,
                                           cc = self.cmdTextFieldChange )
        pu_targetPath = cmds.popupMenu()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        sl_paths = cmds.textScrollList( sc= self.cmdSelectScrollList )
        cmds.setParent( '..' )
        
        firstWidth = (columnWidth - 2) / 3
        secondWidth = (columnWidth - 2) / 3
        thirdWidth = (columnWidth - 2) - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3,  cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)])
        bt_open = cmds.button( l='Open', en=0, c=self.cmdOpen )
        bt_openAtLocal = cmds.button( l='Open At Local', en=0, c=self.cmdOpenAtLocal )
        bt_import = cmds.button( l='Import', en=0, c=self.cmdImport )
        cmds.setParent( '..' )
        
        firstWidth = (columnWidth - 2) / 2
        secondWidth = (columnWidth - 2) - firstWidth
        cmds.rowColumnLayout( nc=2,  cw=[(1,firstWidth),(2,secondWidth)])
        bt_save = cmds.button( l='Save As', c=self.cmdSaveAs )
        bt_backUp = cmds.button( l='Back Up', c=self.cmdBackup )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.tf_targetPath = tf_targetPath
        self.pu_targetPath = pu_targetPath
        
        self.bt_open = bt_open
        self.bt_openAtLocal = bt_openAtLocal
        self.bt_import = bt_import
        self.bt_save = bt_save
        self.bt_backUp = bt_backUp
        self.sl_paths  = sl_paths
        
        cmdModel.loadScrollList( sl_paths )