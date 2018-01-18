import pymel.core

proxyMeshNodes = pymel.core.ls( type='RedshiftProxyMesh' )
proxyConnectedMeshs = [ proxyMeshNode.listConnections( s=0, d=1 )[0] for proxyMeshNode in proxyMeshNodes if proxyMeshNode.listConnections( s=0, d=1 ) ]

origObjectPathAttrs = pymel.core.ls( '*.origObjectPath' )
for proxyConnectedMesh in proxyConnectedMeshs:
    if not pymel.core.attributeQuery( 'origObjectPath',  node=proxyConnectedMesh, ex=1 ): continue
    path = proxyConnectedMesh.attr( 'origObjectPath' ).get()
    targetProxyAttr = proxyConnectedMesh.getShape().inMesh.listConnections( s=1, d=0, p=1 )[0]
    
    for origObjectPathAttr in origObjectPathAttrs:
        if path != origObjectPathAttr.get(): continue
        node = origObjectPathAttr.node()
        if pymel.core.isConnected( targetProxyAttr, node.attr( 'inMesh' ) ): continue
        targetProxyAttr >> node.inMesh