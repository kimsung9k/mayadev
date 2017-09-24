import maya.cmds as cmds
from sgModules import sgcommands

sels = cmds.ls( sl=1 )
curves = []
for sel in sels:
	try:
		sgcommands.addCurveDistanceInfo( sel )
		curves.append( sel )
	except:pass
cmds.select( curves )