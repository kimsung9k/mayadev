import pymel.core
sels = pymel.core.ls( dag=1 )
instanceObjects = []
for sel in sels:
    selParents = sel.listRelatives( allParents=1 )
    if len( selParents ) == 1: continue
    instanceObjects += selParents
pymel.core.select( instanceObjects )