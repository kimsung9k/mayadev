import maya.api.OpenMaya as openMaya
import maya.cmds as cmds
import maya.OpenMaya as om
import sgBModel_mesh
import sgBFunction_dag


def getPolygonData( nameMesh ):
    
    fnMesh = openMaya.MFnMesh( sgBFunction_dag.getMDagPath2( nameMesh ) )
    
    polygonData = sgBModel_mesh.CPolygonData
    
    polygonData.points          = fnMesh.getPoints()
    polygonData.polygonCounts   = openMaya.MIntArray()
    polygonData.polygonConnects = openMaya.MIntArray()
    
    for i in range( fnMesh.numPolygons ):
        idsVertices = fnMesh.getPolygonVertices( i )
        polygonData.polygonCounts.append( len( idsVertices ) )
        for idVertex in idsVertices:
            polygonData.polygonConnects.append( idVertex )
    
    return polygonData



def getUVDatas( nameMesh ):
    
    fnMesh = openMaya.MFnMesh( sgBFunction_dag.getMDagPath2( nameMesh ) )

    uvDatas     = []
    for uvSetName in fnMesh.getUVSetNames():
        uArray,   vArray = fnMesh.getUVs( uvSetName )
        uvCounts, uvIds  = fnMesh.getAssignedUVs( uvSetName )
        uvData = sgBModel_mesh.CUVData()
        uvData.uvSetName = uvSetName
        uvData.uArray    = uArray
        uvData.vArray    = vArray
        uvData.uvCounts  = uvCounts
        uvData.uvIds     = uvIds
        uvDatas.append( uvData )

    return uvDatas

        

def getMeshData( nameMesh ):
    
    fnMesh = openMaya.MFnMesh( sgBFunction_dag.getMDagPath2( nameMesh ) )
    
    insMeshData                 = sgBModel_mesh.CMeshData()
    
    polygonData = insMeshData.polygonData
    uvDatas     = insMeshData.uvDatas
    
    polygonData.points          = fnMesh.getPoints()
    polygonData.polygonCounts   = openMaya.MIntArray()
    polygonData.polygonConnects = openMaya.MIntArray()
    
    for i in range( fnMesh.numPolygons ):
        idsVertices = fnMesh.getPolygonVertices( i )
        polygonData.polygonCounts.append( len( idsVertices ) )
        for idVertex in idsVertices:
            polygonData.polygonConnects.append( idVertex )
            
    for uvSetName in fnMesh.getUVSetNames():
        uArray,   vArray = fnMesh.getUVs( uvSetName )
        uvCounts, uvIds  = fnMesh.getAssignedUVs( uvSetName )
        uvData = sgBModel_mesh.CUVData()
        uvData.uvSetName = uvSetName
        uvData.uArray    = uArray
        uvData.vArray    = vArray
        uvData.uvCounts  = uvCounts
        uvData.uvIds     = uvIds
        uvDatas.append( uvData )
    
    return insMeshData




def buildFromPolygonData( polygonData ):
    
    fnMesh = openMaya.MFnMesh()
    
    points          = polygonData.points
    polygonCounts   = polygonData.polygonCounts
    polygonConnects = polygonData.polygonConnects
    
    targetTr = cmds.createNode( 'transform' )
    mObjTargetTr = sgBFunction_dag.getMObject2( targetTr )
    
    fnMesh.create( points, polygonCounts, polygonConnects, [], [], mObjTargetTr )
    return sgBFunction_dag.getShape( targetTr )
    



def buildFromUVDatas( uvDatas, meshName ):
    
    fnMesh = openMaya.MFnMesh()
    fnMesh.setObject( sgBFunction_dag.getMObject2( meshName ) )
    
    cuUvSetNames = fnMesh.getUVSetNames()
    fnMesh.clearUVs( cuUvSetNames[0] )
    fnMesh.setUVs( uvDatas[0].uArray, uvDatas[0].vArray, cuUvSetNames[0] )
    fnMesh.assignUVs( uvDatas[0].uvCounts, uvDatas[0].uvIds, cuUvSetNames[0] )
    
    buildedUvSets = [cuUvSetNames[0]]
    
    if len( cuUvSetNames ) > 1:
        for i in range( 1, len( cuUvSetNames ) ):
            fnMesh.deleteUVSet( cuUvSetNames[i] )
    
    if len( uvDatas ) > 1:
        for i in range( 1, len( uvDatas ) ):
            uvSetName = fnMesh.createUVSet( uvDatas[i].uvSetName )
            fnMesh.setUVs( uvDatas[i].uArray, uvDatas[i].vArray, uvSetName )
            fnMesh.assignUVs( uvDatas[i].uvCounts, uvDatas[i].uvIds, uvSetName )
            buildedUvSets.append( uvSetName )
    
    return buildedUvSets





def appendUVFromUVDatas( uvDatas, meshName ):
    
    fnMesh = openMaya.MFnMesh()
    fnMesh.setObject( sgBFunction_dag.getMObject2( meshName ) )
    
    uvSetNames = []
    for uvData in uvDatas:
        uvSetName = fnMesh.createUVSet( uvData.uvSetName )
        
        fnMesh.setUVs( uvData.uArray, uvData.vArray, uvSetName )
        fnMesh.assignUVs( uvData.uvCounts, uvData.uvIds, uvSetName )
        uvSetNames.append( uvSetName )
    
    return uvSetNames
    



def buildFromMeshData( meshData, targetTr=None ):
    
    fnMesh = openMaya.MFnMesh()
    
    polygonData = meshData.polygonData
    uvDatas     = meshData.uvDatas
    
    points          = polygonData.points
    polygonCounts   = polygonData.polygonCounts
    polygonConnects = polygonData.polygonConnects
    
    if not targetTr:
        targetTr = cmds.createNode( 'transform' )

    mObjTargetTr = sgBFunction_dag.getMObject2( targetTr )
    fnMesh.create( points, polygonCounts, polygonConnects, [], [], mObjTargetTr )
    
    targetShape = sgBFunction_dag.getShape( targetTr )
    fnMesh.setObject( sgBFunction_dag.getMObject2( targetShape ) )
    cuUvSetNames = fnMesh.getUVSetNames()
    
    fnMesh.setUVs( uvDatas[0].uArray, uvDatas[0].vArray, cuUvSetNames[0] )
    fnMesh.assignUVs( uvDatas[0].uvCounts, uvDatas[0].uvIds, cuUvSetNames[0] )
    
    if len( cuUvSetNames ) > 1:
        for i in range( 1, len( cuUvSetNames ) ):
            fnMesh.deleteUVSet( cuUvSetNames[i] )
    
    if len( uvDatas ) > 1:
        for i in range( 1, len( uvDatas ) ):
            uvSetName = fnMesh.createUVSet( uvDatas[i].uvSetName )
            fnMesh.setUVs( uvDatas[i].uArray, uvDatas[i].vArray, uvSetName )
            fnMesh.assignUVs( uvDatas[i].uvCounts, uvDatas[i].uvIds, uvSetName )
    
    return fnMesh.name()




def assignUvFiles( uvFolderPath, namespace ):    
    import os
    import sgBExcute_data

    for root, dirs, names in os.walk( uvFolderPath ):
        for name in names:
            targetShapeName = namespace + name.split( '.' )[0]
            if not cmds.objExists( targetShapeName ): continue
            
            filePath = root + '/' + name
            sgBExcute_data.importSgUVData( targetShapeName, filePath )



def createMeshRivet( meshName, centerIndices, aimPivIndices, aimIndices, upPivIndices, upIndices, aimIndex, upIndex, rivetType='transform' ):
    
    def convertToList( target ):
        if not type( target ) in [ type( [] ), type(()) ]:
            return [target]
        return target
    
    centerIndices = convertToList(centerIndices)
    aimPivIndices = convertToList(aimPivIndices)
    aimIndices    = convertToList(aimIndices)
    upPivIndices  = convertToList(upPivIndices)
    upIndices     = convertToList(upIndices)
    
    if rivetType == 'transform':
        rivetObject = cmds.group( em=1 )
        cmds.setAttr( rivetObject+'.dh', 1 )
        cmds.setAttr( rivetObject+'.dla', 1 ) 
    else:
        rivetObject = cmds.createNode( 'joint' )
        cmds.setAttr( rivetObject+'.dla', 1 ) 
    
    rivetNode = cmds.createNode( 'meshRivet' )
    cmds.setAttr( rivetNode+'.aimAxis', aimIndex )
    cmds.setAttr( rivetNode+'.upAxis',  upIndex  )
    
    for i in range( len( centerIndices ) ):
        cmds.setAttr( rivetNode+'.centerIndices[%d]' % i, centerIndices[i] )
    for i in range( len( aimPivIndices ) ):
        cmds.setAttr( rivetNode+'.aimPivIndices[%d]' % i, aimPivIndices[i] )
    for i in range( len( aimIndices ) ):
        cmds.setAttr( rivetNode+'.aimIndices[%d]' % i, aimIndices[i] )
    for i in range( len( upPivIndices ) ):
        cmds.setAttr( rivetNode+'.upPivIndices[%d]' % i, upPivIndices[i] )
    for i in range( len( upIndices ) ):
        cmds.setAttr( rivetNode+'.upIndices[%d]' % i, upIndices[i] )
    
    cmds.connectAttr( meshName+'.outMesh', rivetNode+'.inputMesh' )
    cmds.connectAttr( meshName+'.wm', rivetNode+'.meshMatrix' )
    cmds.connectAttr( rivetObject+'.pim', rivetNode+'.parentInverseMatrix' )
    cmds.connectAttr( rivetNode+'.ot', rivetObject+'.t' )
    cmds.connectAttr( rivetNode+'.or', rivetObject+'.r' )
    
    return rivetObject


def createMeshRivetAuto( meshVertex ):
    
    import math
    
    shapeName = meshVertex.split( '.' )[0]
    
    selectNum = int( meshVertex.split( '[' )[-1].replace( ']', '' ) )
    edges = cmds.polyListComponentConversion( meshVertex, toEdge=1 )
    vts   = cmds.polyListComponentConversion( edges, toVertex=1 )
    vts   = cmds.ls( vts, fl=1 )
    
    targetNums = []
    for vtx in vts:
        num = int( vtx.split( '[' )[-1].replace( ']', '' ) )
        targetNums.append( num )
    
    targetNums.remove( selectNum )
    
    targetPoints = []
    for num in targetNums:
        targetPos = cmds.xform( shapeName+'.vtx[%d]' % num, q=1, ws=1, t=1 )[:3]
        targetPoints.append( om.MVector( *targetPos ) )
    
    vectorList = []
    for i in range( len( targetPoints )-1 ):
        for j in range( i+1, len( targetPoints ) ):
            vector = targetPoints[i]-targetPoints[j]
            vector.normalize()
            vectorValue= [i,j,vector]
            vectorList.append( vectorValue )
    
    minDot = 1.0
    targetPointIndices = []
    
    for i in range( len( vectorList )-1 ):
        for j in range( i+1, len( vectorList ) ):
            iIndex1, iIndex2, iVector = vectorList[i]
            jIndex1, jIndex2, jVector = vectorList[j]
            
            dotValue = math.fabs( iVector*jVector )
            if dotValue < minDot:
                minDot = dotValue
                targetPointIndices = [targetNums[iIndex1], targetNums[iIndex2], targetNums[jIndex1], targetNums[jIndex2]]
    
    createMeshRivet( shapeName, selectNum, targetPointIndices[0], targetPointIndices[1], targetPointIndices[2], targetPointIndices[3], 0, 1 )



def createRivetLineAuto( selObjects, rivetType='joint' ):

    shapeName, indices = getMeshAndIndicesPoints( selObjects )
    
    rivetObjs = []
    for meshVtxIndex in indices:
        
        meshVertex = shapeName+'.vtx[%d]'% meshVtxIndex
        
        selectNum = meshVtxIndex
        edges = cmds.polyListComponentConversion( meshVertex, toEdge=1 )
        vts   = cmds.polyListComponentConversion( edges, toVertex=1 )
        vts   = cmds.ls( vts, fl=1 )
        
        targetNums = []
        for vtx in vts:
            num = int( vtx.split( '[' )[-1].replace( ']', '' ) )
            targetNums.append( num )
        
        targetNums.remove( selectNum )
        
        aimIndices = []
        upIndices  = []
        for num in targetNums:
            if num in indices:
                aimIndices.append( num )
            else:
                upIndices.append( num )    
        
        rivetObject = createMeshRivet( shapeName, selectNum, [selectNum], [selectNum], [selectNum], [selectNum], 0, 1, rivetType )
        rivetObjs.append( rivetObject )
        
        rivetNode = cmds.listConnections( rivetObject+'.t' )[0]
        
        if len( aimIndices ) == 2:
            cmds.setAttr( rivetNode+'.aimPivIndices[0]', aimIndices[0] )
            cmds.setAttr( rivetNode+'.aimIndices[0]', aimIndices[1] )
        elif len( aimIndices ) == 1:
            cmds.setAttr( rivetNode+'.aimIndices[0]', aimIndices[0] )
        
        if len( upIndices ) == 2:
            cmds.setAttr( rivetNode+'.upPivIndices[0]', upIndices[0] )
            cmds.setAttr( rivetNode+'.upIndices[0]', upIndices[1] )
        elif len( upIndices ) == 1:
            cmds.setAttr( rivetNode+'.upIndices[0]', upIndices[0] )
    
    return cmds.group( rivetObjs )


mc_createRivetLineAuto = """
import sgBFunction_mesh
import maya.cmds as cmds
createRivetLineAuto( cmds.ls( sl=1 ) )
"""
    
    



def getLocalPoints( mesh ):
    
    import sgBFunction_dag
    import maya.OpenMaya as om
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) )
    points = om.MPointArray()
    fnMesh.getPoints( points )
    return points





def getMeshAndIndicesPoints( selObjects ):
    
    import sgBFunction_dag
    import maya.OpenMaya as om
    
    selObjects = cmds.ls( cmds.polyListComponentConversion( selObjects, tv=1 ), fl=1 )
    
    mesh = ''
    vtxIndices = []
    for obj in selObjects:
        splits = obj.split( '.' )
        if len( splits ) == 1:
            mesh = obj
        else:
            mesh = splits[0]
            index = int( splits[1].split( '[' )[-1].replace( ']', '' ) )
            vtxIndices.append( index )
    
    if vtxIndices:
        vtxIndices = list( set( vtxIndices ) )
    else:
        vtxIndices = [ i for i in range( om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) ).numVertices() ) ]
    
    return mesh, vtxIndices



def cleanMesh( targetObj ):
    
    targetShapes = cmds.listRelatives( targetObj, s=1, f=1 )
    for targetShape in targetShapes:
        if not cmds.getAttr( targetShape+'.io' ): continue
        if cmds.listConnections( targetShape, s=0, d=1 ): continue 
        cmds.delete( targetShape )
        cmds.warning( "%s is deleted" % targetShape )



class MeshMirror:
    
    def __init__(self, meshName = '' ):
        
        if meshName:
            self.setBaseMesh( meshName )


    def setBaseMesh(self, meshName ):
        
        import sgBFunction_dag
        
        meshName = sgBFunction_dag.getShape( meshName )
        oMesh = sgBFunction_dag.getMObject( meshName )
        
        intersector = om.MMeshIntersector()
        fnMesh = om.MFnMesh()
        
        intersector.create( oMesh )
        fnMesh.setObject( oMesh )
        
        pointsMesh = om.MPointArray()
        
        fnMesh.getPoints( pointsMesh )
        
        self.mirrorIndices = om.MIntArray()
        self.mirrorIndices.setLength( pointsMesh.length() )
        for i in range( self.mirrorIndices.length() ):
            self.mirrorIndices[i] = -1
        
        pointOnMesh = om.MPointOnMesh()
        indicesVertices = om.MIntArray()
        
        for i in range( pointsMesh.length() ):
            if self.mirrorIndices[i] != -1: continue
            
            mirrorPoint = om.MPoint( -pointsMesh[i].x, pointsMesh[i].y, pointsMesh[i].z )
            intersector.getClosestPoint( mirrorPoint, pointOnMesh )
            faceIndex = pointOnMesh.faceIndex()
            fnMesh.getPolygonVertices( faceIndex, indicesVertices )
            
            minDist = 10000000.0
            minDistIndex = 0
            for j in range( indicesVertices.length() ):
                dist = mirrorPoint.distanceTo( pointsMesh[ indicesVertices[j] ] )
                if dist < minDist:
                    minDist = dist
                    minDistIndex = indicesVertices[j]
            self.mirrorIndices[i] = minDistIndex
            
            self.mirrorIndices[i] = minDistIndex
            self.mirrorIndices[minDistIndex] = i
        
        self.points = pointsMesh
        self.meshName = meshName
        

    def flip(self, meshName ):
        
        points = om.MPointArray()
        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshName ) )
        fnMesh.getPoints( points )
        
        for i in range( points.length() ):
            mirrorIndex = self.mirrorIndices[i]
            targetPoint = points[ mirrorIndex ]
            
            cmds.move( -targetPoint.x, targetPoint.y, targetPoint.z, meshName+'.vtx[%d]' % i, os=1 )
    
    
    def mirror_L_to_R(self, meshName ):
        
        points = om.MPointArray()
        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshName ) )
        fnMesh.getPoints( points )
        
        for i in range( points.length() ):
            
            if points[i].x > 0: continue
            
            mirrorIndex = self.mirrorIndices[i]
            targetPoint = points[ mirrorIndex ]
            
            cmds.move( -targetPoint.x, targetPoint.y, targetPoint.z, meshName+'.vtx[%d]' % i, os=1 )
    
    
    def mirror_R_to_L(self, meshName ):
        
        points = om.MPointArray()
        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshName ) )
        fnMesh.getPoints( points )
        
        for i in range( points.length() ):
            
            if points[i].x < 0: continue
            
            mirrorIndex = self.mirrorIndices[i]
            targetPoint = points[ mirrorIndex ]
            
            cmds.move( -targetPoint.x, targetPoint.y, targetPoint.z, meshName+'.vtx[%d]' % i, os=1 )
    
    
    def select_L(self, meshName, tol=0.001 ):
        
        import math
        leftIndices = []
        
        for i in range( self.points.length() ):
            if math.fabs( self.points[i].x ) < tol: continue
            if self.points[i].x > 0:
                leftIndices.append( meshName+'.vtx[%d]' % i )
        
        cmds.select( leftIndices )
    
    
    def select_R(self, meshName, tol=0.001 ):
        
        import math
        rightIndices = []
        
        for i in range( self.points.length() ):
            if math.fabs( self.points[i].x ) < tol: continue
            if self.points[i].x < 0:
                rightIndices.append( meshName+'.vtx[%d]' % i )
        
        cmds.select( rightIndices )
    
    
    def select_C(self, meshName, tol=0.001 ):
        
        import math
        centerIndices = []
        
        for i in range( self.points.length() ):
            if not math.fabs( self.points[i].x ) < tol: continue
            centerIndices.append( meshName+'.vtx[%d]' % i )
        
        cmds.select( centerIndices )


mc_meshFlip = """import sgBFunction_mesh

sels = cmds.ls( sl=1 )

meshMirror = MeshMirror( sels[1] )
meshMirror.flip( sels[0] )
"""




def cleanUVSets( targets ):
    
    import sgBFunction_dag
    import maya.OpenMaya as om
    
    def doIt( sel ):
        selShapes = cmds.listRelatives( sel, s=1, f=1 )
        if not selShapes: return None
        selOrigShape = selShapes[-1]
        
        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( selOrigShape ) )
        uvSetNames = cmds.polyUVSet( sel, q=1, allUVSets=1 )
        
        if not uvSetNames:
            print '"%s" has no uvSets' % fnMesh.name()
            return None
        
        numUVs = []
        allUVNums = 0
        hasUVIndex = None
        for i in range( len( uvSetNames ) ):
            numUV = fnMesh.numUVs( uvSetNames[i] )
            if numUV:
                hasUVIndex = i
            numUVs.append( numUV )
            allUVNums += numUV
        
        if not allUVNums: return None
        
        cmds.polyCopyUV( sel, uvSetNameInput=uvSetNames[hasUVIndex], uvSetName=uvSetNames[0], ch=0 )
        cmds.polyUVSet( sel, uvSet=uvSetNames[0], currentUVSet=1 )
        
        for i in range( 1, len( uvSetNames ) ):
            cmds.polyUVSet( selOrigShape, delete=1, uvSet=uvSetNames[i] )

        cmds.select( selOrigShape )
        cmds.DeleteHistory()
        
        if uvSetNames[0] != 'map1':
            cmds.polyUVSet( selOrigShape, rename=1, uvSet=uvSetNames[0], newUVSet='map1' )
        
    targets = sgBFunction_dag.getChildrenMeshExists( targets )
    for sel in targets:
        doIt( sel )


mc_cleanUVSets = """import sgBFunction_mesh
cleanUVSets( cmds.ls( sl=1 ) )"""




def getIndicesFromSelected():
    
    sels = cmds.ls( cmds.polyListComponentConversion( cmds.ls( sl=1 ), toVertex = 1 ), fl=1 )

    strIndices = ''
    targetMesh = ''
    for sel in sels:
        mesh, vtx = sel.split( '.' )
        strIndex = sel.split( '[' )[-1].replace( ']', '' )
        strIndices += strIndex + ","

        if cmds.nodeType( mesh ) == 'transform':
            shapes = cmds.listRelatives( mesh, s=1 )
            if not shapes:return None
            mesh = shapes[0]
        
        if not targetMesh:
            targetMesh = mesh
        else:
            if mesh != targetMesh:
                return None
    
    return targetMesh, strIndices[:-1]



def getMeshFromSelected():
    
    sels = cmds.ls( sl=1 )
    
    target = sels[-1]
    
    if cmds.nodeType( target ) == 'mesh':
        return target
    elif cmds.nodeType( target ) == 'transform':
        shapes = cmds.listRelatives( target, s=1 )
        if not shapes: return None
        if cmds.nodeType( shapes[0] ) == 'mesh':
            return shapes[0]





def getSelectionListFromVertex( vtxName ):
    
    selList = om.MSelectionList()
    om.MGlobal.getSelectionListByName( vtxName, selList )
    
    dagPath = om.MDagPath()
    oIndices = om.MObject()
    selList.getDagPath( 0, dagPath, oIndices )
    component = om.MFnSingleIndexedComponent( oIndices )
    
    indices = om.MIntArray()
    component.getElements( indices )
    
    return dagPath, indices[0]



def getSelectionListFromVertices( vertices ):
    
    selList = om.MSelectionList()
    cmds.select( vertices )
    om.MGlobal.getActiveSelectionList( selList )
    
    dagPath = om.MDagPath()
    oIndices = om.MObject()
    selList.getDagPath( 0, dagPath, oIndices )
    component = om.MFnSingleIndexedComponent( oIndices )
    
    indices = om.MIntArray()
    component.getElements( indices )
    
    return dagPath, indices[0], indices[1]



def getIntersectionPointFromTwoPoint( fnMesh, point1, point2 ):
    
    import copy
    centerPoint = om.MPoint()
    centerPoint.x = (point1.x + point2.x)/2.0
    centerPoint.y = (point1.y + point2.y)/2.0
    centerPoint.z = (point1.z + point2.z)/2.0
    
    dagPath = fnMesh.dagPath()
    meshMtx = dagPath.inclusiveMatrix()
    
    origMeshPoints = om.MPointArray()
    multedMeshPoints = om.MPointArray()
    
    fnMesh.getPoints( origMeshPoints )
    
    multedMeshPoints.setLength( origMeshPoints.length() )
    for i in range( origMeshPoints.length() ):
        multedMeshPoints.set( origMeshPoints[i]*meshMtx, i )

    fnMesh.setPoints( multedMeshPoints )
    
    intersector = om.MMeshIntersector()
    intersector.create( fnMesh.object() )
    
    pointOnMesh = om.MPointOnMesh()
    intersector.getClosestPoint( centerPoint, pointOnMesh )
    pointClose = om.MPoint( pointOnMesh.getPoint() );
    
    vNormal = om.MVector( pointOnMesh.getNormal() );
    vCDirection = om.MVector( pointClose ) - om.MVector( centerPoint )
    vDirection = om.MVector( point1 ) - om.MVector( point2 )
    
    ray = om.MVector()
    if vNormal * vDirection < vCDirection * vDirection:
        ray = vNormal
    else:
        ray = vCDirection
    
    vCross = ray ^ vDirection
    
    intersectPoints = om.MPointArray()
    invIntersectPoints = om.MPointArray()
    fnMesh.intersect( pointClose, ray, intersectPoints )
    fnMesh.intersect( pointClose, -ray, invIntersectPoints )
    
    allIntersectPoints = []
    for i in range( intersectPoints.length() ):
        allIntersectPoints.append( intersectPoints[i] )
    
    for i in range( invIntersectPoints.length() ):
        allIntersectPoints.append( invIntersectPoints[i] )
    
    twoCloseDistances = [100000000.0, 100000000.0]
    twoClosePoints = [None, None]
    
    for point in allIntersectPoints:
        dist = point.distanceTo( pointClose )
        if dist < twoCloseDistances[0] and dist < twoCloseDistances[1]:
            twoCloseDistances[0] = copy.copy( twoCloseDistances[1] )
            twoCloseDistances[1] = dist
            twoClosePoints[0] = copy.copy( twoClosePoints[1] )
            twoClosePoints[1] = point
        elif dist < twoCloseDistances[0]:
            twoCloseDistances[0] = dist
            twoClosePoints[0] = point
    
    pointFirstIntersect = om.MPoint()
    if not twoClosePoints[1]:
        if not twoClosePoints[0]:
            pointFirstIntersect = point1
        else:
            pointFirstIntersect = twoClosePoints[0]
    elif not twoClosePoints[0]:
        if not twoClosePoints[1]:
            pointFirstIntersect = point1
        else:
            pointFirstIntersect = twoClosePoints[1]
    else:
        pointFirstIntersect = om.MPoint( ( om.MVector( twoClosePoints[0] ) + om.MVector( twoClosePoints[1] ) )/ 2 )
    
    #cmds.spaceLocator( p=[pointFirstIntersect.x, pointFirstIntersect.y, pointFirstIntersect.z] )
    
    intersectPoints = om.MPointArray()
    invIntersectPoints = om.MPointArray()
    fnMesh.intersect( pointFirstIntersect, vCross, intersectPoints )
    fnMesh.intersect( pointFirstIntersect, -vCross, invIntersectPoints )
    
    allIntersectPoints = []
    for i in range( intersectPoints.length() ):
        allIntersectPoints.append( intersectPoints[i] )
    
    for i in range( invIntersectPoints.length() ):
        allIntersectPoints.append( invIntersectPoints[i] )
    
    twoCloseDistances = [100000000.0, 100000000.0]
    twoClosePoints = [None, None]
    
    for point in allIntersectPoints:
        for i in range( 2 ):
            dist = point.distanceTo( pointClose )
        if dist < twoCloseDistances[0] and dist < twoCloseDistances[1]:
            twoCloseDistances[0] = copy.copy( twoCloseDistances[1] )
            twoCloseDistances[1] = dist
            twoClosePoints[0] = copy.copy( twoClosePoints[1] )
            twoClosePoints[1] = point
        elif dist < twoCloseDistances[0]:
            twoCloseDistances[0] = dist
            twoClosePoints[0] = point
    
    returnPoint = om.MPoint()
    if not twoClosePoints[1]:
        if not twoClosePoints[0]:
            returnPoint = om.MPoint( om.MVector( point1 ) + om.MVector( point2 ) )/ 2
        else:
            returnPoint = twoClosePoints[0]
    elif not twoClosePoints[0]:
        if not twoClosePoints[1]:
            returnPoint = om.MPoint( om.MVector( point1 ) + om.MVector( point2 ) )/ 2
        else:
            returnPoint = twoClosePoints[1]
    else:
        returnPoint = om.MPoint( ( om.MVector( twoClosePoints[0] ) + om.MVector( twoClosePoints[1] ) )/ 2 )
    
    fnMesh.setPoints( origMeshPoints )
    
    '''
    points = []
    points.append( [twoClosePoints[0].x, twoClosePoints[0].y, twoClosePoints[0].z] )
    points.append( [twoClosePoints[1].x, twoClosePoints[1].y, twoClosePoints[1].z] )
    cmds.curve( p=points, d=1 )
    
    cmds.select( d=1 )
    cmds.joint( p=[returnPoint.x, returnPoint.y, returnPoint.z] )'''
    
    return returnPoint



def createJointLineFromMesh( twoVertices, repeat = 3 ):
    
    dagPath, index1, index2 = getSelectionListFromVertices( twoVertices )
    
    fnMesh = om.MFnMesh( dagPath )
    points = om.MPointArray()
    
    fnMesh.getPoints( points )
    
    point1 = points[index1]
    point2 = points[index2]
    
    centerPoint = om.MPoint()
    centerPoint.x = (point1.x + point2.x)/2.0
    centerPoint.y = (point1.y + point2.y)/2.0
    centerPoint.z = (point1.z + point2.z)/2.0
    
    def getIntersectPoints( point1, point2, length=4 ):
        
        returnList = []
        if length == 0: return  []
        intersectPoint = getIntersectionPointFromTwoPoint( fnMesh, point1, point2 )
        
        returnList += getIntersectPoints( point1, intersectPoint, length-1 )
        returnList.append( intersectPoint )
        returnList += getIntersectPoints( intersectPoint, point2, length-1 )
        
        return returnList
    
    pointList = []
    pointList.append( point1 )
    pointList += getIntersectPoints( point1, point2, repeat )
    pointList.append( point2 )
    
    points = []
    for point in pointList:
        points.append( [ point.x, point.y, point.z ] )
    
    cmds.select( d=1 )
    
    for point in points:
        cmds.joint( p=point )



def createJointLineFromMeshApi( dagPathMesh, point1, point2, repeat = 3 ):
    
    fnMesh = om.MFnMesh( dagPathMesh )
    points = om.MPointArray()
    
    fnMesh.getPoints( points )
    
    centerPoint = om.MPoint()
    centerPoint.x = (point1.x + point2.x)/2.0
    centerPoint.y = (point1.y + point2.y)/2.0
    centerPoint.z = (point1.z + point2.z)/2.0
    
    intersector = om.MMeshIntersector()
    intersector.create( fnMesh.object() )
    
    def getIntersectPoints( point1, point2, length=4 ):
        
        returnList = []
        if length == 0: return  []
        intersectPoint = getIntersectionPointFromTwoPoint( fnMesh, point1, point2 )
        
        returnList += getIntersectPoints( point1, intersectPoint, length-1 )
        returnList.append( intersectPoint )
        returnList += getIntersectPoints( intersectPoint, point2, length-1 )
        
        return returnList
    
    pointList = []
    pointList.append( point1 )
    pointList += getIntersectPoints( point1, point2, repeat )
    pointList.append( point2 )
    
    points = []
    for point in pointList:
        points.append( [ point.x, point.y, point.z ] )
    
    cmds.select( d=1 )
    
    jnts = []
    for point in points:
        jnt = cmds.joint( p=point )
        jnts.append( jnt )
    
    return jnts
    



def getCloseIndex( point, mesh ):
    
    import sgBFunction_dag
    
    if type( point ) in [ type(()), type([]) ]:
        point = om.MPoint( *point )
    
    mesh = sgBFunction_dag.getShape( mesh )
    
    oMesh = sgBFunction_dag.getMObject( mesh )
    fnMesh = om.MFnMesh( oMesh )
    
    intersector = om.MMeshIntersector()
    intersector.create(  oMesh  )
    
    pointOnMesh = om.MPointOnMesh()
    points = om.MPointArray()
    fnMesh.getPoints( points )
    
    intersector.getClosestPoint( point, pointOnMesh )
    
    indexFace = pointOnMesh.faceIndex()
    indicesVts = om.MIntArray()
    
    fnMesh.getPolygonVertices( indexFace, indicesVts )
    
    closeDist = 1000000.0
    closeIndex = indicesVts[0]
    for i in range( indicesVts.length() ):
        compairPoint = points[ indicesVts[i] ]
        dist = point.distanceTo( compairPoint )
        if dist < closeDist:
            closeDist = dist
            closeIndex = indicesVts[i]
    return closeIndex



def getUVAtPoint( point, mesh ):
    
    if type( point ) in [ type([]), type(()) ]:
        point = om.MPoint( *point )
    
    meshShape = sgBFunction_dag.getShape( mesh )
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( meshShape ) )
    
    util = om.MScriptUtil()
    util.createFromList( [0.0,0.0], 2 )
    uvPoint = util.asFloat2Ptr()
    fnMesh.getUVAtPoint( point, uvPoint, om.MSpace.kWorld )
    u = om.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 0 )
    v = om.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 1 )
    
    return u, v



def getPointAttrFromVertex( targetVertex ):

    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgRigAddition' )

    def getNodeFromMesh( mesh, isFirst=True ):
    
        import sgBFunction_dag
        
        if cmds.objectType( mesh ) == 'transform':
            mesh = sgBFunction_dag.getShape( mesh )
        
        cons = cmds.listConnections( mesh+'.wm', type='sgMatrixFromVertices' )
        if cons: return cons[0]
        
        node = cmds.createNode( 'sgMatrixFromVertices' )
        cmds.connectAttr( mesh+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( mesh+'.wm', node+'.inputMeshMatrix' )
        
        return node
    
    import sgCFnc_dag
    cmds.select( targetVertex )
    
    mDagPath, mIntArrU, mIntArrV, mIntArrW = sgCFnc_dag.getMDagPathAndComponent()[0]

    fnMesh = om.MFnMesh( mDagPath )
    mesh   = fnMesh.name()
    
    node = getNodeFromMesh( mesh )
    cmds.setAttr( node+'.verticeId[%d]' % mIntArrU[0], mIntArrU[0] )
    return node+'.outputTranslate[%d]' % mIntArrU[0]



def buildCombineMesh( meshs ):
    
    meshDatas = []
    
    pointLength = 0
    polygonCountsLength = 0
    polygonConnectsLength = 0
    
    uArrayLength = 0
    vArrayLength = 0
    uvCountsLength = 0
    uvIdsLength = 0
    
    for mesh in meshs:
        meshData = getMeshData( mesh )
        meshDatas.append( meshData )
        meshData.matrix = sgBFunction_dag.getMDagPath2( mesh ).inclusiveMatrix()
        
        pointLength += len( meshData.polygonData.points )
        polygonCountsLength += len( meshData.polygonData.polygonCounts )
        polygonConnectsLength += len( meshData.polygonData.polygonConnects )
        
        if meshData.uvDatas:
            uArrayLength += len( meshData.uvDatas[0].uArray )
            vArrayLength += len( meshData.uvDatas[0].vArray )
            uvCountsLength += len( meshData.uvDatas[0].uvCounts )
            uvIdsLength += len( meshData.uvDatas[0].uvIds )
    
    mainMeshData = sgBModel_mesh.CMeshData()
    mainMeshData.uvDatas.append( sgBModel_mesh.CUVData() )
    
    cuPointsIndex = 0
    cuPolyCountsIndex = 0
    cuPolyConnectsIndex = 0
    cuUArrayIndex = 0
    cuVArrayIndex = 0
    cuUvCountsIndex = 0
    cuUvIdsIndex = 0
    
    mainMeshData.polygonData.points.setLength( pointLength )
    mainMeshData.polygonData.polygonCounts.setLength( polygonCountsLength )
    mainMeshData.polygonData.polygonConnects.setLength( polygonConnectsLength )
    
    mainMeshData.uvDatas[0].uArray.setLength( uArrayLength )
    mainMeshData.uvDatas[0].vArray.setLength( vArrayLength )
    mainMeshData.uvDatas[0].uvCounts.setLength( uvCountsLength )
    mainMeshData.uvDatas[0].uvIds.setLength( uvIdsLength )
    
    for meshData in meshDatas:
        polygonData = meshData.polygonData
        uvDatas     = meshData.uvDatas
        matrix      = meshData.matrix
        
        for i in range( len( polygonData.points ) ):
            mainMeshData.polygonData.points[cuPointsIndex + i] = polygonData.points[i] * matrix
        for i in range( len( polygonData.polygonCounts ) ):
            mainMeshData.polygonData.polygonCounts[cuPolyCountsIndex + i] = polygonData.polygonCounts[i]
        for i in range( len( polygonData.polygonConnects ) ):
            mainMeshData.polygonData.polygonConnects[cuPolyConnectsIndex + i] = polygonData.polygonConnects[i] + cuPointsIndex
        
        if uvDatas:
            for i in range( len( meshData.uvDatas[0].uArray ) ):
                mainMeshData.uvDatas[0].uArray[cuUArrayIndex + i] = uvDatas[0].uArray[i]
            for i in range( len( meshData.uvDatas[0].vArray ) ):
                mainMeshData.uvDatas[0].vArray[cuVArrayIndex + i] = uvDatas[0].vArray[i]
            for i in range( len( meshData.uvDatas[0].uvCounts ) ):
                mainMeshData.uvDatas[0].uvCounts[cuUvCountsIndex + i] = uvDatas[0].uvCounts[i]
            for i in range( len( meshData.uvDatas[0].uvIds ) ):
                mainMeshData.uvDatas[0].uvIds[cuUvIdsIndex + i] = uvDatas[0].uvIds[i] + cuPointsIndex
            
            cuUArrayIndex += len( uvDatas[0].uArray )
            cuVArrayIndex += len( uvDatas[0].vArray )
            cuUvCountsIndex += len( uvDatas[0].uvCounts )
            cuUvIdsIndex += len( uvDatas[0].uvIds )
        
        cuPointsIndex += len( meshData.polygonData.points )
        cuPolyCountsIndex += len( meshData.polygonData.polygonCounts )
        cuPolyConnectsIndex += len( meshData.polygonData.polygonConnects )
    
    buildFromMeshData( mainMeshData )



class MeshElementInfo:
    
    def __init__( self ):
        
        import maya.OpenMaya as om
        
        self.meshName = ''
        self.numVertices = 0
        self.numPolygons = 0
        self.bbc = om.MPoint()
        self.faceIndices = om.MIntArray()
        self.shadingSet = ''

    def selectFaces( self ):
        
        import maya.OpenMaya as om
        import sgBFunction_dag
        
        meshShape = sgBFunction_dag.getShape( self.meshName )
        dagPathShape = sgBFunction_dag.getMDagPath( meshShape )
        
        singleComp = om.MFnSingleIndexedComponent()
        singleCompObj = singleComp.create( om.MFn.kMeshPolygonComponent )
        singleComp.addElements( self.faceIndices )
        
        selList = om.MSelectionList()
        selList.add( dagPathShape, singleCompObj )
        om.MGlobal.selectCommand( selList )





def getMeshElementInfo( target ):
    
    import random
    import maya.OpenMaya as om
    import sgBFunction_dag
    import sgBFunction_base
    import copy
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    targetShape = sgBFunction_dag.getShape( target )
    dagPathShape = sgBFunction_dag.getMDagPath( targetShape )
    
    cmds.sgGetMeshElementInfo( target, set=1 )
    numElement  = cmds.sgGetMeshElementInfo( ne=1 )
    numVertices = cmds.sgGetMeshElementInfo( nv=1 )
    numPolygons = cmds.sgGetMeshElementInfo( np=1 )
    bbcs        = cmds.sgGetMeshElementInfo( bbc=1 )
    faceIndices = cmds.sgGetMeshElementInfo( fi=1 )
    
    meshElementInfos = []
    for i in range( numElement ):
        
        meshElementInfo = MeshElementInfo()
        
        startFaceIndex = 0
        lastFaceIndex  = 0
        
        for j in range( i ):
            startFaceIndex += int( numPolygons[j] )
        for j in range( i+1 ):
            lastFaceIndex += int( numPolygons[j] )
    
        compArray = om.MIntArray()
        compArray.setLength( int( numPolygons[i] ) )
        for j in range( startFaceIndex, lastFaceIndex ):
            compArray.set( faceIndices[j], j-startFaceIndex )
        
        pointBbc = om.MPoint()
        pointBbc.x = bbcs[i*3+0]
        pointBbc.y = bbcs[i*3+1]
        pointBbc.z = bbcs[i*3+2]
        
        engine = 'initialShadingGroup'
        engines = cmds.listConnections( targetShape, type='shadingEngine' )
        if engines:
            engine = engines[0]
        
        meshElementInfo.meshName    = targetShape
        meshElementInfo.numVertices = numVertices[i]
        meshElementInfo.numPolygons = numPolygons[i]
        meshElementInfo.bbc         = pointBbc
        meshElementInfo.faceIndices = compArray
        meshElementInfo.shadingSet  = engine
        
        meshElementInfos.append( meshElementInfo )

    return meshElementInfos




def createCombineMesh( meshs ):
    
    import sgBFunction_base
    import sgBFunction_dag
    
    meshs = sgBFunction_dag.getChildrenMeshExists( meshs )
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    node = cmds.createNode( 'sgPolyUnit' )
    
    combineMesh = cmds.createNode( 'mesh' )
    combineMeshObj = cmds.listRelatives( combineMesh, p=1, f=1 )[0]
    
    for i in range( len( meshs ) ):
        mesh = sgBFunction_dag.getShape( meshs[i] )
        cmds.connectAttr( mesh+'.worldMesh[0]', node+'.inputMeshs[%d]' % i )

    cmds.connectAttr( node+'.outputMesh', combineMesh+'.inMesh' )
    cmds.sets( combineMeshObj, e=1, forceElement ='initialShadingGroup' )
    
    return combineMeshObj



def createSeparateMesh( meshs ):
    
    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    meshs = sgBFunction_dag.getChildrenMeshExists( meshs )
    
    node = cmds.createNode( 'sgSeparate' )
    
    allElementLength = 0
    for i in range( len( meshs ) ):
        meshShape = sgBFunction_dag.getShape( meshs[i] )
        cmds.connectAttr( meshShape+'.worldMesh[0]', node+'.inputMeshs[%d]' % i )
        meshElementInfos = getMeshElementInfo( meshs[i] )
        allElementLength += len( meshElementInfos )
    
    index = 0
    for i in range( allElementLength ):
        sepMesh = cmds.createNode( 'mesh' )
        meshObj = sgBFunction_dag.getTransform( sepMesh )
        cmds.setAttr( node+'.elements[%d].elementIndices[%d]' %( i, 0 ), i+1 )
        cmds.connectAttr( node+'.outputMeshs[%d]' % i, sepMesh+'.inMesh' )
        cmds.rename( meshObj, 'element_%d' % (index+1) )
        index +=1



def separateSourceAsTarget( sourceGroup, targetGroup ):
    
    import sgBFunction_base
    import sgBFunction_attribute
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    sources = sgBFunction_dag.getChildrenMeshExists( sourceGroup )
    targets = sgBFunction_dag.getChildrenMeshExists( targetGroup )
    
    sourceElementInfos = []
    node = cmds.createNode( 'sgSeparate' )
    
    elementIndex = 1
    for i in range( len( sources ) ):
        if cmds.attributeQuery( 'skip', node=sources[i], ex=1 ): continue
        elementInfos = getMeshElementInfo( sources[i] )
        
        for j in range( len( elementInfos ) ):
            elementInfos[j].elementIndex = elementIndex
            elementInfos[j].isChecked = False
            sourceElementInfos.append( elementInfos[j] )
            elementIndex += 1
        cmds.connectAttr( sources[i]+'.worldMesh', node+'.inputMeshs[%d]' % i )
    
    returnMeshs = []
    for i in range( len( targets ) ):
        if cmds.attributeQuery( 'skip', node=targets[i], ex=1 ): continue
        targetElementInfos = getMeshElementInfo( targets[i] )

        sameElementIndices = []
        for targetElementInfo in targetElementInfos: 
            
            targetNumVertices = targetElementInfo.numVertices
            targetNumPolygons = targetElementInfo.numPolygons
            targetBBC         = targetElementInfo.bbc
            
            minDistance = 1000000.0
            sameElementInfo = None
            for j in range( len( sourceElementInfos ) ):
                
                sourceNumVertices = sourceElementInfos[j].numVertices
                sourceNumPolygons = sourceElementInfos[j].numPolygons
                sourceBBC         = sourceElementInfos[j].bbc

                if targetNumVertices != sourceNumVertices: continue
                if targetNumPolygons != sourceNumPolygons: continue
                
                dist = targetBBC.distanceTo( sourceBBC )
                
                if dist < minDistance:
                    minDistance = dist
                    sameElementInfo = sourceElementInfos[j]
                    if dist < 0.0001: break
            
            if sameElementInfo:
                sameElementIndices.append( sameElementInfo.elementIndex )

        
        targetTransform = sgBFunction_dag.getTransform( targets[i] )
        targetName = targetTransform.split( '|' )[-1]
        
        if len( targetElementInfos ) != len( sameElementIndices ):
            print " is not same : ", targetName, len( targetElementInfos ), len( sameElementIndices )
            continue
        #print targetName, len( targetElementInfos ), len( sameElementIndices )

        newMeshShape = cmds.createNode( 'mesh' )
        newMeshTr    = sgBFunction_dag.getTransform( newMeshShape )
        newMeshTr    = cmds.rename( newMeshTr, targetName+'_new' )
        newMeshShape = sgBFunction_dag.getShape( newMeshTr )
        
        sgBFunction_attribute.addAttr( newMeshTr, ln='msgTargetMesh', at='message' )
        cmds.connectAttr( targetTransform+'.message', newMeshTr+'.msgTargetMesh' )
        
        for j in range( len( sameElementIndices ) ):
            cmds.setAttr( node+'.elements[%d].elementIndices[%d]' %( i, j ), sameElementIndices[j] )
        
        cmds.connectAttr( node+'.outputMeshs[%d]' % i, newMeshShape+'.inMesh' )
    
        returnMeshs.append( newMeshTr )
    
    return returnMeshs




import copy


def getVerticesFromEdge( fnMesh, edgeNum ):

    util = om.MScriptUtil()
    util.createFromList( [0,0], 2 )
    int2Ptr = util.asInt2Ptr()
    fnMesh.getEdgeVertices( edgeNum, int2Ptr )
    first = om.MScriptUtil.getInt2ArrayItem( int2Ptr, 0, 0 )
    second = om.MScriptUtil.getInt2ArrayItem( int2Ptr, 0, 1 )
    return first, second



def getSortLineVertices():

    selList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList( selList )
    
    returnTargets = []
    for i in range( selList.length() ):
        mDagPath = om.MDagPath()
        mObject  = om.MObject()
        selList.getDagPath( i, mDagPath, mObject )
        
        mIntArr = om.MIntArray()
        if not mObject.isNull():
            if mObject.apiType() == om.MFn.kMeshEdgeComponent:
                component = om.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArr )
        if not mIntArr.length(): continue
        
        checkMap = [ 0 for i in range( mIntArr.length() ) ]
        
        fnMesh = om.MFnMesh( mDagPath )
        sortVertices = []
        
        idLeft, idRight = getVerticesFromEdge( fnMesh, mIntArr[0] ) 
        sortVertices = []
        
        nextLVtx = copy.copy( idLeft )
        nextRVtx = copy.copy( idRight )
        sortVertices = [ idLeft, idRight ]
        print idLeft, idRight
        
        for k in range( mIntArr.length() ):
            for j in range( 1, mIntArr.length() ):
                if checkMap[j]: continue
                idsNextVertices = getVerticesFromEdge( fnMesh, mIntArr[j] )
                
                if nextRVtx in idsNextVertices:
                    if nextRVtx == idsNextVertices[0]:
                        if not idsNextVertices[1] in sortVertices:
                            nextRVtx = copy.copy( idsNextVertices[1] )
                            sortVertices.append( nextRVtx )
                            checkMap[j] = 1
                    else:
                        if not idsNextVertices[0] in sortVertices:
                            nextRVtx = copy.copy( idsNextVertices[0] )
                            sortVertices.append( nextRVtx )
                            checkMap[j] = 1

            for j in range( 1, mIntArr.length() ):
                if checkMap[j]: continue
                idsNextVertices = getVerticesFromEdge( fnMesh, mIntArr[j] )
                
                if nextLVtx in idsNextVertices:
                    if nextLVtx == idsNextVertices[0]:
                        if not idsNextVertices[1] in sortVertices:
                            nextLVtx = copy.copy( idsNextVertices[1] )
                            sortVertices.insert( 0, nextLVtx )
                            checkMap[j] = 1
                    else:
                        if not idsNextVertices[0] in sortVertices:
                            nextLVtx = copy.copy( idsNextVertices[0] )
                            sortVertices.insert( 0, nextLVtx )
                            checkMap[j] = 1
        
        returnTargets.append( [fnMesh.name(), sortVertices] )
        
    return returnTargets




def sgMeshSnap( meshBase, meshDeformTarget ):
    
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    meshDeformTarget = sgBFunction_dag.getShape( meshDeformTarget )
    meshBase         = sgBFunction_dag.getShape( meshBase )
    
    node = cmds.deformer( meshDeformTarget, type='sgMeshSnap' )[0]
    cmds.connectAttr( meshBase+'.worldMesh[0]', node+'.snapMesh' )
    
    dagPathDt = sgBFunction_dag.getMDagPath( meshDeformTarget )
    dagPathBs = sgBFunction_dag.getMDagPath( meshBase )
    
    mtxDt     = dagPathDt.inclusiveMatrix()
    mtxBsInv  = dagPathBs.inclusiveMatrixInverse()
    mtxSrcToTrgLocal = mtxDt * mtxBsInv
    
    fnMeshDt = om.MFnMesh( dagPathDt )
    fnMeshBs = om.MFnMesh( dagPathBs )
    intersector = om.MMeshIntersector()
    intersector.create( fnMeshBs.object() )
    
    pointsDt = om.MPointArray()
    pointsBs = om.MPointArray()
    fnMeshDt.getPoints( pointsDt )
    fnMeshBs.getPoints( pointsBs )
    
    pointOnMesh = om.MPointOnMesh()
    idsVertices = om.MIntArray()
    for i in range( pointsDt.length() ):
        pointLocal = pointsDt[i] * mtxSrcToTrgLocal
        
        intersector.getClosestPoint( pointLocal, pointOnMesh )
        fnMeshBs.getPolygonVertices( pointOnMesh.faceIndex(), idsVertices )
        
        minDist = 100000.0
        minIndex = idsVertices[0]
        for j in range( idsVertices.length() ):
            dist = pointsBs[ idsVertices[j] ].distanceTo( pointLocal )
            if dist < minDist:
                minIndex = idsVertices[j]
                minDist = dist
        if minDist > 0.1: continue
        
        cmds.setAttr( node+'.idsMap[%d]' % i, minIndex )



def separateCacheBodyObject( cachebodyObj, outObj, checkComp= True ):
    
    import sgBFunction_dag
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    sels = cmds.ls( sl=1 )
    source = sels[0]
    target = sels[1]
    
    sourceMeshs = sgBFunction_dag.getChildrenMeshExists( source )
    targetMeshs = sgBFunction_dag.getChildrenMeshExists( target )
    
    srcElementIndex = 0
    sourceElementInfos = []
    
    node = cmds.createNode( 'sgSeparate' )
    for i in range( len( sourceMeshs ) ):
        meshShape = sgBFunction_dag.getShape( sourceMeshs[i] )
        elementInfos = getMeshElementInfo( sourceMeshs[i] )
        
        for element in elementInfos:
            element.elementIndex = srcElementIndex
        
        sourceElementInfos += elementInfos
        srcElementIndex += 1
        cmds.connectAttr( meshShape+'.worldMesh', node+'.inputMeshs[%d]' % i )
    
    outputMeshIndex = 0
    for i in range( len( targetMeshs ) ):
        elementInfos = getMeshElementInfo( targetMeshs[i] )
        
        sameElementInfoIndices = []
        for element in elementInfos:
            numVertices = element.numVertices
            numPolygons = element.numPolygons

            bbc = element.bbc

            minDist = 1000000.0
            sameElementInfoIndex = -1
            for k in range( len( sourceElementInfos ) ):
                if checkComp:
                    if numVertices != sourceElementInfos[k].numVertices: continue
                    if numPolygons != sourceElementInfos[k].numPolygons: continue
                dist = sourceElementInfos[k].bbc.distanceTo( bbc )
                
                if dist > 2: continue
                
                if dist < minDist:
                    minDist = dist
                    sameElementInfoIndex = copy.copy( k )
            if sameElementInfoIndex != -1:
                sameElementInfoIndices.append( sameElementInfoIndex )

        if not sameElementInfoIndices:
            print "%s same indices not exists" % targetMeshs[i].split( '|' )[-1]
            continue
        newMeshShape = cmds.createNode( 'mesh' )
        for j in range( len( sameElementInfoIndices ) ):
            cmds.setAttr( node+'.elements[%d].elementIndices[%d]' %( outputMeshIndex, j ), sameElementInfoIndices[j]+1 )
        cmds.connectAttr( node+'.outputMeshs[%d]' % outputMeshIndex, newMeshShape+'.inMesh' )
        
        newMeshTr = sgBFunction_dag.getTransform( newMeshShape )
        cmds.rename( newMeshTr, targetMeshs[i].split( '|' )[-1] + '_newMesh' )
        outputMeshIndex += 1



def separateCacheBodyObject2( cachebodyObj, outObj, checkComp = False, copyAttrUd = False ):
    
    import sgBFunction_dag
    import sgBFunction_base
    import sgBFunction_attribute
    import sgRigConnection
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    sels = cmds.ls( sl=1 )
    source = sels[0]
    target = sels[1]
    
    sourceMeshs = sgBFunction_dag.getChildrenMeshExists( source )
    targetMeshs = sgBFunction_dag.getChildrenMeshExists( target )
    
    srcElementIndex = 0
    sourceElementInfos = []
    
    node = cmds.createNode( 'sgSeparate' )
    for i in range( len( sourceMeshs ) ):
        print "Source mesh : ", sourceMeshs[i]
        meshShape = sgBFunction_dag.getShape( sourceMeshs[i] )
        elementInfos = getMeshElementInfo( sourceMeshs[i] )
        
        for element in elementInfos:
            element.elementIndex = srcElementIndex
        
        sourceElementInfos += elementInfos
        srcElementIndex += 1
        cmds.connectAttr( meshShape+'.worldMesh', node+'.inputMeshs[%d]' % i )
    
    newElementIndex = 0
    newMeshs = []
    transferTargets = []
    
    for i in range( len( targetMeshs ) ):
        elementInfos = getMeshElementInfo( targetMeshs[i] )
        
        snameElementInfoMeshAndIndices = []
        for element in elementInfos:
            numVertices = element.numVertices
            numPolygons = element.numPolygons

            bbc = element.bbc

            minDist = 1000000.0
            sameElementInfoIndex = -1
            meshName             = ''
            for k in range( len( sourceElementInfos ) ):
                if checkComp:
                    if numVertices != sourceElementInfos[k].numVertices: continue
                    if numPolygons != sourceElementInfos[k].numPolygons: continue
                dist = sourceElementInfos[k].bbc.distanceTo( bbc )
                
                if dist > 2: continue
                
                if dist < minDist:
                    minDist = dist
                    sameElementInfoIndex = k
                    meshName             = sgBFunction_dag.getTransform( sourceElementInfos[k].meshName )
            if sameElementInfoIndex != -1:
                existsMeshName = False
                for m in range( len( snameElementInfoMeshAndIndices) ):
                    if snameElementInfoMeshAndIndices[m][0] == meshName:
                        snameElementInfoMeshAndIndices[m][1].append( sameElementInfoIndex )
                        existsMeshName = True
                if not existsMeshName:
                    snameElementInfoMeshAndIndices.append( [meshName,[sameElementInfoIndex]] )
                    
        if not snameElementInfoMeshAndIndices:
            print "%s same indices not exists" % targetMeshs[i].split( '|' )[-1]
            continue
        
        print "Target mesh : ", targetMeshs[i]
        for j in range( len( snameElementInfoMeshAndIndices ) ):
            meshName, elementIndices = snameElementInfoMeshAndIndices[j]
            newMeshShape = cmds.createNode( 'mesh' )
            for k in range( len( elementIndices ) ):
                cmds.setAttr( node+'.elements[%d].elementIndices[%d]' %( newElementIndex, k ), elementIndices[k]+1 )
            cmds.connectAttr( node+'.outputMeshs[%d]' % newElementIndex, newMeshShape+'.inMesh' )
            newElementIndex += 1
            
            newMeshTr = sgBFunction_dag.getTransform( newMeshShape )
            newMeshTr = cmds.rename( newMeshTr, targetMeshs[i].split( '|' )[-1] + '_newMesh_0' )
            newMeshs.append( newMeshTr )
            
            transferTargets.append( [meshName, newMeshTr] )
    
    print "before refresh"
    cmds.refresh()

    for meshName, newMeshShape in transferTargets:
        try:
            cmds.transferAttributes( meshName, newMeshShape, transferPositions=0, transferNormals=0, transferUVs=1, sourceUvSet="map1", targetUvSet="map1",
                                     transferColors=0, sampleSpace=0, sourceUvSpace="map1", targetUvSpace="map1", searchMethod=3, flipUVs=0, colorBorders=1 )
            meshShape = sgBFunction_dag.getShape( meshName )
            newMeshShape = sgBFunction_dag.getShape( newMeshShape )
            sgBFunction_attribute.copyShapeAttr(meshShape, newMeshShape, copyAttrUd )
            sgRigConnection.copyShader( meshName, newMeshShape )
        except:
            cmds.warning( '%s is not deformable' % newMeshShape )
        
    return newMeshs



def getOrderedEdgeRings( targetEdge ):
    cmds.select( targetEdge )
    cmds.SelectEdgeRingSp()
    ringEdges = cmds.ls( sl=1, fl=1 )
    connectedEdges = []
    
    for edge in ringEdges:
        vertices = cmds.ls( cmds.polyListComponentConversion( edge, tv=1 ), fl=1 )
        edges = cmds.ls( cmds.polyListComponentConversion( vertices, te=1 ), fl=1 )
        secondVertices = cmds.ls( cmds.polyListComponentConversion( edges, tv=1 ), fl=1 )
        
        for vertex in vertices:
            secondVertices.remove( vertex )
        
        lastEdges = []
        existEdges = []
        for secondVertex in secondVertices:
            getEdges = cmds.ls( cmds.polyListComponentConversion( secondVertex, te=1 ), fl=1 )
            for edge in getEdges:
                if edge in lastEdges: existEdges.append( edge )
                else: lastEdges.append( edge )
        connectedEdges.append( existEdges )
    
    for i in range( len( ringEdges ) ):
        if len( connectedEdges[i] ) == 1:
            break
    
    nextIndex = ringEdges.index( connectedEdges[i][0] )
    orderedEdges = [ ringEdges[i], ringEdges[ nextIndex ] ]
    
    startNum = 0
    while len( connectedEdges[ nextIndex ]  )== 2:
        edges = connectedEdges[ nextIndex ]
        exists = False
        for edge in edges:
            if not edge in orderedEdges:
                orderedEdges.append( edge )
                exists = True
                break
        if not exists: break
        nextIndex = ringEdges.index( edge )
        startNum += 1
    
    return orderedEdges