import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

sgCmds.constrainToCurve( sels[0], sels[1], sels[2].getParent() )