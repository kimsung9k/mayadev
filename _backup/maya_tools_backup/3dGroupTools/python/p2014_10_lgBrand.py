import maya.cmds as cmds



def getConstJnt( jnt ):
    
    import sgRigAttribute
    
    sgRigAttribute.addAttr( jnt, ln='ConstJnt', at='message' )
    
    cons = cmds.listConnections( jnt+'.ConstJnt', s=1, d=0 )
    if cons: return cons[0]
    
    mmdc = cmds.createNode( 'sgMultMatrixDecompose' )
    constJnt = cmds.createNode( 'joint' )
    constJntGrp = cmds.group( constJnt )
    cmds.setAttr( constJnt+'.radius', 2 )
    
    cmds.connectAttr( jnt+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( constJntGrp+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', constJntGrp+'.t' )
    cmds.connectAttr( mmdc+'.or', constJntGrp+'.r' )

    cmds.connectAttr( constJnt+'.message', jnt+'.ConstJnt' )

    return constJnt



def connectGear( objs, jnt ):
    
    import sgModelDag
    import sgRigDag
    import sgRigAttribute
    
    for obj in objs:
        size = sgModelDag.getBoundingBoxSize( obj, ws=1 )
        
        sgRigAttribute.addAttr( jnt, ln='size', dv=size[0] )
        
        constJnt = getConstJnt( jnt )
        geometryConstObj = sgRigDag.getGeometryConstObj( constJnt )
        
        obj = sgModelDag.getTransform( obj )
        cmds.parent( obj, geometryConstObj )




def connectChild( parent, child ):
    
    parentSize = cmds.getAttr( parent+'.size' )
    childSize = cmds.getAttr( child+'.size' )
    
    pConstJnt = getConstJnt( parent )
    cConstJnt = getConstJnt( child )
    
    try:
        unit = cmds.listConnections( pConstJnt+'.rz' )[0]
        pConstJntCon = cmds.listConnections( unit+'.input', s=1, d=0, p=1, c=1 )[1]
    except:
        pConstJntCon = cmds.listConnections( pConstJnt+'.rz', s=1, d=0, p=1, c=1 )[1]
    
    multNode = cmds.createNode( 'multDoubleLinear' )
    
    cmds.connectAttr( pConstJntCon, multNode+'.input1' )
    cmds.setAttr( multNode+'.input2', -parentSize/childSize )
    
    cmds.connectAttr( multNode+'.output', cConstJnt+'.rz' )



def connectRotateGearAttr( ctl, others ):
    
    import sgRigAttribute
    
    sgRigAttribute.addAttr( ctl, ln='rotateGear', k=1 )
    
    for other in others:
        
        sgRigAttribute.addAttr( other, ln='rotateGear', k=1 )
        sgRigAttribute.addAttr( other, ln='globalMult', k=1, dv=1 )
    
        addNode = cmds.createNode( 'addDoubleLinear' )
        multNode = cmds.createNode( 'multDoubleLinear' )
        
        cmds.connectAttr( other+'.rotateGear', addNode+'.input1' )
        cmds.connectAttr( ctl+'.rotateGear', multNode+'.input1' )
        cmds.connectAttr( other+'.globalMult', multNode+'.input2' )
        cmds.connectAttr( multNode+'.output', addNode+'.input2' )
        
        cmds.connectAttr( addNode+'.output', other+'.rotateZ' )
