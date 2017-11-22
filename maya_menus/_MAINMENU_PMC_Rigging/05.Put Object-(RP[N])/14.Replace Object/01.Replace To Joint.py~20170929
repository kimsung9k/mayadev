from sgMaya import sgCmds
from maya import cmds

sels = cmds.ls( sl=1 )
newObjects = []
for sel in sels:
    newObject = cmds.createNode( 'joint' )
    newObject = sgCmds.replaceObject( sel, newObject )
    
    replaceNamedSel = cmds.rename( sel, 'replaceBefore_' + sel )
    newObject.rename( sel.split( '|' )[-1] )
    cmds.delete( replaceNamedSel )
    newObjects.append( newObject )
pymel.core.select( newObjects )