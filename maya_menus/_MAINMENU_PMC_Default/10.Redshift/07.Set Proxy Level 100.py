import maya.cmds as cmds

proxys = cmds.ls( type='RedshiftProxyMesh' )
for proxy in proxys:
    cmds.setAttr( proxy + '.displayPercent', 100 )