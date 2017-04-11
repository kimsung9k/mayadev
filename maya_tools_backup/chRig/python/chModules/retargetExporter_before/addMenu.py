import maya.cmds as cmds

import mainInfo


class Cmd:
    
    def __init__(self):
        
        self._motionExportPath = mainInfo.motionExportPath
        self._hikExportPath    = mainInfo.hikExportPath
    
    
    def pathInfoEdit(self):
        
        f = open( mainInfo.pathInfoPath, 'w' )
        fileString = self._motionExportPath +'\n'+self._hikExportPath
        f.write( fileString )
        f.close()
        
        mainInfo.motionExportPath = self._motionExportPath
        mainInfo.hikExportPath    = self._hikExportPath
        
    
    def setMotionDir(self, *args ):
        
        self._motionExportPath = cmds.fileDialog2( fm=3, dir=self._motionExportPath )[0]
        
        self.pathInfoEdit()
    
    
    def setHikDir(self, *args ):
        
        self._hikExportPath = cmds.fileDialog2( fm=3, dir=self._hikExportPath )[0]
        
        self.pathInfoEdit()

    
    
    
class Add( Cmd ):
    
    def __init__( self ):
        
        self.core()
        
        Cmd.__init__(self)
        


    def core( self ):
        
        cmds.menu( l='File' )
        
        cmds.menuItem( l='Set Motion Directory', c= self.setMotionDir )
        cmds.menuItem( l='Set Human IK Directory', c= self.setHikDir )