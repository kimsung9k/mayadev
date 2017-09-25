from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

lookTarget = sels[0]
rotTarget = sels[1]

lookAtChild = sgCmds.makeLookAtChild( lookTarget, rotTarget )
pymel.core.select( lookAtChild )