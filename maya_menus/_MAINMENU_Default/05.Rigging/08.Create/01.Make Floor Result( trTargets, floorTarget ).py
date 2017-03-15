from sgModules import sgcommands
import maya.cmds as cmds

sels = cmds.ls( sl=1 )

targets = sels[:-1]
floor = sels[-1]

for target in targets:
    sgcommands.makeFloorResult( target, floor )