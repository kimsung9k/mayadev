import maya.cmds as cmds

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdCreateSet(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        for sel in sels:
            cmdModel.makeSetSelectedGroup( sel )
            
    
    def cmdConnectSetToYeti(self, *args ):
        
        sels = cmds.ls( sl=1 )
        yeti = sels[-1]
        
        for sel in sels[:-1]:
            cmdModel.connectSetToYeti( sel, yeti )
            
            
    def cmdCreateGroom(self, *args ):
        
        sels = cmds.ls( sl=1 )
        mesh = sels[-1]
        
        for sel in sels[:-1]:
            cmdModel.createGroomAndConnect( sel, mesh )
            
    
    def cmdProcessAll(self, *args ):
        
        sels = cmds.ls( sl=1 )
        yeti = sels[-2]
        mesh = sels[-1]
        
        cmdModel.processAll( sels[:-2], yeti, mesh )
    
    
    def create(self, *args ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width-2
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.button( l='CREATE SET( Select Groups )',
                     c=self.cmdCreateSet )
        cmds.button( l='CONNECT SET( Select Sets and YetiNode )',
                     c=self.cmdConnectSetToYeti )
        cmds.button( l='CREATE GROOM( Select Sets and Mesh )',
                     c=self.cmdCreateGroom )
        cmds.separator()
        cmds.button( l='PROCESS ALL( Select Groups and YetiNode and Mesh )',
                     c=self.cmdProcessAll )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )

mc_showWindow = """import projectFunction.yetiTool.view
projectFunction.yetiTool.view.Window().create()"""