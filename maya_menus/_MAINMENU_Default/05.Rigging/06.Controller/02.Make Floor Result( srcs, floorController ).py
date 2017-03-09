import maya.cmds as cmds
from sgModules import sgcommands
sels = cmds.ls( sl=1 )
for sel in sels[:-1]:
    sgcommands.makeFloorResult( sel, sels[-1] )