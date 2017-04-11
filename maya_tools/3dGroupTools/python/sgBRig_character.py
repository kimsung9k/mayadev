import maya.cmds as cmds
import maya.OpenMaya as om
import sgBFunction_dag



class PolygonsPerJoint:
    
    def __init__(self, meshName ):

        dagPathMesh = sgBFunction_dag.getMDagPath( meshName )
        self.fnMesh = om.MFnMesh( dagPathMesh )
        self.meshMatrix = dagPathMesh.inclusiveMatrix()
        
        self.checkPolygonMap  = om.MIntArray()
        self.startVtxIndexMap = om.MIntArray()
        self.checkVertexMap   = om.MIntArray()
        
        self.vtxCountPerPoly = om.MIntArray()
        self.vtxIndicesList  = om.MIntArray()
        
        self.fnMesh.getVertices( self.vtxCountPerPoly, self.vtxIndicesList )
        self.checkVertexMap.setLength( self.fnMesh.numVertices() )
        self.checkPolygonMap.setLength( self.fnMesh.numPolygons() )
        self.startVtxIndexMap.setLength( self.fnMesh.numPolygons() )
        
        startVtxIndex = 0
        
        for i in range( self.fnMesh.numVertices() ):
            self.checkVertexMap.set( 0, i )
        
        for i in range( self.fnMesh.numPolygons() ):
            self.checkPolygonMap.set( 0, i )
            self.startVtxIndexMap.set( startVtxIndex, i )
            startVtxIndex += self.vtxCountPerPoly[i]
        
        self.indicesCheckedPolygon  = []
        self.indicesCheckedVertices = []



    def check(self, index ):
        
        if not self.checkPolygonMap[ index ]:
            self.checkPolygonMap.set( 1, index )
            self.indicesCheckedPolygon.append( index )

        self.checkPolygonMap.set( 1, index )
        startVtxIndex = self.startVtxIndexMap[ index ]
        
        vtxCount = self.vtxCountPerPoly[ index ]
        
        for i in range( vtxCount ):
            vtxIndex = self.vtxIndicesList[ startVtxIndex+i ]
            if not self.checkVertexMap[ vtxIndex ]:
                self.checkVertexMap.set( 1, vtxIndex )
                self.indicesCheckedVertices.append( vtxIndex )



    def showPolygonIndices(self):
        
        indices=[]
        for i in range( self.checkPolygonMap.length() ):
            if self.checkPolygonMap[i]:
                indices.append( i )
        print indices



    def buildMesh( self ):
        
        newVerticeCounts = om.MIntArray()
        newVerticesIndices = om.MIntArray()

        self.indicesCheckedPolygon.sort()
        self.indicesCheckedVertices.sort()
        
        newPoints = om.MPointArray()
        newPoints.setLength( len( self.indicesCheckedVertices ) )
        
        origPoints = om.MPointArray()
        self.fnMesh.getPoints( origPoints )
        
        for i in range( newPoints.length() ):
            checkedIndex = self.indicesCheckedVertices[i]
            checkedPoint = origPoints[ checkedIndex ] * self.meshMatrix
            newPoints.set( checkedPoint, i )
        
        indicesCheckedVerticesMap = [ -1 for i in range( self.fnMesh.numVertices() ) ]
        for i in range( len( self.indicesCheckedVertices ) ):
            checkedVtxIndex = self.indicesCheckedVertices[i]
            indicesCheckedVerticesMap[ checkedVtxIndex ] = i

        for i in range( len( self.indicesCheckedPolygon ) ):
            polygonIndex = self.indicesCheckedPolygon[i]
            indices = om.MIntArray()
            self.fnMesh.getPolygonVertices( polygonIndex, indices )
            for j in range( indices.length() ):
                checkedVtxIndex = indices[j]
                vtxIndex = indicesCheckedVerticesMap[ checkedVtxIndex ]
                newVerticesIndices.append( vtxIndex )
            newVerticeCounts.append( indices.length() )
        
        fnMesh = om.MFnMesh()
        
        tr = cmds.createNode( 'transform' )
        trObj = sgBFunction_dag.getMObject( tr )
        
        fnMesh.create( len(self.indicesCheckedVertices), len(self.indicesCheckedPolygon), newPoints, newVerticeCounts, newVerticesIndices, trObj )
        
        return tr




class PolygonsPerJoint2:
    
    def __init__(self, meshName ):

        dagPathMesh = sgBFunction_dag.getMDagPath( meshName )
        self.fnMesh = om.MFnMesh( dagPathMesh )
        self.itMesh = om.MItMeshPolygon( dagPathMesh.node() )
        self.meshMatrix = dagPathMesh.inclusiveMatrix()
        self.numVertices = self.fnMesh.numVertices()
        self.numEdges    = self.fnMesh.numEdges()
        self.numPolygons = self.fnMesh.numPolygons()
        self.points = om.MPointArray()
        self.fnMesh.getPoints( self.points )
        
        self.checkVertexMap   = om.MIntArray()
        self.checkPolygonMap   = om.MIntArray()
        
        self.checkVertexMap.setLength( self.numVertices )
        for i in range( self.numVertices ):
            self.checkVertexMap.set( 0, i )
        self.checkPolygonMap.setLength( self.numPolygons )
        for i in range( self.numPolygons ):
            self.checkPolygonMap.set( 0, i )

        self.centerVtxExistsEdges = [ 0 for i in range( self.numEdges ) ]
        self.centerVtxPointPerEdges = [ om.MPoint() for i in range( self.numEdges ) ] 
        self.edgesPerPolygon = [ om.MIntArray() for i in range( self.numPolygons ) ]
        while not self.itMesh.isDone():
            self.itMesh.getEdges( self.edgesPerPolygon[self.itMesh.index()] )
            self.itMesh.next()

        self.renumberedVerticesMap = om.MIntArray()
        self.renumberedVerticesMap.setLength( self.numVertices )

        self.addVtxCurrentNum = 0
        self.addVerticesIndices = om.MIntArray()
        self.addVerticesPoints  = om.MPointArray()
        self.addVerticesCounts  = om.MIntArray()
        self.addVerticesIndices = om.MIntArray()


    def check(self, vtxIndex ):
        
        self.checkVertexMap.set( 1, vtxIndex )


    def getAllCheckedVerticesMap(self):
        
        allCheckedVerticesMap = om.MIntArray()
        allCheckedVerticesMap.setLength( self.numVertices )
        for i in range( self.fnMesh.numVertices() ):
            allCheckedVerticesMap.set( 0, i )
        
        for i in range( self.numPolygons ):
            indicesVertcies = om.MIntArray()
            self.fnMesh.getPolygonVertices( i, indicesVertcies )
            
            isAllChecked = True
            for j in range( indicesVertcies.length() ):
                if not self.checkVertexMap[ indicesVertcies[j] ]:
                    isAllChecked = False
                    break

            if isAllChecked:
                self.checkPolygonMap.set( 1, i )
                for j in range( indicesVertcies.length() ):
                    allCheckedVerticesMap.set( 1, indicesVertcies[j] )
        return allCheckedVerticesMap


    def getBuildMeshInfo( self ):
        
        verticesPoints = om.MPointArray()
        verticesCount = om.MIntArray()
        verticesIndices = om.MIntArray()
        
        allCheckedVerticesMap = self.getAllCheckedVerticesMap()
        mapIndicesRenumVtxForBuild = om.MIntArray()
        mapIndicesRenumVtxForBuild.setLength( self.numVertices )
        
        for i in range( self.numVertices ):
            mapIndicesRenumVtxForBuild.set( -1, i )
        
        checkedNum = 0
        for i in range( allCheckedVerticesMap.length() ):
            if allCheckedVerticesMap[i]:
                mapIndicesRenumVtxForBuild.set( checkedNum, i )
                verticesPoints.append( self.points[i]*self.meshMatrix )
                checkedNum += 1
        self.addVtxCurrentNum = checkedNum
        
        for i in range( self.numPolygons ):
            if not self.checkPolygonMap[i]: continue
            indicesVertcies = om.MIntArray()
            self.fnMesh.getPolygonVertices( i, indicesVertcies )
            
            for j in range( indicesVertcies.length() ):
                indexRenumVtx = mapIndicesRenumVtxForBuild[ indicesVertcies[j] ]
                if indexRenumVtx == -1:
                    return None
                verticesIndices.append( indexRenumVtx )
            verticesCount.append( indicesVertcies.length() )
        
        return verticesPoints.length(), verticesCount.length(), verticesPoints, verticesCount, verticesIndices
    

    def getBuildMeshInfo2(self):

        verticesPoints  = om.MPointArray()
        verticesCounts  = om.MIntArray()
        verticesIndices = om.MIntArray()
        
        appendedVerticesMap = [ -1 for i in range( self.numVertices + self.numEdges ) ]
        
        appendVtxCount = 0
        for i in range( self.numPolygons ):
            indicesEdges    = self.edgesPerPolygon[i]
            indicesVertices = om.MIntArray()
            self.fnMesh.getPolygonVertices( i, indicesVertices )
            verticesPerFaceCount = 0
            
            edgeVerticesIndices = []
            checkedVertices = []
            
            for k in range( indicesEdges.length() ):
                fIndexBefore, sIndexBefore = self.getEdgeVertices( indicesEdges[k] )
                
                indicesVerticesExistsMap = [ 0 for x in range( indicesVertices.length() ) ]
                for j in range( indicesVertices.length() ):
                    if fIndexBefore == indicesVertices[j] or sIndexBefore == indicesVertices[j]:
                        indicesVerticesExistsMap[j] = 1
                
                edgeVertices = []
                for j in range( indicesVertices.length() ):
                    if indicesVerticesExistsMap[j]:
                        edgeVertices.append( indicesVertices[j] )
                
                if k == indicesEdges.length()-1: edgeVertices.reverse()
                firstIndex, secondIndex = edgeVertices
                edgeVerticesIndices.append( edgeVertices )
                
                if self.checkVertexMap[ firstIndex ]:
                    checkedVertices.append( firstIndex )
                    if appendedVerticesMap[ firstIndex ] == -1:
                        appendedVerticesMap[ firstIndex ] = appendVtxCount
                        point = self.points[ firstIndex ]
                        verticesPoints.append( point * self.meshMatrix )
                        verticesIndices.append( appendVtxCount )
                        appendVtxCount += 1
                    else:
                        verticesIndices.append( appendedVerticesMap[ firstIndex ] )
                    verticesPerFaceCount += 1

                if self.checkVertexMap[ secondIndex ] != self.checkVertexMap[ firstIndex ]:
                    if appendedVerticesMap[ self.numVertices + indicesEdges[k] ] == -1:
                        appendedVerticesMap[ self.numVertices + indicesEdges[k] ] = appendVtxCount
                        point = self.getEdgeCenterVerticesPosition( indicesEdges[k] )
                        verticesPoints.append( om.MPoint( point )* self.meshMatrix )
                        verticesIndices.append( appendVtxCount )
                        appendVtxCount += 1
                    else:
                        verticesIndices.append( appendedVerticesMap[ self.numVertices + indicesEdges[k] ] )
                    verticesPerFaceCount += 1
            
            if verticesPerFaceCount > 2:
                verticesCounts.append( verticesPerFaceCount )
        
            #print i, edgeVerticesIndices
        
        #print verticesPoints.length(), appendVtxCount
        #print verticesCounts.length()
        #print verticesCounts
        #print verticesIndices
        
        return verticesPoints.length(), verticesCounts.length(), verticesPoints, verticesCounts, verticesIndices
    
    
    
    def getEdgeVertices(self, edgeIndex):
        
        mutil = om.MScriptUtil()
        mutil.createFromList( [0,0], 2 )
        ptrInt2 = mutil.asInt2Ptr()
        
        self.fnMesh.getEdgeVertices( edgeIndex, ptrInt2 )
        
        vtxIndexFirst  = om.MScriptUtil().getInt2ArrayItem( ptrInt2, 0, 0 )
        vtxIndexSecond = om.MScriptUtil().getInt2ArrayItem( ptrInt2, 0, 1 )
        
        return vtxIndexFirst, vtxIndexSecond
    
    
    
    def getEdgeCenterVerticesPosition(self, edgeIndex ):
        
        firstIndex, secondIndex = self.getEdgeVertices( edgeIndex )
        return ( om.MVector( self.points[ firstIndex ] ) + om.MVector( self.points[ secondIndex ] ) )/ 2


    def buildMesh( self ):
        
        numVertices, numPolygons, verticesPoints, verticesCounts, verticesIndices = self.getBuildMeshInfo()
        
        tr = cmds.createNode( 'transform' )
        trObj = sgBFunction_dag.getMObject( tr )
        
        fnMesh = om.MFnMesh()
        fnMesh.create( numVertices, numPolygons, verticesPoints, verticesCounts, verticesIndices, trObj )
        return tr


    def buildMesh2( self ):
        
        numVertices, numPolygons, verticesPoints, verticesCounts, verticesIndices = self.getBuildMeshInfo2()
        
        tr = cmds.createNode( 'transform' )
        trObj = sgBFunction_dag.getMObject( tr )
        
        fnMesh = om.MFnMesh()
        fnMesh.create( numVertices, numPolygons, verticesPoints, verticesCounts, verticesIndices, trObj )
        return tr
        




class JointsPerVertices:
    
    def __init__(self, skinCluster ):
        
        self.maxJointIndices = om.MIntArray()
        self.maxJointDagPath = om.MDagPathArray()
        
        fnSkinCluster = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinCluster ) )
        self.plugMatrix = fnSkinCluster.findPlug( 'matrix' )
        plugWeightList = fnSkinCluster.findPlug( 'weightList' )
        
        self.existConnectJoints = []
        logicalIndexMax = self.plugMatrix[ self.plugMatrix.numElements()-1 ].logicalIndex()
        
        self.jointLogicalIndexMap = [ -1 for i in range( logicalIndexMax+1 ) ]
        
        for i in range( self.plugMatrix.numElements() ):
            connection = om.MPlugArray()
            self.plugMatrix[i].connectedTo( connection, True, False )
            if connection.length():
                self.existConnectJoints.append( connection[0].node() )
                self.jointLogicalIndexMap[ self.plugMatrix[i].logicalIndex() ] = i
        
        self.maxJointIndices = om.MIntArray()
        self.maxJointIndices.setLength( plugWeightList.numElements() )
        for i in range( plugWeightList.numElements() ):
            plugWeights = plugWeightList[i].child( 0 )
    
            maxWeight = plugWeights[0].asFloat()
            mwJointIndex = plugWeights[0].logicalIndex()
            for j in range( 1, plugWeights.numElements() ):
                jointIndex = plugWeights[j].logicalIndex()
                cuWeight = plugWeights[j].asFloat()
                if cuWeight > maxWeight:
                    maxWeight = cuWeight
                    mwJointIndex = jointIndex
            self.maxJointIndices.set( mwJointIndex, i )


    def getJointIndex(self, vtxIndex ):
        
        return self.maxJointIndices[ vtxIndex ]
    



def separateMeshBySkinWeight( meshObj ):
    
    import sgBFunction_connection
    
    skinClusters = sgBFunction_dag.getNodeFromHistory( meshObj, 'skinCluster' )
    meshShape    = sgBFunction_dag.getShape( meshObj )
    
    if not skinClusters: return []
    skinCluster = skinClusters[0]
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshShape ) )
    
    jntsPerVertices = JointsPerVertices( skinCluster )
    polygonsPerJointArray = [ PolygonsPerJoint( meshShape ) for i in range( len( jntsPerVertices.existConnectJoints ) ) ]
    
    vtxCountsPerPolygon = om.MIntArray()
    vtxIndices = om.MIntArray()
    fnMesh.getVertices( vtxCountsPerPolygon, vtxIndices )
    
    try:
        vtxIndexPerPolygon = 0
        for i in range( fnMesh.numPolygons() ):
            vtxCountPerPolygon = vtxCountsPerPolygon[i]
            for j in range( vtxCountPerPolygon ):
                vtxIndex = vtxIndices[ vtxIndexPerPolygon + j ]
                jointIndex = jntsPerVertices.getJointIndex( vtxIndex )
                physicalIndex = jntsPerVertices.jointLogicalIndexMap[ jointIndex ]
                polygonsPerJointArray[ physicalIndex ].check( i )
            vtxIndexPerPolygon += vtxCountPerPolygon
    except:
        print "errorMesh : ", meshObj
        return []
    
    meshs = []
    for i in range( len( polygonsPerJointArray ) ):
        targetJoint = om.MFnDagNode( jntsPerVertices.existConnectJoints[i] ).fullPathName()
        mesh = polygonsPerJointArray[i].buildMesh()
        
        mesh = cmds.rename( mesh, targetJoint.split( '|' )[-1] + '_mesh' )
        
        cmds.sets( mesh, e=1, forceElement='initialShadingGroup' )
        meshs.append( mesh )
        sgBFunction_connection.bindConnect( mesh, targetJoint )
    
    return meshs


def separateMeshsBySkinWeight( meshObjs ):
    
    import sgBFunction_connection
    import sgBFunction_dag
    
    meshObjs = sgBFunction_dag.getChildrenMeshExists( meshObjs )
    
    
    meshs = []
    for meshObj in meshObjs:
        meshs += separateMeshBySkinWeight( meshObj )
    
    jntAndBindTargets = {}
    appendedJnts = []
    
    for sel in meshs:
        mmdc = cmds.listConnections( sel, s=1, d=0 )[0]
        bindObj = cmds.listConnections( mmdc, s=1, d=0 )[0]
        bindObjP = cmds.listRelatives( bindObj, p=1, f=1 )[0]
        
        if not bindObjP in appendedJnts:
            appendedJnts.append( bindObjP )
            jntAndBindTargets.update( {bindObjP:[]} )
        
        jntAndBindTargets[ bindObjP ].append( sel )
    
    for jnt, bindObjs in jntAndBindTargets.items():
        
        if len( bindObjs ) == 1: continue
        
        bindObj, polyUnite = cmds.polyUnite( bindObjs, n=bindObjs[0] )
        bindObj = cmds.rename( bindObj, jnt.split( '|' )[-1]+'_mesh' )
        sgBFunction_connection.bindConnect( bindObj, jnt )



def separateMeshBySkinWeight2( meshObj ):
    
    import sgBFunction_connection
    
    skinClusters = sgBFunction_dag.getNodeFromHistory( meshObj, 'skinCluster' )
    meshShape    = sgBFunction_dag.getShape( meshObj )
    
    if not skinClusters: return []
    skinCluster = skinClusters[0]
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshShape ) )
    
    jntsPerVertices = JointsPerVertices( skinCluster )
    polygonsPerJointArray = [ PolygonsPerJoint2( meshShape ) for i in range( len( jntsPerVertices.existConnectJoints ) ) ]
    
    vtxCountsPerPolygon = om.MIntArray()
    vtxIndices = om.MIntArray()
    fnMesh.getVertices( vtxCountsPerPolygon, vtxIndices )
    
    for i in range( fnMesh.numVertices() ):
        jointLogicalIndex = jntsPerVertices.getJointIndex( i )
        physicalIndex = jntsPerVertices.jointLogicalIndexMap[ jointLogicalIndex ]
        polygonsPerJointArray[ physicalIndex ].check( i )

    meshs = []
    for i in range( len( polygonsPerJointArray ) ):
        targetJoint = om.MFnDagNode( jntsPerVertices.existConnectJoints[i] ).fullPathName()
        mesh = polygonsPerJointArray[i].buildMesh2()
        meshShape = sgBFunction_dag.getShape( mesh )
        
        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshShape ) )
        print fnMesh.numPolygons(), targetJoint
        
        mesh = cmds.rename( mesh, targetJoint.split( '|' )[-1] + '_mesh' )
        
        cmds.sets( mesh, e=1, forceElement='initialShadingGroup' )
        meshs.append( mesh )
        sgBFunction_connection.bindConnect( mesh, targetJoint )
    
    return meshs



def separateMeshsBySkinWeight2( meshObjs ):
    
    import sgBFunction_connection
    import sgBFunction_dag
    
    meshObjs = sgBFunction_dag.getChildrenMeshExists( meshObjs )
    
    
    meshs = []
    for meshObj in meshObjs:
        meshs += separateMeshBySkinWeight2( meshObj )
    
    jntAndBindTargets = {}
    appendedJnts = []
    
    for sel in meshs:
        mmdc = cmds.listConnections( sel, s=1, d=0 )[0]
        bindObj = cmds.listConnections( mmdc, s=1, d=0 )[0]
        bindObjP = cmds.listRelatives( bindObj, p=1, f=1 )[0]
        
        if not bindObjP in appendedJnts:
            appendedJnts.append( bindObjP )
            jntAndBindTargets.update( {bindObjP:[]} )
        
        jntAndBindTargets[ bindObjP ].append( sel )
    
    for jnt, bindObjs in jntAndBindTargets.items():
        
        if len( bindObjs ) == 1: continue
        
        bindObj, polyUnite = cmds.polyUnite( bindObjs, n=bindObjs[0] )
        bindObj = cmds.rename( bindObj, jnt.split( '|' )[-1]+'_mesh' )
        sgBFunction_connection.bindConnect( bindObj, jnt )