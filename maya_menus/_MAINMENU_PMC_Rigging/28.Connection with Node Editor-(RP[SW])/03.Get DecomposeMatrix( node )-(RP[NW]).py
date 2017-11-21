from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
nodes = []
for sel in sels:
    node = sgCmds.getDecomposeMatrix( sel )
    nodes.append( node )
pymel.core.select( nodes )