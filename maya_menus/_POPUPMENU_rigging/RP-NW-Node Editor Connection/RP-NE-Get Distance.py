from sgModules import sgcommands

sels = cmds.ls( sl=1 )
distNodes = []
for sel in sels:
    distNode = sgcommands.getDistance( sel )
    distNodes.append( distNode )
sgcommands.select( distNodes )