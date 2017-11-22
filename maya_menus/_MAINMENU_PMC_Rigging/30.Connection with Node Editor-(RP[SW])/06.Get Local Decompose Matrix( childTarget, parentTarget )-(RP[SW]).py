from sgMaya import sgCmds
from maya import cmds
import pymel.core

sels = cmds.ls( sl=1 )
targets = sels[:-1]
parentTarget = sels[-1]
dcmps = []
for target in targets:
    node = sgCmds.getLocalMatrix( target, parentTarget )
    dcmp = sgCmds.getDecomposeMatrix(node)
    dcmps.append( dcmp )
pymel.core.select( dcmps )