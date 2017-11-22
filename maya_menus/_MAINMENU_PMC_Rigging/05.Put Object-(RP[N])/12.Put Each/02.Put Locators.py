from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1, fl=1 )
newObjects = []
for sel in sels:
    newObject = sgCmds.putObject( sel, 'locator' )
    newObjects.append( newObject )
pymel.core.select( newObjects )