import maya.cmds as cmds



def mirrorObject( targets ):
    
    import sgBFunction_convert
    
    targets = sgBFunction_convert.singleToList( targets )
    
    for target in targets:
        mtx = cmds.getAttr( target+'.wm' )
        mirrorMtx = sgBFunction_convert.mirrorMatrix( mtx )
        
        tr = cmds.createNode( 'transform', n=sgBFunction_convert.convertSide( target ) )
        cmds.xform( tr, ws=1, matrix=mirrorMtx )
        
        cmds.setAttr( tr+'.dh', 1 )