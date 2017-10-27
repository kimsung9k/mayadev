from sgModules import sgcommands
from maya import cmds

sels = cmds.ls( sl=1 )
targets = sels[:-1]
parentTarget = sels[-1]
dcmps = []
for target in targets:
    node = sgcommands.getLocalMatrix( target, parentTarget )
    dcmp = sgcommands.getDecomposeMatrix(node)
    dcmps.append( dcmp )
sgcommands.select( dcmps )