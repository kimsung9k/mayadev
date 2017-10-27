import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )
sgCmds.createFkControlJoint( sels[0] )