from sgMaya import sgCmds, sgRig
import pymel.core
sels = pymel.core.ls( sl=1 )
grp = pymel.core.group( sels )
sgRig.setMatrixToCenterPoint( grp )
pymel.core.select( grp )