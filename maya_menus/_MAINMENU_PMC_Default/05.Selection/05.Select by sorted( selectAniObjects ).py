from maya import cmds
sels = cmds.ls( sl=1 )
sels.sort()
cmds.select( sels )