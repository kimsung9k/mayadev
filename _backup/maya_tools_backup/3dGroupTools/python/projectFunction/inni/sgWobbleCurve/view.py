import maya.cmds as cmds

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdSet(self, *args ):
        cmdModel.setSgWobbleCurve()
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-4)])
        cmds.button( l='Set', c = self.cmdSet )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )