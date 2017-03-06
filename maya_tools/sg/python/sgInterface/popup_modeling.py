import maya.cmds as cmds
import sgPlugin



def create( parent ):
    
    menuPutObject = cmds.menuItem( l="Put Object", rp='N', p=parent, c=sgPlugin.setTool_SGMPlugMod01 )