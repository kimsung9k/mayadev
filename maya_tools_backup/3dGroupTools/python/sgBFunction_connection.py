import maya.cmds as cmds
import maya.OpenMaya as om
import math




def constraint( first, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )






def constraintMaintainOffset( first, second ):
    
    secondPos = cmds.getAttr( second+'.wm' )
    
    offsetObj = cmds.createNode( 'transform' )
    cmds.xform( offsetObj, ws=1, matrix=secondPos )
    cmds.parent( offsetObj, first )
    
    mm = cmds.createNode( 'multMatrix' )
    dc = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( offsetObj+'.wm', mm+'.i[0]' )
    cmds.connectAttr( second+'.pim', mm+'.i[1]' )
    cmds.connectAttr( mm+'.o', dc+'.imat' )
    cmds.connectAttr( dc+'.ot', second+'.t' )
    cmds.connectAttr( dc+'.or', second+'.r' )






def constraintAll( first, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    cmds.connectAttr( mmdc+'.os', target+'.s' )
    cmds.connectAttr( mmdc+'.osh', target+'.sh' )
    if cmds.nodeType( target ) == 'joint':
        try:cmds.setAttr( target+'.jo', 0,0,0 )
        except:pass
        


def constraintPoint( first, second ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=second + '_mmdc' )
    cmds.connectAttr( first  + '.wm',  mmdc+'.i[0]' )
    cmds.connectAttr( second + '.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc + '.ot', second + '.t' )



def constraintOrient( first, second ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=second + '_mmdcOri' )
    cmds.connectAttr( first + '.wm', mmdc+'.i[0]' )
    cmds.connectAttr( second + '.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc + '.or', second + '.r' )




def replaceSourceConnection( first, second, nodeType=None ):
    
    if nodeType:
        fSrcCons = cmds.listConnections( first, s=1, d=0, p=1, c=1, type=nodeType )
    else:
        fSrcCons = cmds.listConnections( first, s=1, d=0, p=1, c=1 )
    
    if fSrcCons:
        outputs = fSrcCons[1::2]
        inputs  = fSrcCons[::2]
        
        for i in range( len( outputs ) ):
            inputTarget= inputs[i].replace( first, second )
            if cmds.nodeType( first ) == 'joint' and cmds.nodeType( second ) =='transform':
                inputTarget = inputTarget.replace( 'jointOrient', 'rotate' )
            try:
                cmds.connectAttr( outputs[i], inputTarget, f=1 )
                cmds.disconnectAttr( outputs[i], inputs[i] )
            except: pass



def replaceDestConnection( first, second, nodeType=None ):
    
    if nodeType:
        fDesCons = cmds.listConnections( first, s=0, d=1, p=1, c=1, type=nodeType )
    else:
        fDesCons = cmds.listConnections( first, s=0, d=1, p=1, c=1 )
    
    if fDesCons:
        outputs = fDesCons[::2]
        inputs  = fDesCons[1::2]
        
        for i in range( len( outputs ) ):
            try:
                cmds.connectAttr( outputs[i].replace( first, second ), inputs[i], f=1 )
                cmds.disconnectAttr( outputs[i], inputs[i] )
            except:pass





def replaceConnection( first, second, nodeType=None ):
    
    replaceSourceConnection( first, second, nodeType )
    replaceDestConnection( first, second, nodeType )



    


def getSourceConnection( src, trg ):

    src = cmds.ls( src )[0]
    trg = cmds.ls( trg )[0]
    cons = cmds.listConnections( src, s=1, d=0, p=1, c=1 )

    if not cons: return None

    srcCons  = cons[1::2]
    destCons = cons[::2]

    for i in range( len( srcCons ) ):
        srcCon = srcCons[i]
        destCon = destCons[i].replace( src, trg )

        if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
            destCon = destCon.replace( 'jointOrient', 'rotate' )

        if not cmds.ls( destCon ): continue

        if not cmds.isConnected( srcCon, destCon ):
            cmds.connectAttr( srcCon, destCon, f=1 )





def disconnectSourceConnection( target ):
    
    cons = cmds.listConnections( target, s=1, d=0, p=1, c=1 )
    
    srcCons  = cons[1::2]
    destCons = cons[::2]
    
    for i in range( len( srcCons ) ):
        cmds.disconnectAttr( srcCons[i], destCons[i] )





def ctlVisConnection( ctl, targets, attrName = 'ctlVis' ):

    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( ctl, ln=attrName, min=0, max=1, at='long', k=1 )
        
    for target in targets:
        targetP = cmds.listRelatives( target, p=1, f=1 )[0]
        
        if not cmds.isConnected( ctl+'.'+attrName, target+'.v' ):
            try:
                cmds.connectAttr( ctl+'.'+attrName, target+'.v' )
            except:
                if not cmds.isConnected( ctl+'.'+attrName, targetP+'.v' ):
                    try:cmds.connectAttr( ctl+'.'+attrName, targetP+'.v' )
                    except:pass




def bindConnect( targets, jnt ):

    import sgBFunction_dag
    import sgBModel_data
    import sgBFunction_attribute
    import sgBFunction_convert
    
    targets = sgBFunction_convert.singleToList( targets )
    
    def getBindConnectObjectDcmp( jnt ):
        sgBFunction_attribute.addAttr( jnt, ln='bindConnectObject', at='message' ) 
        
        cons = cmds.listConnections( jnt+'.bindConnectObject', d=1, s=0 )
        if not cons:
            bindConnectObject = cmds.createNode( 'transform', n= 'BindCObj_' + jnt )
            sgBFunction_attribute.addAttr( bindConnectObject, ln='bindConnectObject_target', at='message' )
            cmds.connectAttr( jnt+'.bindConnectObject', bindConnectObject+'.bindConnectObject_target' )
            cmds.parent( bindConnectObject, jnt )
        else:
            bindConnectObject = cons[0]
        
        cons = cmds.listConnections( bindConnectObject+'.wm', type='decomposeMatrix' )
        if not cons:
            dcmp = cmds.createNode( 'decomposeMatrix' )
            cmds.connectAttr( bindConnectObject+'.wm', dcmp+'.imat' )
        else:
            dcmp = cons[0]
        
        cmds.xform( bindConnectObject, ws=1, matrix=sgBModel_data.getDefaultMatrix() )
        return dcmp
        
    
    dcmp = getBindConnectObjectDcmp( jnt )
    
    for target in targets:
        cmds.connectAttr( dcmp+'.ot', target+'.t' )
        cmds.connectAttr( dcmp+'.or', target+'.r' )
        cmds.connectAttr( dcmp+'.os', target+'.s' )
        cmds.connectAttr( dcmp+'.osh', target+'.sh' )



def getAttrSourceConnection( attr ):
    
    cons = cmds.listConnections( attr, s=1, d=0, p=1, c=1 )
    if cons: return cons
    
    import sgBFunction_dag
    node, attr = attr.split( '.' )
    
    fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( node ) )
    plugAttr = fnNode.findPlug( attr )
    
    try:
        numChildren = plugAttr.numChildren()
    except:
        return []
    
    cons = []
    for i in range( numChildren ):
        cPlugAttr = plugAttr.child( i )
        attrName = om.MFnAttribute( cPlugAttr.attribute() ).name()
        cons += getAttrSourceConnection( node+'.'+attrName )
    return cons




def aimConstraintByAimObjectMatrix( aimTarget, constTarget, autoAxis=True, maintainOffset=False, createUp=False, lookAt=False, axisIndex=0, *args ):
    
    import sgBFunction_convert
    import sgBFunction_position
    
    def createAimObject( aimTarget, upObject, constTarget ):
    
        aimObjectMatrix = cmds.createNode( 'aimObjectMatrix' )
        cmds.connectAttr( aimTarget+'.wm', aimObjectMatrix+'.targetMatrix' )
        cmds.connectAttr( upObject+'.wm', aimObjectMatrix+'.baseMatrix' )
        
        if cmds.nodeType( constTarget ) == 'joint':
            try: cmds.setAttr( constTarget+'.jo', 0,0,0 )
            except:pass
        
        cmds.connectAttr( aimObjectMatrix+'.outRotate', constTarget+'.r', f=1 )
        cmds.setAttr( aimObjectMatrix+'.worldSpaceOutput', 1 )
        cmds.connectAttr( constTarget+'.pim', aimObjectMatrix+'.parentInverseMatrix', f=1 )
        cons = getAttrSourceConnection( constTarget+'.t' )
        if cons:
            for i in range( 0, len( cons ), 2 ):
                outputCon = cons[i+1]
                inputCon  = upObject + '.' + cons[i+0].split( '.' )[-1]
                cmds.connectAttr( outputCon, inputCon )
                cmds.disconnectAttr( cons[i+1], cons[i] )

        cmds.connectAttr( aimObjectMatrix+'.outTranslate', constTarget+'.t', f=1 )
        
        return aimObjectMatrix
    
    upObject = cmds.listRelatives( constTarget, p=1, f=1 )
    if not upObject:
        createUp = True
    else:
        upObject = upObject[0]
    
    if createUp:
        constName = constTarget.split( '|' )[-1]
        upObject = cmds.createNode( 'transform', n= constName + '_upObject' )
        constTargetP = cmds.listRelatives( constTarget, p=1, f=1 )
        if constTargetP:
            upObject = cmds.parent( upObject, constTargetP[0] )[0]
        cmds.xform( upObject, ws=1, matrix= cmds.getAttr( constTarget+'.wm' ) )
        
    if autoAxis:
        axisIndex = sgBFunction_position.getAimIndex( aimTarget, constTarget )

    inverseAim = False
    if axisIndex > 2:
        inverseAim = True
    else:
        inverseAim = False

    if lookAt and autoAxis:
        sgBFunction_position.lookAt( aimTarget, upObject )
    elif lookAt:
        sgBFunction_position.lookAt( aimTarget, upObject, axisIndex )

    mtxBefore = cmds.getAttr( constTarget+'.wm' )

    aimObjectMatrixNode = createAimObject( aimTarget, upObject, constTarget )
    cmds.setAttr( aimObjectMatrixNode +'.aimAxis', axisIndex%3 )
    cmds.setAttr( aimObjectMatrixNode +'.inverseAim', inverseAim )
    
    mtxAfter = cmds.getAttr( constTarget+'.wm' )
    
    if maintainOffset:
        mmtxBefore = sgBFunction_convert.convertMatrixToMMatrix( mtxBefore )
        mmtxAfter  = sgBFunction_convert.convertMatrixToMMatrix( mtxAfter )
    
        offsetMtx = mmtxBefore * mmtxAfter.inverse()
        
        trMtx = om.MTransformationMatrix( offsetMtx )
        vRot = trMtx.eulerRotation().asVector()
        
        cmds.setAttr( aimObjectMatrixNode + '.offsetX', math.degrees( vRot.x ) )
        cmds.setAttr( aimObjectMatrixNode + '.offsetY', math.degrees( vRot.y ) )
        cmds.setAttr( aimObjectMatrixNode + '.offsetZ', math.degrees( vRot.z ) )



def separateParentConnection( node, attr ):
    
    parentAttr = cmds.attributeQuery( attr, node=node, listParent=1 )
    
    if parentAttr:
        cons = cmds.listConnections( node+'.'+parentAttr[0], s=1, d=0, p=1, c=1 )
        if cons:
            cmds.disconnectAttr( cons[1], cons[0] )
            srcAttr = cons[1]
            srcNode, srcParentAttr = srcAttr.split( '.' )
            srcAttrs = cmds.attributeQuery( srcParentAttr, node=srcNode, listChildren=1 )
            dstAttrs = cmds.attributeQuery( parentAttr[0], node=node,    listChildren=1 )
            for i in range( len( srcAttrs ) ):
                if cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i] ): continue
                cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i], f=1 )




def addMultDoubleLinearConnection( sel, attr ):
    import sgBFunction_attribute
    newAttrName = 'mult_' + attr
    sgBFunction_attribute.addAttr( sel, ln=newAttrName, cb=1, dv=1 )
    multDouble = cmds.createNode( 'multDoubleLinear' )
    
    separateParentConnection( sel, attr )
    
    cons = cmds.listConnections( sel + '.' + attr, s=1, d=0, p=1, c=1 )
    cmds.connectAttr( cons[1], multDouble+'.input1' )
    cmds.connectAttr( sel+'.'+newAttrName, multDouble + '.input2' )
    cmds.connectAttr( multDouble + '.output', sel+'.'+attr, f=1 )




def convertConnectionAsAnimCurve( node, attr ):
    
    separateParentConnection( node, attr )
          
    cons = cmds.listConnections( node+'.'+attr, s=1, d=0, p=1, c=1 )
    if not cons: return None
    
    attrType = cmds.attributeQuery( attr, node= node, attributeType=1 )
    
    if attrType == 'doubleLinear':
        animCurveType= 'animCurveUL'
    elif attrType == 'doubleAngle':
        animCurveType = 'animCurveUA'
    else:
        animCurveType = 'animCurveUU'
    
    animCurve = cmds.createNode( animCurveType )
    cmds.connectAttr( cons[1], animCurve+'.input' )
    cmds.connectAttr( animCurve+'.output', cons[0], f=1 )
    
    cmds.setKeyframe( animCurve, f= -1, v= -1 )
    cmds.setKeyframe( animCurve, f=-.5, v=-.5 )
    cmds.setKeyframe( animCurve, f=  0, v=  0 )
    cmds.setKeyframe( animCurve, f= .5, v= .5 )
    cmds.setKeyframe( animCurve, f=  1, v=  1 )
    
    cmds.setAttr( animCurve + ".postInfinity", 1 )
    cmds.setAttr( animCurve + ".preInfinity", 1 )
    
    cmds.selectKey( animCurve )
    cmds.keyTangent( itt='spline', ott='spline' )
    
    return animCurve



def copyShader( first, second ):
    
    import sgModelDag
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    first = sgModelDag.getTransform( first )
    second = sgModelDag.getTransform( second )
    firstShape = sgModelDag.getShape( first )
    secondShape = sgModelDag.getShape( second )
    
    engines = cmds.listConnections( firstShape, type='shadingEngine' )
    
    if not engines: return None
    
    engines = list( set( engines ) )
    
    for engine in engines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shaders: continue
        shader = shaders[0]
        cmds.hyperShade( objects = shader )
        selObjs = cmds.ls( sl=1, l=1 )
        
        targetObjs = []
        for selObj in selObjs:
            if selObj.find( '.' ) != -1:
                trNode, components = selObj.split( '.' )
                if trNode == first:
                    targetObjs.append( second+'.'+components )
            elif selObj == firstShape:
                targetObjs.append( secondShape )
        
        if not targetObjs: continue
        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine )



def duplicateShaderToOther( first, second ):
    
    import maya.mel as mel
    import sgBFunction_dag
    
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    first = sgBFunction_dag.getTransform( first )
    second = sgBFunction_dag.getTransform( second )
    firstShape = sgBFunction_dag.getShape( first )
    secondShape = sgBFunction_dag.getShape( second )
    
    engines = cmds.listConnections( firstShape, type='shadingEngine' )
    
    if not engines: return None
    
    engines = list( set( engines ) )
    
    for engine in engines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        
        engine = cmds.duplicate( engine, n= 'du_'+engine )[0]
        
        if shaders:
            shader = shaders[0]
            
            cmds.hyperShade( objects = shader )
            selObjs = cmds.ls( sl=1, l=1 )
            
            targetObjs = []
            for selObj in selObjs:
                if selObj.find( '.' ) != -1:
                    trNode, components = selObj.split( '.' )
                    if trNode == first:
                        targetObjs.append( second+'.'+components )
                elif selObj == firstShape:
                    targetObjs.append( secondShape )
            
            cmds.select( shader )
            mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "duplicateShadingNetwork")' )
            shader = cmds.ls( sl=1 )[0]
            cmds.connectAttr( shader+'.outColor', engine+'.surfaceShader' )
        
        aiShaders = cmds.listConnections( engine+'.aiSurfaceShader', s=1, d=0 )

        if aiShaders:
            aiShader = aiShaders[0]
            
            cmds.hyperShade( objects = aiShader )
            selObjs = cmds.ls( sl=1, l=1 )
            
            cmds.select( aiShader )
            mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "duplicateShadingNetwork")' )
            aiShader = cmds.ls( sl=1 )[0]
            cmds.connectAttr( aiShader+'.outColor', engine+'.aiSurfaceShader' )
        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine )


def copyShaderHierarchy( firstTopObj, secondTopObj, topObjName = None ):
    
    replaceName = secondTopObj.replace( firstTopObj, '^' )
    
    if not topObjName:
        targetIsSecond = False
        if replaceName == secondTopObj:
            replaceName = firstTopObj.replace( secondTopObj, '^' )
            targetIsSecond = True
        
        if targetIsSecond:
            secondShapes = cmds.listRelatives( secondTopObj, c=1, ad=1, type='shape', f=1 )
            for shape in secondShapes:
                second = cmds.listRelatives( shape, p=1 )[0]
                first = replaceName.replace( '^', second )
                if not cmds.objExists( second ): continue
                copyShader( first, second )
        else:
            firstShapes = cmds.listRelatives( firstTopObj, c=1, ad=1, type='shape', f=1 )
            for shape in firstShapes:
                first = cmds.listRelatives( shape, p=1 )[0]
                second = replaceName.replace( '^', first )
                if not cmds.objExists( second ): continue
                copyShader( first, second )
    else:
        firstNs = firstTopObj.replace( topObjName, '' )
        secondNs = secondTopObj.replace( topObjName, '' )
        
        firstChildren = cmds.listRelatives( firstTopObj, c=1, ad=1 )
        for i in range( len( firstChildren ) ):
            firstChild = firstChildren[i]
            secondChild = firstChild.replace( firstNs, secondNs )
            
            copyShader( firstChild, secondChild )
            
            