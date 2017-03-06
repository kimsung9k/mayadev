import maya.cmds as cmds
import maya.OpenMaya as om



def getWristAngleNode( target, targetBase=None ):
    wristAngleCons = cmds.listConnections( target+'.m', s=0, d=1, type='wristAngle' )
    wristAngleNode = ''
    
    if not wristAngleCons:
        mmCons = cmds.listConnections( target+'.wm', s=0, d=1, type='multMatrix' )
        if mmCons:
            wristAngleCons = cmds.listConnections( mmCons[0]+'.o', s=0, d=1, type='wristAngle' )
            if wristAngleCons: wristAngleNode = wristAngleCons[0]
    else:
        wristAngleNode = wristAngleCons[0]
    
    if wristAngleNode: return wristAngleNode
    
    wa = cmds.createNode( 'wristAngle' )
    if not targetBase: 
        targetBase = cmds.listRelatives( target, p=1, f=1 )[0]
        cmds.connectAttr( target+'.m', wa+'.inputMatrix' )
    else:
        mm = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( target+'.wm', mm+'.i[0]' )
        cmds.connectAttr( targetBase+'.wim', mm+'.i[1]' )
        cmds.connectAttr( mm+'.o', wa+'.inputMatrix' )
    
    cmds.select( wa )
    return wa




def createWristAngleDriver( target, targetBase=None ):
    
    def getWristAngleNode( target, targetBase ):
        wristAngleCons = cmds.listConnections( target+'.m', s=0, d=1, type='wristAngle' )
        wristAngleNode = ''
        
        if not wristAngleCons:
            mmCons = cmds.listConnections( target+'.wm', s=0, d=1, type='multMatrix' )
            if mmCons:
                wristAngleCons = cmds.listConnections( mmCons[0]+'.o', s=0, d=1, type='wristAngle' )
                if wristAngleCons: wristAngleNode = wristAngleCons[0]
        else:
            wristAngleNode = wristAngleCons[0]
        
        if wristAngleNode: return wristAngleNode
        
        wa = cmds.createNode( 'wristAngle' )
        if not targetBase: 
            targetBase = cmds.listRelatives( target, p=1, f=1 )[0]
            cmds.connectAttr( target+'.m', wa+'.inputMatrix' )
        else:
            mm = cmds.createNode( 'multMatrix' )
            cmds.connectAttr( target+'.wm', mm+'.i[0]' )
            cmds.connectAttr( targetBase+'.wim', mm+'.i[1]' )
            cmds.connectAttr( mm+'.o', wa+'.inputMatrix' )
        
        return wa
    
    
    wa = getWristAngleNode( target, targetBase )
    animCurve = cmds.createNode( 'animCurveUU' )
    cmds.connectAttr( wa+'.outAngle', animCurve+'.input' )
    
    cmds.setKeyframe( animCurve, f=0,  v=0 )
    cmds.setKeyframe( animCurve, f=45, v=0.5 )
    cmds.setKeyframe( animCurve, f=90, v=1.0 )
    
    cmds.select( animCurve )
    return animCurve




def createLocalBlendTwoMatrixObject( first, second, target = None ):
    
    import sgBFunction_attribute
    
    blMtx = cmds.createNode( 'blendTwoMatrixDecompose' )
    cmds.connectAttr( first+'.m', blMtx+'.inMatrix1' )
    cmds.connectAttr( second+'.m', blMtx+'.inMatrix2' )
    
    if not target: target = cmds.createNode( 'transform' )
    
    sgBFunction_attribute.addAttr( target, ln='blend', min=0, max=1, dv=0.5, k=1 )
    cmds.connectAttr( target+'.blend', blMtx+'.attributeBlender' )
    
    if cmds.nodeType( target ) == 'joint':
        try:cmds.setAttr( target+'.jo', 0,0,0 )
        except:pass
    
    if not cmds.isConnected( blMtx+'.ot', target+'.t' ):
        cmds.connectAttr( blMtx+'.ot', target+'.t', f=1 )
    if not cmds.isConnected( blMtx+'.or', target+'.r' ):
        cmds.connectAttr( blMtx+'.or', target+'.r', f=1 )
    if not cmds.isConnected( blMtx+'.os', target+'.s' ):
        cmds.connectAttr( blMtx+'.os', target+'.s', f=1 )
    if not cmds.isConnected( blMtx+'.osh', target+'.sh' ):
        cmds.connectAttr( blMtx+'.osh', target+'.sh', f=1 )
    
    cmds.select( blMtx, target )
    return blMtx, target




def createWorldBlendTwoMatrixObject( first, second, target = None ):
    
    import sgBFunction_attribute
    
    blMtx = cmds.createNode( 'blendTwoMatrix' )
    mmdc  = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( first+'.wm', blMtx+'.inMatrix1' )
    cmds.connectAttr( second+'.wm', blMtx+'.inMatrix2' )
    cmds.connectAttr( blMtx+'.outMatrix', mmdc+'.i[0]' )
    
    if not target: target = cmds.createNode( 'transform' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    sgBFunction_attribute.addAttr( target, ln='blend', min=0, max=1, dv=0.5, k=1 )
    cmds.connectAttr( target+'.blend', blMtx+'.attributeBlender' )
    
    if not cmds.isConnected( mmdc+'.ot', target+'.t' ):
        cmds.connectAttr( mmdc+'.ot', target+'.t', f=1 )
    if not cmds.isConnected( mmdc+'.or', target+'.r' ):
        cmds.connectAttr( mmdc+'.or', target+'.r', f=1 )
    if not cmds.isConnected( mmdc+'.os', target+'.s' ):
        cmds.connectAttr( mmdc+'.os', target+'.s', f=1 )
    if not cmds.isConnected( mmdc+'.osh', target+'.sh' ):
        cmds.connectAttr( mmdc+'.osh', target+'.sh', f=1 )
    
    cmds.select( blMtx, target )
    return blMtx, target





def createRivetBasedOnSkinWeights( selectedObjs ):
    
    import sgBFunction_convert
    import sgBFunction_mesh
    import sgBFunction_dag
    import sgBFunction_skinCluster
    import maya.OpenMaya as om
    
    def getJointMultMatrix( jnt, mtxBindPre ):
        cons = cmds.listConnections( jnt+'.wm', type='multMatrix' )

        if cons:
            for con in cons:
                if cmds.attributeQuery( 'skinWeightInfluenceMatrix', node=con, ex=1 ):
                    if mtxBindPre == cmds.getAttr( con+'.i[0]' ):
                        return con
        
        mmtxNode = cmds.createNode( 'multMatrix' )
        cmds.setAttr( mmtxNode+'.i[0]', mtxBindPre, type='matrix' )
        cmds.connectAttr( jnt+'.wm', mmtxNode+'.i[1]' )
        
        cmds.addAttr( mmtxNode, ln='skinWeightInfluenceMatrix', at='message' )
        
        return mmtxNode


    mesh, vtxIndices = sgBFunction_mesh.getMeshAndIndicesPoints( selectedObjs )
    
    skinClusterNode = sgBFunction_dag.getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusterNode: return None
    skinClusterNode = skinClusterNode[0]
    
    influenceAndWeightList, phygicalMap = sgBFunction_skinCluster.getInfluenceAndWeightList( mesh, vtxIndices )
    
    meshMatrix = sgBFunction_dag.getMDagPath( mesh ).inclusiveMatrix()
    meshPoints = sgBFunction_mesh.getLocalPoints( mesh )
    plugMatrix = sgBFunction_skinCluster.getPlugMatrix( mesh )
    plugBindPre = sgBFunction_skinCluster.getPlugBindPre( mesh )
    
    BB = om.MBoundingBox()
    
    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    mtxPlugIndidcesAndWeights = {}
    allWeights = 0.0
    for i in vtxIndices:
        influenceList, weights = influenceAndWeightList[ phygicalMap[i] ]
        
        for j in range( len( influenceList ) ):
            mtxPlugIndex = influenceList[j]
            if mtxPlugIndex in mtxPlugIndidcesAndWeights.keys():
                mtxPlugIndidcesAndWeights[mtxPlugIndex] += weights[j]
            else:
                mtxPlugIndidcesAndWeights.update( {mtxPlugIndex:weights[j]} )
            allWeights += weights[j]
        BB.expand( meshPoints[i] )
    worldPoint = BB.center()*meshMatrix
    
    items = mtxPlugIndidcesAndWeights.items()
    for i in range( len( items ) ):
        influence, weight = items[i]
        
        plugMatrixElement = plugMatrix.elementByLogicalIndex( influence )
        plugBindPreElement = plugBindPre.elementByLogicalIndex( influence )
        
        jnt = cmds.listConnections( plugMatrixElement.name(), s=1, d=0, type='joint' )[0]
        mtxBindPre = cmds.getAttr( plugBindPreElement.name() )
        mmtxNode = getJointMultMatrix( jnt, mtxBindPre )
        cmds.connectAttr( mmtxNode+'.o', wtAddMtx+'.i[%d].m' % i )
        cmds.setAttr( wtAddMtx+'.i[%d].w' % i, weight/allWeights )
    
    origObj = cmds.createNode( 'transform', n='OrigObject' )
    destObj = cmds.createNode( 'transform', n='destObject' )
    cmds.setAttr( destObj+'.dh' , 1 )
    cmds.setAttr( destObj+'.dla', 1 )
    mmNode = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    mtxWtAdd = cmds.getAttr( wtAddMtx+'.o' )
    
    cmds.connectAttr( origObj+'.wm', mmNode+'.i[0]' )
    cmds.connectAttr( wtAddMtx+'.o', mmNode+'.i[1]' )
    cmds.connectAttr( destObj+'.pim', mmNode+'.i[2]' )
    
    cmds.connectAttr( mmNode+'.o', dcmp+'.imat' )
    
    cmds.connectAttr( dcmp+'.ot', destObj+'.t' )
    cmds.connectAttr( dcmp+'.or', destObj+'.r' )
    
    mmtxWtAdd = sgBFunction_convert.convertMatrixToMMatrix( mtxWtAdd )
    worldPoint *= mmtxWtAdd.inverse()
    cmds.setAttr( origObj+'.t', worldPoint.x, worldPoint.y, worldPoint.z )



def blendTwoMatrixObject( first, second, target=None ):
    
    if not target: target = cmds.createNode( 'transform' )
    
    blendTwoMatrix = cmds.createNode( 'blendTwoMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', blendTwoMatrix+'.inMatrix1' )
    cmds.connectAttr( second+'.wm', blendTwoMatrix+'.inMatrix2' )
    
    cmds.connectAttr( blendTwoMatrix+'.outMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )
    
    if not cmds.attributeQuery( 'blend', node=target, ex=1 ):
        cmds.addAttr( target, ln='blend', min=0, max=1, dv=0.5 )
        cmds.setAttr( target+'.blend', e=1, k=1 )
    
    cmds.connectAttr( target+'.blend', blendTwoMatrix+'.attributeBlender' )




def blendTwoMatrixObject_local( first, second, target=None ):
    
    if not target: target = cmds.createNode( 'transform' )
    
    blendTwoMatrix = cmds.createNode( 'blendTwoMatrixDecompose' )
    
    cmds.connectAttr( first+'.m', blendTwoMatrix+'.inMatrix1' )
    cmds.connectAttr( second+'.m', blendTwoMatrix+'.inMatrix2' )
    
    cmds.connectAttr( blendTwoMatrix+'.ot', target+'.t' )
    cmds.connectAttr( blendTwoMatrix+'.or', target+'.r' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )
    
    if not cmds.attributeQuery( 'blend', node=target, ex=1 ):
        cmds.addAttr( target, ln='blend', min=0, max=1, dv=0.5 )
        cmds.setAttr( target+'.blend', e=1, k=1 )
    
    cmds.connectAttr( target+'.blend', blendTwoMatrix+'.attributeBlender' )





def followMatrixConnection( ctl, others ):
    
    import sgBFunction_attribute
    ctlP = cmds.listRelatives( ctl, p=1 )[0]
    
    followMatrix = cmds.createNode( 'followMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( others[0]+'.wm', followMatrix+'.originalMatrix' )
    
    sgBFunction_attribute.addAttr( ctl, ln='_______', at='enum', en='Parent:', cb=1 )
    
    for other in others[1:]:
        i = others.index( other ) - 1
        cmds.connectAttr( other+'.wm', followMatrix+'.inputMatrix[%d]' % i )
        
        attrName = 'parent' + other.split( '_' )[-1]
        print other, attrName
        sgBFunction_attribute.addAttr( ctl, ln= attrName, min=0, max=10, k=1 )
        cmds.connectAttr( ctl+'.'+attrName, followMatrix+'.inputWeight[%d]' % i )
    
    cmds.connectAttr( followMatrix+'.outputMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( ctlP+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', ctlP+'.t' )
    cmds.connectAttr( mmdc+'.or', ctlP+'.r' )



def createFollowMatrixObject( base, targets, attrName='followWeight' ):
    
    import sgBFunction_attribute
    
    followMatrix = cmds.createNode( 'followMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( base+'.wm', followMatrix+'.originalMatrix' )
    
    for other in targets:
        i = targets.index( other )
        cmds.connectAttr( other+'.wm', followMatrix+'.inputMatrix[%d]' % i )
        
        addAttrName = attrName + '_' + other.split( '_' )[-1]
        
        sgBFunction_attribute.addAttr( base, ln= addAttrName, min=0, max=10, k=1 )
        cmds.connectAttr( base+'.'+addAttrName, followMatrix+'.inputWeight[%d]' % i )
    
    followTarget = cmds.createNode( 'transform' )
    cmds.connectAttr( followMatrix+'.outputMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( followTarget+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', followTarget+'.t' )
    cmds.connectAttr( mmdc+'.or', followTarget+'.r' )




def setNearestPointOnCurveInfo( targetCrvs, createTransform = False ):
    
    import sgBFunction_convert
    import sgBFunction_dag
    
    targetCrvs = sgBFunction_convert.singleToList( targetCrvs )
    
    infos = []
    
    for crv in targetCrvs:
        crv = sgBFunction_dag.getShape( crv )
        
        npc = cmds.createNode( 'nearestPointOnCurve' )
        info = cmds.createNode( 'pointOnCurveInfo' )
        
        cmds.connectAttr( crv+'.worldSpace[0]', npc+'.inputCurve' )
        cmds.connectAttr( crv+'.worldSpace[0]', info+'.inputCurve' )
        cmds.connectAttr( npc+'.parameter', info+'.parameter' )
    
        infos.append( npc )
        
    if createTransform:
        transforms = []
        for info in infos:
            trNode = cmds.createNode( 'transform' )
            fbf = cmds.createNode( 'fourByFourMatrix' )
            mmdc= cmds.createNode( 'multMatrixDecompose' )
            
            cmds.connectAttr( info+'.positionX', fbf+'.i30' )
            cmds.connectAttr( info+'.positionY', fbf+'.i31' )
            cmds.connectAttr( info+'.positionZ', fbf+'.i32' )
            
            cmds.setAttr( trNode+'.dh', 1 )
            cmds.connectAttr( fbf+'.output', mmdc+'.i[0]' )
            cmds.connectAttr( trNode+'.pim', mmdc+'.i[1]' )
            cmds.connectAttr( mmdc+'.ot', trNode+'.t' )
            transforms.append( trNode )
    
        cmds.select( transforms )
    return infos



def removeCloneAttributes():
    
    import sgBModel_dag
    targetAttrs = cmds.ls( '*.'+sgBModel_dag.cloneTargetAttrName )
    
    for targetAttr in targetAttrs:
        cmds.deleteAttr( targetAttr )



def addSquashFromCurve( target, curve ):
    
    import sgBFunction_curve
    import sgBFunction_dag
    import sgBFunction_mscriptUtil
    import math
    
    sgBFunction_curve.addDistanceAttribute( curve )
    
    squashNode = cmds.createNode( 'squash' )
    cmds.connectAttr( curve + '.initCurveLength', squashNode+'.lengthOriginal' )
    cmds.connectAttr( curve + '.curveLength', squashNode+'.lengthModify' )
    
    divNode = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( divNode+'.operation', 2 )
    cmds.connectAttr( curve+'.curveLength', divNode+'.input1X' )
    cmds.connectAttr( curve+'.initCurveLength', divNode+'.input2X' )
    
    curveShape = sgBFunction_dag.getShape( curve )
    mtxTarget = sgBFunction_dag.getMDagPath( target ).inclusiveMatrix()
    fnCurve   = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
    mtxCurve = sgBFunction_dag.getMDagPath( curveShape ).inclusiveMatrix()

    pointTarget = om.MPoint( mtxTarget( 3, 0 ), mtxTarget( 3, 1 ), mtxTarget( 3, 2 ) ) * mtxCurve.inverse()

    ptrParam, utilParam = sgBFunction_mscriptUtil.getDoublePtr()
    fnCurve.getParamAtPoint( pointTarget, ptrParam )
    
    param = utilParam.getDouble( ptrParam )
    tangent = fnCurve.tangent( param )
    
    vX = om.MVector( mtxTarget( 0, 0 ), mtxTarget( 0, 1 ), mtxTarget( 0, 2 ) )
    vY = om.MVector( mtxTarget( 1, 0 ), mtxTarget( 1, 1 ), mtxTarget( 1, 2 ) )
    vZ = om.MVector( mtxTarget( 2, 0 ), mtxTarget( 2, 1 ), mtxTarget( 2, 2 ) )
    
    dotX = math.fabs( tangent * vX )
    dotY = math.fabs( tangent * vY )
    dotZ = math.fabs( tangent * vZ )
    
    if dotX > dotY and dotX > dotZ:
        cmds.connectAttr( divNode+'.outputX', target+'.scaleX', f=1 )
        cmds.connectAttr( squashNode+'.output', target+'.scaleY', f=1 )
        cmds.connectAttr( squashNode+'.output', target+'.scaleZ', f=1 )
    elif dotY > dotZ and dotY > dotX:
        cmds.connectAttr( squashNode+'.output', target+'.scaleX', f=1 )
        cmds.connectAttr( divNode+'.outputX', target+'.scaleY', f=1 )
        cmds.connectAttr( squashNode+'.output', target+'.scaleZ', f=1 )
    elif dotZ > dotX and dotZ > dotY:
        cmds.connectAttr( squashNode+'.output', target+'.scaleX', f=1 )
        cmds.connectAttr( squashNode+'.output', target+'.scaleY', f=1 )
        cmds.connectAttr( divNode+'.outputX', target+'.scaleZ', f=1 )




def createAimObject( axisIndex, inverseAim, displayAxis, worldPosition, *args ):
    
    def createAimObjectCmd( first, second, third, worldPosition=False ):
    
        aimObjectMatrix = cmds.createNode( 'aimObjectMatrix' )
        cmds.connectAttr( first+'.wm', aimObjectMatrix+'.targetMatrix' )
        cmds.connectAttr( second+'.wm', aimObjectMatrix+'.baseMatrix' )
        
        if third:
            aimObject = third
        else:
            aimObject = cmds.createNode( 'transform' )
        
        if cmds.nodeType( aimObject ) == 'joint':
            try: cmds.setAttr( aimObject+'.jo', 0,0,0 )
            except:pass
        cmds.connectAttr( aimObjectMatrix+'.outRotate', aimObject+'.r' )
        
        if not third: cmds.parent( aimObject, second )
        cmds.setAttr( aimObject+'.t', 0,0,0 )
        
        if worldPosition:
            cmds.setAttr( aimObjectMatrix+'.worldSpaceOutput', 1 )
            cmds.connectAttr( aimObject+'.pim', aimObjectMatrix+'.parentInverseMatrix' )
            cmds.connectAttr( aimObjectMatrix+'.outTranslate', aimObject+'.t' )
            cmds.parent( aimObject, w=1 )
        
        return aimObject, aimObjectMatrix
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    second = sels[1]
    third  = None
    if len( sels ) > 2:
        third = sels[2]
    
    aimObject, aimObjectMatrix = createAimObjectCmd( first, second, third )
    
    cmds.setAttr( aimObjectMatrix+'.aimAxis', axisIndex )
    cmds.setAttr( aimObjectMatrix+'.inverseAim', inverseAim )
    cmds.setAttr( aimObject+'.dla', displayAxis )
    cmds.setAttr( aimObject+'.dh', displayAxis )
    
    if worldPosition:
        cmds.setAttr( aimObjectMatrix+'.worldSpaceOutput', 1 )
        cmds.connectAttr( aimObject+'.pim', aimObjectMatrix+'.parentInverseMatrix' )
        cmds.connectAttr( aimObjectMatrix+'.outTranslate', aimObject+'.t' )
        if not third: cmds.parent( aimObject, w=1 )
    
    return aimObject



def getDistanceAttribute( first, second ):
    
    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( second, ln='dist_orig', cb=1 )
    sgBFunction_attribute.addAttr( second, ln='dist_current', cb=1 )
    sgBFunction_attribute.addAttr( second, ln='dist_stretchValue', cb=1 )
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    mult = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( mult+'.op', 2 )
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( second+'.wim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.outputDistance', mult+'.input1X' )
    cmds.setAttr( mult+'.input2X', cmds.getAttr( mmdc+'.outputDistance' ) )
    cmds.connectAttr( mult+'.outputX', second+'.dist_stretchValue' )
    
    cmds.setAttr( second+'.dist_orig', cmds.getAttr( mmdc+'.outputDistance' ) )
    cmds.connectAttr( mmdc+'.outputDistance', second+'.dist_current' )



def createWristAngle( rotBase, target ):
    
    import sgBFunction_attribute

    targetP = cmds.listRelatives( target, p=1, f=1 )[0]
    
    mm = cmds.createNode( 'multMatrix' )
    wa = cmds.createNode( 'wristAngle' )
    
    cmds.connectAttr( rotBase+'.wm', mm+'.i[0]' )
    cmds.connectAttr( targetP+'.wim', mm+'.i[1]' )
    cmds.connectAttr( mm+'.matrixSum', wa+'.inputMatrix' )
    cmds.connectAttr( wa+'.outAngle', target+'.rx' )
    
    sgBFunction_attribute.addAttr( target, ln='wristAngle_Rate', cb=1, dv=1 )
    sgBFunction_attribute.addAttr( target, ln='wristAngle_Axis', cb=1, at='enum', el=':X:Y:Z' )
    cmds.connectAttr( target+'.wristAngle_Rate', wa+'.angleRate' )
    cmds.connectAttr( target+'.wristAngle_Axis', wa+'.axis' )




def addAngleDriverAttribute( sel ):
    
    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( sel, ln='angleRate0', cb=1 )
    sgBFunction_attribute.addAttr( sel, ln='angleRate1', cb=1 )
    sgBFunction_attribute.addAttr( sel, ln='angleRate2', cb=1 )
    
    if cmds.listConnections( sel, s=1, d=0, type='angleDriver' ): return None
    
    selP = cmds.listRelatives( sel, p=1, f=1 )[0]
    selName = sel.split( '|' )[-1]
    targetDriver = cmds.createNode( 'angleDriver', n= 'angleDriver_' + selName )
    mm = cmds.createNode( 'multMatrix', n='mm_' + selName )
    base = cmds.createNode( 'transform', n= 'angleBase_' + selName )

    base = cmds.parent( base, selP )[0]

    cmds.xform( base, ws=1, matrix= cmds.getAttr( sel+'.wm' ) )
    
    cmds.connectAttr( sel+'.wm', mm+'.i[0]' )
    cmds.connectAttr( base+'.wim', mm+'.i[1]' )
    cmds.connectAttr( mm+'.matrixSum', targetDriver+'.angleMatrix' )
        
    
    sgBFunction_attribute.addAttr( sel, ln='angleRate0', cb=1 )
    sgBFunction_attribute.addAttr( sel, ln='angleRate1', cb=1 )
    sgBFunction_attribute.addAttr( sel, ln='angleRate2', cb=1 )
    if not cmds.isConnected( targetDriver+'.outDriver0', sel+'.angleRate0' ):
        cmds.connectAttr( targetDriver+'.outDriver0', sel+'.angleRate0' )
    if not cmds.isConnected( targetDriver+'.outDriver1', sel+'.angleRate1' ):
        cmds.connectAttr( targetDriver+'.outDriver1', sel+'.angleRate1' )
    if not cmds.isConnected( targetDriver+'.outDriver2', sel+'.angleRate2' ):
        cmds.connectAttr( targetDriver+'.outDriver2', sel+'.angleRate2' )





def createSquashObject( distTarget, distBase, scaleTarget ):
    
    import sgBFunction_attribute
    import sgBFunction_base
    import math
    
    scaleTargetMtx = cmds.getAttr( scaleTarget+'.wm' )
    
    xVector = om.MVector( *scaleTargetMtx[0:3] )
    yVector = om.MVector( *scaleTargetMtx[4:4+3] )
    zVector = om.MVector( *scaleTargetMtx[8:8+3] )
    
    targetPos = cmds.xform( distTarget, q=1, ws=1, t=1 )
    basePos   = cmds.xform( distBase, q=1, ws=1, t=1 )
    aimVector = om.MVector( targetPos[0] - basePos[0], targetPos[1] - basePos[1], targetPos[2] - basePos[2] )
    
    vectors = [ xVector, yVector, zVector ]
    maxDotValue = 0
    aimIndex = 0
    for i in range( 3 ):
        dotValue = math.fabs( aimVector * vectors[i] )
        if dotValue > maxDotValue:
            maxDotValue = dotValue
            aimIndex = i

    print "max dot value : ", maxDotValue
    otherIndex1 = ( aimIndex + 1 ) % 3
    otherIndex2 = ( aimIndex + 2 ) % 3
        
    sgBFunction_base.autoLoadPlugin( 'sgLocusChRig' )
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( distTarget+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( distBase+'.wim', mmdc+'.i[1]' )
    
    sgBFunction_attribute.addAttr( scaleTarget, ln='distanceDefault', k=1 )
    sgBFunction_attribute.addAttr( scaleTarget, ln='distanceCurrent', cb=1 )
    sgBFunction_attribute.addAttr( scaleTarget, ln='squashRate', k=1 )
    sgBFunction_attribute.addAttr( scaleTarget, ln='forceScale', k=1 )
    
    cmds.connectAttr( mmdc+'.outputDistance', scaleTarget+'.distanceCurrent', f=1 )
    cmds.setAttr( scaleTarget+'.distanceDefault', cmds.getAttr( mmdc+'.outputDistance' ) )
    
    squashNode = cmds.createNode( 'squash' )
    divNode    = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( divNode+'.operation', 2 )
    
    cmds.connectAttr( scaleTarget+'.distanceDefault', squashNode+'.lengthOriginal' )
    cmds.connectAttr( scaleTarget+'.distanceCurrent', squashNode+'.lengthModify' )
    cmds.connectAttr( scaleTarget+'.distanceDefault', divNode+'.input2X' )
    cmds.connectAttr( scaleTarget+'.distanceCurrent', divNode+'.input1X' )
    
    axisChar = ['X', 'Y', 'Z' ]
    cmds.connectAttr( squashNode+'.output', scaleTarget+'.scale%s' % axisChar[ otherIndex1 ] )
    cmds.connectAttr( squashNode+'.output', scaleTarget+'.scale%s' % axisChar[ otherIndex2 ] )
    cmds.connectAttr( divNode+'.outputX', scaleTarget+'.scale%s' % axisChar[ aimIndex ] )
    
    cmds.connectAttr( scaleTarget+'.squashRate', squashNode+'.squashRate' )
    cmds.connectAttr( scaleTarget+'.forceScale', squashNode+'.forceValue' )



def resetSquashDistanceDefault():
    
    trs = cmds.ls( tr=1 )
    for tr in trs:
        if not cmds.attributeQuery( 'distanceCurrent', node=tr, ex=1 ): continue
        distCurrent = cmds.getAttr( tr+'.distanceCurrent' )
        cmds.setAttr( tr+'.distanceDefault', distCurrent )





def addModification( meshObjs ):
    
    import sgBFunction_attribute
    import sgBFunction_dag
    
    meshObjs = sgBFunction_dag.getChildrenMeshExists( meshObjs )
    softMod = cmds.deformer( meshObjs, type='softMod' )[0]
    
    ctlGrp = cmds.createNode( 'transform' )
    cmds.setAttr( ctlGrp+'.dh', 1 )
    dcmp   = cmds.createNode( 'decomposeMatrix' )
    ctl = cmds.sphere()[0]
    ctl = cmds.parent( ctl, ctlGrp )[0]
    sgBFunction_attribute.addAttr( ctl, ln='__________', at='enum', enumName = ':Modify Attr', cb=1 )
    sgBFunction_attribute.addAttr( ctl, ln='falloffRadius', min=0, dv=1, k=1 )
    sgBFunction_attribute.addAttr( ctl, ln='envelope', min=0, max=1, dv=1, k=1 )
    
    cmds.connectAttr( ctlGrp+'.wim', softMod+'.bindPreMatrix' )
    cmds.connectAttr( ctlGrp+'.wm', softMod+'.preMatrix' )
    cmds.connectAttr( ctl+'.wm', softMod+'.matrix' )
    cmds.connectAttr( ctl+'.m',  softMod+'.weightedMatrix' )
    
    cmds.connectAttr( ctlGrp+'.wm', dcmp+'.imat' )
    
    cmds.connectAttr( dcmp+'.ot', softMod+'.falloffCenter' )
    for i in range( len( meshObjs ) ):
        cmds.connectAttr( meshObjs[i]+'.wm', softMod+'.geomMatrix[%d]' % i )
    
    cmds.connectAttr( ctl+'.envelope', softMod+'.envelope' )
    cmds.connectAttr( ctl+'.falloffRadius', softMod+'.falloffRadius' )
    
    cmds.xform( ctlGrp, ws=1, t=cmds.getAttr( meshObjs[0]+'.wm' )[-4:-1] )
    cmds.select( ctlGrp )


def getMultMatrixAsParenting( childTarget, parentTarget ):
    
    mm = cmds.createNode( 'multMatrix' )
    cmds.connectAttr( childTarget+'.wm', mm+'.i[0]' )
    cmds.connectAttr( parentTarget+'.wim', mm+'.i[1]' )
    return mm



def createWristAngleJoints( orientObject ):

    import sgBFunction_dag

    orientObjP = sgBFunction_dag.getParent( orientObject )
    orientObjectName = orientObject.split( '|' )[-1]
    
    if cmds.nodeType( orientObject ) == 'joint':
        baseJointRad = cmds.getAttr( orientObject+'.radius' )
    else:
        baseJointRad = 1
    
    cmds.select( orientObjP )
    zJoint = cmds.joint( n = orientObjectName+'_waZ', radius = baseJointRad * 1.5 )
    yJoint = cmds.joint( n = orientObjectName+'_waY', radius = baseJointRad * 2.0 )
    xJoint = cmds.joint( n = orientObjectName+'_waX', radius = baseJointRad * 2.5 )
    
    waz = cmds.createNode( 'wristAngle', n='WA_Z_' + orientObjectName )
    way = cmds.createNode( 'wristAngle', n='WA_Y_' + orientObjectName )
    wax = cmds.createNode( 'wristAngle', n='WA_X_' + orientObjectName )
    
    cmds.connectAttr( orientObject+'.m', waz+'.inputMatrix' )
    cmds.setAttr( waz+'.axis', 2 )
    cmds.connectAttr( waz+'.outAngle', zJoint+'.rotateZ' )
    
    mm = getMultMatrixAsParenting( orientObject, zJoint )
    cmds.connectAttr( mm+'.o', way+'.inputMatrix' )
    cmds.setAttr( way+'.axis', 1 )
    cmds.connectAttr( way+'.outAngle', yJoint+'.rotateY' )
    
    mm = getMultMatrixAsParenting( orientObject, yJoint )
    cmds.connectAttr( mm+'.o', wax+'.inputMatrix' )
    cmds.setAttr( wax+'.axis', 0 )
    cmds.connectAttr( wax+'.outAngle', xJoint+'.rotateX' )