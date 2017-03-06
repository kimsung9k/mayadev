import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelMesh
import sgModelSkinCluster
import sgModelDg
import maya.mel as mel

import sgModelDag
import sgModelConvert



def autoCopyWeight( first, second ):
    
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
            
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        cmds.skinCluster( bindObjs, tsb=1 )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )




def replaceObjectSkined( first, second ):
    
    secondParents = sgModelDag.getParents( second )

    if secondParents:
        secondTopParentMMtx = sgModelDag.getMMatrix( secondParents[0] )
    else:
        secondTopParentMMtx = om.MMatrix()
    secondMMtx = sgModelDag.getMMatrix( second )
    secondLocalMMtx = secondMMtx * secondTopParentMMtx.inverse()
    
    secondLocalMtx = sgModelConvert.convertMMatrixToMatrix( secondLocalMMtx )
    
    if cmds.reference( first, inr=1 ):
        first = cmds.duplicate( first )[0]
    
    if secondParents:
        first = cmds.parent( first, secondParents[0] )[0]
    cmds.xform( first, matrix=secondLocalMtx, os=1 )
    if secondParents:
        if not secondParents[-1] in cmds.listRelatives( first, p=1, f=1 ):
            first = cmds.parent( first, secondParents[-1] )[0]
    
    
    autoCopyWeight( second, first )
    
    cmds.delete( second )



def removePositiveNormalInfluence( selectedObjs ):
    
    mesh, vtxIndices = sgModelMesh.getMeshAndIndicesPoints( selectedObjs )
    
    skinClusterNode = sgModelDag.getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusterNode: return None
    skinClusterNode = skinClusterNode[0]
    
    influenceAndWeightList = sgModelSkinCluster.getInfluenceAndWeightList( mesh )
    
    fnMesh = sgModelMesh.getFnMesh( mesh )
    meshInvMatrix = sgModelDag.getDagPath( mesh ).inclusiveMatrixInverse()
    meshPoints = sgModelMesh.getLocalPoints( mesh )
    plugMatrix = sgModelSkinCluster.getPlugMatrix( mesh )
    
    #normal = om.MVector()
    percentRate = 100.0/len( vtxIndices )
    currentRate = 0.0
    for i in vtxIndices:
        
        influenceList, childInfluenceList, weights = influenceAndWeightList[i]
        
        for j in range( len( influenceList ) ):
            jointMatrix = sgModelDg.getMatrixFromPlug( plugMatrix.elementByLogicalIndex( influenceList[j] ) )
            jointPointOnLocalMesh = om.MPoint( jointMatrix(3,0), jointMatrix(3,1), jointMatrix(3,2) )*meshInvMatrix
            
            vMeshPoint = om.MVector( meshPoints[i]-jointPointOnLocalMesh )
            interPoints = om.MPointArray()
            fnMesh.intersect( om.MPoint( jointPointOnLocalMesh ), vMeshPoint, interPoints )
            lengthMeshPoint = vMeshPoint.length()*0.99999
            
            if not interPoints.length(): continue
            if om.MVector( interPoints[0] - jointPointOnLocalMesh ).length() < lengthMeshPoint:
                weights[j] = 0
        
        allWeights = 0.0
        for weight in weights:
            allWeights += weight
        if allWeights == 0:
            continue
        
        for j in range( len( weights ) ):
            logicalIndex = influenceList[j]
            cmds.setAttr( skinClusterNode+'.weightList[%d].weights[%d]' %( i, logicalIndex ), weights[j]/allWeights )
        
        currentRate += percentRate
        
        print "%6.2f" %currentRate +  "% caculated" 

    


def setInverseSkinCluster( skinedObject, shapedObject, target ):
    
    skinCluster = sgModelDag.getNodeFromHistory( skinedObject, 'skinCluster' )
    if not skinCluster: return None
    skinCluster = skinCluster[0]
    
    targetShape = sgModelDag.getShape( target )
    shapedShape = sgModelDag.getShape( shapedObject )
    origShape = sgModelDag.getOrigShape( skinedObject )
    cmds.connectAttr( origShape+'.outMesh', targetShape+'.inMesh', f=1 )
    
    invSkinCluster = cmds.deformer( target, type='inverseSkinCluster' )[0]

    cmds.connectAttr( skinCluster+'.message', invSkinCluster+'.targetSkinCluster' )
    cmds.connectAttr( skinedObject+'.wm', invSkinCluster+'.geomMatrix' )
    cmds.connectAttr( shapedShape+'.outMesh', invSkinCluster+'.inMesh' )




def setInfluenceParentAsBindFre( mesh ):
    
    skinCluster = sgModelDag.getNodeFromHistory( mesh, 'skinCluster' )[0]
    
    cons = cmds.listConnections( skinCluster+'.matrix', type='joint', p=1, c=1, s=1, d=0 )
    
    outputs = cons[1::2]
    inputs  = cons[::2]
    
    for i in range( len( outputs ) ):
        jnt   = outputs[i].split( '.' )[0]
        jntP  = cmds.listRelatives( jnt, p=1, f=1 )[0]
        output = jntP+'.wim'
        input_ = inputs[i].replace( 'matrix', 'bindPreMatrix' )
        
        print output, input_
        
        if cmds.isConnected( output, input_ ): continue
        cmds.connectAttr( output, input_, f=1 )