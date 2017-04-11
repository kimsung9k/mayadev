import maya.cmds as cmds

from uiModel import *
from cmdModel import *



class ModelPannelUI:
    
    def __init__(self):
                                
        self._cam = CaptureViewUIInfo._cam
        
        
    def setCamera(self, cam ):
        
        self._cam = cam
            
    
    def create(self):
        
        form = cmds.formLayout()
        
        editor = cmds.modelEditor( camera=self._cam, displayAppearance='smoothShaded',
                          allObjects=0, polymeshes = 1, nurbsSurfaces=1, dtx=1, grid=0, jointXray=1,
                          hud=0, manipulators=0 )
    
        cmds.formLayout( form, e=1,
                        attachForm=[( editor, 'top', 0),( editor, 'bottom', 0),
                                    ( editor, 'left', 0),( editor, 'right', 0) ] )
        cmds.setParent( '..' )
        
        self._form = form
        
        return form




class CaptureViewUI:
    
    def __init__(self):
        
        self._modelUI = ModelPannelUI()
    
    
    def create(self):
        
        winName  = CaptureViewUIInfo._winName
        winTitle = CaptureViewUIInfo._title
        winWidth = CaptureViewUIInfo._width
        winHeight = CaptureViewUIInfo._height
        
        if cmds.window( winName, ex=1 ):
            cmds.deleteUI( winName, wnd=1 )
        cmds.window( winName, title=winTitle )
        
        form = cmds.formLayout()
        modelUI = self._modelUI.create()
        
        cmds.formLayout( form, e=1,
                         af = [ (modelUI,'top',0),(modelUI,'bottom',0),(modelUI,'left',0),(modelUI,'right',0) ] )
        
        cmds.setParent( '..' )
        
        cmds.window( winName, e=1, 
                     w=winWidth, h=winHeight )
        cmds.showWindow( winName )