import pymel.core
skinClusters = pymel.core.ls( type='skinCluster' )
for skin in skinClusters:
    skin.envelope.set( 1 )