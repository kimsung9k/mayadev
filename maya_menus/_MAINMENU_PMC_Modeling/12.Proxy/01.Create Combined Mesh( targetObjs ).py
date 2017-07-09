import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )
for sel in sels:
    print sel
    combinedMesh = sgCmds.combineMultiShapes( sel )
    combinedMesh.rename( sel.shortName() + '_combined' )