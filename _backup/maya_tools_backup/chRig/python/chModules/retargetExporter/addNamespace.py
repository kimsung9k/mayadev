import maya.cmds as cmds
import mainInfo


class Cmd:
    
    def __init__(self):
        
        pass
    
    

class Add( Cmd ):
    
    def __init__(self):
        
        self._sideWidth = 7
        self._width = mainInfo.fileWidth - self._sideWidth*2 - 2
        
        self.core()
        
        Cmd.__init__( self )
    
    
    
    def core(self):
        
        addSpaceWidth = 20
        editWidt = self._width-addSpaceWidth
        halfWidth = editWidt/2
        lastWidth   = editWidt - halfWidth
        cmds.rowColumnLayout( nc=4, cw=[(1,addSpaceWidth+self._sideWidth),
                                        (2,halfWidth),
                                        (3,lastWidth),
                                        (4,self._sideWidth)] )
        self._nameCollection = cmds.radioCollection()
        mainInfo.setSpace()
        cmds.radioButton( l='Prefix', sl=1 )
        cmds.radioButton( l='Namespace' )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH( 5 )
        
        buttonWidth = self._width/2
        lastWidth   = self._width - buttonWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideWidth),
                                        (2,buttonWidth),
                                        (3,lastWidth),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        self._frontNameOptionMenu = cmds.optionMenu( )
        cmds.menuItem( l='the file name' )
        cmds.menuItem( l='this string')
        self._thisStringField = cmds.textField( en=0 )
        mainInfo.setSpace()
        cmds.setParent( '..' )