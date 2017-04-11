import maya.cmds as cmds
import maya.OpenMaya as om


def mirrorObject( target ):

    import sgBFunction_convert

    nodeType = cmds.nodeType( target )
    mtx = cmds.getAttr( target+'.wm' )
    mirrorMtx = sgBFunction_convert.mirrorMatrix( mtx )
    
    mirrorName = sgBFunction_convert.convertSide( target )
    
    tr = cmds.createNode( nodeType, n= mirrorName.split( '|' )[-1] )
    cmds.xform( tr, ws=1, matrix=mirrorMtx )
    
    if nodeType != 'joint':
        cmds.setAttr( tr+'.dh', 1 )
    
    return tr



def mirrorTransform( target ):
    
    import sgBFunction_convert
    
    targetLocalName = target.split( '|' )[-1]
    mirrorTarget = sgBFunction_convert.convertSide( targetLocalName )
    
    if not cmds.objExists( mirrorTarget ):
        nodeType = cmds.nodeType( target )
        
        mtx = cmds.getAttr( target+'.wm' )
        mirrorMtx = sgBFunction_convert.mirrorMatrix( mtx )
        
        mirrorTarget = cmds.createNode( nodeType, n= mirrorTarget )
        cmds.xform( mirrorTarget, ws=1, matrix=mirrorMtx )
        
        dh = cmds.getAttr( target+'.dh' )
        cmds.setAttr( mirrorTarget+'.dh', dh )
    
    pTargets = cmds.listRelatives( target, p=1, f=1 )
    if pTargets:
        pMirrorTarget = mirrorTransform( pTargets[0] )
        pMirrorTargets = cmds.listRelatives( mirrorTarget, p=1, f=1 )
        if pMirrorTargets:
            if cmds.ls( pMirrorTarget ) != cmds.ls( pMirrorTargets[0] ):
                mirrorTarget = cmds.parent( mirrorTarget, pMirrorTarget )[0]
        else:
            mirrorTarget = cmds.parent( mirrorTarget, pMirrorTarget )[0]
    
    return mirrorTarget



def mirrorNode( target ):
    
    import sgBFunction_convert
    
    mirrorTarget = sgBFunction_convert.convertSide( target )
    
    if not cmds.objExists( mirrorTarget ):
        mirrorTarget = cmds.duplicate( target, n=mirrorTarget )[0]
    
    return mirrorTarget



def mirrorConnect( target ):
    
    import sgBFunction_attribute
    
    if cmds.nodeType( target ) in [ 'transform', 'joint' ]:
        mirrorTarget = mirrorTransform( target )
    else:
        mirrorTarget = mirrorNode( target )
    
    srcCons = cmds.listConnections( target, s=1, d=0, p=1, c=1 )
    
    outCons = srcCons[1::2]
    inCons  = srcCons[::2]
    
    for i in range( len( outCons ) ):
        outputNode, outputAttr = outCons[i].split( '.' )
        inputAttr = inCons[i].split( '.' )[-1]
        
        if cmds.nodeType( outputNode ) in [ 'transform', 'joint' ]:
            mirrorOutputNode = mirrorTransform( outputNode )
        else:
            mirrorOutputNode = mirrorNode( outputNode )
        
        if not cmds.attributeQuery( outputAttr, node=mirrorOutputNode, ex=1 ):
            sgBFunction_attribute.copyAttribute( outputNode+'.'+outputAttr, mirrorOutputNode )
        if not cmds.attributeQuery( inputAttr, node=mirrorTarget, ex=1 ):
            sgBFunction_attribute.copyAttribute( target+'.'+inputAttr, mirrorTarget )

        if not cmds.isConnected( mirrorOutputNode+'.'+outputAttr, mirrorTarget+'.'+inputAttr ):
            cmds.connectAttr( mirrorOutputNode+'.'+outputAttr, mirrorTarget+'.'+inputAttr )
    
    return mirrorTarget



def mirrorRig( transformNode ):

    import sgBModel_data
    import sgBFunction_dag
    
    sgBModel_data.mirrorRigCheckedTargets = []
    targetParents = sgBFunction_dag.getParents( transformNode )
    
    targetParents.append( transformNode )
    
    for i in range( len( targetParents ) ):
        mirrorConnect( targetParents[i] )
