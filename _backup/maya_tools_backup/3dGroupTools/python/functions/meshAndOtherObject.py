import maya.cmds as cmds
import maya.OpenMaya as om


def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj


def findClosestFacePosition( position, mesh ):
    
    meshMatrix = cmds.getAttr( mesh+'.wm' )
    
    mMeshMatrix = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( meshMatrix, mMeshMatrix )
    
    intersector = om.MMeshIntersector(  )
    mPoint = om.MPoint( *position )
    mPoint*= mMeshMatrix.inverse()
    
    pointOnMesh = om.MPointOnMesh()
    intersector.create( getMObject( mesh ) )
    
    intersector.getClosestPoint( mPoint, pointOnMesh )
    
    fnMesh = om.MFnMesh( getMObject( mesh ) )
    
    verticesArr = om.MIntArray()
    fnMesh.getPolygonVertices( pointOnMesh.faceIndex(), verticesArr )
    
    boundingBox = om.MBoundingBox()
    for i in range( verticesArr.length() ):
        point = om.MPoint()
        fnMesh.getPoint( verticesArr[i], point )
        boundingBox.expand( point )
    
    center = boundingBox.center()
    center *= mMeshMatrix
    
    return center.x, center.y, center.z



def moveObjectToClosestFace( targetObject, mesh ):
    
    position = cmds.xform( targetObject, q=1, ws=1, t=1 )[:3]
    
    faceCenter = findClosestFacePosition( position, mesh )
    
    cmds.move( faceCenter[0], faceCenter[1], faceCenter[2], targetObject, ws=1 )