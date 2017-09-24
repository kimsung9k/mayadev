from sgModules import sgcommands
sels = cmds.ls( sl=1 )
for sel in sels:
	sgcommands.addOptionAttribute( sel )