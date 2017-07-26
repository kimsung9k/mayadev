import pymel.core
sels = pymel.core.ls( sl=1 )
sels[-1].rename( 'Geometry' )