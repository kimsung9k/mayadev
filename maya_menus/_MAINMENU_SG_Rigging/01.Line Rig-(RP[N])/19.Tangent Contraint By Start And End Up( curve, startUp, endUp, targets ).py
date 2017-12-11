from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

curve = sels[0]
startUp = sels[1]
endUp = sels[2]
targets = sels[3:]

sgCmds.tangentContraintByStartAndEndUp( curve, startUp, endUp, targets )