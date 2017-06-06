from sgModules import sgcommands
import maya.cmds as cmds

sels = cmds.ls( sl=1, fl=1 )
newObjects = []
for sel in sels:
    newObject = sgcommands.putObject( sel, 'joint' )
    newObjects.append( newObject )
sgcommands.select( newObjects )