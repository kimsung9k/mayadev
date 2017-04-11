from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

srcMesh = sels[0]
dstMesh = sels[1]

orig = sgcommands.getOrigShape( dstMesh )
if not orig:
    srcMesh.shape().attr( 'outMesh' ) >> dstMesh.shape().attr( 'inMesh' )
else:
    srcMesh.shape().attr( 'outMesh' ) >> orig.attr( 'inMesh' )