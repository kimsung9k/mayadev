import maya.cmds as cmds
import maya.OpenMaya as om


def replaceRivetMesh( source, target ):
    
    sourceShape = cmds.listRelatives( source, s=1, f=1 )[0]
    targetShape = cmds.listRelatives( target, s=1, f=1 )[0]
    
    nodes = list( set( cmds.listConnections( sourceShape, d=1, s=0, type='sgMatrixFromVertices' ) ) )
    
    import sgBFunction_dag
    
    fnSourceMesh  = om.MFnMesh( sgBFunction_dag.getMDagPath( sourceShape ) )
    fnTargetMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( targetShape ) )
    
    sourceMeshPoints = om.MPointArray()
    targetMeshPoints = om.MPointArray()
    fnSourceMesh.getPoints( sourceMeshPoints )
    fnTargetMesh.getPoints( targetMeshPoints )
    
    intersector = om.MMeshIntersector()
    intersector.create( fnTargetMesh.object() )
    
    for node in nodes:
        fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( node ) )
        plugVerticeId = fnNode.findPlug( 'verticeId' )
        
        pointOnMesh = om.MPointOnMesh()
        for i in range( plugVerticeId.numElements() ):
            logicalIndex = plugVerticeId[i].logicalIndex()
            pointSource = sourceMeshPoints[ logicalIndex ]
            
            intersector.getClosestPoint( pointSource, pointOnMesh )
            
            faceIndex = pointOnMesh.faceIndex()
            indicesVertices = om.MIntArray()
            fnTargetMesh.getPolygonVertices( faceIndex, indicesVertices )
            
            minDist = 100000.0
            closeIndex = indicesVertices[0]
            for j in range( indicesVertices.length() ):
                pointTarget = targetMeshPoints[ indicesVertices[j] ]
                dist = pointTarget.distanceTo( pointSource )
                if dist < minDist:
                    minDist = dist
                    closeIndex = indicesVertices[j]
            
            print plugVerticeId[i].name(), closeIndex
            cmds.setAttr( plugVerticeId[i].name(), closeIndex )

        cmds.connectAttr( targetShape+'.outMesh', node+'.inputMesh', f=1 )
        cmds.connectAttr( targetShape+'.worldMatrix[0]', node+'.inputMeshMatrix', f=1 )