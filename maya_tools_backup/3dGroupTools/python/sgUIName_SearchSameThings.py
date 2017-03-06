import maya.cmds as cmds


class Window:
    
    def __init__(self):
        
        self.winName = "sgUiNameSearchSameThing"
        self.title   = "SG UI Name Search Same Things"
        self.width   = 400
        self.height  = 200
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )