import maya.cmds as cmds

def createControllerOnTarget( target, pivotCtlOn=True ):

    import sgBFunction_connection
    import sgBFunction_dag
    import sgBModel_data
    targetPos = cmds.getAttr( target+'.wm' )
    targetP = cmds.listRelatives( target, p=1, f=1 )[0]
    
    targetName = target.split( '|' )[-1]
    ctl = cmds.circle( n='CTL_' + targetName )[0]
    ctlChild = cmds.createNode( 'transform', n='CTLChild_'+targetName );ctlChild = cmds.parent( ctlChild, ctl )[0]
    pivCtl = cmds.createNode( 'transform', n='PivCTL_'+targetName  ); cmds.setAttr( pivCtl+'.dh', 1 )
    cmds.setAttr( pivCtl+'.overrideEnabled', 1 )
    cmds.setAttr( pivCtl+'.overrideColor', 18 )
    ctlP = cmds.group( ctl, n='P'+ctl )
    ctlPPiv = cmds.group( ctlP, pivCtl, n='Piv' + ctlP )
    cmds.xform( ctlPPiv, ws=1, matrix=targetPos )

    cloneObject = sgBFunction_dag.getConstrainedObject( targetP )
    ctlPPiv = cmds.parent( ctlPPiv, cloneObject )[0]
    cmds.xform( pivCtl, os=1, matrix= sgBModel_data.getDefaultMatrix() )
    
    ctl = cmds.listRelatives( ctlP, c=1, f=1 )[0]
    sgBFunction_connection.getSourceConnection( target, ctlPPiv )

    for attr in [ 't', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz', 'sh' ]:
        cons = cmds.listConnections( target+'.'+attr, s=1, d=0, p=1, c=1 )
        if not cons: continue
        for i in range( 0, len( cons ), 2 ):
            cmds.disconnectAttr( cons[i+1], cons[i] )
    
    sgBFunction_connection.constraintAll( ctlChild, target )
    
    cmds.connectAttr( pivCtl+'.t',  ctlP+'.t' )
    cmds.connectAttr( pivCtl+'.r',  ctlP+'.r' )
    cmds.connectAttr( pivCtl+'.s',  ctlP+'.s' )
    cmds.connectAttr( pivCtl+'.sh', ctlP+'.sh' )
    
    mmdcCtlChild = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( ctlPPiv+'.wm', mmdcCtlChild+'.i[0]' )
    cmds.connectAttr( pivCtl+'.wim', mmdcCtlChild+'.i[1]' )
    cmds.connectAttr( mmdcCtlChild+'.ot',  ctlChild+'.t' )
    cmds.connectAttr( mmdcCtlChild+'.or',  ctlChild+'.r' )
    cmds.connectAttr( mmdcCtlChild+'.os',  ctlChild+'.s' )
    cmds.connectAttr( mmdcCtlChild+'.osh', ctlChild+'.sh' )
    
    ctlShape = sgBFunction_dag.getShape( ctl )
    circleNode = cmds.listConnections( ctlShape+'.create', s=1, d=0 )[0]
    
    mm = cmds.createNode( 'multMatrix' )
    trGeo = cmds.createNode( 'transformGeometry' )
    
    cmds.connectAttr( ctlPPiv+'.wm', mm+'.i[0]' )
    cmds.connectAttr( pivCtl+'.wim', mm+'.i[1]' )
    
    cmds.connectAttr( circleNode+'.outputCurve', trGeo+'.inputGeometry' )
    cmds.connectAttr( mm+'.matrixSum', trGeo+'.transform' )
    cmds.connectAttr( trGeo+'.outputGeometry', ctlShape+'.create', f=1 )
    
    return ctl