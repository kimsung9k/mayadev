import maya.cmds as cmds


class WinA:
    
    def __init__(self):
        
        self.winName = 'sgPWindow_attr_randomValue'
        self.title   = 'Random Value'
        self.width = 350
        self.height = 50


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        form = cmds.formLayout()
        
        
        
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1, w=self.width, h=self.height )
        cmds.showWindow( self.winName ) 