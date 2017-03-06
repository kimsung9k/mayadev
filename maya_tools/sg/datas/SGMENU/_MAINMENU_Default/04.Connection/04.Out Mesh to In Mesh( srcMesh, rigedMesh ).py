from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

srcMesh = sels[0]
dstMesh = sels[1]

orig = sgcommands.getOrigShape( dstMesh )
srcMesh.shape().attr( 'outMesh' ) >> orig.attr( 'inMesh' )