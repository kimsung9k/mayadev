import maya.cmds as cmds

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
    
    
    def cmdConnect( self, *args ):
        
        axisIndex = cmds.optionMenu( self.optionMenu, q=1, select=1 )-1
        cmdModel.connectFk(axisIndex)
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-2)])
        cmds.text( l='Select Fk End, Fk Start, Joint End, Joint Start', h=25 )
        cmds.setParent( '..' )
        
        firstWidth = ( self.width-2 )*0.5
        secondWidth = ( self.width-2 ) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.text( l='Target Axis : ' )
        optionMenu = cmds.optionMenu()
        cmds.menuItem( l=' X');cmds.menuItem( l=' Y');cmds.menuItem( l=' Z')
        cmds.menuItem( l='-X');cmds.menuItem( l='-Y');cmds.menuItem( l='-Z')
        cmds.setParent( '..' )
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-2)])
        cmds.button( l='Create Connect', h=25, c= self.cmdConnect )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.optionMenu = optionMenu
        