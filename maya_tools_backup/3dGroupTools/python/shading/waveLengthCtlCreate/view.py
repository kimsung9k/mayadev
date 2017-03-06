import maya.cmds as cmds

from uiModel import *
from cmdModel import *

class Window():
    
    def __init__(self):
        
        pass
    
    
    def cmdCreate(self, *args):
        checkValue      = cmds.checkBox( self._sepCheck, q=1, v=1 )
        revCheckValue   = cmds.checkBox( self._revCheck, q=1, v=1 )
        gammaCheckValue = cmds.checkBox( self._gammaCheck, q=1, v=1 )
        RemapConnect().ucCreateSamplerInfo( revCheckValue, checkValue, gammaCheckValue )
    
    
    def cmdCheck(self, *args ):
        
        red = cmds.checkBox( self.from_red, q=1, v=1 )
        green = cmds.checkBox( self.from_green, q=1, v=1 )
        blue = cmds.checkBox( self.from_blue, q=1, v=1 )
        
        valueList = [red, green, blue]
        uiList = [self.to_red,self.to_green,self.to_blue]
        
        allValueTrue = True
        for i in range( 3 ):
            if not valueList[i]: 
                allValueTrue = False
                break
        
        if allValueTrue: return None
        
        for i in range( 3 ):
            cmds.checkBox( uiList[i], e=1, v= not valueList[i] )
            
            
            
    def cmdSync(self, *args ):
        
        fromRed   = cmds.checkBox( self.from_red, q=1, v=1 )
        fromGreen = cmds.checkBox( self.from_green, q=1, v=1 )
        fromBlue  = cmds.checkBox( self.from_blue, q=1, v=1 )
        
        toRed   = cmds.checkBox( self.to_red, q=1, v=1 )
        toGreen = cmds.checkBox( self.to_green, q=1, v=1 )
        toBlue  = cmds.checkBox( self.to_blue, q=1, v=1 )
        
        fromList = []
        toList =[]
        
        if fromRed: fromList.append( 'red' )
        if fromGreen: fromList.append( 'green' )
        if fromBlue: fromList.append( 'blue' )
        if toRed: toList.append( 'red' )
        if toGreen: toList.append( 'green' )
        if toBlue: toList.append( 'blue' )
    
        uiCmd_remapColorSync( fromList, toList )
    
    
    def create(self):
        
        winName   = RemapConnectUIInfo._winName
        winTitle  = RemapConnectUIInfo._title
        winWidth  = RemapConnectUIInfo._width
        winHeight = RemapConnectUIInfo._height
        
        if cmds.window( winName, ex=1 ):
            cmds.deleteUI( winName, wnd=1 )
        cmds.window( winName, title = winTitle )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,winWidth)] )
        cmds.button( l='Create Connections', c=self.cmdCreate )
        revCheck   = cmds.checkBox( l='Add Reverse Node', v=1 )
        cmds.separator()
        sepCheck   = cmds.checkBox( l='Add HSV Node' )
        gammaCheck = cmds.checkBox( l='Add Gamma Control', v=1 )
        cmds.setParent( '..' )
        
        cmds.frameLayout( l='Remap Channel Sync Control')
        columnWidth = winWidth - 2
        firstWidth = ( columnWidth - 2 )*0.25
        secondWidth = firstWidth
        thirdWidth = firstWidth
        fourthWidth = ( columnWidth - 2 ) - firstWidth - secondWidth - thirdWidth
        cmds.rowColumnLayout( nc=4, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth),(4,fourthWidth)] )
        cmds.text( l='From : ' )
        from_red   = cmds.checkBox( l='Red', v=1, cc=self.cmdCheck )
        from_green = cmds.checkBox( l='Green', cc=self.cmdCheck )
        from_blue  = cmds.checkBox( l='Blue', cc=self.cmdCheck )
        cmds.text( l='To : ' )
        to_red   = cmds.checkBox( l='Red' )
        to_green = cmds.checkBox( l='Green', v=1 )
        to_blue  = cmds.checkBox( l='Blue', v=1 )
        cmds.setParent( '..' )
        cmds.rowColumnLayout( nc=1, cw=(1,columnWidth-2))
        cmds.button( l='Sync', c=self.cmdSync )
        cmds.setParent( '..' )
        
        cmds.window( winName, e=1, h=winHeight, w=winWidth )
        cmds.showWindow( winName )
        
        self._sepCheck   = sepCheck
        self._revCheck   = revCheck
        self._gammaCheck = gammaCheck
        
        self.from_red   = from_red
        self.from_green = from_green
        self.from_blue  = from_blue
        self.to_red = to_red
        self.to_green = to_green
        self.to_blue  = to_blue