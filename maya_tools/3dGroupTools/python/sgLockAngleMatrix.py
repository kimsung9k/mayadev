import maya.cmds as cmds


class Window:
    
    def __init__(self):
        
        self.winName = 'sgLockAngleMatrixUi'
        self.title   = 'SG Lock Angle Matrix'
        self.width   = 300
        self.height  = 50
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        
        
        
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )