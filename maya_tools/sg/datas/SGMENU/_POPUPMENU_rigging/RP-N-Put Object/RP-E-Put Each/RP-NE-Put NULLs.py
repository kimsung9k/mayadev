from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
newObjects = sgcommands.putObject( sels, 'null', 'transform' )
sgcommands.select( newObjects )