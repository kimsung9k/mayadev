import maya.cmds as cmds
import uifunctions as uifnc

import part0_rootRoad
import part1_driverInfo
import part2_meshInfo
import part3_editMesh


class Cmd():
    
    def __init__(self):
        
        pass
    


class Show( Cmd ):
    
    def __init__(self, *args ):
        
        self._winName = "jointBasePSD_ui"
        self._title   = "Skined Shape Edit Tool"
        
        self._width = 600
        self._height = 700

        self.core()

        Cmd.__init__(self)
        
        
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )

        cmds.window( self._winName, title= self._title )
        
        cmds.columnLayout()
        
        uifnc.setSpace(10)
        part0_rootRoad.Add( self._width )
        uifnc.setSpace(20)
        part1_driverInfo.Add( self._width )
        uifnc.setSpace(25)
        part2_meshInfo.Add( self._width )
        uifnc.setSpace( 25 )
        part3_editMesh.Add( self._width )

        cmds.window( self._winName, e=1, wh=[ self._width, self._height ] )
        cmds.showWindow( self._winName )