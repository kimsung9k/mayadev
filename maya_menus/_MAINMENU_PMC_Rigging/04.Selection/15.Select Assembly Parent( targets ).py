import pymel.core
sels = pymel.core.ls( sl=1 )
asmList = []
for sel in sels:
    parents = sel.getAllParents()
    parents.insert( 0, sel )
    for parent in parents:
        if parent.nodeType() in ['assemblyReference','assemblyDefinition']:
            asmList.append( parent )
            break
pymel.core.select( asmList )