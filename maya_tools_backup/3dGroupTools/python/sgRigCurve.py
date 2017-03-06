import maya.cmds as cmds
import maya.OpenMaya as om

import sgFunctionDag
import sgModelDg
import sgModelDag
import sgModelCurve
import sgModelRule
import sgRigAttribute
import sgModelConvert
import sgRigDag


def addCurveInfo( crv ):
    
    shape = sgModelDag.getShape( crv )
    
    info = cmds.createNode( 'curveInfo' )
    cmds.connectAttr( shape+'.local', info+'.inputCurve' )
    return info



def createLocatorOnCurve( crv, percentParam=0.5 ):
    if cmds.nodeType( crv ) == 'transform':
        crv = cmds.listRelatives( crv, s=1 )[0]
    info = cmds.createNode( 'pointOnCurveInfo' )
    cmds.connectAttr( crv+'.worldSpace', info+'.inputCurve' )
    cmds.setAttr( info+'.top', 1 )
    handle = cmds.createNode( 'transform' )
    cmds.setAttr( handle+'.dh',1 )
    compose = cmds.createNode( 'composeMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( info+'.position', compose+'.it' )
    cmds.connectAttr( compose+'.outputMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( handle+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', handle+'.t' )
    cmds.addAttr( handle, ln='param', min=0, max=1, dv=percentParam )
    cmds.setAttr( handle+'.param', e=1, k=1 )
    cmds.connectAttr( handle+'.param', info+'.parameter' )
    return handle



def createCurveOnTargetPoints( targets, degrees=3 ):
    
    trObjs = []
    curvePoints = []
    for taregt in targets:
        if cmds.nodeType( taregt ) in ['joint', 'transform']:
            trObjs.append( taregt )
            curvePoints.append( [0,0,0] )

    if len( targets ) == 2:
        crv = cmds.curve( p=curvePoints, d=1 )
    elif len( targets ) ==3:
        crv = cmds.curve( p=curvePoints, d=2 )
    else:
        crv = cmds.curve( p=curvePoints, d=degrees )
    crvShape= cmds.listRelatives( crv, s=1 )[0]
    
    for trObj in trObjs:
        i = trObjs.index( trObj )
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( trObj+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( crvShape+'.pim', mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', crvShape+'.controlPoints[%d]' % i )
    
    return crv




def makeCenterCurveFromCurves( crvs, rebuildSpanRate= 1.0 ):
    
    crvShapes = []
    for crv in crvs:
        crvShape = sgModelDag.getShape( crv )
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
    
    fnNurbsCurve = om.MFnNurbsCurve( sgModelDag.getDagPath( crvShapes[0] ) )
    numCVs = fnNurbsCurve.numCVs()
    
    points = []
    for i in range( numCVs ):
        points.append( [0,0,0] )
    
    curve = cmds.curve( p=points, d=3 )
    
    for i in range( numCVs ):
        sumPoints = om.MVector(0,0,0)
        for crvShape in crvShapes:
            sumPoints += om.MVector( *cmds.xform( crvShape+'.controlPoints[%d]' % i, q=1, ws=1, t=1 ) )
        averagePoints = sumPoints / len( crvShapes )
        cmds.move( averagePoints.x, averagePoints.y, averagePoints.z, curve+'.controlPoints[%d]' % i, os=1 )
        
    return curve



def getAddNameHairSystem( addName ):
        
    sgHairSystemLabelAttrName = sgModelRule.sgHairSystemLabelAttrName
    
    attrs = cmds.ls( '*.' + sgHairSystemLabelAttrName )
    
    for attr in attrs:
        if cmds.getAttr( attr ) == addName:
            hairSystemTransform = attr.split( '.' )[0]
            hairSystemShape = cmds.listRelatives( hairSystemTransform, s=1, f=1 )[0]
            return hairSystemShape
    hairSystemShape = cmds.createNode( 'hairSystem' )
    hairSystemTransform = cmds.listRelatives( hairSystemShape, p=1, f=1 )[0]
    hairSystemTransform = cmds.rename( hairSystemTransform, addName +'HairSystem' )
    cmds.addAttr( hairSystemTransform, ln=sgHairSystemLabelAttrName, dt='string' )
    cmds.setAttr( hairSystemTransform+'.'+sgHairSystemLabelAttrName, addName, type='string' )
    hairSystemShape = cmds.listRelatives( hairSystemTransform, s=1 )[0]
    cmds.connectAttr( 'time1.outTime', hairSystemShape+'.currentTime' )
    return hairSystemShape




def makeDynamicCurveKeepSrc( crvs, addName ):

    import sgBFunction_dag
    crvs = sgBFunction_dag.getChildrenShapeExists( crvs )

    hairSystem = getAddNameHairSystem( addName )
    
    follicels = []
    ioCrvs = []
    for crv in crvs:
        lastIndex = sgModelDg.getLastIndex( hairSystem+'.inputHair' ) + 1
        crvShapes = cmds.listRelatives( crv, s=1 )
    
        if not crvShapes: continue
        crvShape = crvShapes[0]
    
        ioCrv = cmds.createNode( 'nurbsCurve' )
        cmds.setAttr( ioCrv+'.io', 1 )
        follicle = cmds.createNode( 'follicle' )
        cmds.setAttr( follicle+'.degree', 3 )
        cmds.setAttr( follicle+'.startDirection', 1 )
        cmds.setAttr( follicle+'.restPose', 1 )
        srcAttr = sgModelDag.getSourceCurveAttr( crvShape )
        
        rebuild = cmds.createNode( 'rebuildCurve' )
        cmds.connectAttr( srcAttr, rebuild+'.inputCurve' )
        cmds.connectAttr( rebuild+'.outputCurve', ioCrv+'.create' )
        cmds.connectAttr( ioCrv+'.worldSpace', follicle+'.startPosition' )
        cmds.connectAttr( crv+'.wm', follicle+'.startPositionMatrix' )
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % lastIndex )
        cmds.connectAttr( hairSystem+'.outputHair[%d]' % lastIndex, follicle+'.currentPosition' )
        cmds.connectAttr( follicle+'.outCurve', crvShape+'.create', f=1 )
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
    
    return hairSystem





def makeDynamicCurve( crvs, addName ):

    import sgBFunction_dag
    crvs = sgBFunction_dag.getChildrenShapeExists( crvs )

    hairSystem = getAddNameHairSystem( addName )
    
    follicels = []
    ioCrvs = []
    newCrvs = []
    for crv in crvs:
        lastIndex = sgModelDg.getLastIndex( hairSystem+'.inputHair' ) + 1
        crvShapes = cmds.listRelatives( crv, s=1 )
    
        if not crvShapes: continue
        crvShape = crvShapes[0]
    
        ioCrv = cmds.createNode( 'nurbsCurve' )
        newCrv = cmds.createNode( 'nurbsCurve' )
        cmds.setAttr( ioCrv+'.io', 1 )
        follicle = cmds.createNode( 'follicle' )
        cmds.setAttr( follicle+'.degree', 3 )
        cmds.setAttr( follicle+'.startDirection', 1 )
        cmds.setAttr( follicle+'.restPose', 1 )
        
        rebuild = cmds.createNode( 'rebuildCurve' )
        cmds.connectAttr( crvShape+'.local', rebuild+'.inputCurve' )
        cmds.connectAttr( rebuild+'.outputCurve', ioCrv+'.create' )
        cmds.connectAttr( ioCrv+'.worldSpace', follicle+'.startPosition' )
        cmds.connectAttr( crv+'.wm', follicle+'.startPositionMatrix' )
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % lastIndex )
        cmds.connectAttr( hairSystem+'.outputHair[%d]' % lastIndex, follicle+'.currentPosition' )
        cmds.connectAttr( follicle+'.outCurve', newCrv+'.create', f=1 )
        cmds.setAttr( rebuild+'.keepControlPoints', 1 )
        cmds.setAttr( rebuild+'.keepTangents', 0 )
        cmds.setAttr( rebuild+'.degree', 1 )
        
        follicels.append( cmds.listRelatives( follicle, p=1 )[0] )
        ioCrvs.append( cmds.listRelatives( ioCrv, p=1 )[0] )
        newCrvObj = cmds.listRelatives( newCrv, p=1 )[0]
        newCrvObj = cmds.rename( newCrvObj, crv.split( '|' )[-1]+addName )
        newCrvs.append( newCrvObj )
    
    if cmds.objExists( addName+'Follicles' ):
        cmds.parent( follicels, addName+'Follicles' )
    else:
        cmds.group( follicels, n= addName+'Follicles' )
        
    if cmds.objExists( addName+'IoCrvs' ):
        cmds.parent( ioCrvs, addName+'IoCrvs' )
    else:
        cmds.group( ioCrvs, n= addName+'IoCrvs' )
    
    if cmds.objExists( addName+'OutCrvs' ):
        cmds.parent( newCrvs, addName+'OutCrvs' )
    else:
        cmds.group( newCrvs, n=addName + 'OutCrvs' )
    
    return hairSystem
    
        



def editCurveMatrixToStartPoint( crv ):
    
    cvs = cmds.ls( crv+'.cv[*]', fl=1 )
    points = []
    for cv in cvs:
        point = cmds.xform( cv, q=1, ws=1, t=1 )
        points.append( point )
    
    mtx = sgModelCurve.getStartCurveMatrix( crv )
    cmds.xform( crv, ws=1, matrix=mtx )
    
    for i in range( len( cvs ) ):
        cmds.move( points[i][0], points[i][1], points[i][2], cvs[i], ws=1  )
        



def editCurveMatrixSpecifyObjMatrix( trObj, crv ):
    
    cvs = cmds.ls( crv+'.cv[*]', fl=1 )
    points = []
    for cv in cvs:
        point = cmds.xform( cv, q=1, ws=1, t=1 )
        points.append( point )

    mtx = cmds.xform( trObj, q=1, ws=1, matrix=1 )
    cmds.xform( crv, ws=1, matrix=mtx )
    
    for i in range( len( cvs ) ):
        cmds.move( points[i][0], points[i][1], points[i][2], cvs[i], ws=1  )



def clearCurve( crv ):
    
    crvShape = sgModelDag.getShape( crv )
    crv = cmds.listRelatives( crvShape, p=1 )[0]
    
    nCrv = sgFunctionDag.copyShape( crv )
    nCrvShape = sgModelDag.getShape( nCrv )
    cmds.refresh()
    
    cmds.delete( crvShape )
    cmds.parent( nCrvShape, crv, add=1, shape=1 )
    cmds.delete( nCrv )
    
    
    


def createSgWobbleCurve( crv, editMatrix=1, createNewCurve=True, addName = '_' ):
    
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgWobble' )
    crvShape = sgModelDag.getShape( crv )
    
    if createNewCurve:
        srcAttr = crvShape+'.local'
        targetCrvShape = cmds.createNode( 'nurbsCurve' )
        targetCrv = cmds.listRelatives( targetCrvShape, p=1, f=1 )[0]
        targetAttr = targetCrvShape+'.create'
        cmds.xform( targetCrv, ws=1, matrix= cmds.getAttr( crv+'.wm' ) )
    else:
        targetCrv = crv
        srcAttr = sgModelDag.getSourceCurveAttr( crvShape )
        targetAttr = crvShape+'.create'
    
    sgWobbleCurve = cmds.createNode( 'sgWobbleCurve2', n='sgWobbleCurve' )
    mmNode = cmds.createNode( 'multMatrix' )
    
    cmds.connectAttr( srcAttr, sgWobbleCurve+'.inputCurve' )
    cmds.connectAttr( sgWobbleCurve+'.outputCurve', targetAttr, f=1 )
    
    cmds.setAttr( sgWobbleCurve+'.fallOff1[1].fallOff1_Position', 1 )
    cmds.setAttr( sgWobbleCurve+'.fallOff1[1].fallOff1_FloatValue', 1 )
    cmds.setAttr( sgWobbleCurve+'.fallOff2[1].fallOff2_Position', 1 )
    cmds.setAttr( sgWobbleCurve+'.fallOff2[1].fallOff2_FloatValue', 1 )
    
    aimMatrix = cmds.createNode( 'transform', n='aimMatrix' )
    cmds.connectAttr( aimMatrix+'.wm', mmNode+'.i[0]' )
    cmds.connectAttr( crv+'.wim', mmNode+'.i[1]' )
    cmds.connectAttr( mmNode+'.matrixSum', sgWobbleCurve+'.aimMatrix' )
    cmds.connectAttr( 'time1.outTime', sgWobbleCurve+'.time')
    cmds.setAttr( aimMatrix+'.dh',1 )
    cmds.setAttr( aimMatrix+'.dla', 1 )
    mtx = sgModelCurve.getStartCurveMatrix( targetCrv )
    cmds.xform( aimMatrix, ws=1, matrix=mtx )
    
    sgRigAttribute.createSgWobbleAttribute( targetCrv )
    
    try:targetCrv = cmds.rename( targetCrv, crv.split( '|' )[-1]+addName)
    except: pass
    
    return targetCrv, aimMatrix




def createRoofPointers( crv, numPointer, roofLength=None ):
    
    if not roofLength: roofLength = numPointer
    
    crv     = sgModelDag.getTransform( crv )
    crvShape= sgModelDag.getShape( crv )
    
    sgRigAttribute.addAttr( crv, ln='roofValue', k=1 )
    
    minValue = cmds.getAttr( crvShape+'.minValue' )
    maxValue = cmds.getAttr( crvShape+'.maxValue' )
    
    eachInputOffset = float( roofLength ) / numPointer
    
    pointers = []
    for i in range( numPointer ):
        curveInfo = cmds.createNode( 'pointOnCurveInfo' )
        pointer = cmds.createNode( 'transform', n= crv+'_pointer_%d' % i )
        sgRigAttribute.addAttr( pointer, ln='roofPointerNum', dv=i )
        sgRigAttribute.addAttr( pointer, ln='parameter', dv=i*eachInputOffset, k=1 )
        cmds.setAttr( pointer+'.dh', 1 )
        cmds.connectAttr( crvShape+'.local', curveInfo+'.inputCurve' )
        
        addNode = cmds.createNode( 'plusMinusAverage' )
        
        animCurve = sgModelDg.getRoofLinearCurve( 0, float( roofLength ), minValue, maxValue )
        
        cmds.connectAttr( crv+'.roofValue', addNode+'.input1D[0]' )
        cmds.connectAttr( pointer+'.parameter', addNode+'.input1D[1]' )
        cmds.connectAttr( addNode+'.output1D', animCurve+'.input' )
        cmds.connectAttr( animCurve+'.output', curveInfo+'.parameter' )
        cmds.connectAttr( curveInfo+'.position', pointer+'.t' )
        pointer = cmds.parent( pointer, crv )[0]
        
        pointers.append( pointer )
    return pointers



def setRotateRoofPointer( pointer, upObject, worldUpIndex, upIndex = 1 ):
    
    ''' aim index is 0 '''
    
    curveInfos = sgModelDag.getNodeFromHistory( pointer, 'pointOnCurveInfo' )
    curveInfo = curveInfos[0]

    cons = cmds.listConnections( curveInfo+'.inputCurve', s=1, d=0, c=1, p=1 )
    
    inputAttr = cons[1]
    inputCurve = inputAttr.split( '.' )[0]

    inputCurveIsLocal = False
    if inputAttr.split( '.' )[1] == 'local':
        inputCurveIsLocal = True
    
    '''------------------- create nodes ---------------------------'''
    
    mtxToThree = cmds.createNode( 'matrixToThreeByThree' )
    vp = cmds.createNode( 'vectorProduct' )
    fbfm = cmds.createNode( 'fourByFourMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    '''-----------------------------------------------------------'''
    
    '''-------------------matrix connect --------------------------'''
    
    crossIndex = 3-upIndex
    cmds.setAttr( vp+'.operation', 2 ) # cross product
    
    cmds.connectAttr( curveInfo + '.tangentX', fbfm+'.i00' )
    cmds.connectAttr( curveInfo + '.tangentY', fbfm+'.i01' )
    cmds.connectAttr( curveInfo + '.tangentZ', fbfm+'.i02' )
    
    if inputCurveIsLocal:
        mm = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( upObject+'.wm', mm+'.i[0]' )
        cmds.connectAttr( inputCurve+'.pim', mm+'.i[1]' )
        cmds.connectAttr( mm+'.o', mtxToThree+'.inMatrix' )
    else:
        cmds.connectAttr( upObject+'.wm', mtxToThree+'.inMatrix' )
    
    cmds.connectAttr( mtxToThree+'.o%d0' % worldUpIndex, fbfm+'.i%d0' % upIndex )
    cmds.connectAttr( mtxToThree+'.o%d1' % worldUpIndex, fbfm+'.i%d1' % upIndex )
    cmds.connectAttr( mtxToThree+'.o%d2' % worldUpIndex, fbfm+'.i%d2' % upIndex )
    
    cmds.connectAttr( mtxToThree+'.o%d0' % worldUpIndex, vp+'.input%dX' % crossIndex )
    cmds.connectAttr( mtxToThree+'.o%d1' % worldUpIndex, vp+'.input%dY' % crossIndex )
    cmds.connectAttr( mtxToThree+'.o%d2' % worldUpIndex, vp+'.input%dZ' % crossIndex )
    
    cmds.connectAttr( curveInfo+'.tangent', vp+'.input%d' % upIndex )
    
    cmds.connectAttr( vp+'.outputX', fbfm+'.i%d0' % crossIndex )
    cmds.connectAttr( vp+'.outputY', fbfm+'.i%d1' % crossIndex )
    cmds.connectAttr( vp+'.outputZ', fbfm+'.i%d2' % crossIndex )
    
    cmds.connectAttr( fbfm+'.output', mmdc+'.i[0]' )
    
    if inputCurveIsLocal:
        cmds.connectAttr( inputCurve+'.wm', mmdc+'.i[1]' )
        cmds.connectAttr( pointer+'.pim', mmdc+'.i[2]' )
    else:
        cmds.connectAttr( pointer+'.pim', mmdc+'.i[1]' )
    
    '''-----------------------------------------------------------'''
    
    '''---------- result ---------------- '''
    cmds.connectAttr( mmdc+'.or', pointer+'.r' )
    '''---------------------------------- '''
    
        




class CreateJointOnCurveSet:
    
    def __init__( self ):
        
        self._curveShape = ''
        self._minParam   = 0.0
        self._maxParam   = 1.0
        self._infoNum    = 5
        self._numSpans   = 5
        
        
    def setJointNum( self, num ):
        
        self._infoNum = num
        
        
    def setCurve( self, curveShape ):
        
        self._curveShape = curveShape
        self._minParam = cmds.getAttr( self._curveShape+'.minValue' )
        self._maxParam = cmds.getAttr( self._curveShape+'.maxValue' )
        self._numSpans = cmds.getAttr( self._curveShape+'.spans' )
    
    
    def create(self, distanceNode, powRate = 1 ):
        
        eachParam = ( self._maxParam - self._minParam )/( self._infoNum - 1 )
        
        eachInfos = []
        
        for i in range( self._infoNum ):
            
            info = cmds.createNode( 'pointOnCurveInfo', n= self._curveShape+'_info%d' % i )
            cmds.connectAttr( self._curveShape+'.local', info+'.inputCurve' )
            cmds.setAttr( info+'.parameter', eachParam*i + self._minParam )
            eachInfos.append( info )
        
        cmds.setAttr( info+'.parameter', self._maxParam - 0.0001 )
        
        cmds.select( d=1 )
        
        joints = []
        for i in range( self._infoNum ):
            joints.append( cmds.joint(p=[i,0,0]) )
            
        handle, effector = cmds.ikHandle( sj=joints[0], ee=joints[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self._curveShape )
        
        distNodes = []
        for i in range( self._infoNum -1 ):
            
            firstInfo = eachInfos[i]
            secondInfo = eachInfos[i+1]
            targetJoint = joints[i+1]
            
            distNode = cmds.createNode( 'distanceBetween' )
            distNodes.append( distNode )
            
            cmds.connectAttr( firstInfo+'.position', distNode+'.point1' )
            cmds.connectAttr( secondInfo+'.position', distNode+'.point2')
            
            if distanceNode:
                cmds.connectAttr( distNode+'.distance', targetJoint+'.tx' )
            else:
                cmds.setAttr( targetJoint+'.tx', cmds.getAttr( distNode+'.distance' ) )
        
        if not distanceNode:
            cmds.delete( distNodes )
        
        return handle, joints
            
            



def createJointOnEachCurve( targetCrv, numJoint, distanceNode = True ):
    
    curveSetInst = CreateJointOnCurveSet()
    curveSetInst.setJointNum( numJoint )
    
    selCurve = cmds.listRelatives( targetCrv, s=1 )
    
    if not selCurve: return None
    
    selCurve = selCurve[0]
    curveSetInst.setCurve( selCurve )
    joints = curveSetInst.create( distanceNode )
    
    return joints

        
            

def createJointOnCurve( numJoint, distanceNode = True, powRate = 1 ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    curveSetInst.setJointNum( numJoint )
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        curveSetInst.setCurve( selCurve )
        joints = curveSetInst.create( distanceNode )
        
        returnTargets.append( joints )
    
    return returnTargets
        
        


def createJointOnCurveByNumSpans( distanceNode = True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        curveSetInst.setCurve( selCurve )
        curveSetInst.setJointNum( curveSetInst._numSpans+1 )
        joints = curveSetInst.create( distanceNode )
        
        returnTargets.append( joints )
    
    return returnTargets



def createJointOnCurveByLength( multRate, distNode=True, powRate = 1 ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    
    curveInfo = cmds.createNode( 'curveInfo' )
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        cmds.connectAttr( selCurve+'.local', curveInfo+'.inputCurve', f=1 )
        length = cmds.getAttr( curveInfo+'.arcLength' )
        curveSetInst.setJointNum( int( length * multRate ) )
        curveSetInst.setCurve( selCurve )
        joints = curveSetInst.create( distNode )
        
        returnTargets.append( joints )

    return returnTargets



def createBendToCurve( curve ):
    
    import math
    
    curve = sgModelDag.getTransform( curve )
    
    cvs = cmds.ls( curve+'.cv[*]', fl=1 )

    startPoint= cmds.xform( cvs[0], q=1, ws=1, t=1 )
    endPoint  = cmds.xform( cvs[-1], q=1, ws=1, t=1 )
    
    bend, handle = cmds.nonLinear( curve, type='bend',  lowBound=0, highBound=1, curvature=0)
    
    cmds.xform( handle, ws=1, t=startPoint )
    
    vStartPoint = sgModelConvert.convertMVectorFromPointList( startPoint )
    vEndPoint   = sgModelConvert.convertMVectorFromPointList( endPoint )
    
    vAim = vEndPoint - vStartPoint
    yVector = om.MVector( *[0,1,0] )
    zVector = om.MVector( *[1,0,0] )
    
    dotY = math.fabs(vAim * yVector)
    dotZ = math.fabs(vAim * zVector)
    
    vUp = None
    if dotY > dotZ:
        vUp = zVector
    else:
        vUp = yVector
    
    vCross = vAim ^ vUp
    vUp = vCross ^ vAim
    
    lengthAim = vAim.length()
    
    vUp.normalize()
    vCross.normalize()
    
    vUp *= lengthAim
    vCross *= lengthAim
    
    mtx = [ vCross.x,      vCross.y,      vCross.z,      0,
            vAim.x,        vAim.y,        vAim.z,        0,
            vUp.x,         vUp.y,         vUp.z,         0,
            vStartPoint.x, vStartPoint.y, vStartPoint.z, 1 ]
    
    cmds.xform( handle, ws=1, matrix=mtx )

    handle, handleGrp = sgRigDag.addParent( handle )
    
    sgRigAttribute.addAttr( curve, ln='globalTwist', k=1 )
    sgRigAttribute.addAttr( curve, ln='globalBend',  k=1 )
    sgRigAttribute.addAttr( curve, ln='twist', k=1, dv=0 )
    sgRigAttribute.addAttr( curve, ln='bend', k=1, dv=1 )
    
    addTwist = cmds.createNode( 'addDoubleLinear' )
    multBend = cmds.createNode( 'multDoubleLinear' )
    
    cmds.connectAttr( curve+'.globalTwist', addTwist+'.input1' )
    cmds.connectAttr( curve+'.twist', addTwist+'.input2' )
    cmds.connectAttr( curve+'.globalBend', multBend+'.input1' )
    cmds.connectAttr( curve+'.bend', multBend+'.input2' )
    
    cmds.connectAttr( multBend+'.output', bend+'.curvature' )
    cmds.connectAttr( addTwist+'.output', handle+'.ry' )



def createEpCurveNode( *objs ):
    
    curveShape = cmds.createNode( 'nurbsCurve' )
    curve      = cmds.listRelatives( curveShape, p=1 )[0]
    epCurveNode = cmds.createNode( 'sgEpCurveNode' )
    cmds.connectAttr( epCurveNode+'.outputCurve', curveShape+'.create' )
    
    for i in range( len( objs ) ):
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( objs[i]+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( curve+'.wim',  mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', epCurveNode+'.inputPoint[%d]' % i )
    
    return curve, epCurveNode




def addSurfaceLineObject( targetCurve, multValue = 1, range = 1 ):
    
    crvShape = sgModelDag.getShape( targetCurve )
    rebuildCurveNode = cmds.createNode( 'rebuildCurve' )
    detachCurveNode  = cmds.createNode( 'detachCurve' )
    circleNode       = cmds.createNode( 'makeNurbCircle' )
    extrudeNode      = cmds.createNode( 'extrude' )
    surfaceNode      = cmds.createNode( 'nurbsSurface' )
    curveInfo        = cmds.createNode( 'curveInfo' )
    
    cmds.connectAttr( crvShape+'.worldSpace', curveInfo+'.inputCurve' )
    multValue = cmds.getAttr( curveInfo+'.arcLength' ) * multValue
    
    cmds.setAttr( rebuildCurveNode+'.spans', multValue )
    cmds.setAttr( rebuildCurveNode+'.keepRange', 0 )
    
    cmds.setAttr( detachCurveNode+'.parameter[0]', 0.25 )
    cmds.setAttr( detachCurveNode+'.parameter[1]', 0.75 )
    
    cmds.setAttr( extrudeNode+'.fixedPath', 1 )
    cmds.setAttr( extrudeNode+'.useProfileNormal', 1 )
    cmds.setAttr( extrudeNode+'.useComponentPivot', 1 )
    
    cmds.connectAttr( crvShape+'.local', rebuildCurveNode+'.inputCurve' )
    
    cmds.connectAttr( rebuildCurveNode+'.outputCurve', detachCurveNode+'.inputCurve' )
    
    cmds.connectAttr( circleNode+'.outputCurve', extrudeNode+'.profile' )
    cmds.connectAttr( detachCurveNode+'.outputCurve[1]', extrudeNode+'.path' )
    cmds.connectAttr( extrudeNode+'.outputSurface', surfaceNode+'.create' )
    
    surfNodeParent = cmds.listRelatives( surfaceNode, p=1 )[0]
    
    sgRigAttribute.addAttr( surfNodeParent, ln='radius', min=0, dv=1, k=1 )
    sgRigAttribute.addAttr( surfNodeParent, ln='parameter', min= 0, max=range, k=1 )
    sgRigAttribute.addAttr( surfNodeParent, ln='length', min=0, max=range, dv=range*0.5, k=1 )
    
    cmds.connectAttr( surfNodeParent+'.radius',     circleNode+'.radius' )

    rangeNode = cmds.createNode( 'setRange' )
    minusMultNode = cmds.createNode( 'multDoubleLinear' )
    plusMultNode = cmds.createNode( 'multDoubleLinear' )
    minusAddNode = cmds.createNode( 'addDoubleLinear' )
    plusAddNode = cmds.createNode( 'addDoubleLinear' )
    
    cmds.connectAttr( surfNodeParent+'.parameter', rangeNode+'.valueX' )
    cmds.connectAttr( surfNodeParent+'.length', minusMultNode+'.input1' )
    cmds.connectAttr( surfNodeParent+'.length', plusMultNode+'.input1' )
    cmds.setAttr( minusMultNode+'.input2', -0.5 )
    cmds.setAttr( plusMultNode+'.input2',   0.5 )
    cmds.connectAttr( minusMultNode+'.output', minusAddNode+'.input1' )
    cmds.connectAttr( plusMultNode+'.output', plusAddNode+'.input1' )
    cmds.setAttr( minusAddNode+'.input2', 0 )
    cmds.setAttr( plusAddNode +'.input2', range )
    
    cmds.connectAttr( minusAddNode+'.output', rangeNode+'.minX' )
    cmds.connectAttr( plusAddNode+'.output',  rangeNode+'.maxX' )
    cmds.setAttr( rangeNode+'.oldMinX', 0 )
    cmds.setAttr( rangeNode+'.oldMaxX', range )
    
    addMinNode = cmds.createNode( 'addDoubleLinear' )
    addMaxNode = cmds.createNode( 'addDoubleLinear' )
    cmds.connectAttr( rangeNode+'.outValueX', addMinNode+'.input1' )
    cmds.connectAttr( rangeNode+'.outValueX', addMaxNode+'.input1' )
    cmds.connectAttr( minusMultNode+'.output', addMinNode+'.input2' )
    cmds.connectAttr( plusMultNode+'.output', addMaxNode+'.input2' )
    
    minConditionFirst  = cmds.createNode( 'condition' )
    minConditionSecond = cmds.createNode( 'condition' )
    maxConditionFirst  = cmds.createNode( 'condition' )
    maxConditionSecond = cmds.createNode( 'condition' )
    
    cmds.connectAttr( addMinNode+'.output', minConditionFirst+'.firstTerm' )
    cmds.connectAttr( addMinNode+'.output', minConditionFirst+'.colorIfFalseR' )
    cmds.setAttr( minConditionFirst+'.secondTerm', range-0.0001 )
    cmds.setAttr( minConditionFirst+'.colorIfTrueR', range-0.0001 )
    cmds.setAttr( minConditionFirst+'.op', 2 )
    
    cmds.connectAttr( minConditionFirst+'.outColorR', minConditionSecond+'.firstTerm' )
    cmds.connectAttr( minConditionFirst+'.outColorR', minConditionSecond+'.colorIfFalseR' )
    cmds.setAttr( minConditionSecond+'.secondTerm', 0 )
    cmds.setAttr( minConditionSecond+'.colorIfTrueR', 0 )
    cmds.setAttr( minConditionSecond+'.op', 4 )
    
    cmds.connectAttr( addMaxNode+'.output', maxConditionFirst+'.firstTerm' )
    cmds.connectAttr( addMaxNode+'.output', maxConditionFirst+'.colorIfFalseR' )
    cmds.setAttr( maxConditionFirst+'.secondTerm', range )
    cmds.setAttr( maxConditionFirst+'.colorIfTrueR', range )
    cmds.setAttr( maxConditionFirst+'.op', 2 )
    
    cmds.connectAttr( maxConditionFirst+'.outColorR', maxConditionSecond+'.firstTerm' )
    cmds.connectAttr( maxConditionFirst+'.outColorR', maxConditionSecond+'.colorIfFalseR' )
    cmds.setAttr( maxConditionSecond+'.secondTerm', 0.0001 )
    cmds.setAttr( maxConditionSecond+'.colorIfTrueR', 0.0001 )
    cmds.setAttr( maxConditionSecond+'.op', 4 )
    
    minMult = cmds.createNode( 'multDoubleLinear' )
    maxMult = cmds.createNode( 'multDoubleLinear' )
    cmds.connectAttr( minConditionSecond+'.outColorR', minMult+'.input1' )
    cmds.connectAttr( maxConditionSecond+'.outColorR', maxMult+'.input1' )
    cmds.setAttr( minMult+'.input2', 1.0/range )
    cmds.setAttr( maxMult+'.input2', 1.0/range )
    
    cmds.connectAttr( minMult+'.output', detachCurveNode+'.parameter[0]' )
    cmds.connectAttr( maxMult+'.output', detachCurveNode+'.parameter[1]' )
    
    cmds.select( surfNodeParent )



mc_createBendToCurve = """import maya.cmds as cmds
import sgRigCurve
sels = cmds.ls( sl=1 )
for sel in sels:
    sgRigCurve.createBendToCurve( sel )
"""



def mc_makeDynamicCurveKeepSrc( *args ):
    
    sels = cmds.ls( sl=1 )
    
    makeDynamicCurveKeepSrc( sels, 'Dynamic_' )
    
    
    
    
mc_createCurveOnTargetPoints = """import maya.cmds as cmds
import sgRigCurve
sels = cmds.ls( sl=1 )
sgRigCurve.createCurveOnTargetPoints( sels )
"""


mc_createCurveOnSelJoints = """import maya.cmds as cmds
import sgRigCurve
topJnts = cmds.ls( sl=1 )

for topJnt in topJnts:
    
    jnts = cmds.listRelatives( topJnt, c=1, ad=1, type='joint', f=1 )
    jnts.append( topJnt )
    jnts.reverse()
    
    sgRigCurve.createCurveOnTargetPoints( jnts )"""


mc_createPointOnCurve = """import maya.cmds as cmds
import sgRigCurve
for sel in cmds.ls( sl=1 ):
    sgRigCurve.createLocatorOnCurve( sel )"""