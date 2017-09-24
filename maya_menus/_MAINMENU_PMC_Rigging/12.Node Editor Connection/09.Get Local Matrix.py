from sgModules import sgcommands
from maya import cmds

sels = cmds.ls( sl=1 )
node = sgcommands.getLocalMatrix( sels[0], sels[1] )
sgcommands.select( node )