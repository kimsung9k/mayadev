import pymel.core
sels = pymel.core.ls( sl=1 )
grp = pymel.core.createNode( 'transform', n='animObjects' )
pymel.core.parent( sels, grp )
pymel.core.select( grp )