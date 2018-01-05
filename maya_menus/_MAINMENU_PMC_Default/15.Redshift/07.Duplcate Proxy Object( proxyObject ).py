import pymel.core
sels = pymel.core.ls( sl=1 )

for sel in sels:
    duSel = pymel.core.duplicate( sel )[0]
    selShapes = sel.listRelatives( s=1 )
    duShapes  = duSel.listRelatives( s=1 )
    
    for i in range( len( selShapes ) ):
        selShape = selShapes[i]
        duShape = duShapes[i]
        cons = selShape.listConnections( s=1, d=0, p=1, c=1 )
        if not cons: continue
        for origCon, srcCon in cons:
            pymel.core.connectAttr( srcCon, duShape + '.' + origCon.longName() )