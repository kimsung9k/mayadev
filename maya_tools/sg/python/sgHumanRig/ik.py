import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import format
import dag
from sgModules import sgbase


def connectDistanceToSplineJoints( ikHandle ):
    
    startJoint = cmds.listConnections( ikHandle + '.startJoint' )
    endEffector = cmds.listConnections( ikHandle + '.endEffector' )
    curve = cmds.listConnections( ikHandle + '.inCurve', shapes=1 )
    
    if not startJoint or not endEffector or not curve: return None
    
    startJoint = startJoint[0]
    endJoints   = cmds.listConnections( endEffector[0] + '.tx')
    curveShape = dag.getShape( curve[0] )
    sgCurve = format.Curve( curveShape )
    
    print endJoints[0], startJoint
    jointList = dag.getParents( endJoints[0], startJoint, [] )
    
    jointList.append( endJoints[0] )
    
    print "------------"
    for joint in jointList:
        print joint
    print "------------"

    pointOnCurves = []
    for joint in jointList:
        point = OpenMaya.MPoint( *cmds.xform( joint, q=1, ws=1, t=1 ) )
        closeParam = sgCurve.getClosestParamAtPoint( point )
        
        node = cmds.createNode( 'pointOnCurveInfo' )
        cmds.connectAttr( curveShape + '.worldSpace', node + '.inputCurve' )
        cmds.setAttr( node + '.parameter', closeParam )
        pointOnCurves.append( node )
    
    for i in range( 1, len( jointList ) ):
        
        startNode = pointOnCurves[i-1]
        endNode   = pointOnCurves[i]
        targetJoint = jointList[i]
        
        distNode = cmds.createNode( 'distanceBetween' )
        cmds.connectAttr( startNode + '.position', distNode + '.point1' )
        cmds.connectAttr( endNode + '.position', distNode + '.point2' )
        
        cmds.connectAttr( distNode + '.distance', targetJoint + '.tx' )
        cmds.setAttr( targetJoint + '.ty', 0 )
        cmds.setAttr( targetJoint + '.tz', 0 )
    


def createIkSplineHandleJoints( curve, root, numJoint=None ):
    
    curveShape = dag.getShape(curve)
    fnCurve = OpenMaya.MFnNurbsCurve( sgbase.getDagPath( curveShape ) )
    
    minParam = fnCurve.findParamFromLength(0)
    maxParam = fnCurve.findParamFromLength( fnCurve.length() )
    
    if not numJoint:
        numSpan = fnCurve.numSpans()
    else:
        numSpan = numJoint
    
    paramLength = maxParam - minParam
    eachParam = paramLength / float( numSpan )
    
    cmds.select( d=1 )
    joints = []
    points = []
    for i in range( numSpan+1 ):
        param = eachParam * i
        point = OpenMaya.MPoint()
        fnCurve.getPointAtParam( param, point, OpenMaya.MSpace.kWorld )
        points.append( point )
        joint = cmds.joint()
        joints.append( joint )
    
    
    for i in range( numSpan ):
        dist = points[i].distanceTo( points[i+1] )
        cmds.setAttr( joints[i+1] + '.tx', dist )
    
    ikHandle = cmds.ikHandle( sj=joints[0], ee=joints[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=curve )[0]
    
    pointOnCurveNodes= []
    for i in range( numSpan + 1 ):
        pointOnCurveNode = cmds.createNode( 'pointOnCurveInfo' )
        cmds.connectAttr( curveShape + '.local', pointOnCurveNode + '.inputCurve' )
        cmds.setAttr( pointOnCurveNode + '.parameter', i * eachParam )
        pointOnCurveNodes.append( pointOnCurveNode )
        
    for i in range( numSpan ):
        distNode = cmds.createNode( 'distanceBetween' )
        cmds.connectAttr( pointOnCurveNodes[i] + '.position', distNode + '.point1' )
        cmds.connectAttr( pointOnCurveNodes[i+1] + '.position', distNode + '.point2' )
        cmds.connectAttr( distNode + '.distance', joints[i+1] + '.tx' )
        
    ikHandle = cmds.parent( ikHandle, root )[0]
    topJoint = cmds.parent( joints[0], root )[0]
    
    return topJoint, ikHandle
        
        
    
    
    
    




