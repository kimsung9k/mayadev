import maya.cmds as cmds
from sgModules import sgcommands

sels = cmds.ls( sl=1 )

curve = sels[0]
others = sels[1:]

squashAttrName = sgcommands.addCurveSquashInfo( curve )

for other in others:
	cmds.connectAttr( curve + '.' + squashAttrName, other + '.sz' )

cmds.select( sels )