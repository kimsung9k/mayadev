from sgMaya import sgCmds
import pymel.core
from maya import OpenMaya, cmds
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



def edgeLoopVerticalStartAndEndHammer( inputEdges, percent=1.0 ):
    
    meshName = inputEdges[0].split( '.' )[0]
    inputEdgeIndices = [ pymel.core.ls( inputEdge )[0].index() for inputEdge in inputEdges ]
    
    dagPath = sgCmds.getDagPath( meshName )
    fnMesh = OpenMaya.MFnMesh( dagPath )
    
    existsVertices = [ False for i in range( fnMesh.numVertices() ) ]
    for i in inputEdgeIndices:
        util = OpenMaya.MScriptUtil()
        util.createFromList([0,0],2)
        ptrEdgeToVtxIndex = util.asInt2Ptr()
        fnMesh.getEdgeVertices( i, ptrEdgeToVtxIndex )
        index1 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 0 )
        index2 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 1 )
        existsVertices[ index1 ] = True
        existsVertices[ index2 ] = True
    
    for i in range( fnMesh.numVertices() ):
        if not existsVertices[i]: continue
        
        itVertex = OpenMaya.MItMeshVertex( dagPath )
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        prevIndex = util.asIntPtr()
        
        itVertex.setIndex( i, prevIndex )
        edgeIndices = OpenMaya.MIntArray()
        itVertex.getConnectedEdges( edgeIndices )
        
        targetEdges = []
        for j in range( edgeIndices.length() ):
            if edgeIndices[j] in inputEdgeIndices: continue
            targetEdges.append( meshName + '.e[%d]' % edgeIndices[j] )
        sgCmds.edgeStartAndEndWeightHammer( targetEdges, percent )
        cmds.select( targetEdges )
    




def fixEdgeLineJointOrientation( inputTargetJnt ):
    
    targetJnt = pymel.core.ls( inputTargetJnt )[0]
    dcmp = targetJnt.t.listConnections( s=1, d=0, type='decomposeMatrix' )[0]
    mm = dcmp.imat.listConnections( s=1, d=0, type='multMatrix' )[0]
    tr = mm.i[0].listConnections( s=1, d=0 )[0]
    averageNode = tr.listConnections( s=1, d=0, type='plusMinusAverage' )[0]
    
    pointers = averageNode.input3D.listConnections()
    xVector = pymel.core.createNode( 'plusMinusAverage' ); xVector.op.set( 2 )
    zVector = pymel.core.createNode( 'plusMinusAverage' ); zVector.op.set( 2 )
    yVector = pymel.core.createNode( 'vectorProduct' ); yVector.op.set( 2 )
    
    xVector.output3D >> yVector.input2
    zVector.output3D >> yVector.input1
    
    pointers[0].t >> xVector.input3D[0]
    pointers[2].t >> xVector.input3D[1]
    pointers[1].t >> zVector.input3D[0]
    pointers[3].t >> zVector.input3D[1]
    
    fbf = pymel.core.createNode( 'fourByFourMatrix' )
    xVector.output3Dx >> fbf.in00
    xVector.output3Dy >> fbf.in01
    xVector.output3Dz >> fbf.in02
    yVector.outputX >> fbf.in10
    yVector.outputY >> fbf.in11
    yVector.outputZ >> fbf.in12
    zVector.output3Dx >> fbf.in20
    zVector.output3Dy >> fbf.in21
    zVector.output3Dz >> fbf.in22
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    fbf.output >> dcmp.imat
    
    dcmp.outputRotate >> tr.rotate
    tangentCon = targetJnt.listConnections( s=1, d=0, type='tangentConstraint' )
    if tangentCon: pymel.core.delete( tangentCon )
    
    sgCmds.constrain_rotate( tr, targetJnt )




def copyWeightByOnlySpecifyJoints( srcJointsGrp, trgJointsGrp, srcMesh, trgMesh ):
    
    srcJntsGrp = pymel.core.ls( srcJointsGrp )[0]
    trgJntsGrp = pymel.core.ls( trgJointsGrp )[0]
    
    srcJntsChildren = srcJntsGrp.listRelatives( c=1, ad=1, type='joint' )
    trgJntsChildren = trgJntsGrp.listRelatives( c=1, ad=1, type='joint' )
    
    srcPoses = OpenMaya.MPointArray()
    trgPoses = OpenMaya.MPointArray()
    
    srcPoses.setLength( len( srcJntsChildren ) )
    trgPoses.setLength( len( trgJntsChildren ) )
    
    for i in range( srcPoses.length() ):
        srcJnt = srcJntsChildren[i]
        srcJntPos = OpenMaya.MPoint( *srcJnt.wm.get()[-1] )
        srcPoses.set( srcJntPos, i )
        
    for i in range( trgPoses.length() ):
        trgJnt = trgJntsChildren[i]
        trgJntPos = OpenMaya.MPoint( *trgJnt.wm.get()[-1] )
        trgPoses.set( trgJntPos, i )
    
    srcMeshSkin = sgCmds.getNodeFromHistory( srcMesh, 'skinCluster' )[0]
    trgMeshSkin = sgCmds.getNodeFromHistory( trgMesh, 'skinCluster' )[0]
    
    srcToTrgMap = {}
    srcInflueceIndices = []
    for srcJnt in srcJntsChildren:
        cons = srcJnt.wm.listConnections( type='skinCluster', p=1 )
        for con in cons:
            if con.node().name() != srcMeshSkin.name(): continue
            srcInflueceIndices.append( con.index() )
            break
    
    trgInflueceIndices = []
    for trgJnt in trgJntsChildren:
        cons = trgJnt.wm.listConnections( type='skinCluster', p=1 )
        for con in cons:
            if con.node().name() != trgMeshSkin.name(): continue
            trgInflueceIndices.append( con.index() )
            break
    
    for i in range( srcPoses.length() ):
        closeDist = 10000000.0
        closeIndex = 0
        for j in range( trgPoses.length() ):
            dist = srcPoses[i].distanceTo( trgPoses[j] )
            if dist < closeDist:
                closeDist = dist
                closeIndex = j
        srcToTrgMap.update( { srcInflueceIndices[i] : trgInflueceIndices[closeIndex] } )

    fnSrcSkin = OpenMaya.MFnDependencyNode( sgCmds.getMObject( srcMeshSkin ) )
    fnTrgSkin = OpenMaya.MFnDependencyNode( sgCmds.getMObject( trgMeshSkin ) )
    
    plugSrcWeightList = fnSrcSkin.findPlug( 'weightList' )
    plugTrgWeightList = fnTrgSkin.findPlug( 'weightList' )
    
    for i in range( plugSrcWeightList.numElements() ):
        plugSrcWeights = plugSrcWeightList[i].child(0)
        plugTrgWeights = plugTrgWeightList[i].child(0)
        
        trgLogicalIndices = []
        trgValues = []
        sumValue = 0
        for j in range( plugSrcWeights.numElements() ):
            logicalIndex = plugSrcWeights[j].logicalIndex()
            if not srcToTrgMap.has_key( logicalIndex ): continue
            trgInfluenceLogicalIndex = srcToTrgMap[logicalIndex]
            trgLogicalIndices.append( trgInfluenceLogicalIndex )
            trgValues.append( plugSrcWeights[j].asFloat() )
            sumValue += plugSrcWeights[j].asFloat()
        multValue = 1.0 - sumValue
        
        trgOtherLogicalIndices = []
        for j in range( plugTrgWeights.numElements() ):
            trgLogicalIndex = plugTrgWeights[j].logicalIndex()
            if trgLogicalIndex in trgLogicalIndices: continue
            trgOtherLogicalIndices.append( trgLogicalIndex )
        
        for j in range( len( trgLogicalIndices ) ):
            trgAttr = plugTrgWeights.elementByLogicalIndex( trgLogicalIndices[j] ).name()
            cmds.setAttr( trgAttr, trgValues[j] )
        
        for j in range( len( trgOtherLogicalIndices ) ):
            trgAttr = plugTrgWeights.elementByLogicalIndex( trgOtherLogicalIndices[j] ).name()
            cmds.setAttr( trgAttr, cmds.getAttr( trgAttr ) * multValue )
            



        
        


