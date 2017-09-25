from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
first = sels[0]
second = sels[1]
target = sels[2]
blendTwoMatrixNode = sgCmds.getBlendTwoMatrixNode( first, second, local=1 )
dcmp = sgCmds.getDecomposeMatrix( blendTwoMatrixNode.matrixSum )
dcmp.ot >> target.t
dcmp.outputRotate >> target.r
sgCmds.addAttr( target, ln='blend', min=0, max=1, k=1 )
target.attr( 'blend' ) >> blendTwoMatrixNode.attr( 'blend' )