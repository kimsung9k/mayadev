import maya.cmds as cmds
import uifunctions as uifnc
import globalInfo

class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def loadCmd(self, *args):
        
        selObjs = cmds.ls( sl=1 )
        
        if not selObjs: return None
        
        cmds.textField( self._driverRoot, e=1, tx= selObjs[0] )
        
        globalInfo.rootDriver = selObjs[0]
        globalInfo.updateUiCondition()


class Add( Cmd ):
    
    def __init__(self, width ):
        
        self._emptyWidth = 10
        self._width = width - self._emptyWidth*2 - 4
        
        sepList = [ 30, 50, 25 ]
        self._widthList = uifnc.setWidthByPerList( sepList, self._width )
                
        self.core()
    
        Cmd.__init__( self )

    
    def core(self):
        
        cmds.rowColumnLayout( nc= 5, cw=[(1,self._emptyWidth),
                                         (2,self._widthList[0]),
                                         (3,self._widthList[1]),
                                         (4,self._widthList[2]),
                                         (5,self._emptyWidth) ] )
        
        uifnc.setSpace()
        cmds.text( l='Driver Root  :  ', al='right' )
        self._driverRoot = cmds.textField()
        cmds.button( l='Load', c = self.loadCmd )
        uifnc.setSpace()
        
        cmds.setParent( '..' )