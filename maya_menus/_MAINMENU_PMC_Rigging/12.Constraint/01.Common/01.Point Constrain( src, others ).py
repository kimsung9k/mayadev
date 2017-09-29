from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
src = sels[0]
others = sels[1:]

for other in others:
    sgCmds.constrain_point( src, other )