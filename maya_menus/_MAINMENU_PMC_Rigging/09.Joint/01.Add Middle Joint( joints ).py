from sgModules import sgcommands
sels = cmds.ls( sl=1 )
middleJnts = []
for sel in sels:
    middleJnt = sgcommands.addMiddleJoint( sel )
    middleJnts.append( middleJnt )
cmds.select( middleJnts )