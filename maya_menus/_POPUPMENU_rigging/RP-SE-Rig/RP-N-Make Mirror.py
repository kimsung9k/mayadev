from sgModules import sgcommands

nodes = sgcommands.listNodes( sl=1 )
for node in nodes:
    newNode = sgcommands.putObject( node, node.nodeType(), 'transform' )
    sgcommands.setMirror( newNode )
    newNode = sgcommands.convertSg( newNode )
    newNode.rename( sgcommands.convertSideString( node.name() ) )
    newNode.attr( 'dh' ).set( node.attr( 'dh' ).get() )