import maya.cmds as cmds
import uiInfo
from functools import partial
import uiModel


class Cmd:
    
    def __init__(self ):
        
        pass
    
    
    def modeChange(self, winPointer, index ):
        
        if index == 4: return None
    
        layouts = [ winPointer._rebuild,
                    winPointer._simulation,
                    winPointer._volumeHair,
                    winPointer._cutting,
                    winPointer._convert,
                    winPointer._grooming,
                    winPointer._guide,
                    winPointer._bake ]
        
        if index > len( layouts ) -1: 
            return None
        
        editHight = [ 543, 506, 724, 507, 485, 768, 853, 473 ]


        for layout in layouts:
            cmds.frameLayout( layout._uiName, e=1, vis=0 )
        
        cmds.frameLayout( layouts[index]._uiName, e=1, vis=1 )
        
        cmds.window( winPointer._winName, e=1, h=editHight[index] )
        
        if index in [5,6]:
            layouts[index].updateSet()


    
class Add( Cmd ):
    
    
    def __init__(self, pointer ):
        
        self._uiName = "volumnHairTool_mainButton"
        
        self._winPointer = pointer
        
        self.core()

        
    def core(self):
        
        cmds.rowColumnLayout( self._uiName, nc=1, cw=(1,self._winPointer._width) )
        
        cmds.rowColumnLayout( nc=9, cw=[(1,10),(2,94),(3,1),(4,94),(5,1),(6,94),(7,1),(8,94),(9,10)] )
        
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94, image= uiModel.iconPath+"/94/rebulid.png", 
                             c= partial( self.modeChange, self._winPointer, 0 ) )
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94,image= uiModel.iconPath+"/94/nhair.png", 
                             c= partial( self.modeChange, self._winPointer, 1 ) )
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94,image= uiModel.iconPath+"/94/volume.png",
                             c= partial( self.modeChange, self._winPointer, 2 ) )
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94,image= uiModel.iconPath+"/94/cutting.png",
                             c= partial( self.modeChange, self._winPointer, 3 ) )
        uiInfo.setSpace()
        
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=9, cw=[(1,10),(2,94),(3,1),(4,94),(5,1),(6,94),(7,1),(8,94),(9,10)] )
        
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94, image= uiModel.iconPath+"/94/convert_gray.png",
                             c= partial( self.modeChange, self._winPointer, 4 ) )
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94,image= uiModel.iconPath+"/94/grooming.png",
                             c= partial( self.modeChange, self._winPointer, 5 ) )
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94,image= uiModel.iconPath+"/94/guide.png",
                             c= partial( self.modeChange, self._winPointer, 6 ) )
        uiInfo.setSpace()
        cmds.iconTextButton( l="", h=94,image= uiModel.iconPath+"/94/bake.png",
                             c= partial( self.modeChange, self._winPointer, 7 ) )
        uiInfo.setSpace()
        
        cmds.setParent( '..' )
        
        cmds.setParent( '..' )