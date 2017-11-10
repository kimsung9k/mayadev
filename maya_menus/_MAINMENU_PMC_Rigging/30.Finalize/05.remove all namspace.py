import pymel.core
nsList = pymel.core.namespaceInfo( lon=1 )

for ns in nsList:
    nodes = pymel.core.ls( ns + ':*' )
    if not len( nodes ): continue
    for node in nodes:
        node.rename( node.replace( ns + ':', '' ) )
    pymel.core.namespace( rm=ns )