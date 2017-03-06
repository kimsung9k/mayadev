from view import *


def createMenu():
    
    if cmds.menu( M3DGroupUIInfo._uiName, ex=1 ):
        cmds.deleteUI( M3DGroupUIInfo._uiName )
    cmds.menu( M3DGroupUIInfo._uiName, l=M3DGroupUIInfo._title, p=M3DGroupUIInfo._parent, to=1 )
    
    M3DGroupUI()