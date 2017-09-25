from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
for sel in sels:
    selP = sel.parent()
    transform = sgcommands.createNode( 'transform', n= 'P'+ sel.localName() )
    if selP:
        sgcommands.parent( transform, selP )
    transform.xform( ws=1, matrix= sel.wm.get() )
    sgcommands.parent( sel, transform )