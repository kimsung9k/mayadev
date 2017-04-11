import maya.cmds as cmds
import mainInfo



class Cmd:
    
    def __init__(self):
        
        pass




class Add( Cmd ):
    
    def __init__(self):
        
        self._sideWidth = 7
        self._width = mainInfo.userNameWidth - self._sideWidth*2 - 2
        
        self.core()
        
        Cmd.__init__( self )
        
        
    def core(self):
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideWidth),
                                        (2,self._width),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        cmds.textScrollList( h=330 )
        mainInfo.setSpace()
        cmds.setParent( '..' )