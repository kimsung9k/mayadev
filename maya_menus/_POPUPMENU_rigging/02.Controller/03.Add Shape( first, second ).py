import maya.cmds as cmds

sels = cmds.ls( sl=1 )

firstShape = cmds.listRelatives( sels[0], s=1, f=1 )[0]
target = sels[1]

newTr = cmds.createNode( 'transform' )
cmds.parent( firstShape, newTr, add=1, shape=1 )
duTr = cmds.duplicate( newTr )[0]
duTrShape = cmds.listRelatives( duTr, s=1, f=1 )[0]
cmds.parent( duTrShape, target, add=1, shape=1 )
cmds.delete( newTr, duTr )