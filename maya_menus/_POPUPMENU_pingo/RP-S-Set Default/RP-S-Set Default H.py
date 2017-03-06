import sgProject.pingo as pingo
from sgModules import sgcommands

sels = cmds.ls( sl=1 )
parents = sgcommands.getParents( sels[0] )
rootName = parents[0].name().split( ':' )[-1]

for sel in sels:
	exec( 'inst = sgcommands.SymmetryControl( sel, pingo.%s )' % rootName )
	instH = inst.allChildren()
	for h in instH:
		h.setDefault()