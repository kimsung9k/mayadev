from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

blendNode = sgcommands.getBlendTwoMatrixNode( sels[0], sels[1] )
mm = sgcommands.createNode( 'multMatrix' )
blendNode.matrixOutput() >> mm.i[0]
sels[2].pim >> mm.i[1]
dcmp = sgcommands.getDecomposeMatrix( mm )
dcmp.outputRotate >> sels[2].r

sels[2].addAttr( ln='blend', min=0, max=1, k=1, dv=0.5 )
sels[2].blend >> blendNode.blend