from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

for sel in sels[2:]:
    blendNode = sgcommands.createBlendTwoMatrixNode( sels[0], sels[1] )
    mm = sgcommands.createNode( 'multMatrix' )
    blendNode.matrixOutput() >> mm.i[0]
    sel.pim >> mm.i[1]
    dcmp = sgcommands.getDecomposeMatrix( mm )
    dcmp.outputRotate >> sel.r
    
    sel.addAttr( ln='blend', min=0, max=1, k=1, dv=0.5 )
    print sel.blend.name(), " >> ", blendNode.blend.name()
    sel.blend >> blendNode.blend