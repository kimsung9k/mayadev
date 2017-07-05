from sgMaya import sgCmds
reload( sgCmds )

sels = pymel.core.ls( sl=1 )

for sel in sels:
    replaceList = ['_L_', '_R_']
    if sel.find( '_R_' ) != -1:
        replaceList = ['_R_', '_L_']
        
    selChildren = sel.listRelatives( c=1, ad=1, type='transform' )
    selChildren.append( sel )
    
    duSel = pymel.core.duplicate( sel, n=sel.replace( *replaceList ) )[0]
    duSelChildren = duSel.listRelatives( c=1, ad=1, type='transform' )
    duSelChildren.append( duSel )
    
    symmetryMtxLists = []
    for i in range( len( selChildren ) ):
        symmetryMtx = sgCmds.getSymmetryMatrix( cmds.getAttr( selChildren[i].name() + '.wm' ), 0 )
        symmetryMtxList = sgCmds.getListFromMatrix( symmetryMtx )
        symmetryMtxLists.append( symmetryMtxList )
        duSelChildren[i].rename( selChildren[i].replace( *replaceList ) )
    
    duSelChildren.reverse()
    symmetryMtxLists.reverse()
    shapeReverseMatrix = [-1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1]
    
    for i in range( len( duSelChildren ) ):
        pymel.core.xform( duSelChildren[i], ws=1, matrix= symmetryMtxLists[i] )
        duChildShape = duSelChildren[i].getShape()
        if not duChildShape: continue
        sgCmds.editShapeByMatrix( duChildShape, shapeReverseMatrix )