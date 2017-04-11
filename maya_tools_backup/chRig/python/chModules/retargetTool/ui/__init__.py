import maya.cmds as cmds
from functools import partial
import uiData
import menu
import mainButton
import exportData
import retargeting
import timeControl
import editTransform
import bake

class Cmd:
    
    def __init__(self):
        
        pass
        


class Show( Cmd ):
    
    def __init__(self, *args ):
        
        uiData.updateFunctionList = []
        
        self._winName = uiData.winName
        self._title   = "Retarget Set UI"
        
        self._width = uiData.winWidth
        self._height = uiData.winHeight
        
        self._menu = None
        self._exportData = None
        self._retargeting = None
        self._timeControl  = None
        self._editTransform = None
        self._bake = None
        
        self.core()
        self.event()
        
    
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        
        self.win = cmds.window( self._winName, title=self._title, menuBar=True )
        
        self._menu = menu.Add( self )
        
        cmds.columnLayout()
        
        mainButton.Add( self )
        self._exportData = exportData.Add()
        self._retargeting = retargeting.Add()
        self._timeControl  = timeControl.Add()
        self._editTransform = editTransform.Add()
        self._bake = bake.Add()
        
        cmds.window( self.win, e=1, w=self._width, h=self._height )
        cmds.showWindow( self.win )
        
        
    def event(self):

        def allFunctionsDoIt( *args ):
            for function in uiData.updateFunctionList:
                function()
        
        cmds.scriptJob( e=['Undo', allFunctionsDoIt], p= self._winName )
        cmds.scriptJob( e=['Redo', allFunctionsDoIt], p= self._winName )