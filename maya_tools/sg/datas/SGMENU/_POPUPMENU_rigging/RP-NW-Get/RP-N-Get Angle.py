from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
angleNodes = []
for sel in sels:
    angleNode = sgcommands.getAngle( sel )
    angleNodes.append( angleNode )
sgcommands.select( angleNodes )