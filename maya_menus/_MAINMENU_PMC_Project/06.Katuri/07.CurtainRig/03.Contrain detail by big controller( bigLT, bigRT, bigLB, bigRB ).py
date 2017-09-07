import pymel.core
sels = pymel.core.ls( sl=1 )

grid0 = sels[0]
grid1 = sels[1]
grid2 = sels[2]
grid3 = sels[3]

minRow, minCol = [ int( i ) for i in grid0.split( '_' )[-2:] ]
maxRow, maxCol = [ int( i ) for i in grid3.split( '_' )[-2:] ]

rowList = [ i for i in range( minRow, maxRow+1 ) ]
colList = [ i for i in range( minCol, maxCol+1 ) ]

def getRowWeight( first, second, target ):
    firstPos  = pymel.core.xform( first, q=1, ws=1, t=1 )
    secondPos = pymel.core.xform( second, q=1, ws=1, t=1 )
    targetPos = pymel.core.xform( target, q=1, ws=1, t=1 )
    length = secondPos[0] - firstPos[0]
    weight = (targetPos[0]-firstPos[0])/length
    revWeight = 1.0 - weight
    return weight ** 2, revWeight ** 2


def getColWeight( first, second, target ):
    firstPos  = pymel.core.xform( first, q=1, ws=1, t=1 )
    secondPos = pymel.core.xform( second, q=1, ws=1, t=1 )
    targetPos = pymel.core.xform( target, q=1, ws=1, t=1 )
    length = secondPos[1] - firstPos[1]
    weight = (targetPos[1]-firstPos[1])/length
    revWeight = 1.0 - weight
    return weight ** 2, revWeight ** 2
    

targetDts = []
for row in rowList:
    for col in colList:
        targetDetail = pymel.core.ls( 'Ctl_detail_%d_%d' % ( row, col ) )[0].getParent()
        if col == minCol and row == minRow:
            constrain = pymel.core.parentConstraint( grid0, targetDetail, mo=1 )
        elif col == maxCol and row == minRow:
            constrain = pymel.core.parentConstraint( grid2, targetDetail, mo=1 )
        elif col == minCol and row == maxRow:
            constrain = pymel.core.parentConstraint( grid1, targetDetail, mo=1 )
        elif col == maxCol and row == maxRow:
            constrain = pymel.core.parentConstraint( grid3, targetDetail, mo=1 )
        elif col == minCol:
            constrain = pymel.core.parentConstraint( grid0, grid1, targetDetail, mo=1 )
            weight, revWeight = getRowWeight( grid0, grid1, targetDetail )
            constrain.w0.set( revWeight )
            constrain.w1.set( weight )
        elif row == minRow:
            constrain = pymel.core.parentConstraint( grid0, grid2, targetDetail, mo=1 )
            weight, revWeight = getColWeight( grid0, grid2, targetDetail )
            constrain.w0.set( revWeight )
            constrain.w1.set( weight )
        elif col == maxCol:
            constrain = pymel.core.parentConstraint( grid2, grid3, targetDetail, mo=1 )
            weight, revWeight = getRowWeight( grid2, grid3, targetDetail )
            constrain.w0.set( revWeight )
            constrain.w1.set( weight )
        elif row == maxRow:
            constrain = pymel.core.parentConstraint( grid1, grid3, targetDetail, mo=1 )
            weight, revWeight = getColWeight( grid1, grid3, targetDetail )
            constrain.w0.set( revWeight )
            constrain.w1.set( weight )
        else:
            constrain = pymel.core.parentConstraint( grid0, grid1, grid2, grid3, targetDetail, mo=1 )
            rowWeight, revRowWeight = getRowWeight( grid0, grid1, targetDetail )
            colWeight, revColWeight = getColWeight( grid0, grid2, targetDetail )
            constrain.w0.set( revRowWeight*revColWeight )
            constrain.w1.set( rowWeight*revColWeight )
            constrain.w2.set( revRowWeight*colWeight )
            constrain.w3.set( rowWeight*colWeight )

