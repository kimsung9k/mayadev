import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import get



def isShapeNode( target ):
    
    if not cmds.objExists( target ): return False
    if cmds.ls( target, s=1 ): return True
    return False



def isTransformNode( target ):
    
    if not cmds.objExists( target ): return False
    if cmds.nodeType( target ) in ["joint", "transform"]: return True
    return False


def matrixFromList( mtxList ):
    
    matrix = OpenMaya.MMatrix();
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix )
    return matrix


def isMesh( target ):
    
    if not cmds.objExists( target ): return False
    return cmds.nodeType( target ) == "mesh"



def getIntPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asIntPtr()



def getMObject( target ):
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, mObject )
    return mObject



def getDagPath( target ):
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    try:
        selList.getDagPath( 0, dagPath )
        return dagPath
    except:
        return None


class BoundingBox:
    
    def __init__(self, shapeOrTransform ):
        
        self._target = shapeOrTransform
        isEnable = isTransformNode( self._target ) or isShapeNode( self._target )
        
        if not isEnable:return None
        
        self._min = OpenMaya.MPoint( *cmds.getAttr( self._target + '.boundingBoxMin' )[0] )
        self._max = OpenMaya.MPoint( *cmds.getAttr( self._target + '.boundingBoxMax' )[0] )
        self._parentMatrix = matrixFromList( cmds.getAttr( self._target + ".pm" ) )
        self._bb  = OpenMaya.MBoundingBox()
        
        self._bb.expand( OpenMaya.MPoint( self._max ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._max.x, self._min.y, self._max.z ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._max.x, self._max.y, self._min.z ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._max.x, self._min.y, self._min.z ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._min ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._min.x, self._max.y, self._min.z ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._min.x, self._min.y, self._max.z ) * self._parentMatrix )
        self._bb.expand( OpenMaya.MPoint( self._min.x, self._max.y, self._max.z ) * self._parentMatrix )
            
            
    
    def min(self):
        return self._bb.min()


    def max(self):
        return self._bb.max()
    
    
    def center(self):
        return self._bb.center()




class Mesh:
    
    def __init__(self, shape ):
        
        if cmds.nodeType( shape ) != 'mesh' and cmds.nodeType( shape ) == 'transform':
            shapes = cmds.listRelatives( shape, s=1, f=1 )
            if not shapes: return None
            if cmds.nodeType( shapes[0] ) != 'mesh': return None
            shape = shapes[0]
        
        if type( shape ) == type( OpenMaya.MDagPath() ):
            self.dagPath = shape
        elif type( shape ) in [ type( "" ), type( u"" ) ]:
            if not isMesh( shape ): return None
            self.dagPath = getDagPath( shape )
        else: return None
        
        self.fnMesh = OpenMaya.MFnMesh( self.dagPath )
        self.upate()


    def upate(self):
        
        self.numVertices = self.fnMesh.numVertices()
        self.numEdges    = self.fnMesh.numEdges()
        self.numPolys    = self.fnMesh.numPolygons()
        self.pointsWorld = OpenMaya.MPointArray(); self.fnMesh.getPoints( self.pointsWorld, OpenMaya.MSpace.kWorld )
        self.pointsLocal = OpenMaya.MPointArray(); self.fnMesh.getPoints( self.pointsLocal, OpenMaya.MSpace.kObject )
        self.itMeshVtx   = OpenMaya.MItMeshVertex( self.dagPath )
        self.itMeshEdge  = OpenMaya.MItMeshEdge( self.dagPath )
        self.itMeshPoly  = OpenMaya.MItMeshPolygon( self.dagPath )
        self.matrix      = self.dagPath.inclusiveMatrix()
    
    
    def getPolygonCenter(self, polyIndex ):
        
        bb = OpenMaya.MBoundingBox()
        vtxList = self.getVtxsFromPoly(polyIndex)
        for i in range( vtxList.length() ):
            bb.expand( self.pointsWorld[ vtxList[i] ] )
        return bb.center()
        
    
    def getVtxsFromPoly(self, polyIndex ):
        
        prevIndex = getIntPtr()
        self.itMeshPoly.setIndex( polyIndex, prevIndex )
        indices = OpenMaya.MIntArray()
        self.itMeshPoly.getVertices(indices)
        return indices
    
    
    def setPoints(self, points ):
        
        if self.fnMesh.object().isNull(): return None
        if self.fnMesh.numVertices() != points.length(): return None
        self.fnMesh.setPoints( points )
        
        
    def getEmptyMap(self, numIndices ):
        indicesMap = OpenMaya.MIntArray()
        indicesMap.setLength( numIndices )
        for i in range( numIndices ):
            indicesMap.set( -1, i )
        return indicesMap
        
    
    def getIndicesFromMap(self, indicesMap ):
        
        numIndices = 0
        for i in range( indicesMap.length() ):
            if indicesMap[i] == -1: continue
            numIndices += 1
        cuIndex = 0
        indices = OpenMaya.MIntArray()
        indices.setLength( numIndices );
        for i in range( indicesMap.length() ):
            if indicesMap[i] == -1: continue
            indices[cuIndex] = i
            cuIndex += 1
        return indices
    
    
    def setIndicesToMap(self, indices, indicesMap ):
        for i in range( indices.length() ):
            indicesMap[ indices[i] ] = 1
    
    
    def combineArray(self, points1, points2 ):
        
        newPoints = None
        if type( points1 ) == type(OpenMaya.MIntArray()):
            newPoints = OpenMaya.MIntArray()
        elif type( points1 ) == type(OpenMaya.MPointArray()):
            newPoints = OpenMaya.MPointArray()
        elif type( points1 ) == type(OpenMaya.MFloatArray()):
            newPoints = OpenMaya.MFloatArray()
        
        newPoints.setLength( points1.length() + points2.length() )
        
        for i in range( points1.length() ):
            newPoints.set( points1[i], i );
        
        points1Length = points1.length()
        for i in range( points2.length() ):
            newPoints.set( points2[i], i+points1Length )
        return newPoints
    

    def duplicateAndAddFace( self, indicesPoly ):
        
        verticesCounts = OpenMaya.MIntArray()
        verticesList   = OpenMaya.MIntArray()
        
        self.fnMesh.getVertices( verticesCounts, verticesList )
        
        stringArr = []
        self.fnMesh.getUVSetNames( stringArr )
        uvInfoList = []
        for i in range( len(stringArr) ):
            uArrays = OpenMaya.MFloatArray()
            vArrays = OpenMaya.MFloatArray()
            uvCounts = OpenMaya.MIntArray()
            uvIds    = OpenMaya.MIntArray()
            self.fnMesh.getUVs( uArrays, vArrays, stringArr[i] )
            self.fnMesh.getAssignedUVs( uvCounts, uvIds, stringArr[i] )
            uvInfoList.append( {'uvName':stringArr[i], 'uArrays': uArrays, 'vArrays': vArrays, 'uvCounts': uvCounts, 'uvIds':uvIds } )
        
        checkedVtxMap = self.getEmptyMap( self.numVertices )
        for i in range( indicesPoly.length() ):
            vtxIndices = self.getVtxsFromPoly( indicesPoly[i] )
            self.setIndicesToMap( vtxIndices, checkedVtxMap )
        
        cuIndex = 0
        for i in range( checkedVtxMap.length() ):
            if checkedVtxMap[i] == -1: continue
            checkedVtxMap[i] = cuIndex
            cuIndex += 1
            
        targetVtxIndices = self.getIndicesFromMap( checkedVtxMap )
        targetPoints = OpenMaya.MPointArray()
        targetPoints.setLength( targetVtxIndices.length() )
        
        for i in range( targetPoints.length() ):
            targetPoints.set( self.pointsLocal[ targetVtxIndices[i] ], i )
        
        targetVerticesCounts = OpenMaya.MIntArray()
        targetVerticesCounts.setLength( indicesPoly.length() )
        for i in range( indicesPoly.length() ):
            targetVerticesCounts[i] = verticesCounts[ indicesPoly[i] ]
        
        targetVerticesList = OpenMaya.MIntArray()
        for i in range( indicesPoly.length() ):
            vtxIndices = self.getVtxsFromPoly( indicesPoly[i] )
            for j in range( vtxIndices.length() ):
                targetVerticesList.append( checkedVtxMap[vtxIndices[j]])
        
        addedTargetVerticesList = OpenMaya.MIntArray()
        addedTargetVerticesList.setLength( targetVerticesList.length() )
        for i in range( addedTargetVerticesList.length() ):
            addedTargetVerticesList.set( targetVerticesList[i]+self.numVertices, i )
        
        addNumVertices = self.numVertices + targetVtxIndices.length()
        addNumPolys    = self.numPolys + indicesPoly.length()
        addPoints      = self.combineArray( self.pointsLocal, targetPoints )
        addVerticesCounts = self.combineArray( verticesCounts, targetVerticesCounts )
        addVerticesList   = self.combineArray( verticesList, addedTargetVerticesList )
        
        newMeshTransform = cmds.createNode( 'transform' )
        newFnMesh = OpenMaya.MFnMesh()
        newFnMesh.create( addNumVertices, addNumPolys, addPoints, addVerticesCounts, addVerticesList, getMObject( newMeshTransform ) )
        
        for uvInfo in uvInfoList:
            uvName   = uvInfo['uvName']
            uArrays  = uvInfo['uArrays']
            vArrays  = uvInfo['vArrays']
            uvCounts = uvInfo['uvCounts']
            uvIds    = uvInfo['uvIds']
            
            uvIdsPerPolys = []
            searchIndex = 0
            for i in range( uvCounts.length() ):
                uvIdsPerPoly = [ uvIds[searchIndex+j] for j in range( uvCounts[i] ) ]
                searchIndex += uvCounts[i]
                uvIdsPerPolys.append( uvIdsPerPoly )
            
            duUArray = OpenMaya.MFloatArray()
            duVArray = OpenMaya.MFloatArray()
            duUvCounts = targetVerticesCounts
            duUvIds = OpenMaya.MIntArray()
            
            appendedDuTargetUvIds = self.getEmptyMap( uArrays.length() )
            duTargetUvIds = OpenMaya.MIntArray()
            duUvIdsLength = 0
            for i in range( indicesPoly.length() ):
                uvIdsPerPoly = uvIdsPerPolys[indicesPoly[i]]
                duUvIdsLength += len(uvIdsPerPoly)
                for j in range( len( uvIdsPerPoly ) ):
                    if appendedDuTargetUvIds[uvIdsPerPoly[j]] == -1:
                        appendedDuTargetUvIds[uvIdsPerPoly[j]] = duTargetUvIds.length()
                        duTargetUvIds.append( uvIdsPerPoly[j] )
            
            duUArray.setLength( duTargetUvIds.length() )
            duVArray.setLength( duTargetUvIds.length() )
            
            for i in range( duTargetUvIds.length() ):
                duUArray.set( uArrays[duTargetUvIds[i]], i )
                duVArray.set( vArrays[duTargetUvIds[i]], i )
            
            duUvIds.setLength( duUvIdsLength )
            cuIndex = 0
            for i in range( indicesPoly.length() ):
                uvIdsPerPoly = uvIdsPerPolys[ indicesPoly[i] ]
                for j in range( len(uvIdsPerPoly) ):
                    duUvIds[ cuIndex ] = appendedDuTargetUvIds[uvIdsPerPoly[j]]
                    cuIndex += 1
            
            for i in range( duUvIds.length() ):
                duUvIds.set( duUvIds[i] + uArrays.length(), i )
            
            addUArray = self.combineArray( uArrays, duUArray )
            addVArray = self.combineArray( vArrays, duVArray )
            addUvCounts = self.combineArray( uvCounts, duUvCounts )
            addUvIds  = self.combineArray( uvIds, duUvIds )
            
            '''
            print "duTargetUvIds length : ", duTargetUvIds.length()
            print "uArray length :", addUArray.length()
            print "vArray length :", addVArray.length()
            print "addUvCounts length :", addUvCounts.length()
            print "uvIds length :", uvIds.length()
            print "duUvIds length :", duUvIds.length()
            print "addUvIds length :", addUvIds.length()
            
            cuIndex = 0
            for i in range( addUvCounts.length() ):
                print "%d :" %( i ),
                for j in range( addUvCounts[i] ):
                    print " %d (%.2f, %.2f)" % (addUvIds[cuIndex], addUArray[addUvIds[cuIndex]], addVArray[addUvIds[cuIndex]]),
                    cuIndex += 1
                print'''
            
            uvSetNames = []
            newFnMesh.getUVSetNames(uvSetNames)
            
            try:
                if not uvName in uvSetNames:
                    newFnMesh.createUVSetWithName( uvName )
                newFnMesh.setUVs( addUArray, addVArray, uvName )
                newFnMesh.assignUVs( addUvCounts, addUvIds, uvName )
            except: pass
            
        
        newMeshs = get.nonIoMesh( newMeshTransform )
        
        if not newMeshs: return None
        newMesh = newMeshs[0]
        cmds.setAttr( newMesh + '.io', 1 )
        
        origMeshName = self.fnMesh.partialPathName()
        cmds.polyMergeVertex( origMeshName,  d=0 )
        
        cmds.parent( newMesh, get.getTransform( origMeshName ), add=1, shape=1 )
        
        srcCons = cmds.listConnections( origMeshName+'.inMesh', s=1, d=0, shapes=1 )
        cmds.connectAttr( newMesh + '.outMesh', origMeshName + '.inMesh', f=1 )
        cmds.refresh()
        if srcCons:
            cmds.delete( srcCons )
            
        cmds.delete( newMeshTransform )
        
        newPolyIndices = [ self.numPolys + j for j in range( indicesPoly.length() )]
        
        return newPolyIndices


    def getOppositeEdges(self, edgeIndex, removeIndex = -1 ):
        
        polyIndices = OpenMaya.MIntArray()
        prevIndex = getIntPtr()
        self.itMeshEdge.setIndex( edgeIndex, prevIndex )
        self.itMeshEdge.getConnectedFaces( polyIndices )
        
        oppositeEdges = []
        for i in range( polyIndices.length() ):
            polyToEdgeIndices = OpenMaya.MIntArray()
            prevIndex = getIntPtr()
            self.itMeshPoly.setIndex( polyIndices[i], prevIndex )
            self.itMeshPoly.getEdges( polyToEdgeIndices )
            
            oppositeIndices = []
            for j in range( polyToEdgeIndices.length() ):
                if polyToEdgeIndices[j] == edgeIndex: continue
                conEdges = OpenMaya.MIntArray()
                prevIndex = getIntPtr()
                self.itMeshEdge.setIndex( polyToEdgeIndices[j], prevIndex )
                self.itMeshEdge.getConnectedEdges( conEdges )
                
                edgeExists = False
                for k in range( conEdges.length() ):
                    if conEdges[k] != edgeIndex: continue
                    edgeExists = True
                    break
                
                if edgeExists: continue
                if removeIndex == polyToEdgeIndices[j]: continue
                oppositeIndices.append( polyToEdgeIndices[j] )
            if len( oppositeIndices ) > 1: continue
            oppositeEdges += oppositeIndices
        return oppositeEdges


    def getSoltedRingEdges(self, edgeIndex ):
    
        import copy 
        twoEdges = self.getOppositeEdges( edgeIndex )
        
        allIndices = []
        
        for oneEdge in twoEdges:
            removeIndex = copy.copy( edgeIndex )
            targetIndex = copy.copy( oneEdge )
            sides = [targetIndex]
            loopIndex = 0
            while True:
                oppositeIndices = self.getOppositeEdges( targetIndex, removeIndex )
                if not oppositeIndices: break
                sides.append( oppositeIndices[0] )
                removeIndex = copy.copy( targetIndex )
                targetIndex = oppositeIndices[0]
                loopIndex += 1
                if loopIndex > self.numEdges: break
            
            if twoEdges.index( oneEdge ) == 0: sides.reverse()
            allIndices += sides
            if twoEdges.index( oneEdge ) == 0: allIndices.append( edgeIndex )
        
        return allIndices


    def getConnectedEdges(self, edgeIndex, removeIndex=-1 ):
        
        conEdges = OpenMaya.MIntArray()
        prevIndex = getIntPtr()
        self.itMeshEdge.setIndex( edgeIndex, prevIndex )
        self.itMeshEdge.getConnectedEdges( conEdges )
        
        conFaces = OpenMaya.MIntArray()
        self.itMeshEdge.getConnectedFaces( conFaces )

        loopIndices = []
        for i in range( conEdges.length() ):
            conEdgeIndex = conEdges[i]
            
            if removeIndex == conEdgeIndex: continue
            
            conFacesEach = OpenMaya.MIntArray()
            prevIndex = getIntPtr()
            self.itMeshEdge.setIndex( conEdgeIndex, prevIndex )
            self.itMeshEdge.getConnectedFaces( conFacesEach )
            
            sameExists = False
            for j in range( conFaces.length() ):
                for k in range( conFacesEach.length() ):
                    if conFaces[j] == conFacesEach[k]:
                        sameExists = True
                        break
                if sameExists: break

            if not sameExists: loopIndices.append( conEdgeIndex )
        
        return loopIndices
    
    
    def getSoltedLoopEdges(self, edgeIndex ):
        
        import copy 
        twoEdges = self.getConnectedEdges( edgeIndex )
        
        allIndices = []
        
        for oneEdge in twoEdges:
            removeIndex = copy.copy( edgeIndex )
            targetIndex = copy.copy( oneEdge )
            sides = [targetIndex]
            loopIndex = 0
            while True:
                oppositeIndices = self.getConnectedEdges( targetIndex, removeIndex )
                if not oppositeIndices: break
                sides.append( oppositeIndices[0] )
                removeIndex = copy.copy( targetIndex )
                targetIndex = oppositeIndices[0]
                loopIndex += 1
                if loopIndex > self.numEdges: break
            
            if twoEdges.index( oneEdge ) == 0: sides.reverse()
            allIndices += sides
            if twoEdges.index( oneEdge ) == 0: allIndices.append( edgeIndex )
        
        return allIndices




class Curve:
    
    def __init__(self, curveShape ):
        
        self.dagPath = getDagPath( curveShape )
        self.fnCurve = OpenMaya.MFnNurbsCurve( self.dagPath )


    def getClosestParamAtPoint(self, point, space=OpenMaya.MSpace.kWorld ):
        
        util = OpenMaya.MScriptUtil()
        util.createFromDouble( 0.0 )
        ptrDouble = util.asDoublePtr()
        self.fnCurve.closestPoint( point, 0, ptrDouble )
        return OpenMaya.MScriptUtil().getDouble( ptrDouble )







class Node:
    
    def __init__(self, nodeName ):
        
        self.oNode = getMObject( nodeName )
        self.fnNode = OpenMaya.MFnDependencyNode( self.oNode )


    def name(self):
        return self.fnNode.name()


    def __add__(self, other ):
        
        return self.name() + other
    
    
    def __radd__(self, other ):
        
        return other + self.name()
    
    
    def set(self, attrName, value ):
        
        cmds.setAttr( self.name() + '.' + attrName, value )





class DagNode( Node ):
    
    def __init__(self, dagNodeName ):
    
        Node( self ).__init__( dagNodeName )
        self.fnDagNode = OpenMaya.MFnDagNode( getDagPath(dagNodeName) )


    def name(self):        
        return self.fnDagNode.partialPathName()
    
    
    
    
    
    
    


