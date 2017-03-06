import maya.cmds as cmds
import maya.OpenMaya as om



def selectOutJoint( targetMesh ):

    import sgBFunction_dag
    
    skinNode = sgBFunction_dag.getNodeFromHistory( targetMesh, 'skinCluster' )[0]
    topJnt = cmds.listConnections( skinNode+'.matrix[0]' )[0]
    
    cmds.select( topJnt )




def selectOrigJoint( targetMesh ):
    
    import sgBFunction_dag
    
    skinNode = sgBFunction_dag.getNodeFromHistory( targetMesh, 'skinCluster' )[0]
    topJnt = cmds.listConnections( skinNode+'.matrix[0]' )[0]
    dcmp = cmds.listConnections( topJnt, s=1, d=0, type='decomposeMatrix' )[0]
    topJntOrig = cmds.listConnections( dcmp, s=1, d=0 )[0]
    handle = cmds.listConnections( topJntOrig, d=1, s=0, type='ikHandle' )[0]
    crv = cmds.listConnections( handle+'.inCurve' )[0]
    
    follicle = sgBFunction_dag.getNodeFromHistory( crv, 'follicle' )[0]
    
    curves = sgBFunction_dag.getNodeFromHistory( follicle, 'nurbsCurve' )
    
    mmdc = cmds.listConnections( curves[-1]+'.controlPoints[0]' )[0]
    jnt  = cmds.listConnections( mmdc+'.i[0]' )[0]
    
    cmds.select( jnt )




def selectFollicles( targetMesh ):
    
    import sgBFunction_dag
    
    skinNode = sgBFunction_dag.getNodeFromHistory( targetMesh, 'skinCluster' )[0]
    topJnt = cmds.listConnections( skinNode+'.matrix[0]' )[0]
    dcmp = cmds.listConnections( topJnt, s=1, d=0, type='decomposeMatrix' )[0]
    topJntOrig = cmds.listConnections( dcmp, s=1, d=0 )[0]
    handle = cmds.listConnections( topJntOrig, d=1, s=0, type='ikHandle' )[0]
    crv = cmds.listConnections( handle+'.inCurve' )[0]
    
    cmds.select( sgBFunction_dag.getNodeFromHistory( crv, 'follicle' ) )






def createCurveToEdgeLoop( edge ):

    cmds.select( edge )
    cmds.SelectEdgeLoopSp()
    curve = cmds.polyToCurve( form=0, degree=3 )[0]
    
    return curve





class CreateVolumeCurveOnMesh:
    
    def __init__(self, centerCurves, mesh ):
        
        import sgBFunction_dag
        
        self.centerCurves = centerCurves
        meshShape = sgBFunction_dag.getShape( mesh )
        dagPath = sgBFunction_dag.getMDagPath( meshShape )
        self.fnMesh = om.MFnMesh( dagPath )
        self.mtxMesh = dagPath.inclusiveMatrix()

    
    def createVolume_byOneCurve(self, targetCurve, level=6, ignoreVecor=None ):
        
        import sgBFunction_curve
        import sgBFunction_value
        import math
        
        if ignoreVecor:
            mtxList = sgBFunction_curve.getMatricesFromCurve( targetCurve, 2, ignoreVecor )
        else:
            mtxList = sgBFunction_curve.getMatricesFromCurve( targetCurve, 2 )
        
        eachRadValue = ( math.pi * 2.0 )/level
        
        curves = []
        
        for i in range( level ):
            points = []
            
            if ignoreVecor:
                if type( ignoreVecor ) == type( [] ):
                    ignoreVecor = om.MVector( *ignoreVecor )
                vAngle = sgBFunction_value.getVectorFromMatrixByAngle( mtxList[0], eachRadValue * i, 2 )
                if ignoreVecor * vAngle > 0: continue
            
            for mtx in mtxList:
                vAngle = sgBFunction_value.getVectorFromMatrixByAngle( mtx, eachRadValue * i, 2 )
                pPoint = om.MPoint( *mtx[12:-1] )
                
                intersectPoints = om.MPointArray()
                self.fnMesh.intersect( pPoint, vAngle, intersectPoints )
                
                if intersectPoints.length():
                    closeDist = 1000000.0
                    closeDistPoint = intersectPoints[0]
                    
                    for j in range( intersectPoints.length() ):
                        dist = intersectPoints[j].distanceTo( pPoint )
                        if dist < closeDist:
                            closeDist = dist
                            closeDistPoint = intersectPoints[j]
                    
                    vIntersectPoint = ( closeDistPoint - pPoint ) * 0.7 + om.MVector( pPoint )
                    points.append( [vIntersectPoint.x,vIntersectPoint.y,vIntersectPoint.z] )
                else:
                    points.append( [pPoint.x, pPoint.y, pPoint.z] )
                
            curves.append( cmds.curve( ep=points, d=3 ) )
        
        return curves
    
    
    def createVolume_byCurves(self, level= 6 ):
        
        if len( self.centerCurves ) == 1:
            curves = self.createVolume_byOneCurve( self.centerCurves[0], level )
        else:
            dataCurve = om.MFnNurbsCurveData()
            oCurve = dataCurve.create()
            
            epPoints = om.MPointArray()
            for i in range( len( self.centerCurves ) ):
                pos = cmds.xform( self.centerCurves[i] + '.cv[0]', q=1, ws=1, t=1 )
                epPoints.append( om.MPoint( *pos ) )
            
            fnCurve = om.MFnNurbsCurve()
            fnCurve.createWithEditPoints( epPoints, 3, 1, False, False, False, oCurve )
            fnCurve.setObject( oCurve )
            
            minParam = 0.0
            maxParam = fnCurve.findParamFromLength( fnCurve.length() )
            
            vTangentStart = fnCurve.tangent( minParam )
            vTangentEnd   = fnCurve.tangent( maxParam )
            
            curvesStart = self.createVolume_byOneCurve( self.centerCurves[ 0],  level, vTangentStart )
            curvesSide  = self.createVolume_byCurvesLine( level )
            curvesEnd   = self.createVolume_byOneCurve( self.centerCurves[-1],  level, -vTangentEnd )
            
            curves = []
            curves += curvesStart
            curves += curvesSide
            curves += curvesEnd
            
            
        
        return curves
    
    
    def createVolume_byCurvesLine(self, level=6 ):
        
        import sgBFunction_dag
        
        avSpans = 0
        eachMinParams = []
        eachMaxParams = []
        
        for i in range( len( self.centerCurves ) ):
            curve = self.centerCurves[i]
            curveShape = sgBFunction_dag.getShape( curve )
            fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
            
            avSpans += fnCurve.numSpans()
            eachMinParam = fnCurve.findParamFromLength( 0 )
            eachMaxParam = fnCurve.findParamFromLength( fnCurve.length() )
            
            eachMinParams.append( eachMinParam )
            eachMaxParams.append( eachMaxParam )
        
        avSpans = int( avSpans / len( self.centerCurves ) )
        
        eachParamRates = []
        for i in range( len( self.centerCurves ) ):
            paramRate = float( eachMaxParams[i] - eachMinParams[i] )
            paramRate /= (avSpans-1)
            eachParamRates.append( paramRate )
        
        curvePointsList = [ [] for j in range( (level/2)*2 ) ]
        
        for i in range( avSpans ):
            epPoints = om.MPointArray()
            epPoints.setLength( len( self.centerCurves ) )
            
            avTangent = om.MVector( 0,0,0 )
            for j in range( len( self.centerCurves ) ):
                curveShape = sgBFunction_dag.getShape( self.centerCurves[j] )
                fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
                point = om.MPoint()
                fnCurve.getPointAtParam( eachParamRates[j] * i + eachMinParams[j], point )
                epPoints.set( point, j )
                avTangent += fnCurve.tangent( eachParamRates[j] * i + eachMinParams[j] )
            
            dataCurve = om.MFnNurbsCurveData()
            oCurve = dataCurve.create()
            
            fnCurveCreate = om.MFnNurbsCurve()
            fnCurveCreate.createWithEditPoints( epPoints, 3, 1, False, False, False, oCurve )
            fnCurveCreate.setObject( oCurve )
            
            maxParam  = fnCurveCreate.findParamFromLength( fnCurveCreate.length() )
            eachParam = maxParam / ( level/2 + 2 )
            
            for j in range( level/2 ):
                param = eachParam * ( j+1 )
                
                point = om.MPoint()
                fnCurveCreate.getPointAtParam( param, point )
                vAim = fnCurveCreate.tangent( param )
                vUp  = avTangent
                vCross = vAim ^ vUp
                vInvCross = -vCross
                
                pointsIntersects = om.MPointArray()
                pointsIntersectsInv = om.MPointArray()
                self.fnMesh.intersect( point, vCross, pointsIntersects )
                self.fnMesh.intersect( point, vInvCross, pointsIntersectsInv )
                
                if pointsIntersects.length():
                    targetPoint    = ( pointsIntersects[0] - om.MVector( point ) ) * 0.7 + om.MVector( point )
                    curvePointsList[j].append( [ targetPoint.x, targetPoint.y, targetPoint.z ] )
                else:
                    curvePointsList[j].append( [ point.x, point.y, point.z ] )
                if pointsIntersectsInv.length():
                    targetPointInv = ( pointsIntersectsInv[0] - om.MVector( point ) ) * 0.7 + om.MVector( point )
                    curvePointsList[j+( level/2 )].append( [ targetPointInv.x, targetPointInv.y, targetPointInv.z ]  )
                else:
                    curvePointsList[j+( level/2 )].append( [ point.x, point.y, point.z ] )
        
        createCurves = []
        for curvePoints in curvePointsList:
            createCurves.append( cmds.curve( ep=curvePoints ) )
        
        return createCurves


def getTubeIntersectionPointAndNormal( tubeMesh, baseMesh ):
    
    import math
    import sgBFunction_dag
    
    hairMesh = tubeMesh
    headMesh  = baseMesh
    
    headMeshShape = sgBFunction_dag.getShape( headMesh )
    
    dagPathHead = sgBFunction_dag.getMDagPath( headMeshShape )
    intersector = om.MMeshIntersector()
    intersector.create( dagPathHead.node() )
        
    hairMeshShape = sgBFunction_dag.getShape( hairMesh )
    dagPathHairMesh = sgBFunction_dag.getMDagPath( hairMeshShape )

    fnMesh = om.MFnMesh( dagPathHairMesh )
    
    points = om.MPointArray()
    fnMesh.getPoints( points )
    
    pointOnMesh = om.MPointOnMesh()
    
    minDist = 100000.0
    minDistIndex = 0
    minDistNormal = om.MVector()
    for i in range( points.length() ):
        intersector.getClosestPoint( points[i], pointOnMesh )
        closePoint = om.MPoint( pointOnMesh.getPoint() )
        
        dist = closePoint.distanceTo( points[i] )
        if dist < minDist:
            normal = om.MVector()
            itNormal = om.MVector( pointOnMesh.getNormal() )
            fnMesh.getVertexNormal( i, True, normal )
            
            if math.fabs( itNormal.normal() * normal.normal() ) < 0.4:
                minDist = dist
                minDistIndex = i
                minDistNormal = itNormal

    pointMinDist = points[ minDistIndex ]
    normalMinDist = om.MVector()
    fnMesh.getVertexNormal( minDistIndex, True, normalMinDist )
    
    srcPoint = om.MPoint( pointMinDist + normalMinDist )
    ray      = -normalMinDist
    
    intersectPoints = om.MPointArray()
    fnMesh.intersect( srcPoint, ray, intersectPoints )
    
    if intersectPoints.length() == 1:
        return intersectPoints[0], minDistNormal
    else:
        bb = om.MBoundingBox()
        for k in range( intersectPoints.length() ):
            bb.expand( intersectPoints[k] )
        return bb.center(), minDistNormal




def getSgWobbleCurve( curve ):
    
    import sgBFunction_dag
    
    wobbles = sgBFunction_dag.getNodeFromHistory( curve, 'sgWobbleCurve2' )
    if not wobbles:
        follicles = sgBFunction_dag.getNodeFromHistory( curve, 'follicle' )
        wobbles   = sgBFunction_dag.getNodeFromHistory( follicles[0], 'sgWobbleCurve2' ) 
    return wobbles[0]