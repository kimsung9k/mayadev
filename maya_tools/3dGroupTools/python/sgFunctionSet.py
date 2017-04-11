
import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDag



def setPivotToLowerPoint( target ):
    
    dagPath = sgModelDag.getDagPath( sgModelDag.getShape( target ) ) 
    fnMesh = om.MFnMesh( dagPath )
    points = om.MPointArray()
    fnMesh.getPoints( points )
    
    lowerHeight = 1000000.0
    lowerIndex = 0
    for i in range( points.length() ):
        if lowerHeight > points[i].y:
            lowerHeight = points[i].y
            lowerIndex = i
    lowerPoint = points[ lowerIndex ]*dagPath.inclusiveMatrix()
    cmds.move( lowerPoint.x, lowerPoint.y, lowerPoint.z, target+'.rotatePivot', target+'.scalePivot' )




def moveObjectToClosestPoint( targets, base ):
    
    if not type( targets ) in [ type([]), type(()) ]:
        targets = [targets]
    
    dagPathBase = sgModelDag.getDagPath( sgModelDag.getShape( base ) )
    baseMatrix = dagPathBase.inclusiveMatrix()
    baseInvMatrix = dagPathBase.inclusiveMatrixInverse()
    
    intersector = om.MMeshIntersector()
    intersector.create( sgModelDag.getMObject( sgModelDag.getShape( base ) ) )
    
    pointOnMesh = om.MPointOnMesh()
    for target in targets:
        pivPoint = om.MPoint( *cmds.xform( target, q=1, ws=1, piv=1 )[:3] )*baseInvMatrix
        intersector.getClosestPoint( pivPoint, pointOnMesh )
        point = pointOnMesh.getPoint()
        
        pointDiff = (om.MVector( point ) - om.MVector( pivPoint ))*baseMatrix
        
        cmds.move( pointDiff.x, pointDiff.y, pointDiff.z, target, ws=1, r=1 )




def selectJoint( sels=None ):
    
    if not sels: sels = cmds.ls( type='joint' )
    
    jnts = []
    for sel in sels:
        if cmds.nodeType( sel ) == 'joint':
            jnts.append( sel )
    
    if not jnts: 
        cmds.select( d=1 )
        return None
    cmds.select( jnts )



def goToObject( first, second ):
    
    secondPos = cmds.getAttr( second+'.wm' )
    cmds.xform( first, ws=1, matrix=secondPos )