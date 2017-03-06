import uiModel
import cmdModel

import maya.cmds as cmds

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
    
    def cmdCreate(self, *args ):
        
        offset = cmds.floatFieldGrp( self.floatFieldGrp, q=1, v=1 )
        cmdModel.uiCmd_createMiddleJoint( offset )
        
        
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title=self.title )
        
        offset = 2
        columnWidth = self.width - 4
        fieldWidth = (columnWidth*0.7)*0.333-offset
        labelWidth = columnWidth - (fieldWidth+offset)*3

        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        floatFieldGrp = cmds.floatFieldGrp( l='Offset : ', nf=3, value1=0.0, value2=0.0, value3=0.0,
                            cw =[(1,labelWidth),(2,fieldWidth),(3,fieldWidth),(4,fieldWidth)] )
        cmds.text( l='', h=5 )
        cmds.button( l='Create', c=self.cmdCreate )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1, w=self.width, h=self.height )
        cmds.showWindow( self.winName )
        
        
        self.floatFieldGrp = floatFieldGrp