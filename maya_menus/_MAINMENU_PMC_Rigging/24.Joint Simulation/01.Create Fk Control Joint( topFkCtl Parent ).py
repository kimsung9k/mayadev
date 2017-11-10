import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )
for sel in sels:
    sgCmds.createFkControlJoint( sel )