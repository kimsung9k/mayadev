import maya.cmds as cmds
import sgModelDg, sgRigDag
import sgRigConnection
import sgRigAttribute
import sgRigCurve
import sgModelDag



def addControllerToBag( bagObject ):
    
    PBagObject = cmds.listRelatives( bagObject, p=1 )[0]

    bagObject, PivBagObject = sgRigDag.addParent( bagObject, 'Piv' )
    cmds.setAttr( bagObject+'.ty',    -0.16 )
    cmds.setAttr( PivBagObject+'.ty',  0.16 )
    
    cons = cmds.listConnections( bagObject, s=1, d=0, type='animCurve' )
    if cons: cmds.delete( cons )

    mainCtl = cmds.circle( n='Ctl_' + bagObject, normal=[0,0,1], center=[0,0,1.4] )[0]
    mainCtl, pmainCtl = sgRigDag.addParent( mainCtl )
    mainCtl, omainCtl  = sgRigDag.addParent( mainCtl )
    cmds.setAttr( mainCtl+'.overrideEnabled', 1 )
    cmds.setAttr( mainCtl+'.overrideColor', 6 )
    
    cmds.setAttr( omainCtl+'.ty', 0.16 )
    
    pointDCtl    = [[0.0, 0.53619110199777498, -0.080351999999999979], 
                    [0.0, 0.53619110199777498, -0.16070399999999996], 
                    [0.0, 0.73851681927679846, 0.0], 
                    [0.0, 0.53619110199777498, 0.16071360000000001], 
                    [0.0, 0.53619110199777498, 0.080356800000000006], 
                    [0.0, -0.53616508520269901, 0.080356800000000117], 
                    [1.1102230246251568e-16, -0.53616508520269901, 0.16071360000000018], 
                    [0.0, -0.73851215501375644, 0.0], 
                    [0.0, -0.53616508520269901, -0.1607039999999999], 
                    [-1.1102230246251568e-16, -0.53616508520269901, -0.080351999999999923], 
                    [0.0, 0.53619110199777498, -0.080351999999999979], 
                    [0.0, 0.53619110199777498, -0.080351999999999979]]
    
    dCtl = cmds.curve( n='Ctl_DirObj_'+bagObject, p=pointDCtl, d=1 )
    cmds.setAttr( dCtl+'.overrideEnabled', 1 )
    cmds.setAttr( dCtl+'.overrideColor', 18 )
    dCtlChild = sgRigDag.addChild( dCtl )
    dCtl, PdCtl = sgRigDag.addParent( dCtl )
    
    shakeObject = sgRigDag.addChild( mainCtl )
    shakeObject, pshakeObject = sgRigDag.addParent( shakeObject )
    cshakeObject = sgRigDag.addChild( shakeObject )
    
    sgRigConnection.constraint( PdCtl, dCtlChild )
    sgRigConnection.constraintAll( mainCtl, PdCtl )
    sgRigConnection.constraint( PBagObject, pmainCtl )
    sgRigConnection.constraintAll( cshakeObject, PivBagObject )
    
    sgRigConnection.constraint( dCtl, pshakeObject )
    cmds.connectAttr( dCtlChild+'.r', cshakeObject+'.r')
    
    sgRigAttribute.addAttr( mainCtl, ln='globalShake', k=1, dv=1 )
    sgRigAttribute.addAttr( mainCtl, ln='globalTimeMult', k=1, dv=1 )
    sgRigAttribute.addAttr( mainCtl, ln='globalOffset', k=1 )
    sgRigAttribute.addAttr( mainCtl, ln='shake', k=1, dv=1 )
    sgRigAttribute.addAttr( mainCtl, ln='timeMult', k=1, dv=1 )
    sgRigAttribute.addAttr( mainCtl, ln='offset', k=1 )
    sgRigAttribute.addAttr( mainCtl, ln='showBag', at='long', k=1, min=0, max=1, dv=1 )
    
    mdForTime1 = cmds.createNode( 'multDoubleLinear' )
    mdForTime2 = cmds.createNode( 'multDoubleLinear' )
    mdForShake1 = cmds.createNode( 'multDoubleLinear' )
    mdForShake2 = cmds.createNode( 'multDoubleLinear' )
    addForOfs1 = cmds.createNode( 'addDoubleLinear' )
    addForOfs2 = cmds.createNode( 'addDoubleLinear' )
    animCurve = sgModelDg.getRoofSineCurve( 0, 10, -10, 10 )
    
    cmds.connectAttr( mainCtl+'.globalTimeMult', mdForTime1+'.input1' )
    cmds.connectAttr( mainCtl+'.timeMult',       mdForTime1+'.input2' )
    cmds.connectAttr( mdForTime1+'.output', mdForTime2+'.input1' )
    cmds.connectAttr( 'time1.outTime',      mdForTime2+'.input2' )
    cmds.connectAttr( mainCtl+'.globalOffset', addForOfs1+'.input1' )
    cmds.connectAttr( mainCtl+'.offset', addForOfs1+'.input2' )
    cmds.connectAttr( addForOfs1+'.output', addForOfs2+'.input1' )
    cmds.connectAttr( mdForTime2+'.output', addForOfs2+'.input2' )
    cmds.connectAttr( addForOfs2+'.output', animCurve+'.input' )
    cmds.connectAttr( mainCtl+'.globalShake', mdForShake1+'.input1' )
    cmds.connectAttr( mainCtl+'.shake', mdForShake1+'.input2' )
    cmds.connectAttr( mdForShake1+'.output', mdForShake2+'.input1' )
    cmds.connectAttr( animCurve+'.output', mdForShake2+'.input2' )
    cmds.connectAttr( mainCtl+'.showBag', bagObject+'.v' )
    
    cmds.connectAttr( mdForShake2+'.output', shakeObject+'.rx' )
    
    cmds.setAttr( mainCtl+'.v', e=1, lock=1 )




def addCacheAttr( sels ):
    
    attrName = 'cacheAttr'
    index= 0
    for sel in sels:
        sel = cmds.rename( sel, 'riceType_%02d' % index )
        sgRigAttribute.addAttr( sel, ln=attrName, at='long', dv=index )
        index += 1




def makeFile( fileName, data =None ):
    
    import sgFunctionFileAndPath
    path = 'D:/makeFile/' + fileName + '.txt'
    sgFunctionFileAndPath.makeFile( path )
    
    if data:
        f = open( path, 'w' )
        f.write( data )
        f.close()




def addWobbleDeform( mainCtl, targets ):
  
    import math
    if not type( targets ) in [ type(()), type([]) ]:
        targets = [targets]

    failedTargets = []
    for target in targets:
        vtxList = cmds.ls( target+'.vtx[*]', fl=1 )
        topVtxPos = [0,0,0]
        bottomVtxPos = [0,10000,0]
        for vtx in vtxList:
            pos = cmds.xform( vtx, q=1, ws=1, t=1 )
            if math.fabs( pos[1] ) > math.fabs( topVtxPos[1] ):
                topVtxPos = pos
            if math.fabs( pos[1] ) < math.fabs( bottomVtxPos[1] ):
                bottomVtxPos = pos
        
        if( (topVtxPos[0]-bottomVtxPos[0])**2 + (topVtxPos[1]-bottomVtxPos[1])**2 + (topVtxPos[2]-bottomVtxPos[2])**2 ) < 0.001:
            failedTargets.append( target )
            continue 
        crv = cmds.curve( p=[bottomVtxPos,topVtxPos], d=1 )
        cmds.rebuildCurve( crv, ch=0, d=3, s=10 )
        
        sgRigCurve.createSgWobbleCurve( crv, False )
        
        copyAttrs = [ 'globalEnvelope', 'globalTimeMult', 'globalOffset' ]
        
        for copyAttr in copyAttrs:
            sgRigAttribute.copyAttribute( crv+'.'+copyAttr, mainCtl )
            cmds.connectAttr( mainCtl+'.'+copyAttr, crv+'.'+copyAttr )

        wire = cmds.deformer( target, type='wire' )[0]
        crvOrig = sgModelDag.getOrigShape( crv )
        crvShape= sgModelDag.getShape( crv )

        cmds.connectAttr( crvOrig+'.local', wire+'.baseWire[0]' )
        cmds.connectAttr( crvShape+'.local', wire+'.deformedWire[0]' )

        cmds.setAttr( wire+'.rotation', 0.2 )
        cmds.setAttr( wire+'.dropoffDistance[0]', 10 )
    
    return failedTargets





def getSurfaceColorValue( crv, surf ):
    
    import sgFunctionDag
    
    crvPoint = cmds.xform( crv+'.cv[0]', q=1, ws=1, t=1 )
    value = sgFunctionDag.getSurfaceColorValues( crvPoint, surf )[0]
    
    return value





def importCache( targets, cacheFolderPath ):
    
    import sgFunctionCache
    import random
    
    for target in targets:
        target = sgModelDag.getTransform( target )
        attrNum = cmds.getAttr( target+'.cacheAttr' )
        
        xmlFileName = 'riceType_%02dShape.xml' % ( attrNum )
        xmlFilePath = cacheFolderPath + '/' + xmlFileName
        
        animCurve = sgModelDg.getRoofLinearCurve( 1, 32, 1, 32 )
        addNode = cmds.createNode( 'addDoubleLinear' )
        sgFunctionCache.importCache( target, xmlFilePath )

        time1 = sgModelDag.getNodeFromHistory( target, 'time' )[0]
        cacheFile = sgModelDag.getNodeFromHistory( target, 'cacheFile' )[0]
        
        sgRigAttribute.addAttr( target, ln='cacheOffset', k=1, dv=random.uniform( 1, 32 ) )
        
        cmds.connectAttr( time1+'.outTime', addNode+'.input1' )
        cmds.connectAttr( target+'.cacheOffset', addNode+'.input2' )
        cmds.connectAttr( addNode+'.output', animCurve+'.input' )
        cmds.connectAttr( animCurve+'.output', cacheFile+'.time', f=1 )




def addHairDeformToBag( bag, controller ):
    
    startVtxIndex = 40
    endVtxIndex   = 105
    
    pBag = cmds.listRelatives( bag, p=1,f=1 )[0]
    
    cons = cmds.listConnections( pBag, type='multMatrixDecompose',s=1, d=0 )
    
    if not cons: return None
    
    mmdc = cons[0]
    cons = cmds.listConnections( mmdc+'.i[0]', s=1, d=0 )
    
    if not cons: return None
    
    constObj = cons[0]
    
    constObj
    cmds.select( constObj )
    jnt = cmds.joint()
    
    startPos = cmds.xform( bag+'.vtx[%d]' % startVtxIndex, q=1, ws=1, t=1 )
    endPos   = cmds.xform( bag+'.vtx[%d]' % endVtxIndex, q=1, ws=1, t=1 )
    
    crv = cmds.curve( p=[startPos, endPos], d=1 )
    cmds.rebuildCurve( crv, ch=0, d=3, s=7 )
    
    cmds.skinCluster( [crv, jnt] )
    
    import sgRigCurve
    hairSystem = sgRigCurve.makeDynamicCurveKeepSrc( [crv], 'dynamic_' )
    
    sgRigAttribute.connectHairAttribute( controller, hairSystem )
    
    cmds.select( crv )
    handle, jnts = sgRigCurve.createJointOnEachCurve( crv, 7, False )
    
    topJnt = jnts[0]
    cmds.parent( handle, topJnt, constObj )
    
    jnts.append( bag )
    cmds.parent( bag, w=1 )
    cmds.skinCluster( jnts )




def pfxhairDynamicSetting( hairSystems, skinMesh ):

    startCurvesAll = []
    for hairSystem in hairSystems:
        hairSystemShape = cmds.listRelatives( hairSystem, s=1 )[0]
        follicles = cmds.listConnections( hairSystemShape+'.inputHair', s=1, d=0, type='follicle', shapes=1 )
        startCurves = cmds.listConnections( follicles, s=1, d=0, type='nurbsCurve' )
        
        startCurvesShapes = cmds.listRelatives( startCurves, s=1, f=1 )
        
        for shape in startCurvesShapes:
            cons = cmds.listConnections( shape, d=1, s=0, shapes=1 )
            if not cons: 
                cmds.delete( shape )
                continue
            if cmds.nodeType( cons[0] ) == 'follicle':
                cmds.setAttr( shape+'.io', 1 )
        
        startCurvesAll += startCurves
    
    grp = cmds.group( startCurvesAll, n='startCurveGrps' )
    
    startCurvesAll = cmds.listRelatives( grp, c=1, type='transform', f=1 )
    
    import sgRigSkinCluster
    
    for curve in startCurvesAll:
        sgRigSkinCluster.autoCopyWeight( skinMesh, curve )
    
    return grp
        



def setRestCurve( startCurves ):
    
    restCurves = []
    index = 0
    for startCurve in startCurves:
        
        follicle = cmds.listConnections( startCurve+'.wm', type='follicle', shapes=1 )[0]
        
        if cmds.listConnections( follicle+'.restPosition', s=1, d=0 ): continue
        
        startShape = cmds.listConnections( follicle+'.startPosition', s=1, d=0, shapes=1 )[0]
        
        rebuildCurve= cmds.listConnections( startShape+'.create', type='rebuildCurve' )[0]
        
        crvShape = cmds.createNode( 'nurbsCurve' )
        cmds.connectAttr( rebuildCurve+'.outputCurve', crvShape+'.create' )
        cmds.connectAttr( crvShape+'.worldSpace', follicle+'.restPosition' )
        cmds.setAttr( crvShape+'.io', 1 )
        
        crv = cmds.listRelatives( crvShape, p=1 )[0]
        crv = cmds.rename( crv, 'restCurve_%03d' % index )
        
        startMtx = cmds.getAttr( crv+'.wm' )
        cmds.xform( crv, ws=1, matrix=  startMtx )
        
        restCurves.append( crv )
        index += 1
    
    cmds.group( restCurves, n='restCurveGrps' )




def connectVisibilty( ctl, mesh, outputCurves, pfxHairs ):
    
    sgRigAttribute.addAttr( ctl, ln='meshVis', at='long', min=0, max=1, cb=1 )
    sgRigAttribute.addAttr( ctl, ln='outputCurves', at='long', min=0, max=1, cb=1 )
    sgRigAttribute.addAttr( ctl, ln='pfxHairs', at='long', min=0, max=1, cb=1 )
    
    sgRigConnection.connectAttrCommon( ctl+'.meshVis',      mesh+'.v' )
    sgRigConnection.connectAttrCommon( ctl+'.outputCurves', outputCurves+'.v' )
    sgRigConnection.connectAttrCommon( ctl+'.pfxHairs',     pfxHairs+'.v' )




def selectRebuildCurve( startCurves ):
    
    rebuildCurves = []
    
    for startCurve in startCurves:
        folicle = cmds.listConnections( startCurve+'.wm', type='follicle', shapes=1 )[0]
        startCurveShape = cmds.listConnections( folicle+'.startPosition', s=1, d=0, shapes=1 )[0]
        
        rebuildCurve = cmds.listConnections( startCurveShape, type='rebuildCurve', s=1, d=0 )[0]
        rebuildCurves.append( rebuildCurve )
    
    cmds.select( rebuildCurves )





def setCurveAsStatic( currentCurves ):
    
    for currentCurve in currentCurves:
        follicle = cmds.listConnections( currentCurve+'.create', type='follicle', shapes=1 )[0]
        
        cmds.setAttr( follicle+'.simulationMethod', 0 )





def pfxHairScaleConnect( ctl, hairSystemGrp ):
    
    hairSystems = cmds.listRelatives( hairSystemGrp, c=1, ad=1, type='hairSystem' )
    
    def getMultDoubleLinear( attr ):
        multNodes = cmds.listConnections( attr, type='multDoubleLinear', s=1, d=0 )
        if not multNodes:
            multNode = cmds.createNode( 'multDoubleLinear' )
            sgRigAttribute.addAttr( multNode, ln='clumpWidthMult', at='message' )
            attrValue = cmds.getAttr( attr )
            cmds.setAttr( multNode+'.input1', attrValue )
            cmds.connectAttr( multNode+'.output', attr )
            return multNode
        else:
            if not cmds.attributeQuery( 'clumpWidthMult', node=multNodes[0], ex=1 ):
                multNode = cmds.createNode( 'multDoubleLinear' )
                sgRigAttribute.addAttr( multNode, ln='clumpWidthMult', at='message' )
                attrValue = cmds.getAttr( attr )
                cmds.setAttr( multNode+'.input1', attrValue )
                cmds.connectAttr( multNode+'.output', attr )
                return multNode
            else:
                return multNodes[0]
                
    
    for hairSystem in hairSystems:
        dcmp = cmds.createNode( 'decomposeMatrix' )
        multNode = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( ctl+'.wm', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.osx', multNode+'.input1' )
        cmds.setAttr( multNode+'.input2', cmds.getAttr( hairSystem+'.clumpWidth' ) )
        cmds.connectAttr( multNode+'.output', hairSystem+'.clumpWidth' )
        
        