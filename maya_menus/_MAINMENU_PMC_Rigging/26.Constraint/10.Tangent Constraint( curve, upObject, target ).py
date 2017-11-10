from sgMaya import sgCmds

import pymel.core
sels = pymel.core.ls( sl=1 )

curve = sels[0]
upObject = sels[1]
target = sels[2]

sgCmds.tangentContraint( curve, upObject, target )