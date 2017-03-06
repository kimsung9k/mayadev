import maya.cmds as cmds

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdCreate(self, *args ):
        
        sels = cmds.ls( sl=1 )
        numCtl = cmds.intSliderGrp( self.intf_numCtl, q=1, v=1 )
        
        for sel in sels:
            cmdModel.CreateController( sel, numCtl )
            
            
    def cmdCopy(self, *args ):
        
        cmdModel.uiCmd_CopyController()
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width - 2
        labelWidth = (columnWidth-2) * 0.4
        fieldWidth = 50
        sliderWidth = (columnWidth-2) - fieldWidth - labelWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        intf_numCtl = cmds.intSliderGrp( l="Number Of Controller : ", f=1, min=1, max=5, fmn=1, fmx=100,v=0, cw=[(1,labelWidth),(2,fieldWidth),(3,sliderWidth)])
        cmds.button( l='Set Controller', c=self.cmdCreate )
        cmds.separator()
        cmds.button( l='Copy Controller', c=self.cmdCopy )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.intf_numCtl = intf_numCtl