import maya.cmds as cmds

import uiModel
import cmdModel
import functions


def updatePopupCmdDefault( textFieldGrp, popupMenu, *args ):
    
    functions.updatePopupMenu( textFieldGrp, popupMenu, updatePopupCmdDefault )



class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdChangeCutName(self, *args):
        functions.updatePopupMenu( self.fd_cutName, self.pu_cutName, updatePopupCmdDefault )


    def cmdChangeSceneName(self, *args ):
        functions.updatePopupMenu( self.fd_cutName, self.pu_cutName, updatePopupCmdDefault )


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width - 2
        firstWidth  = ( columnWidth -2 )* 0.23
        secondWidth = ( columnWidth -2 ) - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.text( l='', h=5 )
        fd_cutName = cmds.textFieldGrp( l='Cut Path : ', cw=[(1,firstWidth),(2,secondWidth)],
                                        cc=self.cmdChangeCutName )
        pu_cutName = cmds.popupMenu()
        cmds.text( l='', h=5 )
        cmds.separator()
        cmds.text( l='', h=5 )
        
        fd_sceneName = cmds.textFieldGrp( l='Scene Path : ', cw=[(1,firstWidth),(2,secondWidth)],
                                        cc=self.cmdChangeSceneName )
        pu_sceneName = cmds.popupMenu()
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.fd_cutName = fd_cutName
        self.pu_cutName = pu_cutName