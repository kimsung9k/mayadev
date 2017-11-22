from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

aimTarget = sels[0]
baseTarget = sels[1]
jntTarget = sels[2]

dcmp = sgCmds.getLocalDecomposeMatrix( aimTarget.wm, baseTarget.wim )
angleNode = sgCmds.getAngleNode( dcmp.ot )
compose = pymel.core.createNode( 'composeMatrix' )
angleNode.euler >> compose.ir
multMatrix = pymel.core.createNode( 'multMatrix' )
compose.outputMatrix >> multMatrix.i[0]
baseTarget.wm >> multMatrix.i[1]
jntTarget.pim >> multMatrix.i[2]
dcmp = sgCmds.getDecomposeMatrix( multMatrix.matrixSum )
dcmp.ot >> jntTarget.t
dcmp.outputRotate >> jntTarget.r
if jntTarget.nodeType() == 'joint':
    jntTarget.jo.set( 0,0,0 )