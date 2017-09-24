from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
first = sels[0]
second = sels[1]
target = sels[2]
sgCmds.blendTwoMatrixConnect( first, second, third )