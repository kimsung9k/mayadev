import pymel.core
sels = cmds.ls( 'Ctl_*', type='joint' )

for sel in sels:
    sel = pymel.core.ls( sel )[0]
    newNode = pymel.core.createNode( 'transform' )
    
    selP = sel.listRelatives( p=1 )
    if selP:
        pymel.core.parent( newNode, selP[0] )
    
    selShapes = sel.listRelatives( s=1 )
    for selShape in selShapes:
        pymel.core.parent( selShape, newNode, add=1, shape=1 )
    
    dstCons = sel.listConnections( s=0, d=1, p=1, c=1 )
    for origCon, dstCon in dstCons:
        if not cmds.attributeQuery( origCon.attrName(), node=newNode.name(), ex=1 ): continue
        origAttr = origCon.name().replace( sel.name(), newNode.name() )
        cmds.connectAttr( origAttr, dstCon.name(), f=1 )