from sgModules import sgcommands

sels = cmds.ls( sl=1 )
sgcommands.lookAt( sels[0], sels[1] )