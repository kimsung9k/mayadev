import pymel.core
from maya import cmds
from maya import OpenMaya



mocParentOrder = {
        'root' : None,
        'spines' : 'root',
        'chest' : 'spines',
        'neck' : 'chest',
        'head' : 'neck',
        'headEnd' : 'head',
        
        'hip_L_' : 'root',
        'knee_L_' : 'hip_L_',
        'ankle_L_' : 'knee_L_',
        'ball_L_' : 'ankle_L_',
        'ballEnd_L_' : 'ball_L_',
        
        'clevicle_L_' : 'chest',
        'shoulder_L_' : 'clevicle_L_',
        'elbow_L_' : 'shoulder_L_',
        'wrist_L_' : 'elbow_L_',
        
        'thumb_L_' : 'wrist_L_',
        'index_L_' : 'wrist_L_',
        'middle_L_' : 'wrist_L_',
        'ring_L_' : 'wrist_L_',
        'pinky_L_' : 'wrist_L_',
        
        'hip_R_' : 'root',
        'knee_R_' : 'hip_R_',
        'ankle_R_' : 'knee_R_',
        'ball_R_'  : 'ankle_R_',
        'ballEnd_R_'  : 'ball_R_',
        
        'clevicle_R_' : 'chest',
        'shoulder_R_' : 'clevicle_R_',
        'elbow_R_' : 'shoulder_R_',
        'wrist_R_' : 'elbow_R_',
        
        'thumb_R_' : 'wrist_R_',
        'index_R_' : 'wrist_R_',
        'middle_R_' : 'wrist_R_',
        'ring_R_' : 'wrist_R_',
        'pinky_R_' : 'wrist_R_'
    }


def createMocapJoints( mocCreateDict ):
    
    items = mocCreateDict.items()
    
    mocJntDict = {}
    mocJnts = []
    originalJoints = []
    
    for key, value in items:
        if key == 'meshs': continue
        cmds.select( d=1 )
        if type( value ) == list:
            mocJntList = []
            for i in range( len( value ) ):
                if not cmds.objExists( value[i] ): 
                    print "%s is not exists" % value[i]
                    continue
                if cmds.objExists( 'MOCJNT_%s_%d' %( key, i ) ): continue
                mocJnt = cmds.joint( n= 'MOCJNT_%s_%d' %( key, i ) )
                cmds.xform( mocJnt, ws=1, matrix=cmds.getAttr( value[i] + '.wm' ) )
                originalJoints.append( value[i] )
                mocJntList.append( mocJnt )
                mocJnts.append( mocJnt )
            mocJntDict.update( { key:mocJntList} )
        else:
            if not cmds.objExists( value ): continue
            if cmds.objExists( 'MOCJNT_%s' % key ): continue
            mocJnt = cmds.createNode( 'joint', n='MOCJNT_%s' % key )
            cmds.xform( mocJnt, ws=1, matrix=cmds.getAttr( value + '.wm' ) )
            originalJoints.append( value )
            mocJntDict.update( {key:mocJnt} )
            mocJnts.append( mocJnt )

    for key, value in mocParentOrder.items():
        if not value: continue
        if not mocJntDict.has_key( key ): continue
        target  = mocJntDict[ key ]
        if not target: continue
        pTarget = mocJntDict[ value ]
        if type( pTarget ) == list:
            pTarget = pTarget[-1]
        try:
            if type( target ) == list:
                cmds.parent( target[0], pTarget )
            else:
                cmds.parent( target, pTarget )
        except:
            pass
    
    import math
    
    for mocJnt in mocJnts:
        mtx = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList( cmds.getAttr( mocJnt + '.m' ), mtx )
        trMtx = OpenMaya.MTransformationMatrix( mtx )
        rotVector = trMtx.eulerRotation().asVector()
        rotValue = [ math.degrees( rotVector.x ), math.degrees( rotVector.y ), math.degrees( rotVector.z ) ]
        cmds.setAttr( mocJnt + '.jo', *rotValue )
        cmds.setAttr( mocJnt + '.r', 0,0,0 )
        
    
    meshs = mocCreateDict['meshs']
    meshChildren = pymel.core.listRelatives( meshs, c=1, ad=1, type='transform' )
    meshChildren += pymel.core.ls( meshs )
    
    newMeshs = []
    for meshChild in meshChildren:
        shape = meshChild.getShape()
        if not shape or shape.type() != 'mesh': continue
        if not shape: continue
        hists = shape.history()
        
        origMesh = None
        for hist in hists:
            if hist.type() != 'mesh': continue
            if not hist.isVisible(): continue 
            if shape.numVertices() != hist.numVertices(): continue
            origMesh = hist
            break

        if not origMesh: continue
        
        newMesh = pymel.core.createNode( 'mesh' )
        origMesh.outMesh >> newMesh.inMesh
        cmds.refresh()
        origMesh.outMesh // newMesh.inMesh
        
        newMesh.parent(0).setMatrix( origMesh.worldMatrix.get() )
        print "orig parent name : " , origMesh.parent(0).name()
        newMesh.parent(0).rename( 'MOCMESH_' + origMesh.parent(0).name() )
        
        pymel.core.skinCluster( mocJnts, newMesh, tsb=1 )
        try:
            pymel.core.copySkinWeights( shape, newMesh, noMirror=1, surfaceAssociation='closestComponent', influenceAssociation=['closestJoint'] )
        except:
            pass
        cmds.sets( newMesh.name(), e=1, forceElement='initialShadingGroup' )
        
        newMeshs.append( newMesh.parent(0) )
    
    mocJntParents = pymel.core.ls( mocJnts[0] )[0].getAllParents()
    if mocJntParents:
        mocRoot = mocJntParents[-1]
    else:
        mocRoot = pymel.core.ls( mocJnts[0] )[0]
    
    pymel.core.group( newMeshs, n='MOCMESH_grp' )
    jntGrp = pymel.core.group( mocRoot, n='MOCJNT_grp' )
    cmds.move( 0,0,0, jntGrp.scalePivot.name(), jntGrp.rotatePivot.name() ,rpr=1 )




def getMObject( target ):
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, mObject )
    return mObject



def getDagPath( target ):
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    try:
        selList.getDagPath( 0, dagPath )
        return dagPath
    except:
        return None
    
    

def matrixToList( matrix ):
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList



def listToMatrix( mtxList ):
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix




def cutCurve( curves, mesh ):
    
    mesh = cmds.listRelatives( mesh, s=1, f=1 )[0]
    fnMesh = OpenMaya.MFnMesh( getDagPath( mesh ) )
    meshIntersector = OpenMaya.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    
    cutCrvs = []
    
    for curve in curves:
        curveShape = cmds.listRelatives( curve, s=1, f=1 )[0]
        
        fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( curveShape ) )
        curveMtx = fnCurve.dagPath().inclusiveMatrix()
        
        multMtx = curveMtx * meshMtx.inverse()
        
        numSpans = fnCurve.numSpans()
        degree   = fnCurve.degree()
        
        minParam = fnCurve.findParamFromLength( 0.0 )
        maxParam = fnCurve.findParamFromLength( fnCurve.length() )
        
        eachParam = (maxParam-minParam) / ( numSpans*10-1 )
        
        pointOnMesh = OpenMaya.MPointOnMesh()
        
        pointInCurve = OpenMaya.MPoint();
        pointInMesh = OpenMaya.MPoint();
    
        closestParam = 0.0;
    
        for i in range( numSpans*10 ):
            targetParam = eachParam * i + minParam
            fnCurve.getPointAtParam( targetParam, pointInCurve )
            pointInCurve*= multMtx
            meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
            normal = pointOnMesh.getNormal()
            pointInMesh = OpenMaya.MVector( pointOnMesh.getPoint() )
            
            if OpenMaya.MVector( pointInCurve - pointInMesh ) * OpenMaya.MVector( normal ) > 0:
                closestParam = targetParam
                break
        
        currentParam = targetParam
        
        if closestParam != 0:
            
            pointInCurvePlus = OpenMaya.MPoint()
            pointInCurveMinus = OpenMaya.MPoint()
            pointOnMeshPlus = OpenMaya.MPointOnMesh()
            pointOnMeshMinus = OpenMaya.MPointOnMesh()
            
            for i in range( 10 ):
                currentParamPlus  = currentParam + eachParam
                currentParamMinus = currentParam - eachParam
                
                if currentParamMinus < minParam: currentParamMinus = minParam
                
                fnCurve.getPointAtParam( currentParamPlus, pointInCurvePlus )
                fnCurve.getPointAtParam( currentParamMinus, pointInCurveMinus )
                pointInCurvePlus *= multMtx
                pointInCurveMinus *= multMtx
                meshIntersector.getClosestPoint( pointInCurvePlus, pointOnMeshPlus )
                meshIntersector.getClosestPoint( pointInCurveMinus, pointOnMeshMinus )
                pointInMeshPlus = OpenMaya.MPoint( pointOnMeshPlus.getPoint() )
                pointInMeshMinus = OpenMaya.MPoint( pointOnMeshMinus.getPoint() )
                
                if pointInMeshPlus.distanceTo( pointInCurvePlus ) < pointInMeshMinus.distanceTo( pointInCurveMinus ):
                    currentParam = currentParamPlus
                else:
                    currentParam = currentParamMinus
                
                if currentParam < minParam:
                    currentParam = minParam
                if currentParam > maxParam:
                    currentParam  = maxParam
                
                eachParam *= 0.5
        
        detachNode = cmds.createNode( 'detachCurve' )
        cmds.setAttr( detachNode+'.parameter[0]', currentParam )
        
        cutCurve  = cmds.createNode( 'nurbsCurve' )
        cutCurveP = cmds.listRelatives( cutCurve, p=1, f=1 )[0]
        
        cmds.connectAttr( curveShape+'.local', detachNode+'.inputCurve' )
        cmds.connectAttr( detachNode+'.outputCurve[1]', cutCurve+'.create' )
        
        if currentParam < 0.0001:
            fnCurve.getPointAtParam( currentParam, pointInCurve )
            pointInCurve*= multMtx
            meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
            pointClose = OpenMaya.MPoint( pointOnMesh.getPoint() ) * multMtx.inverse()
            cmds.move( pointClose.x, pointClose.y, pointClose.z, cutCurveP+'.cv[0]', os=1 )
        else:
            cmds.rebuildCurve( cutCurveP, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=numSpans, degree=degree, tol=0.01 )

        cmds.DeleteHistory( cutCurveP )
        cmds.xform( cutCurveP, ws=1, matrix = matrixToList( curveMtx ) )

        curveName = curve.split( '|' )[-1]
        cutCurveP = cmds.rename( cutCurveP, curveName+'_cuted' )

        cutCrvs.append( cutCurveP )

    return cutCrvs



def cleanController( controller ):

    pController = cmds.listRelatives( controller, p=1, f=1 )
    if not pController: return None
    
    controllerAttrList = ['shape_tx', 'shape_ty', 'shape_tz', 'shape_rx', 'shape_ry', 'shape_rz', 'shape_sx', 'shape_sy', 'shape_sz', 'radius']
    controllerKeyAttrList = ['v']

    for attr in controllerAttrList:
        if not cmds.attributeQuery( attr, node=controller, ex=1 ): continue
        try:cmds.setAttr( controller + '.' + attr, e=1, cb=0 )
        except:pass
    
    for attr in controllerKeyAttrList:
        if not cmds.attributeQuery( attr, node=controller, ex=1 ): continue
        try:cmds.setAttr( controller + '.' + attr, e=1, k=0 )
        except:pass
    
    attrs = cmds.listAttr( pController[0] )
    for attr in attrs:
        try:cmds.setAttr( pController[0] + '.' + attr, e=1, lock=1 )
        except:pass




def makeController( pointList, defaultScaleMult = 1, **options ):
    
    import copy
    import pymel.core
    
    newPointList = copy.deepcopy( pointList )
    for point in newPointList:
        point[0] *= defaultScaleMult
        point[1] *= defaultScaleMult
        point[2] *= defaultScaleMult
    
    options.update( {'p':newPointList, 'd':1} )
    
    crv = pymel.core.curve( **options )
    ioCrv = pymel.core.ls( cmds.duplicate( crv.name() )[0] )[0]
    crvShape = crv.getShape()
    ioCrvShape = ioCrv.getShape()
    
    if options.has_key( 'n' ):
        name = options['n']
    elif options.has_key( 'name' ):
        name = options['name']
    else:
        name = None
    
    jnt = pymel.core.createNode( 'joint' )
    jnt.setAttr( 'drawStyle', 2 )
    jnt.setAttr( 'segmentScaleCompensate', 0 )
    if name: jnt.rename( name )
    pymel.core.parent( crvShape, jnt, add=1, shape=1 )
    pymel.core.parent( ioCrvShape, jnt, add=1, shape=1 )
    cmds.refresh()
    
    jnt.addAttr( 'shape_tx', dv=0 ); jnt.shape_tx.showInChannelBox(1)
    jnt.addAttr( 'shape_ty', dv=0 ); jnt.shape_ty.showInChannelBox(1)
    jnt.addAttr( 'shape_tz', dv=0 ); jnt.shape_tz.showInChannelBox(1)
    jnt.addAttr( 'shape_rx', dv=0, at='doubleAngle' ); jnt.shape_rx.showInChannelBox(1)
    jnt.addAttr( 'shape_ry', dv=0, at='doubleAngle' ); jnt.shape_ry.showInChannelBox(1)
    jnt.addAttr( 'shape_rz', dv=0, at='doubleAngle' ); jnt.shape_rz.showInChannelBox(1)
    jnt.addAttr( 'shape_sx', dv=1 ); jnt.shape_sx.showInChannelBox(1)
    jnt.addAttr( 'shape_sy', dv=1 ); jnt.shape_sy.showInChannelBox(1)
    jnt.addAttr( 'shape_sz', dv=1 ); jnt.shape_sz.showInChannelBox(1)
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    jnt.shape_tx >> composeMatrix.inputTranslateX
    jnt.shape_ty >> composeMatrix.inputTranslateY
    jnt.shape_tz >> composeMatrix.inputTranslateZ
    jnt.shape_rx >> composeMatrix.inputRotateX
    jnt.shape_ry >> composeMatrix.inputRotateY
    jnt.shape_rz >> composeMatrix.inputRotateZ
    jnt.shape_sx >> composeMatrix.inputScaleX
    jnt.shape_sy >> composeMatrix.inputScaleY
    jnt.shape_sz >> composeMatrix.inputScaleZ
    trGeo = pymel.core.createNode( 'transformGeometry' )
    jnt.attr( 'radius' ).set( 0 )

    ioCrvShape.local >> trGeo.inputGeometry
    composeMatrix.outputMatrix >> trGeo.transform
    
    trGeo.outputGeometry >> crvShape.create
    
    ioCrvShape.setAttr( 'io', 1 )
    pymel.core.delete( crv )
    pymel.core.delete( ioCrv )

    return jnt




def createDefaultPropRig( propGrp ):
    
    import pymel.core
    from sgModules import sgdata
    propGrp = pymel.core.ls( propGrp )[0]
    
    def makeParent( target ):
        targetP = pymel.core.createNode( 'transform' )
        pymel.core.xform( targetP, ws=1, matrix= target.wm.get() )
        pymel.core.parent( target, targetP )
        targetP.rename( 'P' + target.shortName() )
        return targetP
    
    worldCtl = makeController( sgdata.Controllers.circlePoints )
    moveCtl  = makeController( sgdata.Controllers.crossPoints )
    rootCtl  = makeController( sgdata.Controllers.circlePoints )
    
    bbmin = propGrp.boundingBoxMin.get()
    bbmax = propGrp.boundingBoxMax.get()
    
    bbsize = max( bbmax[0] - bbmin[0], bbmax[2] - bbmin[2] )/2
    
    center = ( ( bbmin[0] + bbmax[0] )/2, ( bbmin[1] + bbmax[1] )/2, ( bbmin[2] + bbmax[2] )/2 )
    floorPoint = ( ( bbmin[0] + bbmax[0] )/2, bbmin[1], ( bbmin[2] + bbmax[2] )/2 )
    
    worldCtl.t.set( *floorPoint )
    moveCtl.t.set( *floorPoint )
    rootCtl.t.set( *center )
    
    rootCtl.shape_sx.set( bbsize*1.2 )
    rootCtl.shape_sy.set( bbsize*1.2 )
    rootCtl.shape_sz.set( bbsize*1.2 )

    moveCtl.shape_sx.set( bbsize*1.3 )
    moveCtl.shape_sy.set( bbsize*1.3 )
    moveCtl.shape_sz.set( bbsize*1.3 )
    
    worldCtl.shape_sx.set( bbsize*1.5 )
    worldCtl.shape_sy.set( bbsize*1.5 )
    worldCtl.shape_sz.set( bbsize*1.5 )
    
    rootCtl.getShape().setAttr( 'overrideEnabled', 1 )
    rootCtl.getShape().setAttr( 'overrideColor', 29 )
    moveCtl.getShape().setAttr( 'overrideEnabled', 1 )
    moveCtl.getShape().setAttr( 'overrideColor', 20 )
    worldCtl.getShape().setAttr( 'overrideEnabled', 1 )
    worldCtl.getShape().setAttr( 'overrideColor', 17 )
    
    rootCtl.rename( 'Ctl_Root' )
    moveCtl.rename( 'Ctl_Move' )
    worldCtl.rename( 'Ctl_World' )
    
    pRootCtl = makeParent( rootCtl )
    pMoveCtl = makeParent( moveCtl )
    pWorldCtl = makeParent( worldCtl )
    
    pymel.core.parent( pRootCtl, moveCtl )
    pymel.core.parent( pMoveCtl, worldCtl )
    rigGrp = pymel.core.group( pWorldCtl, n='rig' )
    
    pointer = pymel.core.createNode( 'transform', n='pointer_geo' )
    pymel.core.parent( pointer, rootCtl )
    pymel.core.xform( pointer, ws=1, matrix= propGrp.wm.get() )

    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    
    pointer.wm >> mm.i[0]
    propGrp.pim >> mm.i[1]
    mm.matrixSum >> dcmp.imat
    
    dcmp.outputTranslate >> propGrp.t
    dcmp.outputRotate >> propGrp.r
    dcmp.outputScale >> propGrp.s
    dcmp.outputShear >> propGrp.sh


def putControllerToGeo( target, points, multSize = 1.0 ):
    
    def makeParent( target ):
        targetP = pymel.core.createNode( 'transform' )
        pymel.core.xform( targetP, ws=1, matrix= target.wm.get() )
        pymel.core.parent( target, targetP )
        targetP.rename( 'P' + target.shortName() )
        return targetP
    
    target = pymel.core.ls( target )[0]
    targetP = target.getParent()
    parentMatrix = OpenMaya.MMatrix()
    if targetP:
        print targetP.wm.get()
        parentMatrix = listToMatrix( cmds.getAttr( targetP.wm.name() ) )
    
    bbmin = target.boundingBoxMin.get()
    bbmax = target.boundingBoxMax.get()
    
    center = ( ( bbmin[0] + bbmax[0] )/2, ( bbmin[1] + bbmax[1] )/2, ( bbmin[2] + bbmax[2] )/2 )
    sizeX = (bbmax[0]-bbmin[0])/2 * multSize
    sizeY = (bbmax[1]-bbmin[1])/2 * multSize
    sizeZ = (bbmax[2]-bbmin[2])/2 * multSize
    
    if not sizeX: sizeX = 1
    if not sizeY: sizeY = 1
    if not sizeZ: sizeZ = 1

    targetCtl = makeController( points )
    targetCtl.shape_sx.set( sizeX )
    targetCtl.shape_sy.set( sizeY )
    targetCtl.shape_sz.set( sizeZ )

    worldCenter = OpenMaya.MPoint( *center ) * parentMatrix

    print center
    print worldCenter.x, worldCenter.y, worldCenter.z

    targetCtl.t.set( worldCenter.x, worldCenter.y, worldCenter.z )
    makeParent( targetCtl )
    
    return targetCtl



