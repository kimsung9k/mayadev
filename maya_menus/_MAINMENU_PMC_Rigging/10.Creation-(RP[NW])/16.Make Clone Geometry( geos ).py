from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

cloneObjects = []
for sel in sels:
    cloneObjects.append( sgCmds.makeCloneObject( sel, connectionOn=1, shapeOn=1, cloneAttrName='cloneGeo' ) )
pymel.core.select( cloneObjects )