import maya.cmds as cmds

import rigObject.meshRivetConnect.cmdModel
import sgRigAttribute
import sgModelDag



def closePointBlendToTargetMesh( jnts, mesh ):
    
    def rivetBlend( first, second ):
    
        firstP = cmds.listRelatives( first, p=1 )[0]
        
        blendTwoMatrix = cmds.createNode( 'blendTwoMatrix' )
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( firstP+'.wm', blendTwoMatrix+'.inMatrix1' )
        cmds.connectAttr( second+'.wm', blendTwoMatrix+'.inMatrix2' )
        
        cmds.connectAttr( blendTwoMatrix+'.outMatrix', mmdc+'.i[0]' )
        cmds.connectAttr( firstP+'.wim', mmdc+'.i[1]' )
        
        cmds.connectAttr( mmdc+'.ot', first+'.t' )
        
        sgRigAttribute.addAttr( first, ln='blend', min=0, max=1, k=1, dv=0.9 )
        
        cmds.connectAttr( first+'.blend', blendTwoMatrix+'.ab' )
    
    sels = jnts
    
    dcmp = cmds.createNode( 'decomposeMatrix' )
    closestPointOnMesh = cmds.createNode( 'closestPointOnMesh' )
    
    mesh = sgModelDag.getShape( mesh )
    
    cmds.connectAttr( mesh+'.outMesh', closestPointOnMesh+'.inMesh' )
    cmds.connectAttr( mesh+'.wm', closestPointOnMesh+'.inputMatrix' )
    cmds.connectAttr( dcmp+'.ot', closestPointOnMesh+'.inPosition', f=1 )
    
    for sel in sels:
        
        cmds.connectAttr( sel+'.wm', dcmp+'.imat', f=1 )
        
        vtxIndex = cmds.getAttr( closestPointOnMesh+'.closestVertexIndex' )
        
        rivetObject = rigObject.meshRivetConnect.cmdModel.createRivet( mesh, [vtxIndex], [vtxIndex],
                                                               [vtxIndex], [vtxIndex], [vtxIndex],
                                                               0, 1 )
        rivetBlend( sel, rivetObject )
        
        cmds.setAttr( sel+'.blend', 0.5 )
    
    cmds.delete( dcmp, closestPointOnMesh )