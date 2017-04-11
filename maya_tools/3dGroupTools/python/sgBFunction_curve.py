import maya.OpenMaya as om
import maya.cmds as cmds


def getCurveLength(target ):
    
    import sgBFunction_dag
    targetShape = sgBFunction_dag.getShape( target )
    
    fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( targetShape ) )
    return fnCurve.length()




def getKnots( target ):
    
    import sgBFunction_dag
    target = sgBFunction_dag.getShape( target )
    
    fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMObject( target ) )
    
    dArr = om.MDoubleArray()
    fnCurve.getKnots( dArr )
    
    return dArr





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




def makeControledCurveFromJoints( sels ):
    
    import sgBFunction_dag
    
    for sel in sels:
        children = cmds.listRelatives( sel, c=1, ad=1, f=1 )
        children.append( sel )
        
        children.reverse()
        
        points = [[0,0,0] for i in range( len( children ) ) ]
        
        crv = cmds.curve( p=points, d=3 )
        crvShape = sgBFunction_dag.getShape( crv )
        
        for i in range( len( children ) ):
            mmdc = cmds.createNode( 'multMatrixDecompose' )
            cmds.connectAttr( children[i]+'.wm', mmdc+'.i[0]' )
            cmds.connectAttr( sel+'.pim', mmdc+'.i[1]' )
            cmds.connectAttr( mmdc+'.ot', crvShape+'.controlPoints[%d]' % i )




def setWobbleCurveRandom( wobbleCurves, randOffset=[0.0, 0.5], randLength= [0.2, 0.25], randRotate= [0, 0] ):

    import random
    
    import sgBFunction_dag
    
    for curve in wobbleCurves:
        
        wobbleNode = sgBFunction_dag.getNodeFromHistory( curve, 'sgWobbleCurve2' )
        if not wobbleNode: continue
        
        mmdc = cmds.listConnections( wobbleNode[0]+'.aimMatrix' )
        if not mmdc: continue
        aimMatrixObj = cmds.listConnections( mmdc[0]+'.i[0]' )
        if not aimMatrixObj: continue
        
        randomValueOffset = random.uniform( randOffset[0], randOffset[1] )
        randomValueLength = random.uniform( randLength[0], randLength[1] )
        randomValueRotate = random.uniform( randRotate[0], randRotate[1] )
        cmds.setAttr( curve+'.offset', randomValueOffset )
        cmds.setAttr( curve+'.waveLength', randomValueLength )
        cmds.setAttr( aimMatrixObj[0]+'.rotateY', randomValueRotate )




def setWobbleCurveRotateRandom( wobbleCurves, randMin, randMax ):

    import random
    
    import sgBFunction_convert
    import sgBFunction_dag
    
    wobbleCurves = sgBFunction_convert.singleToList( wobbleCurves )
    
    for curve in wobbleCurves:
        
        wobbleNode = sgBFunction_dag.getNodeFromHistory( curve, 'sgWobbleCurve2' )
        if not wobbleNode: continue
        
        mmdc = cmds.listConnections( wobbleNode[0]+'.aimMatrix' )
        if not mmdc: continue
        aimMatrixObj = cmds.listConnections( mmdc[0]+'.i[0]' )
        if not aimMatrixObj: continue
        
        randomValueRotate = random.uniform( randMin, randMax )
        cmds.setAttr( aimMatrixObj[0]+'.rotateY', randomValueRotate )




def addWobbleCurve( targetCurves ):
    
    import sgBFunction_convert
    import sgBFunction_dag
    
    targetCurves = sgBFunction_convert.singleToList( targetCurves )
    targetCurves = sgBFunction_dag.getChildrenShapeExists( targetCurves )

    for targetCurve in targetCurves:
        targetShape = sgBFunction_dag.getShape( targetCurve )
        
        cons = cmds.listConnections( targetShape+'.create', p=1, c=1, s=1, d=0 )
        
        sourceAttr = ''
        if not cons:
            origShape = cmds.createNode( 'nurbsCurve' )
            cmds.connectAttr( targetShape+'.local', origShape+'.create' )
            cmds.refresh()
            cmds.disconnectAttr( targetShape+'.local', origShape+'.create' )
            origObject = cmds.listRelatives( origShape, p=1 )[0]
            origShape = cmds.parent( origShape, targetCurve )
            cmds.setAttr( origShape+'.io', 1 )
            cmds.delete( origObject )
            sourceAttr = origShape+'.local'
        else:
            sourceAttr = cons[1]
        
        sgWobbleCurve = cmds.createNode( 'sgWobbleCurve2' )
        cmds.connectAttr( sourceAttr, sgWobbleCurve + '.inputCurve' )
        cmds.connectAttr( sgWobbleCurve+'.outputCurve', targetShape+'.create', f=1 )
        cmds.connectAttr( 'time1.outTime', sgWobbleCurve+'.time' )
        
        cmds.setAttr( sgWobbleCurve +'.fallOff1[0].fallOff1_Position', 0.2 )
        cmds.setAttr( sgWobbleCurve +'.fallOff1[0].fallOff1_FloatValue', 0.0 )
        cmds.setAttr( sgWobbleCurve +'.fallOff1[1].fallOff1_Position', 1 )
        cmds.setAttr( sgWobbleCurve +'.fallOff1[1].fallOff1_FloatValue', 1 )
        
        cmds.setAttr( sgWobbleCurve + '.timeMult1', 2 )



def getCenterCurve( curves=None ):
    
    import sgBFunction_dag
    
    posList = []
    bbox    = om.MBoundingBox()
    
    if not curves: curves = cmds.ls( sl=1 )
    
    numSpans = 0
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        fnCurve    = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
        numSpans  += fnCurve.numSpans()
    numSpans /= len( curves )
    
    posList = [ [] for i in range( numSpans ) ]
    
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        curvePath = sgBFunction_dag.getMDagPath( curveShape )
        curveWorldMatrix = curvePath.inclusiveMatrix()
        fnCurve    = om.MFnNurbsCurve( curvePath )
        minParam = fnCurve.findParamFromLength( 0 )
        maxParam = fnCurve.findParamFromLength( fnCurve.length() )
        eachParam = ( float( maxParam ) - float( minParam ) ) / numSpans
        bbox = om.MBoundingBox()
        for i in range( numSpans ):
            eachPoint = om.MPoint()
            fnCurve.getPointAtParam( eachParam * i + minParam, eachPoint )
            posList[i].append( eachPoint * curveWorldMatrix )
    
    bbCenterList = []
    for i in range( numSpans ):
        bbox = om.MBoundingBox()
        for j in range( len( curves ) ):
            bbox.expand( posList[i][j] )
        bbCenterList.append( bbox.center() )
    
    minIndexList = []
    
    for i in range( numSpans ):
        minDist = 1000000.0
        minIndex = 0
        for j in range( len( curves ) ):
            dist = posList[i][j].distanceTo( bbCenterList[i] )
            if dist < minDist:
                minDist = dist
                minIndex = j
        minIndexList.append( minIndex )
    
    minIndexRateList = [ 0 for i in range( len( curves ) ) ]
    
    for i in range( numSpans ):
        minIndexRateList[ minIndexList[i] ] += 1

    targetCurveIndex = 0
    maxIndexRate = 0
    for i in range( len( minIndexRateList ) ):
        if minIndexRateList[i] > maxIndexRate:
            maxIndexRate = minIndexRateList[i]
            targetCurveIndex = i
    
    cmds.select( curves[targetCurveIndex] )
    return curves[minIndex]



def createInCurveFromCurve( numCurve ):
    
    import sgBFunction_surface
    import sgBFunction_dag
    
    def optimizeConnection( targetObject ):
        targetShape = sgBFunction_dag.getShape( targetObject )
        src = cmds.listConnections( targetShape + '.create', p=1 )[0]
        dst = cmds.listConnections( targetShape, d=1, s=0, p=1,type="volumeCurvesOnSurface" )[0]
        cmds.connectAttr( src, dst, f=1 )
        cmds.delete( targetObject )
    
    curves = sgBFunction_dag.getChildrenShapeExists( cmds.ls( sl=1 ) )

    surface = sgBFunction_surface.getLoftSurfaceFromSelCurves( curves, True )
    curves = sgBFunction_surface.createInCurve( surface, numCurve )
    
    surfShape = cmds.listRelatives( surface, s=1, f=1 )[0]
    reverseNode = cmds.listConnections( surfShape, s=1, type='reverseSurface' )[0]
    cmds.setAttr( reverseNode+'.direction', 0  )
    cmds.refresh()
    cmds.setAttr( reverseNode+'.direction', 3  )
    cmds.refresh()
    cmds.select( curves )
    #cmds.setAttr( surfShape+'.io', 1 )
    optimizeConnection( surfShape )
    
    return curves




def rebuildByMinMaxSpans( curves, minSpans, maxSpans ):
    
    import sgBFunction_dag
    
    sels = sgBFunction_dag.getChildrenShapeExists( curves )
    
    lengthList = []
    
    minLength = 10000000.0
    maxLength = 0.0
    
    targetCurves = []
    for sel in sels:
        selShape = sgBFunction_dag.getShape( sel )
        if not selShape: continue
        if not cmds.nodeType( selShape ) == 'nurbsCurve': continue
        
        fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( selShape ) )
        
        curveLength = fnCurve.length()
        
        if curveLength < minLength:
            minLength = curveLength
        if curveLength > maxLength:
            maxLength = curveLength
        
        targetCurves.append( sel )
        lengthList.append( fnCurve.length() )
    
    
    diffSpans = maxSpans - minSpans
    diffLength = maxLength - minLength
    
    for i in range( len( targetCurves ) ):
        lengthRate = ( lengthList[i] - minLength ) / diffLength
        
        spansRate = lengthRate * diffSpans
        spans = spansRate + minSpans
        cmds.rebuildCurve( targetCurves[i], rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=1, s=spans, d=3, tol=0.01 )



def getMatricesFromCurve( curve, aimIndex = 0, vUpVector=None ):
    
    import sgBFunction_dag
    
    curveShape = sgBFunction_dag.getShape( curve )
    curvePath = sgBFunction_dag.getMDagPath( curveShape )
    mtxCurve = curvePath.inclusiveMatrix()
    
    fnCurve = om.MFnNurbsCurve( curvePath )
    
    minParam = fnCurve.findParamFromLength( 0 )
    maxParam = fnCurve.findParamFromLength( fnCurve.length() )
    numSpans = fnCurve.numSpans()
    
    lengthParam = maxParam - minParam
    eachParam = lengthParam / ( numSpans - 1 )
    
    if not vUpVector:
        vUp = om.MVector( 0, 1, 0 )
    else:
        vUp = vUpVector
    mtxArr = []
    for i in range( numSpans ):
        point = om.MPoint()
        fnCurve.getPointAtParam( eachParam * i, point )
        vTangent = fnCurve.tangent( eachParam * i ) * mtxCurve 
        vCross = vTangent ^ vUp
        vUp = vCross ^ vTangent
        
        vTangent.normalize()
        vUp.normalize()
        vCross.normalize()
        
        mtx = [ float(i%5 == 0) for i in range( 16 ) ]
        
        indexAim   = (3+aimIndex)%3
        indexUp    = (3+aimIndex+1)%3
        indexCross = (3+aimIndex+2)%3
        
        mtx[ indexAim*4+0 ] = vTangent.x
        mtx[ indexAim*4+1 ] = vTangent.y
        mtx[ indexAim*4+2 ] = vTangent.z
        mtx[ indexUp*4+0 ] = vUp.x
        mtx[ indexUp*4+1 ] = vUp.y
        mtx[ indexUp*4+2 ] = vUp.z
        mtx[ indexCross*4+0 ] = vCross.x
        mtx[ indexCross*4+1 ] = vCross.y
        mtx[ indexCross*4+2 ] = vCross.z
        mtx[ 3*4+0 ] = point.x
        mtx[ 3*4+1 ] = point.y
        mtx[ 3*4+2 ] = point.z
        
        mtxArr.append( mtx )
    
    return mtxArr



def addDistanceAttribute( curve ):
    
    import sgBFunction_attribute
    import sgBFunction_dag
    
    curveLength = getCurveLength( curve )
    sgBFunction_attribute.addAttr( curve, ln='initCurveLength', k=1 )
    sgBFunction_attribute.addAttr( curve, ln='curveLength', k=1 )
    
    cmds.setAttr( curve+'.initCurveLength', e=1, lock=0 )
    cmds.setAttr( curve+'.curveLength', e=1, lock=0 )
    
    cmds.setAttr( curve+'.initCurveLength', curveLength )
    
    if not cmds.listConnections( curve+'.curveLength', s=1, d=0, type='curveInfo' ):
        curveShape = sgBFunction_dag.getShape( curve )
        curveInfo = cmds.createNode( 'curveInfo' )
        cmds.connectAttr( curveShape+'.local', curveInfo+'.inputCurve' )
        cmds.connectAttr( curveInfo+'.arcLength', curve+'.curveLength' )
    
    cmds.setAttr( curve+'.initCurveLength', e=1, lock=1 )
    cmds.setAttr( curve+'.curveLength', e=1, lock=1 )




def getCurveInfo_worldSpace( curve ):
    
    import sgBFunction_dag
    curveShape = sgBFunction_dag.getShape( curve )
    
    cons = cmds.listConnections( curveShape+'.worldSpace', d=1, s=0 )
    
    if not cons:
        info = cmds.createNode( 'curveInfo' )
        cmds.connectAttr( curveShape+'.worldSpace[0]', info+'.inputCurve' )
        return info
    else:
        return cons[0]



def getCurveInfo_localSpace( curve ):
    
    import sgBFunction_dag
    curveShape = sgBFunction_dag.getShape( curve )
    
    cons = cmds.listConnections( curveShape+'.local', d=1, s=0 )
    
    if not cons:
        info = cmds.createNode( 'curveInfo' )
        cmds.connectAttr( curveShape+'.local', info+'.inputCurve' )
        return info
    else:
        return cons[0]



def setKeyCurve( keyCurve, targetCurve, objBaseMatrix = None ):
    
    import sgBFunction_dag
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )
    
    nodes = sgBFunction_dag.getNodeFromHistory( targetCurve, 'sgHair_keyCurve' )
    if not nodes:
        node = cmds.deformer( targetCurve, type= 'sgHair_keyCurve' )[0]
        cmds.connectAttr( 'time1.outTime', node+'.time' )
        if objBaseMatrix:
            mm = cmds.createNode( 'multMatrix' )
            cmds.connectAttr( objBaseMatrix+'.wm', mm+'.i[0]' )
            cmds.connectAttr( targetCurve+'.wim', mm+'.i[1]' )
            cmds.connectAttr( mm+'.o', node+'.baseLocalMatrix' )
    else:
        node = nodes[0]
    
    fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( node ) )
    
    cuTime   = cmds.currentTime( q=1 )
    plugKeys = fnNode.findPlug( 'keys' )
    
    targetIndex = 0
    for i in range( plugKeys.numElements() ):
        plugKey = plugKeys[i]
        
        plugFrame = plugKey.child( 0 )
        timeValue = plugFrame.asMTime().value()
        
        if cuTime == timeValue:
            targetIndex = plugKey.logicalIndex()
            break
        
        if plugKey.logicalIndex() >= targetIndex:
            targetIndex = plugKey.logicalIndex() + 1
    
    if objBaseMatrix:
        import sgBFunction_convert
        mtxObj = cmds.getAttr( objBaseMatrix+'.wm' )
        mtxInvCurve = cmds.getAttr( keyCurve+'.wim' )
        
        mMtxObj = sgBFunction_convert.convertMatrixToMMatrix( mtxObj )
        mMtxInvCurve = sgBFunction_convert.convertMatrixToMMatrix( mtxInvCurve )
        
        mMtxLocal = mMtxObj * mMtxInvCurve
        mtxLocal = sgBFunction_convert.convertMMatrixToMatrix( mMtxLocal )
        cmds.setAttr( node+'.keys[%d].baseMatrix' % targetIndex, mtxLocal, type='matrix' )
    cmds.setAttr( node+'.keys[%d].keyframe' % targetIndex, cuTime )
    keyCurveShape = sgBFunction_dag.getShape( keyCurve )
    if not cmds.isConnected( keyCurveShape+'.local', node+'.keys[%d].inputCurve' % targetIndex ):
        cmds.connectAttr( keyCurveShape+'.local', node+'.keys[%d].inputCurve' % targetIndex, f=1 )
    
    '''
    fnKeyCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( keyCurveShape ) )
    points = om.MPointArray()
    fnKeyCurve.getCVs( points )
    
    for i in range( points.length() ):
        cmds.setAttr( node+'.keys[%d].cvPoint[%d].cvPointX' %( targetIndex, i ), points[i].x )
        cmds.setAttr( node+'.keys[%d].cvPoint[%d].cvPointY' %( targetIndex, i ), points[i].y )
        cmds.setAttr( node+'.keys[%d].cvPoint[%d].cvPointZ' %( targetIndex, i ), points[i].z )'''



def setKeyCurveMatrixObjects( curves, mtxObj ):
    
    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( mtxObj, ln='keyCurveTarget', at='message' )
    
    for curve in curves:
        sgBFunction_attribute.addAttr( curve, ln='mtxObj_forKeyCurve', at='message' )
        if cmds.isConnected( mtxObj + '.keyCurveTarget', curve + '.mtxObj_forKeyCurve' ): continue
        cmds.connectAttr( mtxObj + '.keyCurveTarget', curve + '.mtxObj_forKeyCurve', f=1 )



def setKeyCurves( curves ):
    
    import sgBFunction_dag
    import sgBFunction_attribute
    import math
    
    curves = sgBFunction_dag.getChildrenCurveExists( curves )
    
    currentFrame = str( '%.2f' % cmds.currentTime( q=1 ) ).replace( '.', '_' ).replace( '-', 'm' )
    
    frameGroup = 'keyCurveGroup_%s' % currentFrame
    if not cmds.objExists( frameGroup ):
        cmds.group( em =1, n=frameGroup )
        sgBFunction_attribute.addAttr( frameGroup, ln='frameValue', dt='string' )
        cmds.setAttr( frameGroup+'.frameValue', currentFrame, type='string' )
        
        cmds.setAttr( frameGroup+'.overrideEnabled', 1 )
        cmds.setAttr( frameGroup+'.overrideColor', int( math.fabs( cmds.currentTime( q=1 ) ) )%32 )
        
    
    keyCurves = []
    for curve in curves:
        sgBFunction_attribute.addAttr( curve, ln='keyCurveBase', at='message' )
        cons = cmds.listConnections( curve+'.keyCurveBase', d=1, s=0  )
        if cons:
            targetCurve = None
            for con in cons:
                conP = cmds.listRelatives( con, p=1, f=1 )[0]
                if cmds.getAttr( conP+'.frameValue' ) == currentFrame:
                    targetCurve = con
            if targetCurve:
                keyCurves.append( targetCurve )
                continue
        
        keyCurveShape = cmds.createNode( 'nurbsCurve' )
        curveShape = sgBFunction_dag.getShape( curve )
        cmds.connectAttr( curveShape+'.local', keyCurveShape+'.create' )
        keyCurve = sgBFunction_dag.getTransform( keyCurveShape )
        
        curveName = curve.split( '|' )[-1]
        keyCurve = cmds.rename( keyCurve, curveName+'_'+currentFrame )
        keyCurves.append( keyCurve )
        
        sgBFunction_attribute.addAttr( keyCurve, ln='keyCurve', at='message' )
        cmds.connectAttr( curve+'.keyCurveBase', keyCurve+'.keyCurve' )
    
    cmds.refresh()
    
    for i in range( len( curves ) ):
        baseCurve = sgBFunction_dag.getShape( curves[i] )
        keyCurve  = sgBFunction_dag.getShape( keyCurves[i] )
        if cmds.isConnected( baseCurve+'.local', keyCurve+'.create' ):
            cmds.disconnectAttr( baseCurve+'.local', keyCurve+'.create' )
        try:keyCurves[i] = cmds.parent( keyCurves[i], frameGroup )[0]
        except:continue
    
    targetKeyCurves = []
    for i in range( len( curves ) ):
        baseCurve = curves[i]
        keyCurve  = keyCurves[i]
        if not cmds.attributeQuery( 'mtxObj_forKeyCurve', node=baseCurve, ex=1 ): 
            cmds.delete( keyCurve )
            continue
        mtxObj = cmds.listConnections( baseCurve + '.mtxObj_forKeyCurve', s=1, d=0 )
        if not mtxObj:
            cmds.delete( keyCurve )
            continue
        targetKeyCurves.append( keyCurve )
        setKeyCurve( keyCurve, baseCurve, mtxObj[0] )
    
    return targetKeyCurves


def createLocalCurve( curveAimTarget, curveBase ):
    
    import sgBFunction_convert
    import sgBModel_data
    
    mtxCurveAimTarget = sgBFunction_convert.convertMatrixToMMatrix( cmds.getAttr( curveAimTarget+'.wm' ) )
    mtxCurveBase      = sgBFunction_convert.convertMatrixToMMatrix( cmds.getAttr( curveBase+'.wm' ) )
    
    mtxCurveLocal     = mtxCurveAimTarget * mtxCurveBase.inverse()
    
    curveLastPos = [ mtxCurveLocal( 3, 0 ), mtxCurveLocal( 3, 1 ), mtxCurveLocal( 3, 2 ) ]
    
    curve = cmds.curve( p=[ [0,0,0], curveLastPos ], d=1 )
    curve = cmds.parent( curve, curveBase )[0]
    
    cmds.xform( curve, os=1, matrix= sgBModel_data.getDefaultMatrix() )



def duplicateOnlyCurve( curves ):
    
    import sgBFunction_dag
    curves = sgBFunction_dag.getChildrenCurveExists( curves )
    
    newCurves = []
    for curve in curves:
        curveP = sgBFunction_dag.getParent( curve )
        if curveP:
            newCurveParent = sgBFunction_dag.makeCloneObject( curveP )
        else:
            newCurveParent = None
        
        newCurveShape = cmds.createNode( 'nurbsCurve' )
        curveShape = sgBFunction_dag.getShape( curve )
        cmds.connectAttr( curveShape+'.local', newCurveShape+'.create' )
        
        newCurve = sgBFunction_dag.getTransform( newCurveShape )
        newCurve = cmds.rename( newCurve, 'du_' + curve.split( '|' )[-1] )
        if newCurveParent:
            newCurve = cmds.parent( newCurve, newCurveParent )[0]
        newCurves.append( newCurve )
    
    cmds.refresh()
    
    for i in range( len( newCurves ) ):
        curveShape = sgBFunction_dag.getShape( curves[i] )
        newCurveShape = sgBFunction_dag.getShape( newCurves[i] )
        if cmds.isConnected( curveShape+'.local', newCurveShape+'.create' ):
            cmds.disconnectAttr( curveShape+'.local', newCurveShape+'.create' )
    
    return newCurves



def getClosestParameter( targetObj, curve ):
    
    import sgBFunction_dag
    
    crvShape = sgBFunction_dag.getShape( curve )
    
    dagPathTarget = sgBFunction_dag.getMDagPath( targetObj )
    mtxTarget = dagPathTarget.inclusiveMatrix()
    dagPathCurve  = sgBFunction_dag.getMDagPath( crvShape )
    mtxCurve  = dagPathCurve.inclusiveMatrix()
    
    pointTarget = om.MPoint( mtxTarget[3] )
    pointTarget *= mtxCurve.inverse()
    
    fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( crvShape ) )
    
    util = om.MScriptUtil()
    util.createFromDouble( 0.0 )
    ptrDouble = util.asDoublePtr()
    fnCurve.closestPoint( pointTarget, 0, ptrDouble )
    
    paramValue = om.MScriptUtil().getDouble( ptrDouble )
    
    return paramValue




def tool_curveEditBrush():
    
    import sgBFunction_base
    import maya.cmds as cmds
    import maya.mel as mel
    sgBFunction_base.autoLoadPlugin( 'sgTools' )
    
    melScript = '''
    proc int isGreasePencilContext()
    //
    //    Description:
    //        Returns true if this is Grease Pencil context.
    //
    {
        string $tc = currentToolClass();
        return ($tc == "greasePencil");
    }
    
    
    global proc artActivateScreenSlider(
        string $sliderName
    )
    //
    //    Description:
    //        Global procs for activating screen sliders
    //        - sets the flag to activate them.
    //
    {
        // New Artisan Tools.
        if ( isArtisanCtx() ) {
            string $artisanCmd = artisanCommand();
            if( $sliderName == "upper_radius" ) {
                artBaseCtx -e -dragSlider "radius" `currentCtx`;
            } else if( $sliderName == "lower_radius" ) {
                artBaseCtx -e -dragSlider "lowradius" `currentCtx`;
            } else if( $sliderName == "opacity" ) {
                artBaseCtx -e -dragSlider "opacity" `currentCtx`;
            } else if( $sliderName == "value" ) {
                artBaseCtx -e -dragSlider "value" `currentCtx`;
            } else if( $sliderName == "stamp_depth" ) {
                artBaseCtx -e -dragSlider "depth" `currentCtx`;
            } else if( $sliderName == "displacement" ) {
                artBaseCtx -e -dragSlider "displacement" `currentCtx`;
            } else if( $sliderName == "uv_vector" ) {
                artBaseCtx -e -dragSlider "uvvector" `currentCtx`;
            }
        }
        else if ( isGreasePencilContext() )
        {
            if( $sliderName == "upper_radius" )
            {
                // Map B to radius
                artBaseCtx -e -dragSlider "radius" greasePencilContext;
            }
            else if( $sliderName == "displacement" )
            {
                // Map m to opacity rather than value but not for the eraser
                // as this has no effect
                if ( 4 != `greasePencilCtx -query -greasePencilType greasePencilContext` )
                {
                    artBaseCtx -e -dragSlider "opacity" greasePencilContext;
                }
            }
        }
        // UV Smudge Tool
        else if ( isSmudgeCtx() ) {
            texSmudgeUVContext -edit -dragSlider "radius" texSmudgeUVCtx;
        }
        // Soft Mod
        else if ( size( getActiveSoftMod() ) > 0 )
        {
            string $ctx = `currentCtx`;
            if( `contextInfo -c $ctx` != "softMod" )
                $ctx = "softModContext";
            softModCtx -e -dragSlider "radius" $ctx;
        }
        // Paint Effects.
        else if ((`isTrue "MayaCreatorExists"`) && isDynPaint())
        {
            if( $sliderName == "displacement" ) {
                dynPaintResize("offset");
            } else if( $sliderName == "lower_radius" ) {
                dynPaintResize("width");
            } else {
                dynPaintResize("size");
            }
        }
        else if ($sliderName == "upper_radius")
        {
            // upper_radius is the "b" key by default.  We only want to use that one
            // for soft select.  The "n" and "m" keys can also come in here so we want
            // to filter those out.
            global string $gSoftSelectOptionsCtx;
            softSelectOptionsCtx -edit -buttonDown $gSoftSelectOptionsCtx;
            if( `currentCtx` == "sgCurveEditBrushContext1" )
            {
                sgCurveEditBrushContext -e -radiusEditOn 1 sgCurveEditBrushContext1;
            }
        }
    }
    
    global proc artDeactivateScreenSlider()
    //
    //    Description:
    //        Global procs for deactivating screen sliders - sets the flag to
    //        deactivate them.
    //
    {
        // New Artisan Tools.
        if ( isArtisanCtx() ) {
            artBaseCtx -e -dragSlider "none" `currentCtx`;
        }
        else if ( isGreasePencilContext() )
        {
            artBaseCtx -e -dragSlider "none" greasePencilContext;
        }
        // UV Smudge
        else if ( isSmudgeCtx() ) {
            texSmudgeUVContext -e -dragSlider "none" texSmudgeUVCtx;
        }
        // Soft Mod
        else if ( size( getActiveSoftMod() ) > 0 )
        {
            string $ctx = `currentCtx`;
            if( `contextInfo -c $ctx` != "softMod" )
                $ctx = "softModContext";
            softModCtx -e -dragSlider "none" $ctx;
        }
        // Paint Effects.
        else if (`isTrue "MayaCreatorExists"` && isDynPaint())
        {
            dynPaintResize("none");
        }
        else
        {
            // We filter out the "n" and "m" keys in the activate call
            // but don't here because there isn't a slider name passed
            // in for deactivate.  To soft select context is smart
            // enough to know that it didn't start and edit so we are
            // ok to just call this in case we did.
            global string $gSoftSelectOptionsCtx;
            softSelectOptionsCtx -edit -buttonUp $gSoftSelectOptionsCtx;
        }
        if( `currentCtx` == "sgCurveEditBrushContext1" )
        {
            sgCurveEditBrushContext -e -radiusEditOn 0 sgCurveEditBrushContext1;
        }
    }
    
    global proc sgCurveEditBrush_contextProperties()
    {
    }
    
    global proc sgCurveEditBrush_contextValues( string $context )
    {
    }
    '''
    
    mel.eval( melScript )
    
    import sgBFunction_dag
    sels = sgBFunction_dag.getChildrenCurveExists( cmds.ls( sl=1 ) )
    cmds.select( sels )
    
    if not cmds.contextInfo( "sgCurveEditBrushContext1", ex=1 ):
        mel.eval( 'sgCurveEditBrushContext sgCurveEditBrushContext1' )
    cmds.setToolTo( "sgCurveEditBrushContext1" )