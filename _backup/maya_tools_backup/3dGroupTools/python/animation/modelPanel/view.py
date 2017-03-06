import maya.cmds as cmds


class Window:
    
    def __init__(self):
        
        self.title   = 'Model Panel'
        self.width   = 1920
        self.height  = 1080 + 50
        
        
    def create(self):
        
        window = cmds.window( title=self.title )
        
        form = cmds.formLayout()
        modelPanel = cmds.modelPanel()
        
        cmds.formLayout( form, e=1,
                         af=[(modelPanel, 'top', 0), (modelPanel, 'bottom', 0),
                             (modelPanel, 'left', 0), (modelPanel, 'right', 0)] )
        cmds.setParent( '..' )
        
        cmds.window( window, e=1, w=self.width, h=self.height )
        cmds.showWindow( window )