from sgModules import sgcommands
from maya import cmds

sels = sgcommands.listNodes( sl=1 )
nodes = []
for sel in sels:
    node = sgcommands.getDecomposeMatrix( sel )
    nodes.append( node )
sgcommands.select( nodes )