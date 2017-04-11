import maya.cmds as cmds
import mainInfo



class Cmd:
    
    def __init__(self):
        
        pass




class Add( Cmd ):
    
    def __init__(self):
        
        self._sideWidth = 7
        self._width = mainInfo.width - self._sideWidth*2 - 2
        
        self.core()
        
        Cmd.__init__( self )
        
        
    def core(self):
        
        buttonWidth = self._width/2
        lastWidth   = self._width - buttonWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideWidth),
                                        (2,buttonWidth),
                                        (3,lastWidth),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        cmds.button( l='Import File', h=30 )
        cmds.button( l='Reference File', h=30 )
        mainInfo.setSpace()
        cmds.setParent( '..' )