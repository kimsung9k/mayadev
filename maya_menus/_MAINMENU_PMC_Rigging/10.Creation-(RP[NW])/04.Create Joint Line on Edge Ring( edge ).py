from sgMaya import sgCmds

sels = pymel.core.ls( sl=1, fl=1 )
edgeRings = sgCmds.getOrderedEdgeRings( sels[0] )

beforeObject = None
for edgeRing in edgeRings:
    pymel.core.select( edgeRing )
    cmds.SelectEdgeLoopSp()
    loopEdges = pymel.core.ls( sl=1, fl=1 )
    jnt = sgCmds.putObject( loopEdges, typ='joint' )
    if beforeObject:
        jnt.setParent( beforeObject )
    beforeObject = jnt