import maya.cmds as cmds

sels = cmds.ls( sl=1 )

selPos = cmds.xform( sels[-1], q=1, ws=1, t=1 )
for sel in sels[:-1]:
    cmds.xform( sel, ws=1, t=selPos )