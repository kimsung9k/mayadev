import maya.cmds as cmds


def bake( setNode ):
    
    ns = setNode.replace( 'SET', '' )
    
    skinJnts = cmds.ls( ns + 'SkinJnt_*', type='joint' )
    skinJnts.append( ns + 'Grp_skinJnt' )
    
    cmds.select( skinJnts )
    
    ctlCons = []
    for skinJnt in skinJnts:
        if not cmds.nodeType( skinJnt ) in ['joint', 'transform']: continue
        cons = cmds.listConnections( skinJnt, s=1, d=0, p=1, c=1 )
        if not cons: continue
        ctlCons += cons
    
    minFrame = cmds.playbackOptions( q=1, min=1 )
    maxFrame = cmds.playbackOptions( q=1, max=1 )
    
    cmds.bakeResults( simulation=1, t=( minFrame, maxFrame ), sampleBy=1,
                       disableImplicitControl=True, preserveOutsideKeys=False, sparseAnimCurveBake=False,
                       removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False,
                       minimizeRotation=True, controlPoints=False, shape=False )
    
    for i in range( 0, len( ctlCons ), 2 ):
        srcCon = ctlCons[i+1]
        dstCon = ctlCons[i]
        
        if cmds.isConnected( srcCon, dstCon ):
            cmds.disconnectAttr( srcCon, dstCon )