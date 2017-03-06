from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
mtxNode = sgcommands.getFbfMatrix( sels[0], sels[1], sels[2] )
sgcommands.select( mtxNode )