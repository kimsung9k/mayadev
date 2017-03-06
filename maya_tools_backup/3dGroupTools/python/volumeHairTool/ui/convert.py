import volumeHairTool.command.convert as mainCmd
import uiInfo
import maya.cmds as cmds
from functools import partial


class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def setCmd(self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )
        
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        if sels:
            cmds.select( sels )
            

class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        self._uiName = "volumeHairTool_convert"
        self._label = "  Convert"
        self._width = winPointer._width-4
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self.core()
        
    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )

        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        uiInfo.setButton( partial( self.setCmd, self._winPointer, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.getOutFrameLayout()