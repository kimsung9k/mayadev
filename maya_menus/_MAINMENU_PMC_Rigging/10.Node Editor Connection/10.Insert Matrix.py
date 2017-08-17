from sgModules import sgcommands
sels = sgcommands.listNodes( sl=1 )
sgcommands.insertMatrix( sels[0], sels[1] )