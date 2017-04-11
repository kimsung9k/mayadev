import maya.cmds as cmds
import sgModelConvert


def combineMultiShapes( shapeObjs ):
    
    mtxGroup = cmds.getAttr( shapeObjs[0]+'.wm' )
    mmtxInvGroup = sgModelConvert.convertMatrixToMMatrix( mtxGroup ).inverse()
    
    shapes = cmds.listRelatives( shapeObjs[1:], c=1, ad=1, type='shape', f=1 )
    
    for shape in shapes:
        shapeType = cmds.nodeType( shape )
        
        shapeTransform = cmds.listRelatives( shape, p=1 )[0]
        
        mtxShapeTransform = cmds.getAttr( shapeTransform+'.wm' )
        
        mmtxShapeTransform = sgModelConvert.convertMatrixToMMatrix( mtxShapeTransform )
        mmtxLocal = mmtxShapeTransform * mmtxInvGroup
        
        mtxLocal = sgModelConvert.convertMMatrixToMatrix( mmtxLocal )
        trGeoNode = cmds.createNode( 'transformGeometry' )
        
        outputShapeNode = cmds.createNode( shapeType )
        outputShapeObject = cmds.listRelatives( outputShapeNode, p=1 )[0]
        if shapeType == 'mesh':
            outputAttr = 'outMesh'
            inputAttr = 'inMesh'
        elif shapeType == 'nurbsCurve':
            outputAttr = 'local'
            inputAttr  = 'create'
        elif shapeType == 'nurbsSurface':
            outputAttr = 'local'
            inputAttr = 'create'
        else:
            continue
            
        cmds.connectAttr( shape+'.'+outputAttr, trGeoNode+'.inputGeometry' )
        cmds.setAttr( trGeoNode+'.transform', mtxLocal, type='matrix' )
        cmds.connectAttr( trGeoNode+'.outputGeometry', outputShapeNode+'.'+inputAttr )
        
        outputShapeNode = cmds.parent( outputShapeNode, shapeObjs[0], add=1, shape=1 )
        cmds.delete( outputShapeObject )
        cmds.rename( outputShapeNode, shapeObjs[0]+'Shape' )
        cmds.refresh()
    
    cmds.delete( shapeObjs[1:])
    
    return shapeObjs[0]


mc_combineMultiShapes = """import maya.cmds as cmds
import sgRigController
sels = cmds.ls( sl=1 )
sgRigController.combineMultiShapes( sels )"""



def addScaleControlObjectToSkined( ctl, target ):
    
    import sgModelDag
    
    def getMultMtx( ctl, outputAttr ):
        
        ctlP = cmds.listRelatives( ctl, p=1 )[0]
        jntMms  = cmds.listConnections( outputAttr, type='multMatrix' )
        ctlPMms = cmds.listConnections( ctlP+'.wim', type='multMatrix' )
        ctlMms  = cmds.listConnections( ctl+'.wm', type='multMatrix' )
        
        if not jntMms:  jntMms = []
        if not ctlPMms: ctlPMms = []
        if not ctlMms:  ctlMms = []
        
        targetMms = []
        for jntMm in jntMms:
            if jntMm in ctlMms and jntMm in ctlPMms:
                targetMms.append( jntMm )
        
        if targetMms: return targetMms[0]
        
        mm = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( outputAttr, mm+'.i[0]' )
        cmds.connectAttr( ctlP+'.wim', mm+'.i[1]' )
        cmds.connectAttr( ctl+'.wm', mm+'.i[2]' )
        
        return mm
    
    skinClusters = sgModelDag.getNodeFromHistory( target, 'skinCluster' )
    if not skinClusters: return None
    
    targetSkinCluster = skinClusters[0]
    
    cons = cmds.listConnections( targetSkinCluster+'.matrix', s=1, d=0, p=1, c=1 )
    
    for i in range( 0, len( cons ), 2 ):
        outputAttr = cons[i+1]
        mmNode = getMultMtx( ctl, outputAttr )
        if not cmds.isConnected( mmNode+'.matrixSum', cons[i] ):
            cmds.connectAttr( mmNode+'.matrixSum', cons[i], f=1 )