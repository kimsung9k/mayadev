import maya.cmds as cmds




class CmdCharacterBake:
    
    def __init__(self, ptr_window ):
        
        import sgFunctionCharacterBake
        self.ptr_window = ptr_window
        
        self.ptr_cmdExport = sgFunctionCharacterBake.exportCharactersAnimationToFile
        self.ptr_cmdImport = sgFunctionCharacterBake.importCharacterAnimationFromFile


    def cmdExport( self, *args ):
        
        exportPath = cmds.textField( self.ptr_window.firstField, q=1, tx=1 )
        minFrame = cmds.floatField( self.ptr_window.minField, q=1, v=1 )
        maxFrame = cmds.floatField( self.ptr_window.maxField, q=1, v=1 )
        self.ptr_cmdExport( cmds.ls( sl=1 ), exportPath, minFrame, maxFrame )
    
    
    def cmdImport( self, *args ):
        
        importPath = cmds.textField( self.ptr_window.secondField, q=1, tx=1 )
        minFrame = cmds.floatField( self.ptr_window.minField, q=1, v=1 )
        self.ptr_cmdImport( cmds.ls( sl=1 ), importPath, minFrame )





class UICharacterBake:
    
    def __init__(self):
        
        self.winName = 'characterBakeui'
        self.title   = 'UI Character Bake'
        self.width = 400
        self.height = 50
    
        self.cmd = CmdCharacterBake( self )
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        firstWidth = 120
        secondWidth = self.width - firstWidth - 2
        cmds.rowColumnLayout( nc=2, cw=[(1, firstWidth),(2, secondWidth)])
        cmds.text( l='Export Path : ' )
        fieldFirst = cmds.textField()
        cmds.text( l='Import Path : ' )
        fieldSecond = cmds.textField()
        cmds.setParent( '..' )
        
        firstWidth = self.width * 0.5
        secondWidth = self.width - firstWidth
        numWidth = 50
        cmds.rowColumnLayout( nc=4, cw=[(1,firstWidth-numWidth),(2,numWidth),(3,secondWidth-numWidth),(4,numWidth)])
        cmds.text( l='min frame : ' )
        minField = cmds.floatField( v=1, pre=2 )
        cmds.text( l='max frame : ' )
        maxField = cmds.floatField( v=24, pre=2 )
        cmds.setParent( '..' )
        
        firstWidth = self.width * 0.5
        secondWidth = self.width - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Export Characters', c= self.cmd.cmdExport )
        cmds.button( l='Import Character', c= self.cmd.cmdImport )
        
        cmds.window( self.winName, e=1, w= self.width, h= self.height )
        cmds.showWindow( self.winName )
        
        self.firstField = fieldFirst
        self.secondField = fieldSecond
        self.minField   = minField
        self.maxField   = maxField


mc_showWindow = '''import sgUI_characterBake
sgUI_characterBake.UICharacterBake().create()'''