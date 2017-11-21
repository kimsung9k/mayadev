import pymel.core
sels = pymel.core.ls( sl=1 )

targetGrp = sels[-1]

targets = []

for sel in sels[:-1]:
    allParents = sel.getAllParents()
    for parent in allParents:
        if parent == targetGrp:
            targets.append( sel )
            break

pymel.core.select( targets )