import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )
interPointers = sgCmds.makeInterPointer( sels )
pymel.core.select( sels[0], interPointers, sels[-1] )