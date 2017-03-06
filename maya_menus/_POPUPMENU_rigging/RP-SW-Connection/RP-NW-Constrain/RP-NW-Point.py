from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
sgcommands.constrain_point( sels[0], sels[1] )