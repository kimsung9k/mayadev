from sgMaya import sgCmds

import pymel.core
sels = pymel.core.ls( sl=1 )

curve = sels[0]
upObject = sels[1]
targets = sels[2:]

for target in targets:
    sgCmds.tangentContraint( curve, upObject, target.getParent() )