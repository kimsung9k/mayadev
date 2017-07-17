import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels[1:]:
	pymel.core.parentConstraint( sels[0], sel.getParent(), mo=1 )