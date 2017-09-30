from sgModules import sgcommands
nodes = sgcommands.listNodes( sl=1 )
for node in nodes:
    md = sgcommands.createNode( 'multDoubleLinear' )
    node.scalarOutput() >> md.input1