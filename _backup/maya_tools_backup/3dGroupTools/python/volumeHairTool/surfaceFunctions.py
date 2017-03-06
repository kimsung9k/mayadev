import maya.cmds as cmds
import maya.OpenMaya as om
import functions as fnc


def getSurfaceUDistance( surface, multMatrix=False ):
    
    fnSurface = om.MFnNurbsSurface( fnc.getMObject( surface ) )
    if multMatrix:
        surfaceMatrix = fnc.getMMatrixFromMtxList( cmds.getAttr( surface+'.wm' ) )
    else:
        surfaceMatrix = om.MMatrix()
    
    degreeU = fnSurface.degreeU()
    numSpansU = fnSurface.numSpansInU()
    numU = fnSurface.numCVsInU()
    numV = fnSurface.numCVsInV()
    
    cvPoints = om.MPointArray()
    cvPoints.setLength( numU )
    knots    = om.MDoubleArray()
    knots.setLength( numU+degreeU-1 )
    
    for i in range( numU ):
        bbox = om.MBoundingBox()
        point = om.MPoint()
        for j in range( numV ):
            fnSurface.getCV( i, j, point )
            bbox.expand( point )
        minPoint = om.MVector( bbox.min() )
        maxPoint = om.MVector( bbox.max() )
        cPoint = om.MPoint(( minPoint + maxPoint )/2)*surfaceMatrix
        cvPoints.set( cPoint, i )
        
    for i in range( numU+degreeU-1 ):
        if i < degreeU-1:
            knots[i] = 0
        elif i-degreeU+1 > numSpansU:
            knots[i] = numSpansU
        else:
            knots[i] = i-degreeU+1
    
    curveData = om.MFnNurbsCurveData()
    createCurveObj = curveData.create()
    fnCreateCurve = om.MFnNurbsCurve()
    fnCreateCurve.create( cvPoints, knots, degreeU, om.MFnNurbsCurve.kOpen, 0,0, createCurveObj )
    
    fnCurve = om.MFnNurbsCurve( createCurveObj )
    return fnCurve.length()


def getSurfaceCenterCurve( surface, multMatrix=False ):
    
    fnSurface = om.MFnNurbsSurface( fnc.getMObject( surface ) )
    if multMatrix:
        surfaceMatrix = fnc.getMMatrixFromMtxList( cmds.getAttr( surface+'.wm' ) )
    else:
        surfaceMatrix = om.MMatrix()
    
    degreeU = fnSurface.degreeU()
    numU = fnSurface.numCVsInU()
    numV = fnSurface.numCVsInV()
    
    cvPoints = []
    
    for i in range( numU ):
        bbox = om.MBoundingBox()
        point = om.MPoint()
        for j in range( numV ):
            fnSurface.getCV( i, j, point )
            bbox.expand( point )
        minPoint = om.MVector( bbox.min() )
        maxPoint = om.MVector( bbox.max() )
        cPoint = om.MPoint(( minPoint + maxPoint )/2)*surfaceMatrix
        cvPoints.append( [cPoint.x,cPoint.y,cPoint.z] )
        
    return cmds.curve( p=cvPoints, d=degreeU )