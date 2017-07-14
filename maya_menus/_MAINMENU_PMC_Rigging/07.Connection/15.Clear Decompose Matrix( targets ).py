import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    dcmp = sel.listConnections( s=1, d=0, type='decomposeMatrix' )
    pymel.core.delete( dcmp )