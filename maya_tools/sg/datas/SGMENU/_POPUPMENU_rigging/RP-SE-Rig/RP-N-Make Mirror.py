from sgModules import sgcommands
from sgModules import sgbase

nodes = sgcommands.listNodes( sl=1 )
for node in nodes:
    newNode = sgcommands.putObject( [node], node.nodeType(), 'transform' )[0]
    sgcommands.setMirror( newNode )
    newNode.rename( sgbase.convertSideString( node.name() ) )
    newNode.attr( 'dh' ).set( node.attr( 'dh' ).get() )