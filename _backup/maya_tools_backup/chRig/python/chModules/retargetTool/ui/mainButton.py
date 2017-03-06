import maya.cmds as cmds
import uiData
from functools import partial

class Cmd:
    
    def __init__(self ):
        
        pass
    
    
    def setUI(self, index, *args ):
        
        uiList = [ self._winPointer._exportData,
                   self._winPointer._retargeting,
                   self._winPointer._timeControl,
                   self._winPointer._editTransform,
                   self._winPointer._bake ]
        
        heightList = [uiData.exportData_height,
                      uiData.retargeting_height,
                      uiData.timeControl_height,
                      uiData.editTransform_height,
                      uiData.bake_height]
        
        for i in range( len( uiList ) ):
            cmds.frameLayout( uiList[i]._uiName, e=1, vis=0 )
            
        cmds.frameLayout( uiList[index]._uiName, e=1, vis=1 )
        cmds.textField( uiList[index]._worldCtl, e=1, tx=uiData.targetWorldCtl )
        uiList[index].refreshTextScrollList()
        cmds.window( self._winPointer._winName, e=1, h= heightList[index] )

    
    
class Add( Cmd ):
    
    def __init__(self, winPointer ):
        
        Cmd.__init__( self )
        
        self._uiName = 'retarget_mainButton_ui'
        
        self._width = uiData.winWidth
        self._height = 45
        
        self._winPointer = winPointer
        
        self.core()
        
    
    def core(self):
        
        eachWidth = self._width / 5
        lastWidth = self._width - eachWidth*4
        
        cmds.rowColumnLayout( nc=5, cw=[( 1,eachWidth ),( 2,eachWidth ),( 3,eachWidth ),( 4,eachWidth ),( 5,lastWidth )] )
        
        cmds.button( l='Export\nData', c= partial( self.setUI, 0 ), h=self._height )
        cmds.button( l='Retargeting', c= partial( self.setUI, 1 ) )
        cmds.button( l='Time\nControl', c= partial( self.setUI, 2 ) )
        cmds.button( l='Edit\nTransform', c= partial( self.setUI, 3 )  )
        cmds.button( l='Bake', c= partial( self.setUI, 4 ) )
        
        cmds.setParent( '..' )