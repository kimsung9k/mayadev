import maya.cmds as cmds

class Cmd:
    
    def __init__(self):
        
        pass
        
        
    def defaultAll(self, *args):
        
        self._uiList = [ self._winPointer._exportData,
                         self._winPointer._retargeting,
                         self._winPointer._timeControl,
                         self._winPointer._editTransform,
                         self._winPointer._bake ]
        
        for ui in self._uiList:
            ui.setDefault()


    
    def refreshVeiwport(self, *args):
        
        cmds.refresh( su=0 )



class File( Cmd ):
    
    
    def __init__( self, winPointer ):

        self._winPointer = winPointer
        self._uiName = "volumnHairTool_FileMenu"
        self._label  = "File"
        
        self.core()
        
        Cmd.__init__(self)
        
        
    def core(self):
            
        cmds.menu( self._uiName, l=self._label )
        cmds.menuItem( l='Refresh Veiwport', c = self.refreshVeiwport )
        cmds.menuItem( d=1 )
        cmds.menuItem( l='Default All', c=self.defaultAll )
        
        
        
class About( Cmd ):
    
    
    def __init__(self):
        
        self._uiName = "volumnHairTool_AboutMenu"
        self._label  = "About"
        
        self.core()
        
        
    def core(self):
        
        cmds.menu( self._uiName, l=self._label )
        
        
        
        
class Add:
    
    def __init__(self, winPoiner ):
        
        self._winPoiner = winPoiner
        self.core()
        
    
    def core(self):
        
        File( self._winPoiner )
        About()