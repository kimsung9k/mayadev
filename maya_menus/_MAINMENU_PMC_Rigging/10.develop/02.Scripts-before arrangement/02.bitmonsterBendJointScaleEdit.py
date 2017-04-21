from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
jnts = sels[:-1]
targetJnt = sels[-1]
targetP = targetJnt.parent()

sumNodeOrig = sgcommands.createNode( 'plusMinusAverage' )
sumNodeCurrent = sgcommands.createNode( 'plusMinusAverage' )
scaleNode = sgcommands.createNode( 'multiplyDivide' ).setAttr( 'op', 2 )

for i in range( len( jnts ) ):
    jnt = jnts[i]
    sel = sgcommands.getDecomposeMatrix( sgcommands.getLocalMatrix( jnt, targetP ) )
    distNode = sgcommands.createNode( 'distanceBetween' )
    sel.ot >> distNode.point1
    distNode.addAttr( ln='origDist', k=1, dv= distNode.distance.get() )
    
    distNode.origDist >> sumNodeOrig.input1D[i]
    distNode.distance >> sumNodeCurrent.input1D[i]

sumNodeCurrent.output1D >> scaleNode.input1X
sumNodeOrig.output1D >> scaleNode.input2X

scaleNode.outputX >> targetJnt.sy
scaleNode.outputX >> targetJnt.sz