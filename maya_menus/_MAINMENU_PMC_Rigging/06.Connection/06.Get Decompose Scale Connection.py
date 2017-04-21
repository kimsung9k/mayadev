import maya.cmds as cmds

sels = cmds.ls( sl=1 )
for sel in sels:
    dcmp = cmds.listConnections( sel, s=1, d=0, type='decomposeMatrix' )[0]
    cmds.connectAttr( dcmp + '.os', sel + '.s' )