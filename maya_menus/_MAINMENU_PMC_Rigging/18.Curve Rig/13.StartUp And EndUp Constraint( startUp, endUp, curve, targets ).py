from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

startUp = sels[0]
endUp = sels[1]
curve = sels[2]
targets = sels[3:]

for target in targets:
    sgCmds.tangentContraintByStartAndEndUp( startUp, endUp, curve, target )