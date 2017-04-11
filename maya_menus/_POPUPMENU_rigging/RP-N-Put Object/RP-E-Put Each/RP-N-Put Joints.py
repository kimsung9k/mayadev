from sgModules import sgcommands
import maya.cmds as cmds

sels = cmds.ls( sl=1 )
newObjects = []
for sel in sels:
    newObject = sgcommands.putObject( sel, 'joint', 'transform' )
    newObjects.append( newObject )
sgcommands.select( newObjects )