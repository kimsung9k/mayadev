import maya.cmds as cmds

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdMakeWire(self, *args ):
        
        value = cmds.floatSliderGrp( self.fSlider, q=1, v=1 )
        cmdModel.makeWire( value )
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        firstWidth = ( self.width - 4 )*0.35
        secondWidth = 50
        thirdWidth = ( self.width - 4 ) - secondWidth - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-4)])
        fSlider = cmds.floatSliderGrp( l='Dropoff Distance : ', f=1, min=0, v=10, max=100, pre=2,
                                             cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-4)] )
        cmds.button( l='Create', c= self.cmdMakeWire )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.fSlider = fSlider