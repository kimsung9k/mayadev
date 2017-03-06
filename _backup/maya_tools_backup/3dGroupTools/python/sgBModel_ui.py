import maya.cmds as cmds


class ModelEditorWindow:
    
    def __init__(self, windowName, width, height, tlc=None, titleBar=True, titleBarMenu=True, **options ):
        
        self.winName = windowName
        self.title   = 'Model Editor Window'
        
        self.width  = width
        self.height = height
        self.options = options
        self.tlc = tlc
        self.titleBar = titleBar
        self.titleBarMenu = titleBarMenu
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title, titleBar= self.titleBar, titleBarMenu= self.titleBarMenu )
        
        panLayout = cmds.paneLayout( w=self.width, h=self.height )
        modelEditor = cmds.modelEditor( **self.options )
        cmds.setParent( '..' )

        cmds.showWindow( self.winName )
        if self.tlc:
            cmds.window( self.winName, e=1, tlc= self.tlc, w= self.width+2, h= self.height+2 )
        else:
            cmds.window( self.winName, e=1, w= self.width+2, h= self.height+2 )
        
        return panLayout, modelEditor