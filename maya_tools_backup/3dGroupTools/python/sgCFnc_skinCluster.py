import maya.OpenMaya as om
import maya.cmds as cmds


def setWeightInnerPointsToTargetJoint( baseMesh, baseJoint, targetMeshs ):
    
    import sgBFunction_dag
    
    baseMeshShape = sgBFunction_dag.getShape( baseMesh )
    dagPathBaseMesh = sgBFunction_dag.getMDagPath( baseMeshShape )
    mtxBaseMesh = dagPathBaseMesh.inclusiveMatrix()
    headIntersector = om.MMeshIntersector()
    headIntersector.create( dagPathBaseMesh.node() )
    
    targetMeshs = cmds.ls( sl=1 )
    
    for targetMesh in targetMeshs:
    
        skinNodes = sgBFunction_dag.getNodeFromHistory( targetMesh ,'skinCluster')
        if not skinNodes: continue
        
        skinNode = skinNodes[0]
        fnSkinNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinNode ) )
        
        joints = cmds.listConnections( skinNode+'.matrix', s=1, d=0 )
        if not baseJoint in joints: continue
        indexInfluence = joints.index( baseJoint )
        
        plugWeightList = fnSkinNode.findPlug( 'weightList' )
        
        targetMeshShape = sgBFunction_dag.getShape( targetMesh )
        dagPathTargetMesh = sgBFunction_dag.getMDagPath( targetMeshShape )
        fnTargetMesh = om.MFnMesh( dagPathTargetMesh )
        
        mtxTarget = dagPathTargetMesh.inclusiveMatrix()
        mtxToBase = mtxTarget * mtxBaseMesh.inverse()
        
        numVertices = fnTargetMesh.numVertices()
        pointsTarget = om.MPointArray()
        fnTargetMesh.getPoints( pointsTarget )
        
        pointOnMesh = om.MPointOnMesh()
        
        targetVertices = []
        
        for i in range( numVertices ):
            pointLocal = pointsTarget[i] * mtxToBase
            headIntersector.getClosestPoint( pointLocal, pointOnMesh )
            
            point = pointOnMesh.getPoint()
            normal = om.MVector( pointOnMesh.getNormal() )
            
            vDir = om.MVector( pointLocal ) - om.MVector( point )
            
            if vDir * normal > 0: continue
            
            plugWeights = plugWeightList[i].child( 0 )
            for j in range( plugWeights.numElements() ):
                cmds.setAttr( plugWeights.name() + "[%d]" % j, 0 )
            
            cmds.setAttr( plugWeights.name() + "[%d]" % indexInfluence, 1 )
            targetVertices.append( targetMesh+'.vtx[%d]' % i )

        cmds.select( targetVertices )
            