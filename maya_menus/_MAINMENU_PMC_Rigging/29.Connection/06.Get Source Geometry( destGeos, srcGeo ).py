from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels[:-1]:
    sgCmds.getSourceGeometry( sel, sels[-1] )