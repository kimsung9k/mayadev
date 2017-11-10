from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
blendTwoMatrixNode = sgCmds.getBlendTwoMatrixNode( sels[0], sels[1] )
print blendTwoMatrixNode