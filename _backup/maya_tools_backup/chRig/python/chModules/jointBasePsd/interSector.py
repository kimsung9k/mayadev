import maya.OpenMaya as om


def getCloseIndices( firstMesh, secondMesh ):
    
    intersector = om.MMeshIntersector()
    
    snapPoints = om.MPointArray()
    basePoints = om.MPointArray()
    
    selList = om.MSelectionList()
    selList.add( firstMesh )
    selList.add( secondMesh )
    
    fObj = om.MObject()
    sObj = om.MObject()
    
    selList.getDependNode( 0, fObj )
    selList.getDependNode( 1, sObj )
  
    intersector.create( sObj, om.MMatrix() )
    fnFMesh = om.MFnMesh( fObj )
    fnSMesh = om.MFnMesh( sObj )
    
    fnFMesh.getPoints( snapPoints )
    fnSMesh.getPoints( basePoints )
    
    meshPoint = om.MPointOnMesh()
    
    vtxList = om.MIntArray()
    for i in range( snapPoints.length() ):
        intersector.getClosestPoint( snapPoints[i], meshPoint )
        faceIndex = meshPoint.faceIndex()
        fnSMesh.getPolygonVertices( faceIndex, vtxList )
        
        minDistance = 999999.0
        
        closeVtxIndex = 0
        for j in range( vtxList.length() ):
            vtxIndex = vtxList[j]
            
            cuDistance = basePoints[vtxIndex].distanceTo( snapPoints[i] )
            if cuDistance < minDistance:
                minDistance = cuDistance
                closeVtxIndex = vtxIndex
                if minDistance < 0.0001:
                    break
                
    print "isDone"