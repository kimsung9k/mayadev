import maya.cmds as cmds
import sgRigAttribute


def connectMeshAtScaleObjectControl( first, second ):    

    secondShape = cmds.listRelatives( second, s=1 )[0]
    
    def getConedObject( ctl ):
        import sgRigAttribute
        
        sgRigAttribute.addAttr( ctl, ln='conedObject', at='message' )
        condObjs = cmds.listConnections( ctl+'.conedObject' )
        if condObjs: return condObjs[0]
        
        conedObj = cmds.createNode( 'transform', n='ConedObj_' + ctl )
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( ctl+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( conedObj+'.pim', mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', conedObj+'.t' )
        cmds.connectAttr( mmdc+'.or', conedObj+'.r' )
        cmds.connectAttr( mmdc+'.os', conedObj+'.s' )
        cmds.connectAttr( mmdc+'.osh', conedObj+'.sh' )
        
        cmds.connectAttr( conedObj+'.message', ctl+'.conedObject', f=1 )
        return conedObj
    
    def getOriginalMatrixObject( target ):
        mmdc = cmds.listConnections( target, type='multMatrixDecompose' )
        if not mmdc:
            return cmds.listConnections( target+'.t', s=1, d=0 )[0]
        mmdc = mmdc[0]
        srcObj = cmds.listConnections( mmdc+'.i[0]' )[0]
        if cmds.nodeType( srcObj ) == 'transform': return srcObj
        return cmds.listConnections( srcObj, s=1, d=0 )[0]
    
    mainGrp = 'TransformObject_Grp'
    if not cmds.objExists( mainGrp ):
        cmds.createNode( 'transform', n=mainGrp )
    
    mesh = cmds.createNode( 'mesh' )
    meshObj = cmds.listRelatives( mesh, p=1 )[0]
    trObj = cmds.rename( meshObj, second+'_trObj' )
    mesh = cmds.listRelatives( trObj, s=1 )[0]
    cmds.connectAttr( secondShape+'.outMesh', mesh+'.inMesh' )
    
    secondShapeMtx = cmds.getAttr( secondShape+'.wm' )
    cmds.xform( trObj, ws=1, matrix=secondShapeMtx )
    
    conedObj = getConedObject( first )
    cmds.parent( trObj, conedObj )
    
    firstP = cmds.listRelatives( first, p=1 )[0]
    originMtxObj = getOriginalMatrixObject( firstP )
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( second+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( originMtxObj+'.wim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', trObj+'.t' )
    cmds.connectAttr( mmdc+'.or', trObj+'.r' )
    cmds.connectAttr( mmdc+'.os', trObj+'.s' )
    cmds.connectAttr( mmdc+'.osh', trObj+'.sh' )
    
    conedObjP = cmds.listRelatives( conedObj, p=1 )
    if not conedObjP: conedObjP = []
    if not mainGrp in conedObjP:
        cmds.parent( conedObj, mainGrp )
    
    cmds.setAttr( second+'.v', 0 )
    
    cmds.select( first )