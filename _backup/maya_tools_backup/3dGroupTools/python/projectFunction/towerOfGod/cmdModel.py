import maya.cmds as cmds
import maya.OpenMaya as om
import math

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
        


def getMFnMesh( meshName ):
    selList = om.MSelectionList()
    selList.add( meshName )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return om.MFnMesh( dagPath )

def getMFnCurve( curveName ):
    selList = om.MSelectionList()
    selList.add( curveName )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return om.MFnNurbsCurve( dagPath )


def createCurveFromMesh( meshName, centerIndices, startIndex, endIndices, numSample=20 ):
    
    bb = om.MBoundingBox()
    for i in centerIndices:
        point = om.MPoint( *cmds.xform( meshName+'.vtx[%d]' % i, q=1, ws=1, t=1 ) )
        bb.expand( point )
    centerPoint = bb.center()
    
    bb = om.MBoundingBox()
    for i in endIndices:
        point = om.MPoint( *cmds.xform( meshName+'.vtx[%d]' % i, q=1, ws=1, t=1 ) )
        bb.expand( point )
    endPoint = bb.center()
    startPoint = om.MPoint( *cmds.xform( meshName+'.vtx[%d]' % startIndex, q=1, ws=1, t=1 ) )
    
    aimVector = om.MVector( endPoint ) - om.MVector( startPoint )
    eachPoints = []
    
    multRate = 1.0/( numSample-1 )
    for i in range( numSample ):
        eachPoint = aimVector * (multRate*i) + om.MVector( centerPoint )
        eachPoints.append( om.MPoint( eachPoint ) )
    
    fnMesh = getMFnMesh( meshName )
    mtx = fnMesh.dagPath().inclusiveMatrix()
    mtxInv = mtx.inverse()
    intersector = om.MMeshIntersector()
    intersector.create( fnMesh.object() )
    
    pointOnMesh = om.MPointOnMesh()
    for point in eachPoints:
        intersector.getClosestPoint( point*mtxInv, pointOnMesh )
        closePoint = om.MPoint( pointOnMesh.getPoint() )*mtx
        cmds.spaceLocator( p=[closePoint.x, closePoint.y, closePoint.z] )



def createCurveToEdgeLoop():
    
    sels = cmds.ls( sl=1, fl=1 )
    selObject = cmds.ls( sl=1, o=1 )[0]
    selObject = cmds.listRelatives( selObject, p=1 )[0]
    excutedEdges = []
    curves = []
    for sel in sels:
        if sel in excutedEdges: continue
        cmds.select( sel )
        cmds.SelectEdgeLoopSp()
        excutedEdges += cmds.ls(sl=1, fl=1 )
        curves.append( cmds.polyToCurve( form=0, degree=3 )[0] )
    
    cmds.select( curves )
    cmds.DeleteHistory()
    return cmds.ls( sl=1 )
        


def createLocator( mpoint ):
    loc = cmds.spaceLocator( p=[mpoint.x, mpoint.y, mpoint.z] )[0]
    locShape = cmds.listRelatives( loc, s=1 )[0]
    cmds.setAttr( locShape+'.localScale', 0.1, 0.1, 0.1 )
    

def sortPoints( pointArr ):
    points = om.MPointArray()
    for i in range( pointArr.length() ):
        samePositionExists = False
        for j in range( points.length() ):
            if pointArr[i].distanceTo( points[j] ) < 0.0001:
                samePositionExists = True
        if not samePositionExists:
            points.append( pointArr[i] )
    return points

        
def offsetCurveBasedOnMesh( curve, mesh, offsetRate ):
    
    fnMesh = getMFnMesh( mesh )
    fnCurve = getMFnCurve( curve )
    invOffsetRate = 1.0 - offsetRate
    
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    curveMtx = fnCurve.dagPath().inclusiveMatrix()
    toMeshLocalMtx = curveMtx*meshMtx.inverse()
    toCurveLocalMtx = meshMtx*curveMtx.inverse()
    
    curveCVs = om.MPointArray()
    fnCurve.getCVs( curveCVs )
    
    localPoints = []
    for i in range( curveCVs.length() ):
        cvPoint = curveCVs[i]*toMeshLocalMtx
        localPoints.append( cvPoint )
    
    meshIntersector = om.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    dirVector = om.MVector( localPoints[-1] ) - om.MVector( localPoints[0] )
    dirVector.normalize()
    
    pointOnMesh = om.MPointOnMesh()
    
    getPoints = om.MPointArray()
    for i in range( len( localPoints ) ):
        try:meshIntersector.getClosestPoint( localPoints[i], pointOnMesh )
        except: 
            print "%s.cv[%d] check is failed" %( curve, i )
            continue
        normal = om.MVector( pointOnMesh.getNormal() )
        projVector = dirVector * ( normal*dirVector )
        intersectVector = normal - projVector
        interPoint = om.MPoint( (om.MVector( localPoints[i] ) + intersectVector ) )
        
        getPoints.clear()
        fnMesh.intersect( interPoint,-intersectVector, getPoints )
        
        if not getPoints.length(): continue
        getPoints = sortPoints( getPoints )
        
        pointsInfos = []
        for j in range( getPoints.length() ):
            dist = interPoint.distanceTo( getPoints[j] )
            pointsInfos.append( [dist,getPoints[j]] )
        pointsInfos.sort()
        
        sumLen = 0.0
        centerPoint = om.MVector( 0,0,0 )
        for j in range( len( pointsInfos ) ):
            if j >= 2: break
            centerPoint += om.MVector( pointsInfos[j][1] )
            sumLen += 1.0
        
        centerPoint /= sumLen
        
        cuPoint = centerPoint*offsetRate + om.MVector( pointsInfos[0][1] )*invOffsetRate
        cuPoint *= toCurveLocalMtx
        
        cmds.move( cuPoint.x, cuPoint.y, cuPoint.z, curve+'.cv[%d]' % i )
        
        
        
def cutCurve( curve, mesh, loopCheck = False ):
    
    fnMesh = getMFnMesh( mesh )
    fnCurve = getMFnCurve( curve )
    meshIntersector = om.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    curveMtx = fnCurve.dagPath().inclusiveMatrix()
    toMeshLocalMtx = curveMtx*meshMtx.inverse()
    
    numSpans = fnCurve.numSpans()
    
    maxParam = fnCurve.findParamFromLength( fnCurve.length() )
    
    paramRate = maxParam / ( numSpans-1 )
    
    point = om.MPoint()
    pointOnMesh = om.MPointOnMesh()
    
    closestParam = 0.0
    for i in range( numSpans ):
        fnCurve.getPointAtParam( paramRate*i, point )
        toMeshPoint = point*toMeshLocalMtx
        meshIntersector.getClosestPoint( toMeshPoint, pointOnMesh )
        closePoint = om.MPoint( pointOnMesh.getPoint() )
        normal  = om.MVector( pointOnMesh.getNormal() )
        
        closePivVector = om.MVector( toMeshPoint )-om.MVector( closePoint )
        if closePivVector*normal < 0:
            closestParam = paramRate*i
        else:
            if i == 0:
                if loopCheck: return None
                cmds.reverseCurve( curve, ch=0, rpo=1 )
                cutCurve( curve, mesh, True )
    
    i = 0
    addParam = 1
    while i < 100:
        fnCurve.getPointAtParam( closestParam, point )
        toMeshPoint = point*toMeshLocalMtx
        meshIntersector.getClosestPoint( toMeshPoint, pointOnMesh )
        closePoint = om.MPoint( pointOnMesh.getPoint() )
        cuDist = closePoint.distanceTo( toMeshPoint )
        if cuDist < 0.0001: break
        
        normal  = om.MVector( pointOnMesh.getNormal() )
        
        closePivVector = om.MVector( toMeshPoint ) - om.MVector( closePoint )
        if closePivVector*normal > 0:
            addParam = math.fabs( addParam ) * -0.5
        else:
            addParam = math.fabs( addParam ) * 0.5
        
        closestParam += addParam
        i+=1
    
    fnCurve.getPointAtParam( closestParam, point )
    first, second = cmds.detachCurve( "%s.u[%f]" %( curve, closestParam ), ch=0, cos=True, rpo=0 )
    curveObj = cmds.listRelatives( curve, p=1 )[0]
    cmds.delete( first, curveObj )
    second = cmds.rename( second, curveObj )
    cmds.select( second )
    cmds.DeleteHistory()