import maya.cmds as cmds
sels = cmds.ls( '*.origDist' )
for sel in sels:
    node = sel.split( '.' )[0]
    if cmds.nodeType( sel ) != 'joint': continue
    cmds.setAttr( node + '.origDist', cmds.getAttr( node + '.cuDist' ) )