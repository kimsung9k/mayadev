import maya.cmds as cmds
import sgBFunction_ui



class WinA_Global:
    
    winName = "sgImportMeshGroup"
    title   = "Import Mesh Group"
    width   = 500
    height  = 50
    titleBarMenu = True
    
    import sgBFunction_fileAndPath
    infoFolderPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh_importGroup'
    infoPathPath= sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh_group/filePath.txt'
    infoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh_importGroup/info.txt'




class WinA_ImportPath:
    
    def __init__(self, label, w, h, al ):
        
        self.label  = label
        self.width  = w
        self.height = h
        self.aline  = al


    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l=self.label, w=self.width, h=self.height, al= self.aline )
        txf  = cmds.textField( h = self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( text, 'top', 0 ), ( text, 'left', 0 ),
                               ( txf,  'top', 0 ), ( txf,  'right', 0 )],
                         ac = [( txf, 'left', 0, text )] )
        
        WinA_Global.importPath_txf  = txf
        WinA_Global.importPath_form = form
        
        return form



class WinA_ImportByMatrix:
    
    def __init__(self, label ):
        
        self.label = label
    
    def create(self):
        
        checkBox = cmds.checkBox( l = self.label )
        WinA_Global.checkBox = checkBox
        
        return checkBox




class WinA_Button:
    
    def __init__( self, label, bgc, height ):
        
        self.label = label
        self.bgc = bgc
        self.height = height

    
    def create(self):
        
        button = cmds.button( l=self.label, h= self.height, bgc=self.bgc )
        WinA_Global.button = button
        
        return button
        



class WinA_Cmd:
    
    @staticmethod
    def cmdImport( *args ):
        
        import sgBExcute_data, os
        
        importPath = cmds.textField( WinA_Global.importPath_txf, q=1, tx=1 )
        importByMatrix = cmds.checkBox( WinA_Global.checkBox, q=1, v=1 )
        
        sgBExcute_data.importSgMeshDatas( importPath, importByMatrix )
        
        WinA_uiCmd.saveInfo()
        



class WinA_uiCmd:
    
    @staticmethod
    def setUiDefault( *args ):
        cmds.checkBox( WinA_Global.checkBox, e=1, v=0 )
    
    
    @staticmethod
    def setUiCommand( *args ):
        cmds.button( WinA_Global.button, e=1, c=WinA_Cmd.cmdImport )
        popupMenu = cmds.popupMenu( p= WinA_Global.importPath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.importPath_txf, popupMenu )
        
    
    @staticmethod
    def saveInfo( *args ):
        import sgBFunction_fileAndPath
        import cPickle
        importPath = cmds.textField( WinA_Global.importPath_txf, q=1, tx=1 )
        importByMatrix = cmds.checkBox( WinA_Global.checkBox, q=1, v=1 )
        data = [ importPath, importByMatrix ]
        
        sgBFunction_fileAndPath.makeFolder( WinA_Global.infoFolderPath )
        f = open( WinA_Global.infoPath, 'w' )
        cPickle.dump( data, f )
        f.close()
    
    
    @staticmethod
    def loadInfo( *args ):
        import cPickle
        import sgBFunction_fileAndPath
        
        sgBFunction_fileAndPath.makeFolder( WinA_Global.infoFolderPath )
        
        print WinA_Global.infoPathPath
        
        try:
            f = open( WinA_Global.infoPath, 'r' )
            importPath, importByMatrix = cPickle.load( f )
            f.close()
            
            f = open( WinA_Global.infoPathPath, 'r' )
            importPath = cPickle.load( f )
            f.close()
        except: return None
        
        cmds.textField( WinA_Global.importPath_txf, e=1, tx= importPath )
        cmds.checkBox( WinA_Global.checkBox, e=1, v=importByMatrix )




class WinA:
    
    def __init__(self):
        
        self.uiImportPath   = WinA_ImportPath( 'Import Path : ', 120, 22, 'right' )
        self.importByMatrix = WinA_ImportByMatrix( 'Import By Matrix' )
        self.uiButton       = WinA_Button( '>>   IMPORT   M E S H   <<', [0.5,0.5,0.6], 30 )
    
    
    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title= WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )

        form = cmds.formLayout()
        importPathForm     = self.uiImportPath.create()
        importByMatrixForm = self.importByMatrix.create()
        buttonForm         = self.uiButton.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(importPathForm, 'top', 8), (importPathForm, 'left', 0), (importPathForm, 'right', 0),
                             (importByMatrixForm, 'left', 120 ), (importByMatrixForm, 'right', 0 ),
                             (buttonForm,     'left', 0 ), (buttonForm,    'right', 0 )],
                         ac=[(importByMatrixForm, 'top', 8, importPathForm),
                             (buttonForm, 'top', 8, importByMatrixForm)] )
        
        cmds.window( WinA_Global.winName, e=1, w= WinA_Global.width, h= WinA_Global.height, rtf=1 )
        cmds.showWindow( WinA_Global.winName )
    
        WinA_uiCmd.setUiDefault()
        WinA_uiCmd.loadInfo()
        WinA_uiCmd.setUiCommand()


mc_showWindow = """import sgPWindow_data_mesh_importGroup
sgPWindow_data_mesh_importGroup.WinA().create()"""