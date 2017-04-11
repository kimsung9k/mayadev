import maya.cmds as cmds
import sgBFunction_ui



class WinA_Global:
    
    winName = "sgImportSceneBakeInfo"
    title   = "Import Scene Bake Info"
    width   = 500
    height  = 50
    titleBarMenu = True
    
    import sgBFunction_fileAndPath
    filePathInfo = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_sceneBakeInfo/filePath.txt'
    
    



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
        
        import sgBFunction_scene
        
        importPath = cmds.textField( WinA_Global.importPath_txf, q=1, tx=1 )
        cmds.currentTime( cmds.currentTime( q=1 ) )
        sgBFunction_scene.setSceneFromSceneBakeInfo( importPath )
        
        WinA_uiCmd.saveInfo()
        



class WinA_uiCmd:
    
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
        data = importPath
        
        sgBFunction_fileAndPath.makeFolder( WinA_Global.filePathInfo )
        f = open( WinA_Global.filePathInfo, 'w' )
        cPickle.dump( data, f )
        f.close()
    
    
    @staticmethod
    def loadInfo( *args ):
        import cPickle
        import sgBFunction_fileAndPath
        
        try:
            f = open( WinA_Global.filePathInfo, 'r' )
            importPath = cPickle.load( f )
            f.close()
            
            cmds.textField( WinA_Global.importPath_txf, e=1, tx= importPath )
        except: return None



class WinA:
    
    def __init__(self):
        
        self.uiImportPath = WinA_ImportPath( 'Import Path : ', 120, 22, 'right' )
        self.uiButton     = WinA_Button( '>>   IMPORT    S C E N E    B A K E    I N F O   <<', [0.7,0.7,0.7], 30 )
    
    
    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title= WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )

        form = cmds.formLayout()
        importPathForm = self.uiImportPath.create()
        buttonForm     = self.uiButton.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(importPathForm, 'top', 8), (importPathForm, 'left', 0), (importPathForm, 'right', 0),
                             (buttonForm,     'left', 0 ), (buttonForm,    'right', 0 )],
                         ac=[(buttonForm, 'top', 8, importPathForm)] )
        
        cmds.window( WinA_Global.winName, e=1, w= WinA_Global.width, h= WinA_Global.height, rtf=1 )
        cmds.showWindow( WinA_Global.winName )
    
        WinA_uiCmd.loadInfo()
        WinA_uiCmd.setUiCommand()


mc_showWindow = """import sgPWindow_data_sceneBakeInfo_import
sgPWindow_data_sceneBakeInfo_import.WinA().create()"""