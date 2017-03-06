import maya.cmds as cmds
import rigTool.view as rigToolView
import rigTool2.view as rigTool2View
import animationTool.view as animToolView
import model

from functools import partial



def deleteAllTools( *args ):
    
    if cmds.popupMenu( rigToolView.model._uiName, ex=1 ):
        cmds.deleteUI( rigToolView.model._uiName )
        
    if cmds.popupMenu( rigTool2View.model._uiName, ex=1 ):
        cmds.deleteUI( rigTool2View.model._uiName )
        
    if cmds.popupMenu( animToolView.model._uiName, ex=1 ):
        cmds.deleteUI( animToolView.model._uiName )


mc_deleteAllTool = """import markingMenu.control
markingMenu.control.deleteAllTools()
"""


def createRigTool( *args ):
    
    deleteAllTools()
    cmds.popupMenu( rigToolView.model._uiName, ctl=1, alt=1, button=3, mm=1, p=model.markingMenuParentUI, 
                    pmc= partial( rigToolView.Create, rigToolView.model._uiName ) )
    

mc_createRigTool = """import markingMenu.control
markingMenu.control.createRigTool()
"""


def createRigTool2( *args ):
    
    deleteAllTools()
    cmds.popupMenu( rigTool2View.model._uiName, ctl=1, alt=1, button=3, mm=1, p=model.markingMenuParentUI, 
                    pmc= partial( rigTool2View.Create, rigTool2View.model._uiName ) )
    

mc_createRigTool2 = """import markingMenu.control
markingMenu.control.createRigTool2()
"""


def createAnimTool( *args ):
    
    deleteAllTools()
    cmds.popupMenu( animToolView.model._uiName, ctl=1, alt=1, button=3, mm=1, p=model.markingMenuParentUI, 
                    pmc= partial( animToolView.Create, animToolView.model._uiName ) )


mc_createAnimTool = """import markingMenu.control
markingMenu.control.createAnimTool()
"""