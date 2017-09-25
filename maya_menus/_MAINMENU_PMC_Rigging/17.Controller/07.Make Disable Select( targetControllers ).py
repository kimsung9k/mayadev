import maya.cmds as cmds

sels = cmds.ls( sl=1 )
for sel in sels:
    selShape = cmds.listRelatives( sel, s=1, f=1 )
    if not selShape: continue
    cmds.setAttr( selShape[0] + '.overrideEnabled', 1 )
    cmds.setAttr( selShape[0] + '.overrideDisplayType', 2 )