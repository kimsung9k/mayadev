import maya.cmds as cmds
import maya.OpenMaya as om
import copy
import sgModelDag


import skinClusterFunctions as skinF


def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj



def getDagPath( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    path = om.MDagPath()
    selList.getDagPath( 0, path )
    return path


def getDist( first, second ):
    
    return ( ( second[0] - first[0] )**2 + ( second[1] - first[1] )**2 + ( second[2] - first[2] )**2 ) **0.5


class MeshInfo:
    
    def __init__(self, mesh ):
        
        fnMesh = om.MFnMesh( getDagPath( mesh ) )
        
        numVtx  = fnMesh.numVertices()
        numPoly = fnMesh.numPolygons()
        
        verticesPolygons  = []
        polygonsVertices = []
        
        for i in range( numVtx ):
            verticesPolygons.append( om.MIntArray() )
        
        for i in range( numPoly ):
            intArr = om.MIntArray()
            fnMesh.getPolygonVertices( i, intArr )
            polygonsVertices.append( intArr )
            
            for j in range( intArr.length() ):
                vtxIndex = intArr[j]
                faceIndices = verticesPolygons[vtxIndex]
                
                faceIndexExists = False
                for k in range( faceIndices.length() ):
                    if i == faceIndices[k]:
                        faceIndexExists = True
                        break
                if not faceIndexExists:
                    verticesPolygons[vtxIndex].append( i )
        
        self.verticesPolygons = verticesPolygons
        self.polygonsVertices = polygonsVertices
        self.fnMesh = fnMesh
        
        self.verticesCheckList = []
        for i in range( numVtx ):
            self.verticesCheckList.append( False )
        self.numVtx = numVtx
        self.expendLoofVertices = []


    def resetVerticesCheckList(self):
        
        for i in range( self.numVtx ):
            self.verticesCheckList[i] = False
        
    
    def getExpendVertices(self, vtxIndex ):
        
        faceIndices = self.verticesPolygons[ vtxIndex ]
        
        expendVertices = []
        for i in range( faceIndices.length() ):
            faceIndex = faceIndices[i]
            vertexIndices = self.polygonsVertices[ faceIndex ]
            for j in range( len( vertexIndices ) ):
                vertexIndex = vertexIndices[j]
                if not vertexIndex in expendVertices:
                    expendVertices.append( vertexIndex )
        return expendVertices
    
    
    def getExpendLoof(self, vtxIndex ):
        
        self.resetVerticesCheckList()
        self.expendedVertices = []
        
        def loofArea( vtxIndex ):
            self.expendedVertices.append( vtxIndex )
            self.verticesCheckList[ vtxIndex ] = True
            indices = self.getExpendVertices( vtxIndex )
            for index in indices:
                if not self.verticesCheckList[ index ]:
                    loofArea( index )
        loofArea( vtxIndex )
        
        return self.expendedVertices
        
    
    
    def selectExpendVertices(self, vtxNames ):
        
        vertices = []
        for vtxName in vtxNames:
            vtxIndex = int( vtxName.split( '[' )[-1].replace( ']', '' ) )
            indices = self.getExpendVertices( vtxIndex )
            for i in range( len( indices ) ):
                vertices.append( self.fnMesh.name() + '.vtx[%d]' % indices[i] )
        cmds.select( vertices )
        
    
    def selectExpendLoofVertices(self, vtxNames ):
        
        vertices = []
        for vtxName in vtxNames:
            vtxIndex = int( vtxName.split( '[' )[-1].replace( ']', '' ) )
            self.getExpendLoof( vtxIndex )
            for i in self.expendedVertices:
                vertices.append( self.fnMesh.name() + '.vtx[%d]' % i )
        cmds.select( vertices )
        
        
        
    def selectEachSeparatedVertices(self):
        
        checkList = [ False for i in range( self.numVtx ) ]
        targetVerties = []
        for i in range( self.numVtx ):
            if checkList[i] == True: continue
            self.getExpendLoof( i )
            for j in self.expendedVertices:
                checkList[j] = True
            targetVerties.append( self.fnMesh.name() + '.vtx[%d]' % i )
        cmds.select( targetVerties )
        
        
        
        
class getDeepVertex:
    
    def __init__(self, baseMesh, outMesh ):
        
        baseMesh = sgModelDag.getShape( baseMesh )
        outMesh = sgModelDag.getShape( outMesh )
        
        self.baseIntersector = om.MMeshIntersector()
        self.baseIntersector.create( getMObject( baseMesh ) )
        self.outMeshInfo  = MeshInfo( outMesh )
        self.meshPoints = om.MPointArray()
        self.outMeshInfo.fnMesh.getPoints( self.meshPoints )
        self.outMeshName = outMesh
        self.copyVtxWeightAndPast = skinF.CopyVtxAndPast( outMesh )
        
    
    def getDeepVertex(self, vtxId ):
        
        self.outMeshInfo.getExpendLoof( vtxId )
        vtxIds = self.outMeshInfo.expendedVertices
        
        pointOnMesh = om.MPointOnMesh()
        deepIndex = vtxId
        deepDist = 1000000
        for i in vtxIds:
            point = self.meshPoints[i]
            self.baseIntersector.getClosestPoint( point, pointOnMesh )
            closePoint = om.MPoint( pointOnMesh.getPoint() )
            closeNormal = om.MVector( pointOnMesh.getNormal() )
            closeVector = om.MVector( point - closePoint )
            
            closeDist = closeVector.length()
            if closeNormal * closeVector < 0:
                closeDist *= -1
            
            if deepDist > closeDist:
                deepDist = closeDist
                deepIndex = i
        return deepIndex, vtxIds
    
    
    def selectDeepVertices(self, vtxNames ):
        
        targetVertices = []
        for vtxName in vtxNames:
            vtxId = int( vtxName.split( '[' )[-1].replace( ']', '' ) )
            deepId, vtxIdes = self.getDeepVertex( vtxId )
            targetVertices.append( self.outMeshInfo.fnMesh.name() + '.vtx[%d]' % deepId )
        cmds.select( targetVertices )
    
    
    def setWeightDeepVertexWeight(self, vtxNames ):
        
        for vtxName in vtxNames:
            vtxId = int( vtxName.split( '[' )[-1].replace( ']', '' ) )
            deepIndex, vtxIdes = self.getDeepVertex( vtxId )
            self.copyVtxWeightAndPast.getWeightAndPast( deepIndex, vtxIdes )
            
            
    def setWeightTargetVtx(self, vtxNames ):
        
        for vtxName in vtxNames:
            vtxId = int( vtxName.split( '[' )[-1].replace( ']', '' ) )
            self.outMeshInfo.getExpendLoof( vtxId )
            vtxIds = self.outMeshInfo.expendedVertices
            self.copyVtxWeightAndPast.getWeightAndPast( vtxId, vtxIds )
            
            
    def getDeepVertices(self):
        
        checkIds = [False for i in range( self.outMeshInfo.numVtx )]
        deepIds = []
        deepVertices = []
        for i in range( self.outMeshInfo.numVtx ):
            if checkIds[i]: continue
            deepVtx, vtxIds = self.getDeepVertex( i )
            for id in vtxIds:
                checkIds[id] = True
            deepIds.append( deepVtx )
            deepVertices.append( self.outMeshInfo.fnMesh.name()+'.vtx[%d]' % deepVtx )
            
        return deepIds, deepVertices
    
    
    def getDeepAndOutAndMiddleVertices(self):
        
        checkIds = [False for i in range( self.outMeshInfo.numVtx )]
        deepIds = []
        deepVertices = []
        outIds = []
        outVertices = []
        middleIds = []
        middleVertices = []
        
        for i in range( self.outMeshInfo.numVtx ):
            if checkIds[i]: continue
            deepVtx, vtxIds = self.getDeepVertex( i )
            for index in vtxIds:
                checkIds[index] = True
            deepIds.append( deepVtx )
            deepVertices.append( self.outMeshInfo.fnMesh.name()+'.vtx[%d]' % deepVtx )
            
            deepPoint = self.meshPoints[deepVtx]
            maxDist = 0.0
            maxDistId = deepVtx
            for index in vtxIds:
                if index == deepVtx: continue
                point = self.meshPoints[index]
                dist = deepPoint.distanceTo( point )
                if maxDist < dist:
                    maxDist = dist
                    maxDistId =index
            outIds.append( maxDistId )
            outVertices.append( self.outMeshInfo.fnMesh.name()+'.vtx[%d]' % maxDistId )
            
            middlePoint = om.MPoint( om.MVector( deepPoint ) + om.MVector( self.meshPoints[ maxDistId ] ) ) * 0.5
            minDist = 1000000.0
            minDistId = deepVtx
            for index in vtxIds:
                if index in [deepVtx,maxDistId]: continue
                point = self.meshPoints[index]
                dist = middlePoint.distanceTo( point )
                if minDist > dist:
                    minDist = dist
                    minDistId = index
            middleIds.append( minDistId )
            middleVertices.append( self.outMeshInfo.fnMesh.name()+'.vtx[%d]' % minDistId )
        
        return deepVertices, middleVertices, outVertices
    '''
    def createFollicleAndJointOnVertices(self, deepIndices, middleIndices, endIndices, baseMesh ):
        
        meshMtxGrp = cmds.group( em=1 )
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( baseMesh+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( meshMtxGrp+'.pim', mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', meshMtxGrp+'.t' )
        cmds.connectAttr( mmdc+'.or', meshMtxGrp+'.r' )
        cmds.connectAttr( mmdc+'.os', meshMtxGrp+'.s' )
        cmds.connectAttr( mmdc+'.osh', meshMtxGrp+'.sh' )
        
        closeMesh = cmds.createNode( 'closestPointOnMesh' )
        cmds.connectAttr( baseMesh+'.outMesh', closeMesh+'.inMesh' )
        for i in range( len( deepIndices ) ):
            deepPoint = self.meshPoints[deepIndices[i]]
            middlePoint = self.meshPoints[middleIndices[i]]
            endPoint = self.meshPoints[endIndices[i]]
            
            cmds.setAttr( closeMesh+'.inPosition', deepPoint.x, deepPoint.y, deepPoint.z )
            deepFollicle = cmds.createNode( 'follicle' )
            deepFollicls = cmds.createNode( 'follicle' )
            cmds.connectAttr( baseMesh+'.outMesh', follicleShape+'.inputMesh' )
            follicle = cmds.listRelatives( follicleShape, p=1 )[0]
            cmds.connectAttr( follicleShape+'.outTranslate', follicle+'.t' )
            cmds.connectAttr( follicleShape+'.outRotate', follicle+'.r' )
            cmds.setAttr( follicleShape+'.parameterU', cmds.getAttr( closeMesh+'.parameterU' ) )
            cmds.setAttr( follicleShape+'.parameterV', cmds.getAttr( closeMesh+'.parameterV' ) )
            cmds.parent( follicle, meshMtxGrp )
            wsPos = cmds.xform( vertex, q=1, ws=1, t=1 )[:3]
            cmds.select( follicle )
            jnt = cmds.joint()
            cmds.move( wsPos[0], wsPos[1], wsPos[2], jnt, ws=1 )
            cmds.undoInfo( swf=0 )
            if skinCluster:
                vtxIndex = int( vertex.split( '[' )[-1].replace( ']', '' ) )
                indices = self.outMeshInfo.getExpendLoof(vtxIndex)
                cmds.skinCluster( skinCluster, e=1, ug=1, lw=1, wt=0, ai=jnt )
                skinF.setJointInfluence(skinCluster, jnt, indices )
            cmds.undoInfo( swf=1 )
        cmds.delete( closeMesh )'''
        
        
class SetJntsInfluence:
    
    def __init__(self, mesh ):

        self.mesh = mesh
        hists = cmds.listHistory()
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinCluster = hist
        self.fnSkinNode = om.MFnDependencyNode( getMObject( skinCluster ) )


    def setJointsInfluence( self, jnts, vtxIndices ):

        cons = []
        for jnt in jnts:
            cons += cmds.listConnections( jnt+'.wm', type='skinCluster', c=1, p=1, d=1, s=0 )

        skinClusterAttrs = []
        for con in cons:
            if con.find( self.fnSkinNode.name() ) != -1:
                if not con in skinClusterAttrs:
                    skinClusterAttrs.append( con )

        jntIndices = []
        for skinClusterAttr in skinClusterAttrs:
            jntIndex = int( skinClusterAttr.split( '[' )[-1].replace( ']', '' ) )
            jntIndices.append( jntIndex )

        jntPoses = []
        for jnt in jnts:
            childJnt = cmds.listRelatives( jnt, c=1 )
            if not childJnt:
                pos = cmds.xform( jnt, q=1, ws=1, piv=1 )[:3]
                jntPoses.append( pos )
            else:
                childPos = cmds.xform( childJnt[0], q=1, ws=1, piv=1 )[:3]
                pos = cmds.xform( jnt, q=1, ws=1, piv=1 )[:3]
                sumPos = ( (childPos[0] + pos[0]) *0.5, (childPos[1] + pos[1]) *0.5, (childPos[2] + pos[2]) *0.5 )
                jntPoses.append( sumPos )

        weightListPlug = self.fnSkinNode.findPlug( 'weightList' )

        for vtxIndex in vtxIndices:
            vtxPos = cmds.xform( self.mesh+'.vtx[%d]' % vtxIndex, q=1, ws=1, t=1 )[:3]
            
            minDist = 100000000
            secondMinDist = 100000000
            minDistIndex = 0
            secondMinDistIndex = 1
            for i in range( len(jntPoses) ):
                dist = getDist( vtxPos, jntPoses[i] )
                if minDist > dist:
                    secondMinDist = copy.copy( minDist )
                    minDist = dist
                    secondMinDistIndex = copy.copy( minDistIndex )
                    minDistIndex = i 
                elif secondMinDist > dist:
                    secondMinDist = dist
                    secondMinDistIndex = i

            weightListPlugElement = weightListPlug.elementByLogicalIndex( vtxIndex )
            weightPlug = weightListPlugElement.child( 0 )
            
            for i in range( weightPlug.numElements() ):
                cmds.removeMultiInstance( weightPlug[0].name() )

            allDist = minDist + secondMinDist
            secondMinWeightValue = (minDist/allDist)**2
            minWeightValue = 1-secondMinWeightValue

            cmds.setAttr( self.fnSkinNode.name()+'.weightList[%d].weights[%d]' %( vtxIndex, jntIndices[minDistIndex] ), minWeightValue )
            cmds.setAttr( self.fnSkinNode.name()+'.weightList[%d].weights[%d]' %( vtxIndex, jntIndices[secondMinDistIndex] ), secondMinWeightValue )