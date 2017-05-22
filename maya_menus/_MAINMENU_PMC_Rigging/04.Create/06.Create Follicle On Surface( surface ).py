from sgModules import sgcommands
import maya.cmds as cmds
sels = cmds.ls( sl=1 )
for sel in sels:
    sgcommands.createFollicleOnSurface( sel )