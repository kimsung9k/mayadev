from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

cloneObjectGroups = []
for sel in sels:
    cloneObjectGroups.append( sgCmds.makeCloneObjectGroup( sel, connectionOn=1, shapeOn=1, cloneAttrName='cloneGeo' ) )
pymel.core.select( cloneObjectGroups )