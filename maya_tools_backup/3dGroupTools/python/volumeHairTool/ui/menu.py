import maya.cmds as cmds
from functools import partial

class Cmd:
    
    
    def __init__(self):
        
        pass
    
    
    def clearAllCmd(self, winPointer, *args):
        
        layouts = [ winPointer._baseSetting, 
                    winPointer._rebuild,
                    winPointer._simulation,
                    winPointer._volumeHair,
                    winPointer._cutting,
                    winPointer._convert,
                    winPointer._grooming,
                    winPointer._guide,
                    winPointer._bake ]
        
        for layout in layouts:
            try:
                layout.clear()
            except: 
                print layout._uiName
            
            
    def refreshVeiwport(self, *args):
        
        cmds.refresh( su=0 )
    
    


class File( Cmd ):
    
    def __init__(self, winPointer ):
        
        self._winPointer = winPointer
        self._uiName = "volumnHairTool_FileMenu"
        self._label  = "File"
        
        self.core()
        
        
    def core(self):
            
        cmds.menu( self._uiName, l=self._label )
        cmds.menuItem( l='Refresh Veiwport', c= self.refreshVeiwport )
        cmds.menuItem( d=1 )
        cmds.menuItem( l='Default All', c= partial( self.clearAllCmd, self._winPointer ) )
        
        
class About( Cmd ):
    
    
    def __init__(self, winPointer ):
        
        self._uiName = "volumnHairTool_AboutMenu"
        self._label  = "About"
        
        self.core()
        
        
    def core(self):
        
        cmds.menu( self._uiName, l=self._label )