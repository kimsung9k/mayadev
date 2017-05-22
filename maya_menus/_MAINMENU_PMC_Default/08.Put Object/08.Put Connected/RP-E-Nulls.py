from sgModules import sgcommands
from maya import cmds

sels = cmds.ls( sl=1 )
for sel in sels:
    newObj = sgcommands.putObject( sel, 'null' )
    cmds.connectAttr( sel + '.t', newObj + '.t' )
    cmds.connectAttr( sel + '.r', newObj + '.r' )
    cmds.connectAttr( sel + '.s', newObj + '.s' )