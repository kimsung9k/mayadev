import maya.cmds as cmds
import maya.OpenMaya as om


class model:
    
    fnMesh = om.MFnMesh()
    numVtx = 0
    numPoly = 0
    mPointArr = om.MPointArray()
    mCountArr = om.MIntArray()
    verticesInFaces = []
    facesInVertices = []
    normals = om.MFloatVectorArray()
    nearestDists = om.MDoubleArray()
    weights   = om.MFloatArray()
    circleNames = []
    checkLevels = om.MIntArray()
    continueIndex = om.MIntArray()
    
    def clear( cls ):
        cls.fnMesh = om.MFnMesh()
        cls.numVtx = 0
        cls.numPoly = 0
        cls.mPointArr = om.MPointArray()
        cls.mCountArr = om.MIntArray()
        cls.verticesInFaces = []
        cls.facesInVertices = []
        cls.normals = om.MFloatVectorArray()
        cls.nearestDists = om.MDoubleArray()
        cls.weights = om.MFloatArray()
        cls.circleNames = []
        cls.checkLevels = om.MIntArray()
        cls.continueIndex = om.MIntArray()
    
    clear = classmethod( clear )



def getPolyCreateInfo( meshName ):
    
    model.clear()
    
    selList = om.MSelectionList()
    selList.add( meshName )
    path = om.MDagPath()
    selList.getDagPath( 0,path )
    
    fnMesh = om.MFnMesh( path )
    model.fnMesh = fnMesh
    meshMatrix = path.inclusiveMatrix()
    meshMtxList = []
    
    for i in range( 4 ):
        for j in range( 4 ):
            meshMtxList.append( meshMatrix( i, j ) )
    
    model.numVtx  = fnMesh.numVertices()
    model.numPoly = fnMesh.numPolygons()
    model.mPointArr = om.MPointArray()
    model.mCountArr = om.MIntArray()
    model.mConnectArr = om.MIntArray()
    
    fnMesh.getPoints( model.mPointArr )
    fnMesh.getNormals( model.normals )
    
    model.mCountArr.setLength( model.numPoly )
    
    model.checkLevels.setLength( model.numVtx )
    model.nearestDists.setLength( model.numVtx )
    for i in range( model.numVtx ):
        model.facesInVertices.append( om.MIntArray() )
        model.checkLevels[i] = -1
        model.nearestDists[i] = 10000000.0
        model.circleNames.append( '' )
        
    for i in range( model.numPoly ):
        model.mCountArr[i] = fnMesh.polygonVertexCount( i )
        intArr = om.MIntArray()
        fnMesh.getPolygonVertices( i, intArr )
        
        model.verticesInFaces.append( intArr )
        
        for j in range( intArr.length() ):
            model.facesInVertices[intArr[j]].append( i )
            
    model.checkIndicesLen = 0


def createCircleFromVtxToDistanceArea( startIndex, createCircleDist, scaleDefault = 1.0 ):
    
    model.checkLevels[startIndex] = 0
    
    pointVtx = model.mPointArr[startIndex]
    
    model.circleNames[startIndex] = cmds.createNode( 'joint' )
    cmds.setAttr( model.circleNames[startIndex]+'.t', pointVtx.x, pointVtx.y, pointVtx.z )
    cmds.setAttr( model.circleNames[startIndex]+'.type', 18 )
    cmds.setAttr( model.circleNames[startIndex]+'.otherType', '%5.2f'  %( scaleDefault ), type='string' )
    cmds.setAttr( model.circleNames[startIndex]+'.radius', scaleDefault )
    cmds.setAttr( model.circleNames[startIndex]+'.drawLabel', 0 )
    
    def recursiveFunction( index, level, sumDist ):

        facesInVertex = model.facesInVertices[index]
        
        vtxIndexList = []
        for faceIndex in facesInVertex:
            for vtxIndex in model.verticesInFaces[ faceIndex ]:
                if not vtxIndex in vtxIndexList:
                    vtxIndexList.append( vtxIndex )
        
        pointBaseVtx = model.mPointArr[index]
        recursiveVerticesIndices = []
        for vtxIndex in vtxIndexList:
            if model.checkLevels[ vtxIndex ] != -1:
                if model.checkLevels[ vtxIndex ] <= level:
                    continue
            model.checkLevels[ vtxIndex ] = level + 1
            
            pointCurrentVtx = model.mPointArr[vtxIndex]
            twoPointDist = pointBaseVtx.distanceTo( pointCurrentVtx )
            cuDist = twoPointDist + sumDist
            
            if cuDist > createCircleDist:
                continue
            
            if model.nearestDists[vtxIndex] > twoPointDist:
                model.nearestDists[vtxIndex] = twoPointDist
            else:
                continue
            
            distRate = (1 - cuDist/createCircleDist)
            radiusRate = distRate*scaleDefault
            
            if not model.circleNames[vtxIndex]:
                model.circleNames[vtxIndex] = cmds.createNode( 'joint' )
                cmds.setAttr( model.circleNames[vtxIndex]+'.t', pointCurrentVtx.x, pointCurrentVtx.y, pointCurrentVtx.z )
                cmds.setAttr( model.circleNames[vtxIndex]+'.type', 18 )
                cmds.setAttr( model.circleNames[vtxIndex]+'.drawLabel', 0 )
            else:
                pass

            cmds.setAttr( model.circleNames[vtxIndex]+'.radius', radiusRate )
            cmds.setAttr( model.circleNames[vtxIndex]+'.otherType', '%5.2f'  %radiusRate, type='string' )
            recursiveVerticesIndices.append( vtxIndex )
        
        for vtxIndex in recursiveVerticesIndices:
            recursiveFunction( vtxIndex, model.checkLevels[ vtxIndex ], cuDist )
            
    recursiveFunction( startIndex, 0, 0.0 )



def printCheckIndices():
    
    print model.checkIndicesLen