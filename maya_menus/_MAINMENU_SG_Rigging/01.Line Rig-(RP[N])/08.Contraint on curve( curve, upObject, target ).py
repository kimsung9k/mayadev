import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

for sel in sels[2:]:
    sgCmds.constrainToCurve( sels[0], sels[1], sel )

pymel.core.select( sels[0], sels[1] )