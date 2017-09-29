from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
src = sels[-1]
others = sels[:-1]

for other in others:
    sgCmds.constrain_parent( src, other )