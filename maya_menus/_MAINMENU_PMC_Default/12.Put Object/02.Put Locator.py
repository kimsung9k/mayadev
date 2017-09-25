from sgModules import sgcommands
from maya import cmds

sels = cmds.ls( sl=1 )
sgcommands.putObject( sels, 'locator' )