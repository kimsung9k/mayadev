import pymel.core
sels = pymel.core.ls( sl=1 )

if not pymel.core.pluginInfo( 'matrixNodes.mll', q=1, l=1 ):
    pymel.core.loadPlugin( 'matrixNodes.mll' )

def putObject( typ='null' ):
    
    if typ == 'joint':
        newObject = pymel.core.createNode( 'joint' )
    elif typ == 'locator':
        newObject = pymel.core.spaceLocator()[0]
    else:
        newObject = pymel.core.createNode( 'transform' )
        newObject.dh.set( 1 )
    return newObject
        

for sel in sels:
    
    selShape = sel.getShape()
    if selShape:
        sel = selShape
    
    averageNode = pymel.core.createNode( 'plusMinusAverage' )
    averageNode.op.set( 3 )
    sel.boundingBoxMin >> averageNode.input3D[0]
    sel.boundingBoxMax >> averageNode.input3D[1]
    
    pointer = putObject( 'locator' )
    composeMtx =  pymel.core.createNode( 'composeMatrix' )
    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' ); mm.o >> dcmp.imat
    
    averageNode.output3D >> composeMtx.it
    
    composeMtx.outputMatrix >> mm.i[0]
    sel.parentMatrix >> mm.i[1]
    pointer.pim >> mm.i[2]
    
    dcmp.ot >> pointer.t