from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

cloneObjectGroups = []
for sel in sels:
    cloneObjectGroups.append( sgCmds.createBoundingBoxCubeConnected( sel ) )
pymel.core.select( cloneObjectGroups )