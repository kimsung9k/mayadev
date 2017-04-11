import maya.cmds as cmds


def displayModCombine( sels ):
    import sgBFunction_dag
    
    targetMeshObjs = []
    
    sels = cmds.listRelatives( sels, s=1, f=1 )
    
    for sel in sels:
        if cmds.getAttr( sel+'.io' ): continue
        selP = cmds.listRelatives( sel, p=1, f=1 )[0]
        if selP.find( 'display_' ) == -1: continue
        targetMeshObjs.append( selP )
    
    targetMeshObjs = list( set( targetMeshObjs ) )
    
    cmds.select( targetMeshObjs )
    
    for targetMesh in targetMeshObjs:
        displayMod = cmds.ls( targetMesh )[0]
        realMod    = displayMod.replace( 'display_', '' )
        
        if not cmds.objExists( realMod ): continue
        
        displayModShape = sgBFunction_dag.getShape( displayMod )
        realModShape     = sgBFunction_dag.getShape( realMod )
        
        displayOrig = sgBFunction_dag.getOrigShape( displayModShape )
        
        if not cmds.isConnected( realModShape+'.outMesh', displayOrig+'.inMesh' ):
            cmds.connectAttr( realModShape+'.outMesh', displayOrig+'.inMesh', f=1 )



def makeDisplayMod_deformed( baseModel ):
    
    import sgBFunction_dag
    targetShape = cmds.createNode( 'mesh' )
    baseShape = sgBFunction_dag.getShape( baseModel )
    cmds.connectAttr( baseShape+'.outMesh', targetShape+'.inMesh' )
    target = cmds.listRelatives( targetShape, p=1, f=1 )[0]
    cmds.select( target )
    cmds.sets( e=1, forceElement='initialShadingGroup' )
    cmds.xform( target, ws=1, matrix= cmds.getAttr( baseModel+'.wm' ) )
    return cmds.rename( target, 'display_' + baseModel.split( '|' )[-1] )



def makeDisplayMod( baseModel ):
    
    import sgBFunction_dag
    targetShape = cmds.createNode( 'mesh' )
    baseShape = sgBFunction_dag.getShape( baseModel )

    cmds.connectAttr( baseShape+'.outMesh', targetShape+'.inMesh' )
    cmds.refresh()
    cmds.disconnectAttr( baseShape+'.outMesh', targetShape+'.inMesh' )
    
    target = cmds.listRelatives( targetShape, p=1, f=1 )[0]
    cmds.select( target )
    cmds.sets( e=1, forceElement='initialShadingGroup' )
    cmds.xform( target, ws=1, matrix= cmds.getAttr( baseModel+'.wm' ) )
    return cmds.rename( target, 'display_' + baseModel.split( '|' )[-1] )