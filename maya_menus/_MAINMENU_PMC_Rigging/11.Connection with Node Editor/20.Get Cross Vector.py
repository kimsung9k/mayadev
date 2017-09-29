from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
crossVectorNode = sgCmds.getCrossVectorNode( sels[0], sels[1] )
pymel.core.select( crossVectorNode )