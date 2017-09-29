from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
distNodes = []
for sel in sels:
    distNode = sgMaya.getDistance( sel )
    distNodes.append( distNode )
pymel.core.select( distNodes )