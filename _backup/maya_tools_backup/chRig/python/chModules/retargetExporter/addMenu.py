import maya.cmds as cmds

import mainInfo


class Cmd:
    
    def __init__(self):
        
        pass

    
    
    
class Add( Cmd ):
    
    def __init__( self ):
        
        self.core()
        
        Cmd.__init__(self)
        


    def core( self ):
        
        cmds.menu( l='File' )
        
        cmds.menuItem( l='menu' )