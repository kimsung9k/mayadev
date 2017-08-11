import maya.cmds as cmds

sels = cmds.ls( sl=1 )

for sel in sels:
    srcCons = cmds.listConnections( sel, s=1, d=0, p=1 )
    dstCons = cmds.listConnections( sel, s=0, d=1, p=1 )    
    if not srcCons or not dstCons: continue
    cmds.connectAttr( srcCons[0], dstCons[0], f=1 )