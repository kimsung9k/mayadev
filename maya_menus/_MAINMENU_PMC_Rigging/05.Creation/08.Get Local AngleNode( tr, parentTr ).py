from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
sgCmds.getLocalAngleNode( sels[0], sels[1] )