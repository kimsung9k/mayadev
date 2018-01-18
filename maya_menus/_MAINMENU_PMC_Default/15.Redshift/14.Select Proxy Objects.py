import pymel.core
proxyNodes = pymel.core.ls( type='RedshiftProxyMesh' )

targets = []
for proxyNode in proxyNodes:
    targets += [ target for target in proxyNode.listConnections( s=0, d=1, type='mesh' ) ]
    
pymel.core.select( targets )