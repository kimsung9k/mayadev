from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

blendNode = sgCmds.getBlendTwoMatrixNode( sels[0], sels[1] )
mm = pymel.core.createNode( 'multMatrix' )
sgCmds.matrixOutput( blendNode ) >> mm.i[0]
sels[2].pim >> mm.i[1]
dcmp = sgCmds.getDecomposeMatrix( mm.matrixSum )
dcmp.ot >> sels[2].t
dcmp.outputRotate >> sels[2].r

sgCmds.addAttr( sels[2], ln='blend', min=0, max=1, k=1, dv=0.5 )
sels[2].blend >> blendNode.blend