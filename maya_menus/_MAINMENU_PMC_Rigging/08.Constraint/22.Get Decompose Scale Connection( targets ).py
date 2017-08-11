import maya.cmds as cmds
sels = cmds.ls( sl=1 )
for sel in sels:
    dcmp = cmds.listConnections( sel, s=1, d=0, type='decomposeMatrix' )
    if not dcmp: continue
    if cmds.isConnected( dcmp[0] + '.os', sel + '.s' ): continue
    cmds.connectAttr( dcmp[0] + '.os', sel + '.s' )