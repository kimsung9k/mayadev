import pymel.core
sels = pymel.core.ls( pymel.core.polyListComponentConversion( pymel.core.ls( sl=1 ), tv=1 ), fl=1 )
from sgMaya import sgCmds

average = pymel.core.createNode( 'plusMinusAverage' )
pointer = pymel.core.createNode( 'transform' )
pointer.dh.set( 1 )
average.output3D >> pointer.t
average.op.set(3)
for i in range( len( sels )-1 ):
    pointOnCurve = sgCmds.getPointOnCurveFromMeshVertex( sels[i] )
    pointOnCurve.position >> average.input3D[i]