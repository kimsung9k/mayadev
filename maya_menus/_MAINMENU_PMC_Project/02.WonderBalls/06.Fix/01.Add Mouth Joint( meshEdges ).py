import pymel.core

curveTr, curveNode = pymel.core.polyToCurve( form=2, degree=1 )

curveNode = pymel.core.ls( curveNode )[0]
compose = pymel.core.createNode( 'composeMatrix' )
mm = pymel.core.createNode( 'multMatrix' )
dcmp =  pymel.core.createNode( 'decomposeMatrix' )
pymel.core.select( 'Center_joint' )
tr = pymel.core.joint( n='Mouth_joint' )
compose.outputMatrix >> mm.i[0]
tr.pim >> mm.i[1]
mm.o >> dcmp.imat
dcmp.ot >> tr.t

averageNode = pymel.core.createNode( 'plusMinusAverage' )
averageNode.op.set( 3 )

for i in range( 4 ):
    paramValue = 1.0/4
    curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
    curveNode.outputcurve >> curveInfo.inputCurve
    curveInfo.top.set( 1 )
    curveInfo.parameter.set( paramValue * i )
    curveInfo.position >> averageNode.input3D[i]

averageNode.output3D >> compose.it
pymel.core.delete( curveTr )
pymel.core.select( tr )