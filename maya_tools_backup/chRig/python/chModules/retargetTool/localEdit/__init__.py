import maya.cmds as cmds
from functools import partial

class Cmd:
    
    def __init__(self):
        
        pass
        


class Show( Cmd ):
    
    def __init__(self):
        
        self._winName = 'retargetConnectSimple_ui'
        self._title   = "Retarget Control UI"
        
        self.core()
    
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        
        self.win = cmds.window( self._winName, title=self._title )
        
        cmds.columnLayout()
        
        cmds.window( self.win, e=1, wh=( 304, 300 ) )
        cmds.showWindow( self.win )