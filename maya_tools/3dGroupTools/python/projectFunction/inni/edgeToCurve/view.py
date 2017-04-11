import maya.cmds as cmds

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdCreate( self, *args ):
        select = cmds.optionMenu( self.optionMenu, q=1, sl=1 )
        if cmds.checkBox( self.checkKeepOrig, q=1, v=1 ):
            if select == 1:
                cmdModel.createCurveFromEdge( None, 1 )
            else:
                cmdModel.createCurveFromEdge( None, 3 )
        else:
            value = cmds.intSliderGrp( self.intSlider, q=1, v=1 )
            if select == 1:
                cmdModel.createCurveFromEdge( value, 1 )
            else:
                cmdModel.createCurveFromEdge( value, 3 )
    
    
    def cmdCVOnOff( self, *args ):
        cmdModel.cvOnOff()
        
        
    def cmdChangeCheck( self, *args ):
        if cmds.checkBox( self.checkKeepOrig, q=1, v=1 ):
            cmds.intSliderGrp( self.intSlider, e=1, en=0 )
        else:
            cmds.intSliderGrp( self.intSlider, e=1, en=1 )
            
        
        
    def cmdClose(self, *args ):
        cmds.deleteUI( self.winName )
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        firstWidth = ( self.width - 4 )*0.3
        secondWidth = 50
        thirdWidth = ( self.width - 4 ) - secondWidth - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-4)])
        intSlider = cmds.intSliderGrp( l='Number of Spans : ', f=1, min=3, v=10, max=50,
                                             cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.setParent( '..' )
        
        firstWidth = ( self.width-4 )*0.5
        secondWidth = ( self.width - 4 )-firstWidth
        cmds.rowColumnLayout( nc=2, co=[(1,'left', 10)], cw=[(1,firstWidth), (2,secondWidth)] )
        checkKeepOrig = cmds.checkBox( l='Keep Original', cc= self.cmdChangeCheck )
        optionMenu = cmds.optionMenu( l='Degree' )
        cmds.menuItem( l='degree 1' )
        cmds.menuItem( l='degree 3' )
        cmds.setParent( '..' )
        
        firstWidth = ( self.width-4 )*0.5
        secondWidth = ( self.width - 4 )-firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Create Curve', c=self.cmdCreate )
        cmds.button( l='CV On Off', c=self.cmdCVOnOff )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-4) ])
        cmds.button( l='Close', c= self.cmdClose )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.intSlider = intSlider
        self.checkKeepOrig = checkKeepOrig
        self.optionMenu = optionMenu