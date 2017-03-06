from toSimpleFunctions import *
import maya.cmds as cmds
import maya.OpenMaya as om


def getLastIndices( hairSystem ):
    selList = om.MSelectionList()
    selList.add( hairSystem )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    fnNode = om.MFnDependencyNode( mObj )
    plugInputHair = fnNode.findPlug( 'inputHair' )
    lastIndex = int(plugInputHair.numElements()-1)
    if lastIndex == -1: return 0
    return plugInputHair[ lastIndex ].logicalIndex()+1


def makeCenterCurve( crvs, rebuildSpanRate= 1.0 ):
    
    crvShapes = []
    for crv in crvs:
        crvShape = getShape( crv )
        if not crvShape: continue
        
        crvShapes.append( crvShape )
        
    lengthAll = 0.0
    crvInfo = cmds.createNode( 'curveInfo' )
    for crvShape in crvShapes:
        if not cmds.isConnected( crvShape+'.local', crvInfo+'.inputCurve' ):
            cmds.connectAttr( crvShape+'.local', crvInfo+'.inputCurve', f=1 )
        length = cmds.getAttr( crvInfo+'.arcLength' )
        lengthAll += length
    cmds.delete( crvInfo )
    
    lengthAverage = lengthAll / len( crvShapes )
    
    rebuildSpans = int( lengthAverage * rebuildSpanRate )
    
    for crvShape in crvShapes:
        cmds.rebuildCurve( crvShape, constructionHistory=0, 
                           replaceOriginal=1, 
                           rebuildType=0, 
                           endKnots=1, 
                           keepRange=0, 
                           keepControlPoints=0, 
                           keepEndPoints=1, 
                           keepTangents=0,
                           s=rebuildSpans, d=3, tol=0.01 )
    
    fnNurbsCurve = om.MFnNurbsCurve( getDagPath( crvShapes[0] ) )
    numCVs = fnNurbsCurve.numCVs()
    
    points = []
    for i in range( numCVs ):
        points.append( [0,0,0] )
    
    curve = cmds.curve( p=points, d=3 )
    
    for i in range( numCVs ):
        sumPoints = om.MVector(0,0,0)
        for crvShape in crvShapes:
            sumPoints += om.MVector( *cmds.xform( crvShape+'.controlPoints[%d]' % i, q=1, os=1, t=1 ) )
        averagePoints = sumPoints / len( crvShapes )
        cmds.move( averagePoints.x, averagePoints.y, averagePoints.z, curve+'.controlPoints[%d]' % i, os=1 )
        
    return curve


def makeCurveAsBindedCurve( crv, rebuildRate = 1 ):
    
    crvShape = getShape( crv )
    crvShapePath = getDagPath( crvShape )
    fnNurbsCurve = om.MFnNurbsCurve( crvShapePath )
    spans = fnNurbsCurve.numSpans()
    rebuildSpans = spans * rebuildRate
    
    cmds.rebuildCurve( crvShape, constructionHistory=0, 
                           replaceOriginal=1,
                           rebuildType=0, 
                           endKnots=1, 
                           keepRange=0, 
                           keepControlPoints=0, 
                           keepEndPoints=1, 
                           keepTangents=0,
                           s=rebuildSpans, d=3, tol=0.01 )
    
    exclusiveMtx = crvShapePath.exclusiveMatrix()
    
    localPoints = om.MPointArray()
    fnNurbsCurve.getCVs( localPoints )
    mtxList = []
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList.append( exclusiveMtx( i, j ) )
    
    grp = cmds.createNode( 'transform' )
    for i in range( localPoints.length() ):
        jnt = cmds.joint()
        cmds.move( localPoints[i].x, localPoints[i].y, localPoints[i].z, jnt, ws=1 )
        multMtx = cmds.createNode( 'multMatrix' )
        dcmp    = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( jnt+'.wm', multMtx+'.i[0]' )
        cmds.connectAttr( grp+'.wim', multMtx+'.i[1]' )
        cmds.connectAttr( multMtx+'.o', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.ot', crvShape+'.controlPoints[%d]' % i )
        cmds.select( jnt )
    
    cmds.xform( grp, ws=1, matrix=mtxList )



def makeBaseDynamicCurve( crvs, addName ):
    
    hairSystem = addName +'HairSystemShape'
    if not cmds.objExists( hairSystem ):
        hairSystem = cmds.createNode( 'hairSystem' )
        hairSystemTransform = cmds.listRelatives( hairSystem, p=1 )[0]
        hairSystemTransform = cmds.rename( hairSystemTransform, addName +'HairSystem' )
        hairSystem = cmds.listRelatives( hairSystemTransform, s=1 )[0]
        cmds.connectAttr( 'time1.outTime', hairSystem+'.currentTime' )
        
    follicels = []
    baseCurves = []
    ioCrvs = []
    currentCrvs = []
    for crv in crvs:
        lastIndex = getLastIndices( hairSystem )
        crvShapes = cmds.listRelatives( crv, s=1 )
    
        if not crvShapes: continue
        baseCrv = crvShapes[0]
    
        currentCrv = cmds.createNode( 'nurbsCurve' )
        ioCrv = cmds.createNode( 'nurbsCurve' )
        cmds.setAttr( ioCrv+'.io', 1 )
        follicle = cmds.createNode( 'follicle' )
        cmds.setAttr( follicle+'.degree', 3 )
        cmds.setAttr( follicle+'.startDirection', 1 )
        cmds.setAttr( follicle+'.restPose', 1 )
        
        rebuild = cmds.createNode( 'rebuildCurve' )
        cmds.connectAttr( baseCrv+'.local', rebuild+'.inputCurve' )
        cmds.connectAttr( rebuild+'.outputCurve', ioCrv+'.create' )
        cmds.connectAttr( ioCrv+'.local', follicle+'.startPosition' )
        cmds.connectAttr( baseCrv+'.wm', follicle+'.startPositionMatrix' )
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % lastIndex )
        cmds.connectAttr( hairSystem+'.outputHair[%d]' % lastIndex, follicle+'.currentPosition' )
        cmds.connectAttr( follicle+'.outCurve', currentCrv+'.create' )
        cmds.setAttr( rebuild+'.keepControlPoints', 1 )
        cmds.setAttr( rebuild+'.keepTangents', 0 )
        cmds.setAttr( rebuild+'.degree', 1 )
        
        follicels.append( cmds.listRelatives( follicle, p=1 )[0] )
        baseCurves.append( cmds.listRelatives( baseCrv, p=1 )[0] )
        ioCrvs.append( cmds.listRelatives( ioCrv, p=1 )[0] )
        currentCrvs.append( cmds.listRelatives( currentCrv, p=1 )[0] )
    
    if cmds.objExists( addName+'Follicles' ):
        cmds.parent( follicels, addName+'Follicles' )
    else:
        cmds.group( follicels, n= addName+'Follicles' )
    
    if cmds.objExists( addName+'BaseCurves' ):
        cmds.parent( baseCurves, addName+'BaseCurves' )
    else:
        cmds.group( baseCurves, n= addName+'BaseCurves' )
        
    if cmds.objExists( addName+'IoCrvs' ):
        cmds.parent( ioCrvs, addName+'IoCrvs' )
    else:
        cmds.group( ioCrvs, n= addName+'IoCrvs' )
    
    if cmds.objExists( addName+'CurrentCrvs' ):
        cmds.parent( currentCrvs, addName+'CurrentCrvs' )
    else:
        cmds.group( currentCrvs, n= addName+'CurrentCrvs' )



def copyFollicleAttr( fromCrv, toCrv ):
    
    fromShape = getShape( fromCrv )
    toShape = getShape( toCrv )
    
    fromFollicle = cmds.listConnections( fromShape, type='follicle' )[0]
    toFollicle   = cmds.listConnections( toShape, type='follicle' )[0]
    
    fnFromFollicle = om.MFnDependencyNode( getMObject( fromFollicle ) )
    fnToFollicle   = om.MFnDependencyNode( getMObject( toFollicle ) )
    
    stiffnessScaleValues = []
    plugStiffnessScale = fnFromFollicle.findPlug( 'stiffnessScale' )
    
    for i in range( plugStiffnessScale ):
        pass
    
    

def makeCurrentDynamicCurve( crvs, addName ):
    
    if not cmds.objExists( addName +'HairSystem' ):
        hairSystem = cmds.createNode( 'hairSystem' )
        hairSystemTransform = cmds.listRelatives( hairSystem, p=1 )[0]
        hairSystemTransform = cmds.rename( hairSystemTransform, addName +'HairSystem' )
        hairSystem = cmds.listRelatives( hairSystemTransform, s=1 )[0]
        cmds.connectAttr( 'time1.outTime', hairSystem+'.currentTime' )
    hairSystem = addName + 'HairSystemShape'
    
    follicels = []
    baseCurves = []
    ioCrvs = []
    for crv in crvs:
        lastIndex = getLastIndices( hairSystem )
        crvShapes = cmds.listRelatives( crv, s=1 )
    
        if not crvShapes: continue
        crvShape = crvShapes[0]
    
        baseCrv = cmds.createNode( 'nurbsCurve' )
        ioCrv = cmds.createNode( 'nurbsCurve' )
        cmds.setAttr( ioCrv+'.io', 1 )
        follicle = cmds.createNode( 'follicle' )
        cmds.setAttr( follicle+'.degree', 3 )
        cmds.setAttr( follicle+'.startDirection', 1 )
        cmds.setAttr( follicle+'.restPose', 1 )
        cmds.connectAttr( crvShape+'.local', baseCrv+'.create' )
        cmds.refresh()
        cmds.disconnectAttr( crvShape+'.local', baseCrv+'.create' )
        
        rebuild = cmds.createNode( 'rebuildCurve' )
        cmds.connectAttr( baseCrv+'.local', rebuild+'.inputCurve' )
        cmds.connectAttr( rebuild+'.outputCurve', ioCrv+'.create' )
        cmds.connectAttr( ioCrv+'.local', follicle+'.startPosition' )
        cmds.connectAttr( baseCrv+'.wm', follicle+'.startPositionMatrix' )
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % lastIndex )
        cmds.connectAttr( hairSystem+'.outputHair[%d]' % lastIndex, follicle+'.currentPosition' )
        cmds.connectAttr( follicle+'.outCurve', crvShape+'.create' )
        cmds.setAttr( rebuild+'.keepControlPoints', 1 )
        cmds.setAttr( rebuild+'.keepTangents', 0 )
        cmds.setAttr( rebuild+'.degree', 1 )
        
        follicels.append( cmds.listRelatives( follicle, p=1 )[0] )
        baseCurves.append( cmds.listRelatives( baseCrv, p=1 )[0] )
        ioCrvs.append( cmds.listRelatives( ioCrv, p=1 )[0] )
    
    if cmds.objExists( addName+'Follicles' ):
        cmds.parent( follicels, addName+'Follicles' )
    else:
        cmds.group( follicels, n= addName+'Follicles' )
    
    if cmds.objExists( addName+'BaseCurves' ):
        cmds.parent( baseCurves, addName+'BaseCurves' )
    else:
        cmds.group( baseCurves, n= addName+'BaseCurves' )
        
    if cmds.objExists( addName+'IoCrvs' ):
        cmds.parent( ioCrvs, addName+'IoCrvs' )
    else:
        cmds.group( ioCrvs, n= addName+'IoCrvs' )
    
    if cmds.objExists( addName+'Crvs' ):
        cmds.parent( ioCrvs, addName+'Crvs' )
    else:
        cmds.group( ioCrvs, n= addName+'Crvs' )
        


def getShapeSrcCon( crv ):
    
    try:
        return cmds.listConnections( crv, s=1, d=0, p=1, c=1 )[1]
    except:
        duObj = cmds.duplicate( crv )[0]
        duShape = cmds.listRelatives( duObj, s=1, f=1 )[0]
        duShape = cmds.parent( duShape, crv, add=1, shape=1 )
        cmds.delete( duObj )
        cmds.setAttr( duShape+'.io', 1 )
        return duShape+'.local'



def makeDynamicCurveKeepSrc( crvs, addName ):
    
    if not cmds.objExists( addName +'HairSystem' ):
        hairSystem = cmds.createNode( 'hairSystem' )
        hairSystemTransform = cmds.listRelatives( hairSystem, p=1 )[0]
        hairSystemTransform = cmds.rename( hairSystemTransform, addName +'HairSystem' )
        hairSystem = cmds.listRelatives( hairSystemTransform, s=1 )[0]
        cmds.connectAttr( 'time1.outTime', hairSystem+'.currentTime' )
    hairSystem = addName + 'HairSystemShape'
    
    follicels = []
    ioCrvs = []
    for crv in crvs:
        lastIndex = getLastIndices( hairSystem )
        crvShapes = cmds.listRelatives( crv, s=1 )
    
        if not crvShapes: continue
        crvShape = crvShapes[0]
    
        ioCrv = cmds.createNode( 'nurbsCurve' )
        cmds.setAttr( ioCrv+'.io', 1 )
        follicle = cmds.createNode( 'follicle' )
        trGrometry = cmds.createNode( 'transformGeometry' )
        cmds.setAttr( follicle+'.degree', 3 )
        cmds.setAttr( follicle+'.startDirection', 1 )
        cmds.setAttr( follicle+'.restPose', 1 )
        srcAttr = getShapeSrcCon( crvShape )
        
        rebuild = cmds.createNode( 'rebuildCurve' )
        cmds.connectAttr( srcAttr, rebuild+'.inputCurve' )
        cmds.connectAttr( rebuild+'.outputCurve', ioCrv+'.create' )
        cmds.connectAttr( ioCrv+'.local', follicle+'.startPosition' )
        cmds.connectAttr( crv+'.wm', follicle+'.startPositionMatrix' )
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % lastIndex )
        cmds.connectAttr( hairSystem+'.outputHair[%d]' % lastIndex, follicle+'.currentPosition' )
        cmds.connectAttr( crv+'.wim', trGrometry+'.transform' )
        cmds.connectAttr( follicle+'.outCurve', trGrometry+'.inputGeometry' )
        cmds.connectAttr( trGrometry+'.outputGeometry', crvShape+'.create', f=1 )
        cmds.setAttr( rebuild+'.keepControlPoints', 1 )
        cmds.setAttr( rebuild+'.keepTangents', 0 )
        cmds.setAttr( rebuild+'.degree', 1 )
        
        follicels.append( cmds.listRelatives( follicle, p=1 )[0] )
        ioCrvs.append( cmds.listRelatives( ioCrv, p=1 )[0] )
    
    if cmds.objExists( addName+'Follicles' ):
        cmds.parent( follicels, addName+'Follicles' )
    else:
        cmds.group( follicels, n= addName+'Follicles' )
        
    if cmds.objExists( addName+'IoCrvs' ):
        cmds.parent( ioCrvs, addName+'IoCrvs' )
    else:
        cmds.group( ioCrvs, n= addName+'IoCrvs' )
    
    if cmds.objExists( addName+'Crvs' ):
        cmds.parent( ioCrvs, addName+'Crvs' )
    else:
        cmds.group( ioCrvs, n= addName+'Crvs' )