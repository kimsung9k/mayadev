from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
crossVectorNode = sgcommands.getCrossVectorNode( sels[0], sels[1] )
sgcommands.select( crossVectorNode )