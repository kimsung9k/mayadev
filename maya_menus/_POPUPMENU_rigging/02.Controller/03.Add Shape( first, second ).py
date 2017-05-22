import maya.cmds as cmds

sels = cmds.ls( sl=1 )

firstShape = cmds.listRelatives( sels[0], s=1, f=1 )[0]
target = sels[1]

cmds.parent( firstShape, target, add=1, shape=1 )