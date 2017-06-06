import maya.cmds as cmds
from sgMaya import sgCmds
sels = cmds.ls( sl=1 )

ctl = sels[0]
meshs = sels[1:]

for mesh in meshs:
	wobbleDeformer, handle = cmds.deformer( mesh, type='wobble' )
	cmds.parent( handle, ctl )

	sgCmds.addAttr( ctl, ln='speed', k=1, min=0 )
	sgCmds.addAttr( ctl, ln='weight', k=1, min=0 )

	cmds.connectAttr( ctl + '.speed', wobbleDeformer + '.timeFrequency' )
	cmds.connectAttr( ctl + '.weight', wobbleDeformer + '.Strength' )