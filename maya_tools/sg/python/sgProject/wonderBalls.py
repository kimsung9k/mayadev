from sgMaya import sgCmds
import pymel.core
from maya import OpenMaya
import copy


def buildJointFromEdgeLineVertices( edges ):
    pymel.core.select( edges )
    resultCurve = pymel.core.ls( pymel.core.polyToCurve( form=2, degree=1 )[0] )[0]
    resultCurveShape = resultCurve.getShape()
    maxValue = int( resultCurveShape.maxValue.get() ) + 1
    
    nulls = sgCmds.createPointOnCurve( resultCurve, maxValue )
    
    startObj = nulls[0]
    endObj = nulls[-1]
    
    poseStart = OpenMaya.MPoint( *pymel.core.xform( startObj, q=1, ws=1, t=1 ) )
    poseEnd   = OpenMaya.MPoint( *pymel.core.xform( endObj,   q=1, ws=1, t=1 ) )
    
    dist = poseStart.distanceTo( poseEnd )
    if dist == 0:
        pymel.core.delete( nulls.pop() )
    
    newJoints = []
    for null in nulls:
        newJoint = pymel.core.createNode( 'joint' )
        sgCmds.replaceObject( null, newJoint )
        newJoints.append( newJoint )
    pymel.core.select( newJoints )
    pymel.core.delete( nulls )




def getInt2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList([0,0],2)
    return util.asInt2Ptr()




def getListFromInt2Ptr( ptr ):
    util = OpenMaya.MScriptUtil()
    v1 = util.getInt2ArrayItem( ptr, 0, 0 )
    v2 = util.getInt2ArrayItem( ptr, 0, 1 )
    return [v1, v2]




def edgeStartAndEndWeightHammer( inputEdges ):
    
    inputEdgeIndices = [ pymel.core.ls( inputEdge )[0].index() for inputEdge in inputEdges ]
    orderedIndices = sgCmds.getOrderedEdgeLoopIndices( inputEdges[0] )
    
    orderedInputIndices = []
    for orderedIndex in orderedIndices:
        if not orderedIndex in inputEdgeIndices: continue
        orderedInputIndices.append( orderedIndex )
    
    mesh = pymel.core.ls( inputEdges[0] )[0].node()
    srcMeshs = sgCmds.getNodeFromHistory( mesh, 'mesh' )
    
    origMesh = copy.copy( mesh )
    for srcMesh in srcMeshs:
        if mesh.name() == srcMesh.name(): continue
        if mesh.numVertices() != srcMesh.numVertices(): continue
        origMesh = srcMesh
    
    orderedVtxIndices = []
    dagPath = sgCmds.getDagPath( origMesh )
    fnMesh = OpenMaya.MFnMesh( dagPath )
    
    for orderedIndex in orderedInputIndices:
        util = OpenMaya.MScriptUtil()
        util.createFromList([0,0],2)
        int2Ptr = util.asInt2Ptr()
        
        fnMesh.getEdgeVertices( orderedIndex, int2Ptr )
        appendTargets = []
        for vtxIndex in [util.getInt2ArrayItem( int2Ptr, 0, i ) for i in range(2) ]:
            appendTargets.append( vtxIndex )
        if len( orderedVtxIndices ) == 2:
            if orderedVtxIndices[0] in appendTargets:
                orderedVtxIndices.reverse()
        for appendTarget in appendTargets:
            if appendTarget in orderedVtxIndices: continue
            orderedVtxIndices.append( appendTarget )
    
    distList = []
    allDist = 0
    for i in range( len( orderedVtxIndices ) -1 ):
        firstPoint =  OpenMaya.MPoint( *pymel.core.xform( origMesh + '.vtx[%d]' % orderedVtxIndices[i], q=1, ws=1, t=1 )[:3] )
        secondPoint = OpenMaya.MPoint( *pymel.core.xform( origMesh + '.vtx[%d]' % orderedVtxIndices[i+1], q=1, ws=1, t=1 )[:3] )
        dist = firstPoint.distanceTo( secondPoint )
        distList.append( dist )
        allDist += dist
    
    startVtx = mesh + '.vtx[%d]' % orderedVtxIndices[0]
    endVtx   = mesh + '.vtx[%d]' % orderedVtxIndices[-1]
    
    startPlugs = sgCmds.getWeightPlugFromSkinedVertex(startVtx)
    endPlugs   = sgCmds.getWeightPlugFromSkinedVertex(endVtx)
    
    for i in range( 1, len( orderedVtxIndices )-1 ):
        currentDist = reduce( lambda x, y : x+y, distList[:i] )
        targetVtx = mesh + '.vtx[%d]' % orderedVtxIndices[i]
        targetPlugs = sgCmds.getWeightPlugFromSkinedVertex(targetVtx)
        weightValue = currentDist/allDist
        revValue    = 1.0 - weightValue
        
        targetPlugArray = targetPlugs[0].array()
        for targetPlug in targetPlugs:
            pymel.core.removeMultiInstance( targetPlug )
        
        for startPlug in startPlugs:
            startIndex = startPlug.index()
            targetPlugArray[startIndex].set( revValue )
        
        for endPlug in endPlugs:
            endIndex = endPlug.index()
            targetPlugArray[endIndex].set( weightValue )


