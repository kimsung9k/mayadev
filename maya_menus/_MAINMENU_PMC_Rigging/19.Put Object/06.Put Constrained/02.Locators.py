from sgModules import sgcommands
from maya import cmds

sels = cmds.ls( sl=1 )
for sel in sels:
    newObj = sgcommands.putObject( sel, 'locator' )
    sgcommands.constrain_parent( sel, newObj )