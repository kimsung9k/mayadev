from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
targets = sels[:-1]
parentTarget = sels[-1]
dcmps = []
for target in targets:
    node = sgCmds.getLocalMatrix( target.wm, parentTarget.wim )
    dcmp = sgCmds.getDecomposeMatrix(node.o)
    dcmps.append( dcmp )
pymel.core.select( dcmps )