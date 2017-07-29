import pymel.core
dcmps = []
for target in pymel.core.ls( sl=1 ):
    dcmps += target.listConnections( s=1, d=0, type='decomposeMatrix' )
pymel.core.delete( dcmps )