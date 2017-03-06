import maya.cmds as cmds
import maya.OpenMaya as om


setTool_createJointOnMesh = """
import sgBFunction_base
import maya.cmds as cmds
import maya.mel as mel
sgBFunction_base.autoLoadPlugin( 'sgTools' )

if not cmds.contextInfo( "createJointContext1", ex=1 ):
    mel.eval( 'createJointContext createJointContext1' )
cmds.setToolTo( "createJointContext1" )
"""



createCurveOnSelJoints = """
import sgBFunction_curve
import maya.cmds as cmds

topJoints = cmds.ls( sl=1 )

for joint in topJoints:
    jnts = cmds.listRelatives( joint, c=1, ad=1, type='joint', f=1 )
    jnts.append( joint )
    jnts.reverse()
    
    sgBFunction_curve.createCurveOnTargetPoints( jnts )
"""



import sgPWindow_set_jointLineOnMesh
showUi_createJointLineOnMesh = sgPWindow_set_jointLineOnMesh.mc_showWindow



import sgPWindow_set_jointLineOnMesh2
showUi_createJointLineOnMesh2 = sgPWindow_set_jointLineOnMesh2.mc_showWindow




import sgPWindow_set_joint
showUi_setJointLine = sgPWindow_set_joint.mc_showWindow




import sgUIsgWobbleCurve
showUi_createWobbleCurve = sgUIsgWobbleCurve.mc_showWindow




import sgUIMakeCurveDynamic
showUi_createDynamicCurve = sgUIMakeCurveDynamic.mc_showWindow




import sgUICurve_createJoint
showUi_createJointOnCurve = sgUICurve_createJoint.mc_showWindow



makeControledCurveFromJoints = """
import sgBFunction_curve
sgBFunction_curve.makeControledCurveFromJoints( cmds.ls( sl=1 ) )
"""
            


createEditAbleJoints = """
import sgBFunction_joint
sgBFunction_joint.createEditableJoints( cmds.ls( sl=1 ) )
"""



def createCurveToEdgeLoop_before():
    
    sels = cmds.ls( sl=1, fl=1 )
    selObject = cmds.ls( sl=1, o=1 )[0]
    selObject = cmds.listRelatives( selObject, p=1 )[0]
    excutedEdges = []
    curves = []
    for sel in sels:
        if sel in excutedEdges: continue
        cmds.select( sel )
        cmds.SelectEdgeLoopSp()
        excutedEdges += cmds.ls(sl=1, fl=1 )
        curves.append( cmds.polyToCurve( form=0, degree=3, ch=1 )[0] )
    
    cmds.select( curves )
    cmds.DeleteHistory()
    return cmds.ls( sl=1 )





def gravityConnect( *args ):
    
    sels = cmds.ls( sl=1 )

    ctl = sels[-1]
    
    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( ctl, ln='gravityWeight', dv=0, k=1, min=0, max=1 )
    
    newObject = cmds.createNode( 'transform', n='GravityObject' )
    cmds.setAttr( newObject+'.dh', 1 )
    
    for sel in sels[:-1]:
        selChild = cmds.listRelatives( sel, c=1, f=1 )[0]
        mmdcFirst = cmds.createNode( 'multMatrixDecompose' )
        blmtxFirst = cmds.createNode( 'blendTwoMatrix' )
        mmdcSecond = cmds.createNode( 'multMatrixDecompose' )
        blmtxSecond = cmds.createNode( 'blendTwoMatrix' )
        
        multNode = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( ctl+'.gravityWeight', multNode+'.input1' )
        cmds.setAttr( multNode+'.input2', 0.5 )
        cmds.connectAttr( multNode+'.output', blmtxFirst+'.attributeBlender' )
        cmds.connectAttr( ctl+'.gravityWeight', blmtxSecond+'.attributeBlender' )
        
        cmds.connectAttr( ctl+'.wm', blmtxFirst+'.inMatrix1' )
        cmds.connectAttr( newObject+'.wm', blmtxFirst+'.inMatrix2' )
        cmds.connectAttr( blmtxFirst+'.outMatrix', mmdcFirst+'.i[0]' )
        cmds.connectAttr( sel+'.pim', mmdcFirst+'.i[1]' )
        cmds.connectAttr( mmdcFirst+'.or', sel+'.jo' )
        
        cmds.connectAttr( ctl+'.wm', blmtxSecond+'.inMatrix1' )
        cmds.connectAttr( newObject+'.wm', blmtxSecond+'.inMatrix2' )
        cmds.connectAttr( blmtxSecond+'.outMatrix', mmdcSecond+'.i[0]' )
        cmds.connectAttr( selChild+'.pim', mmdcSecond+'.i[1]' )
        cmds.connectAttr( mmdcSecond+'.or', selChild+'.jo' )




def createCurveFromJoint( topJoint, connection=True ):
    
    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'sgRigAddition' )
    
    children = cmds.listRelatives( topJoint, c=1, ad=1,f=1, type='joint' )
    children.append( topJoint )
    children.reverse()
    
    node = cmds.createNode( 'sgCurveFromPoints' )
    cmds.setAttr( node + '.createType', 1 )
    cmds.setAttr( node+'.degrees', 2 )
    curveShape = cmds.createNode( 'nurbsCurve' )
    curve = cmds.listRelatives( curveShape, p=1, f=1 )[0]
    
    cmds.connectAttr( node + '.outputCurve', curveShape + '.create' )
    for i in range( len( children ) ):
        cmds.connectAttr( children[i] + '.wm', node+'.input[%d].inputMatrix' % i )
    return curve



mc_createCurveFromJoint = """import sgBRig_hair
sels = cmds.ls( sl=1 )
for sel in sels:
    sgBRig_hair.createCurveFromJoint( sel )
"""



def cutCurve( curves, mesh ):
    
    import sgBFunction_dag
    import sgBFunction_convert
    
    curves = sgBFunction_convert.singleToList( curves )
    curves = sgBFunction_dag.getChildrenShapeExists( curves )
    
    mesh = sgBFunction_dag.getShape( mesh )
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) )
    meshIntersector = om.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    
    cutCrvs = []
    
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        
        fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
        curveMtx = fnCurve.dagPath().inclusiveMatrix()
        
        multMtx = curveMtx * meshMtx.inverse()
        
        numSpans = fnCurve.numSpans()
        degree   = fnCurve.degree()
        
        minParam = fnCurve.findParamFromLength( 0.0 )
        maxParam = fnCurve.findParamFromLength( fnCurve.length() )
        
        eachParam = (maxParam-minParam) / ( numSpans*10-1 )
        
        pointOnMesh = om.MPointOnMesh()
        
        pointInCurve = om.MPoint();
        pointInMesh = om.MPoint();
    
        closestParam = 0.0;
    
        for i in range( numSpans*10 ):
            targetParam = eachParam * i + minParam
            fnCurve.getPointAtParam( targetParam, pointInCurve )
            pointInCurve*= multMtx
            meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
            normal = pointOnMesh.getNormal()
            pointInMesh = om.MVector( pointOnMesh.getPoint() )
            
            if om.MVector( pointInCurve - pointInMesh ) * om.MVector( normal ) > 0:
                closestParam = targetParam
                break
        
        currentParam = targetParam
        
        if closestParam != 0:
            
            pointInCurvePlus = om.MPoint()
            pointInCurveMinus = om.MPoint()
            pointOnMeshPlus = om.MPointOnMesh()
            pointOnMeshMinus = om.MPointOnMesh()
            
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
                pointInMeshPlus = om.MPoint( pointOnMeshPlus.getPoint() )
                pointInMeshMinus = om.MPoint( pointOnMeshMinus.getPoint() )
                
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
            pointClose = om.MPoint( pointOnMesh.getPoint() ) * multMtx.inverse()
            cmds.move( pointClose.x, pointClose.y, pointClose.z, cutCurveP+'.cv[0]', os=1 )
        else:
            cmds.rebuildCurve( cutCurveP, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=numSpans, degree=degree, tol=0.01 )

        cmds.DeleteHistory( cutCurveP )
        cmds.xform( cutCurveP, ws=1, matrix = sgBFunction_convert.convertMMatrixToMatrix( curveMtx ) )

        curveName = curve.split( '|' )[-1]
        cutCurveP = cmds.rename( cutCurveP, curveName+'_cuted' )
        
        curveParent = cmds.listRelatives( curve, p=1, f=1 )
        if curveParent:
            cloneObject = sgBFunction_dag.makeCloneObject( curveParent, '_cuted' )
            cutCurveP = cmds.parent( cutCurveP, cloneObject )[0]
        cutCrvs.append( cutCurveP )

    return cutCrvs





def getCuttingParams( curves, mesh ):
    
    import sgBFunction_dag
    
    mesh = sgBFunction_dag.getShape( mesh )
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) )
    meshIntersector = om.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    
    cuttingParams = []
    for curve in curves:
        curve = sgBFunction_dag.getShape( curve )
        
        print curve
        
        dagPathCurve = sgBFunction_dag.getMDagPath( curve ) 
        fnCurve = om.MFnNurbsCurve( dagPathCurve )
        curveMtx = dagPathCurve.inclusiveMatrix()
        
        multMtx = curveMtx * meshMtx.inverse()
        
        numSpans = fnCurve.numSpans()
        degree   = fnCurve.degree()
        
        minParam = fnCurve.findParamFromLength( 0.0 )
        maxParam = fnCurve.findParamFromLength( fnCurve.length() )
        
        eachParam = (maxParam-minParam) / ( numSpans*10-1 )
        
        pointOnMesh = om.MPointOnMesh()
        
        pointInCurve = om.MPoint();
        pointInMesh = om.MPoint();
    
        closestParam = 0.0;
    
        for i in range( numSpans*10 ):
            targetParam = eachParam * i + minParam
            fnCurve.getPointAtParam( targetParam, pointInCurve )
            pointInCurve*= multMtx
            meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
            normal = pointOnMesh.getNormal()
            pointInMesh = om.MVector( pointOnMesh.getPoint() )
            
            if om.MVector( pointInCurve - pointInMesh ) * om.MVector( normal ) > 0:
                closestParam = targetParam
                break
        
        currentParam = targetParam
        
        if closestParam != 0:
            
            pointInCurvePlus = om.MPoint()
            pointInCurveMinus = om.MPoint()
            pointOnMeshPlus = om.MPointOnMesh()
            pointOnMeshMinus = om.MPointOnMesh()
            
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
                pointInMeshPlus = om.MPoint( pointOnMeshPlus.getPoint() )
                pointInMeshMinus = om.MPoint( pointOnMeshMinus.getPoint() )
                
                if pointInMeshPlus.distanceTo( pointInCurvePlus ) < pointInMeshMinus.distanceTo( pointInCurveMinus ):
                    currentParam = currentParamPlus
                else:
                    currentParam = currentParamMinus
                
                if currentParam < minParam:
                    currentParam = minParam
                if currentParam > maxParam:
                    currentParam  = maxParam
                
                eachParam *= 0.5
        
        cuttingParams.append( currentParam )

    return cuttingParams



def getCuttingPoints( curves, mesh ):
    
    import sgBFunction_dag
    
    params = getCuttingParams( curves, mesh )
    points = []
    for i in range( len( curves ) ):
        curve = curves[i]
        param = params[i]
        
        curveDagPath = sgBFunction_dag.getMDagPath( curve )
        curveShape = sgBFunction_dag.getShape( curve )
        
        fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
        
        pointCurve = om.MPoint()
        fnCurve.getPointAtParam( param, pointCurve )
        pointCurve *= curveDagPath.inclusiveMatrix()

        points.append( [ pointCurve.x, pointCurve.y, pointCurve.z] )
    
    return points




def cutCurveToTarget( curves, mesh, keepHist = False ):
    
    import sgBFunction_dag
    import sgBFunction_convert
    import sgBFunction_base
    import sgBFunction_attribute
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )
    
    curves = sgBFunction_convert.singleToList( curves )
    
    curves = sgBFunction_dag.getChildrenShapeExists( curves )
    
    mesh = sgBFunction_dag.getShape( mesh )
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) )
    meshIntersector = om.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    
    if not keepHist:
        newCurves = []
        for curve in curves:
            curveShape = sgBFunction_dag.getShape( curve )
            newCurveShape = cmds.createNode( 'nurbsCurve' )
            
            cutInfo = cmds.createNode( 'sgHair_cutInfo' )
            cmds.connectAttr( mesh+'.wm', cutInfo+'.inputMeshMatrix' )
            cmds.connectAttr( mesh+'.outMesh', cutInfo+'.inputMesh' )
            cmds.connectAttr( curveShape+'.wm', cutInfo+'.inputCurveMatrix' )
            cmds.connectAttr( curveShape+'.local', cutInfo+'.inputCurve' )
            
            detachNode = cmds.createNode( 'detachCurve' )
            rebuildNode = cmds.createNode( 'rebuildCurve' )
            cmds.setAttr( rebuildNode+'.keepControlPoints', 1 )
            cmds.connectAttr( curveShape+'.local', detachNode+'.inputCurve' )
            cmds.connectAttr( detachNode+'.outputCurve[1]', rebuildNode+'.inputCurve' )
            cmds.connectAttr( cutInfo+'.outParam', detachNode+'.parameter[0]' )
            cmds.connectAttr( rebuildNode+'.outputCurve', newCurveShape+'.create' )
            
            newCurve = sgBFunction_dag.getParent( newCurveShape )
            cmds.xform( newCurve, ws=1, matrix=cmds.getAttr( curve+'.wm' ) )
            
            udAttrs = cmds.listAttr( curve, ud=1 )
            if not udAttrs: udAttrs = []
            for udAttr in udAttrs:
                sgBFunction_attribute.copyAttribute( curve+'.'+udAttr, newCurve )
                cmds.connectAttr( newCurve+'.'+udAttr, curve+'.'+udAttr, f=1 )
            
            if cmds.getAttr( detachNode+'.parameter[0]' ) == 0:
                closePoint = cmds.getAttr( cutInfo+'.outPoint' )[0]
                cmds.move( closePoint[0], closePoint[1], closePoint[2], curve+'.cv[0]', os=1 )
    
            cmds.select( newCurve )
            cmds.DeleteHistory()
            newCurves.append( newCurve )
        
        cmds.refresh()
        
        for i in range( len( newCurves ) ):
            newCurveShape = sgBFunction_dag.getShape( newCurves[i] )
            curveShape = sgBFunction_dag.getShape( curves[i] )
            cmds.connectAttr( newCurveShape+'.local', curveShape+'.create', f=1 )
        
        cmds.refresh()
    
        cmds.delete( newCurves )
        return curves
    
    else:
        newCurves0 = []
        newCurves1 = []
        for curve in curves:
            curveShape = sgBFunction_dag.getShape( curve )
            newCurveShape0 = cmds.createNode( 'nurbsCurve' )
            newCurveShape1 = cmds.createNode( 'nurbsCurve' )
            
            cutInfo = cmds.createNode( 'sgHair_cutInfo' )
            cmds.connectAttr( mesh+'.wm', cutInfo+'.inputMeshMatrix' )
            cmds.connectAttr( mesh+'.outMesh', cutInfo+'.inputMesh' )
            cmds.connectAttr( curveShape+'.wm', cutInfo+'.inputCurveMatrix' )
            cmds.connectAttr( curveShape+'.local', cutInfo+'.inputCurve' )
            
            detachNode = cmds.createNode( 'detachCurve' )
            rebuildNode0 = cmds.createNode( 'rebuildCurve' )
            rebuildNode1 = cmds.createNode( 'rebuildCurve' )
            
            cmds.connectAttr( curveShape+'.local', detachNode+'.inputCurve' )
            cmds.connectAttr( cutInfo+'.outParam', detachNode+'.parameter[0]' )
            
            cmds.setAttr( rebuildNode0+'.keepControlPoints', 1 )
            cmds.connectAttr( detachNode+'.outputCurve[0]', rebuildNode0+'.inputCurve' )
            cmds.connectAttr( rebuildNode0+'.outputCurve', newCurveShape0+'.create' )
            cmds.setAttr( rebuildNode1+'.keepControlPoints', 1 )
            cmds.connectAttr( detachNode+'.outputCurve[1]', rebuildNode1+'.inputCurve' )
            cmds.connectAttr( rebuildNode1+'.outputCurve', newCurveShape1+'.create' )
            
            newCurve0 = sgBFunction_dag.getParent( newCurveShape0 )
            newCurve1 = sgBFunction_dag.getParent( newCurveShape1 )
            cmds.xform( newCurve0, ws=1, matrix=cmds.getAttr( curve+'.wm' ) )
            cmds.xform( newCurve1, ws=1, matrix=cmds.getAttr( curve+'.wm' ) )
            
            curveName = curve.split( '|' )[-1]
            newCurve0 = cmds.rename( newCurve0, curveName+'_detach_0' )
            newCurve1 = cmds.rename( newCurve1, curveName+'_detach_1' )
            
            newCurves0.append( newCurve0 )
            newCurves1.append( newCurve1 )

        return newCurves0, newCurves1


mc_cutCurve = """import sgBRig_hair

sels = cmds.ls( sl=1 )

cutCurves = sgBRig_hair.cutCurve( sels[:-1], sels[-1] )

for sel in sels[:-1]:
    cmds.setAttr( sel+'.v', 0 )

cmds.select( cutCurves )"""



def cutCurveByCutInfo( curves, mesh, addName = '_cuted' ):
    
    import sgBFunction_dag
    import sgBFunction_convert
    import sgBFunction_base
    import sgBFunction_attribute
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )
    
    curves = sgBFunction_convert.singleToList( curves )
    curves = sgBFunction_dag.getChildrenShapeExists( curves )
    
    meshShape = sgBFunction_dag.getShape( mesh )
    
    newCurves = []
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        newCurveShape = cmds.createNode( 'nurbsCurve' )
        
        cutInfo = cmds.createNode( 'sgHair_cutInfo' )
        cmds.connectAttr( meshShape+'.wm', cutInfo+'.inputMeshMatrix' )
        cmds.connectAttr( meshShape+'.outMesh', cutInfo+'.inputMesh' )
        cmds.connectAttr( curveShape+'.wm', cutInfo+'.inputCurveMatrix' )
        cmds.connectAttr( curveShape+'.local', cutInfo+'.inputCurve' )
        
        detachNode = cmds.createNode( 'detachCurve' )
        rebuildNode = cmds.createNode( 'rebuildCurve' )
        cmds.setAttr( rebuildNode+'.keepControlPoints', 1 )
        cmds.connectAttr( curveShape+'.local', detachNode+'.inputCurve' )
        cmds.connectAttr( detachNode+'.outputCurve[1]', rebuildNode+'.inputCurve' )
        cmds.connectAttr( cutInfo+'.outParam', detachNode+'.parameter[0]' )
        cmds.connectAttr( rebuildNode+'.outputCurve', newCurveShape+'.create' )
        
        newCurve = sgBFunction_dag.getParent( newCurveShape )
        cmds.xform( newCurve, ws=1, matrix=cmds.getAttr( curve+'.wm' ) )
        
        udAttrs = cmds.listAttr( curve, ud=1 )
        if not udAttrs: udAttrs = []
        for udAttr in udAttrs:
            sgBFunction_attribute.copyAttribute( curve+'.'+udAttr, newCurve )
            cmds.connectAttr( newCurve+'.'+udAttr, curve+'.'+udAttr, f=1 )
        
        curveName = curve.split( '|' )[-1]
        newCurve = cmds.rename( newCurve, curveName+'_cuted' )
        
        curveParent = cmds.listRelatives( curve, p=1, f=1 )[0]
        if curveParent:
            cloneObject = sgBFunction_dag.makeCloneObject( curveParent, '_cuted' )
            newCurve = cmds.parent( newCurve, cloneObject )[0]
        
        newCurve = cmds.rename( newCurve, curve.split( '|' )[-1] +addName )
        newCurves.append( newCurve )
        
        if cmds.getAttr( detachNode+'.parameter[0]' ) == 0:
            closePoint = cmds.getAttr( cutInfo+'.outPoint' )[0]
            cmds.move( closePoint[0], closePoint[1], closePoint[2], curve+'.cv[0]', os=1 )

    cmds.select( newCurves )
    return newCurves


mc_cutCurveByCutInfo = """import sgBRig_hair

sels = cmds.ls( sl=1 )

cutCurves = sgBRig_hair.cutCurveByCutInfo( sels[:-1], sels[-1] )
"""



def createFollicleByCutInfo( curves, mesh, addName='_' ):
    
    import sgBFunction_convert
    import sgBFunction_dag
    
    curves = sgBFunction_convert.singleToList( curves )
    curves = sgBFunction_dag.getChildrenShapeExists( curves )
    
    follicles = []
    for curve in curves:
        cutInfo = sgBFunction_dag.getNodeFromHistory( curve, 'sgHair_cutInfo' )
        if not cutInfo: continue
        
        follicle = cmds.createNode( 'follicle' )
        follicleObj = sgBFunction_dag.getParent( follicle )
        meshShape = sgBFunction_dag.getShape( mesh )
        
        cmds.connectAttr( follicle+'.outTranslate', follicleObj+'.t' )
        cmds.connectAttr( follicle+'.outRotate', follicleObj+'.r' )
    
        cmds.connectAttr( meshShape+'.outMesh', follicleObj+'.inputMesh' )
        cmds.connectAttr( meshShape+'.wm', follicleObj+'.inputWorldMatrix' )
        
        cmds.connectAttr( cutInfo[0]+'.outU', follicle+'.parameterU' )
        cmds.connectAttr( cutInfo[0]+'.outV', follicle+'.parameterV' )
        
        follicleObj = cmds.rename( follicleObj, curve.split( '|' )[-1]+addName )
        follicles.append( follicleObj )
    return follicles



def createFollicleToCuttingPoint( curves, mesh ):
    
    import sgBFunction_convert
    import sgBFunction_mesh
    import sgBFunction_dag
    
    meshShape = sgBFunction_dag.getShape( mesh )
    
    curves = sgBFunction_convert.singleToList( curves )
    points = getCuttingPoints( curves, mesh )
    
    follicleObjs = []
    for i in range( len( curves ) ):
        curveName = curves[i].split( '|' )[-1]
        u, v = sgBFunction_mesh.getUVAtPoint( points[i], mesh )
        follicle = cmds.createNode( 'follicle' )
        follicleObj = sgBFunction_dag.getTransform( follicle )
        
        cmds.connectAttr( meshShape+'.outMesh', follicle+'.inputMesh' )
        cmds.connectAttr( meshShape+'.wm', follicle+'.inputWorldMatrix' )
        cmds.setAttr( follicle+'.parameterU', u )
        cmds.setAttr( follicle+'.parameterV', v )
        cmds.connectAttr( follicle+'.outTranslate', follicleObj+'.t' )
        cmds.connectAttr( follicle+'.outRotate', follicleObj+'.r' )
        
        follicleObj = cmds.rename( follicleObj, 'cutFollicle_' + curveName )
        follicleObjs.append( follicleObj )
    return follicleObjs




mc_createFollicleByCutInfo = """import sgBRig_hair

sels = cmds.ls( sl=1 )

cutCurves = sgBRig_hair.createFollicleByCutInfo( sels[:-1], sels[-1] )
"""



def createEditableJoints( sels ):
    
    import sgBFunction_dag
    import sgBFunction_joint
    
    for sel in sels:
        jnts = sgBFunction_joint.createControlAbleJoint( sel )
        
        skinClusterNodes = cmds.listConnections( sel+'.worldMatrix', d=1, s=0, type='skinCluster' )
        if not skinClusterNodes: continue
        
        for skinClusterNode in skinClusterNodes:
            matrixCons = cmds.listConnections( skinClusterNode+'.matrix', p=1, c=1 )
            
            srcCons = matrixCons[1::2]
            dstCons = matrixCons[::2]
            
            for i in range( len( srcCons ) ):
                srcCon = srcCons[i]
                dstCon = dstCons[i]
                
                srcNode, attrName = srcCon.split( '.' )
                dcmps = cmds.listConnections( srcNode+'.m', d=1, s=0, type='decomposeMatrix' )
                if not dcmps: continue
                jnt  = cmds.listConnections( dcmps[0]+'.or', s=0, d=1 )[0]
 
                cmds.connectAttr( jnt+'.'+attrName, dstCon, f=1 )

        selP = cmds.listRelatives( sel, p=1, f=1 )[0]
        targetClone = sgBFunction_dag.makeCloneObject( selP, '_controlable' )
        cmds.parent( jnts[0], targetClone )


mc_createEditableJoints = """import sgBRig_hair
sels = cmds.ls( sl=1 )

sgBRig_hair.createEditableJoints( sels )"""




def createCurveOnLineMesh( edge ):
    
    import sgBFunction_selection
    
    selEdges = sgBFunction_selection.getGetOrderedEdgeRing( edge )
    
    print selEdges
    
    bb = om.MBoundingBox()
    
    centerPoints = []
    for edge in selEdges:
        cmds.select( edge )
        cmds.SelectEdgeLoopSp()
        vtxList = cmds.polyListComponentConversion( cmds.ls( sl=1 ), tv=True )
        vts = cmds.ls( vtxList, fl=1 )
        bb.clear()
        for vtx in vts:
            bb.expand( om.MPoint( *cmds.xform( vtx, q=1, ws=1, t=1 ) ) )
        center = bb.center()
        centerPoints.append( [center.x, center.y, center.z] )
    
    return cmds.curve( p=centerPoints )


mc_createCurveOnLineMesh = """import sgBRig_hair

sels = cmds.ls( sl=1, fl=1 )

for sel in sels:
    sgBRig_hair.createCurveOnLineMesh( sel )"""
    
    

setSimulationTransformMult_expression ="""
int $dynamicOn = %CTL%.%DYNAMICON%;

int   $dynamicStartFrame = %CTL%.%ATTRSTARTFRAME%;
float $posWidthMult      = %CTL%.%ATTRWIDTHMULT%;
float $posHeightMult     = %CTL%.%ATTRHEIGHTMULT%;

if( !$dynamicOn )
{
    %CURRENTPOSTARGET%.translateX = %CTL%.translateX;
    %CURRENTPOSTARGET%.translateY = %CTL%.translateY;
    %CURRENTPOSTARGET%.translateZ = %CTL%.translateZ;
}
else
{
    float $DX_x = %DX_X%.translateX;
    float $DX_y = %DX_X%.translateY;
    float $DX_z = %DX_X%.translateZ;
    
    float $DY_x = %DX_Y%.translateX;
    float $DY_y = %DX_Y%.translateY;
    float $DY_z = %DX_Y%.translateZ;
    
    float $DZ_x = %DX_Z%.translateX;
    float $DZ_y = %DX_Z%.translateY;
    float $DZ_z = %DX_Z%.translateZ;
    
    float $beforePosX, $beforePosY, $beforePosZ; 
    float $beforeOutputPosX, $beforeOutputPosY, $beforeOutputPosZ; 
    float $currentPosX, $currentPosY, $currentPosZ;
    float $addPosX, $addPosY, $addPosZ;
    float $outputX, $outputY, $outputZ; 
    
    if( `currentTime -q` == $dynamicStartFrame )
    {
        $beforePosX = %CTL%.translateX;
        $beforePosY = %CTL%.translateY;
        $beforePosZ = %CTL%.translateZ;
    
        $currentPosX = $beforePosX;
        $currentPosY = $beforePosX;
        $currentPosZ = $beforePosX;
    
        $outputX = $beforePosX;
        $outputY = $beforePosY;
        $outputZ = $beforePosZ;
    }
    
    $currentPosX = %CTL%.translateX;
    $currentPosY = %CTL%.translateY;
    $currentPosZ = %CTL%.translateZ;
    
    float $diffX = $currentPosX - $beforePosX;
    float $diffY = $currentPosY - $beforePosY;
    float $diffZ = $currentPosZ - $beforePosZ;
    
    float $powDistX = pow( $DX_x, 2 ) + pow( $DX_y, 2 ) + pow( $DX_z, 2 );
    float $powDistY = pow( $DY_x, 2 ) + pow( $DY_y, 2 ) + pow( $DY_z, 2 );
    float $powDistZ = pow( $DZ_x, 2 ) + pow( $DZ_y, 2 ) + pow( $DZ_z, 2 );
    
    float $projXValue = ( $diffX * $DX_x + $diffY * $DX_y + $diffZ * $DX_z )/$powDistX * $posWidthMult;
    float $projYValue = ( $diffX * $DY_x + $diffY * $DY_y + $diffZ * $DY_z )/$powDistY * $posHeightMult;
    float $projZValue = ( $diffX * $DZ_x + $diffY * $DZ_y + $diffZ * $DZ_z )/$powDistZ * $posWidthMult;
    
    $outputX += $projXValue * $DX_x + $projYValue * $DY_x + $projZValue * $DZ_x;
    $outputY += $projXValue * $DX_y + $projYValue * $DY_y + $projZValue * $DZ_y;
    $outputZ += $projXValue * $DX_z + $projYValue * $DY_z + $projZValue * $DZ_z;
    
    %CURRENTPOSTARGET%.translateX = $outputX;
    %CURRENTPOSTARGET%.translateY = $outputY;
    %CURRENTPOSTARGET%.translateZ = $outputZ;
    
    $beforePosX = $currentPosX;
    $beforePosY = $currentPosY;
    $beforePosZ = $currentPosZ;
}
"""


def setSimulationTransformMult( ctl, currentPosObj ):
    
    pos = cmds.getAttr( currentPosObj+'.wm' )
    
    dynamicDirObjX = cmds.createNode( 'transform', n='Dynamic_DirObjX' )
    dynamicDirObjY = cmds.createNode( 'transform', n='Dynamic_DirObjY' )
    dynamicDirObjZ = cmds.createNode( 'transform', n='Dynamic_DirObjZ' )
    dynamicDirObj  = cmds.createNode( 'transform', n='Dynamic_DirObj' )
    
    for target in [ dynamicDirObjX, dynamicDirObjY, dynamicDirObjZ, dynamicDirObj ]:
        cmds.setAttr( target+'.dh', 1 )
    
    dynamicDirObjP = cmds.group( dynamicDirObjX, dynamicDirObjY, dynamicDirObjZ, dynamicDirObj, n='PDynamic_DirObj' )
    
    cmds.xform( dynamicDirObjP, ws=1, matrix=pos )
    
    mtxToThree = cmds.createNode( 'matrixToThreeByThree' )
    
    cmds.connectAttr( dynamicDirObj+'.m', mtxToThree+'.inMatrix' )
    cmds.connectAttr( mtxToThree+'.o00', dynamicDirObjX+'.tx' )
    cmds.connectAttr( mtxToThree+'.o01', dynamicDirObjX+'.ty' )
    cmds.connectAttr( mtxToThree+'.o02', dynamicDirObjX+'.tz' )
    cmds.connectAttr( mtxToThree+'.o10', dynamicDirObjY+'.tx' )
    cmds.connectAttr( mtxToThree+'.o11', dynamicDirObjY+'.ty' )
    cmds.connectAttr( mtxToThree+'.o12', dynamicDirObjY+'.tz' )
    cmds.connectAttr( mtxToThree+'.o20', dynamicDirObjZ+'.tx' )
    cmds.connectAttr( mtxToThree+'.o21', dynamicDirObjZ+'.ty' )
    cmds.connectAttr( mtxToThree+'.o22', dynamicDirObjZ+'.tz' )
    
    dynamicOnAttrName  = 'dynamicOn'
    startFrameAttrName = 'startFrame'
    widthMultAttrName  = 'widthMult'
    heightMultAttrName = 'heightMult'
    
    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( ctl, ln= dynamicOnAttrName, at='long', cb=1, min=0, max=1 )
    sgBFunction_attribute.addAttr( ctl, ln= startFrameAttrName, at='long', cb=1 )
    sgBFunction_attribute.addAttr( ctl, ln= widthMultAttrName, at='double', k=1 )
    sgBFunction_attribute.addAttr( ctl, ln= heightMultAttrName, at='double', k=1 )
    
    expressionString = setSimulationTransformMult_expression.replace( '%CTL%', ctl )
    expressionString = expressionString.replace( '%DYNAMICON%', dynamicOnAttrName )
    expressionString = expressionString.replace( '%ATTRSTARTFRAME%', startFrameAttrName )
    expressionString = expressionString.replace( '%ATTRWIDTHMULT%',  widthMultAttrName )
    expressionString = expressionString.replace( '%ATTRHEIGHTMULT%', heightMultAttrName )
    expressionString = expressionString.replace( '%DX_X%', dynamicDirObjX )
    expressionString = expressionString.replace( '%DX_Y%', dynamicDirObjY )
    expressionString = expressionString.replace( '%DX_Z%', dynamicDirObjZ )
    expressionString = expressionString.replace( '%CURRENTPOSTARGET%', currentPosObj )
    
    cmds.expression( s= expressionString, o="", ae=1, uc='all' )


mc_setSimulationTransformMult = """import sgBFunction_hair
sels = cmds.ls( sl=1 )

sgBFunction_hair.setSimulationTransformMult( sels[0], sels[1] )"""




def makeControlJointOnCurve( curve ):
    
    import sgBFunction_dag
    
    crvShape = sgBFunction_dag.getShape( curve )
    crv = sgBFunction_dag.getTransform( curve )
    
    dagPathCurve = sgBFunction_dag.getMDagPath( crvShape )
    fnCurve = om.MFnNurbsCurve( dagPathCurve )
    
    cvs = om.MPointArray()
    fnCurve.getCVs( cvs )
    curveMtx = dagPathCurve.inclusiveMatrix()
    
    cmds.select( d=1 )
    jnts = []
    handles = []
    for i in range( cvs.length() ):
        pos = cvs[i] * curveMtx
        jnt = cmds.joint( p= [pos.x, pos.y, pos.z] )
        jnts.append( jnt )
    
    import sgBFunction_joint
    sgBFunction_joint.orientJointRelatives( jnts[0] )
    
    for i in range( cvs.length() ):
        handle = cmds.createNode( 'transform' )
        handles.append( handle )
        cmds.parent( handle, jnts[i] )
        cmds.setAttr( handle+'.t', 0,0,0 )
        cmds.setAttr( handle+'.dh', 1 )
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( handle+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( crv +'.wim', mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', crvShape+'.controlPoints[%d]' % i )



mc_makeControlJointOnCurve = """import sgBRig_hair
for sel in cmds.ls( sl=1 ):
    sgBRig_hair.makeControlJointOnCurve( sel )"""



def createCenterCurve( curves ):
    
    targetCurves = []
    degrees = 3
    
    allSpans = 0
    lenCurve = 0
    
    for curve in curves:
        curveShapes = cmds.listRelatives( curve, s=1, f=1 )
        if not curveShapes: continue
        allSpans += cmds.getAttr( curveShapes[0]+'.spans' )
        targetCurves.append( curveShapes[0] )
        lenCurve +=1
    
    if not lenCurve: return None
    
    avSpans = allSpans / lenCurve
    
    rebuildCurves = []
    for targetCurve in targetCurves:
        targetCurve = cmds.rebuildCurve( targetCurve, ch=1, 
                           rpo=1, rt=0, end=1, kr=0, kcp=0, 
                           kep=1, kt=0, s=avSpans, d=degrees, tol=0.01 )
        rebuildCurves.append( targetCurve )

    pointList = []
    for i in range( degrees + avSpans ):
        bbox = om.MBoundingBox()
        for targetCurve in targetCurves:
            bbox.expand( om.MPoint( *cmds.xform( targetCurve+'.cv[%d]' % i, q=1, ws=1, t=1 ) ) )
        vPos = bbox.center()
        pointList.append( [vPos.x, vPos.y, vPos.z] )
    
    centerCurve = cmds.curve( p=pointList, d=3 )
    
    import sgBFunction_attribute
    
    sgBFunction_attribute.addAttr( centerCurve, ln='srcCurve', at='message' )
    for curve in curves:
        sgBFunction_attribute.addAttr( curve, ln='centerCurve', at='message' )
        if cmds.isConnected( centerCurve + '.srcCurve', curve + '.centerCurve' ): continue
        cmds.connectAttr( centerCurve + '.srcCurve', curve + '.centerCurve', f=1 )
    
    return centerCurve




def createCenterRadiusEditCurve( curves ):
    
    import sgBFunction_dag
    import sgBFunction_attribute
    
    centerCurve = createCenterCurve( curves )
    centerCurveShape = sgBFunction_dag.getShape( centerCurve )
    cmds.setAttr( centerCurveShape+'.overrideEnabled', 1 )
    cmds.setAttr( centerCurveShape+'.overrideColor', 4 )
    
    allCurves = curves + [ centerCurve ]
    for curve in allCurves:
        sgBFunction_attribute.addAttr( curve, ln='toCenter', dv=0 )
        cmds.setAttr( curve+'.toCenter', e=1, k=1 )
    
    for curve in curves:
        blendShapeNode = cmds.blendShape( centerCurve, curve )[0]
        cmds.connectAttr( curve+'.toCenter', blendShapeNode+'.w[0]' )
        curveShape = sgBFunction_dag.getShape( curve )
        cmds.setAttr( curveShape+'.overrideEnabled', 1 )
        cmds.setAttr( curveShape+'.overrideColor', 24 )
    
    cmds.select( allCurves )
    return allCurves



mc_setCurvesAsRadiusCurve = """import sgBRig_hair
sgBRig_hair.createCenterRadiusEditCurve( cmds.ls( sl=1 ) )
"""



def createControledCurve( topJoints, addName ):
    
    import sgBFunction_convert
    import sgBFunction_dag
    
    topJoints = sgBFunction_convert.singleToList( topJoints )
    topJoints = sgBFunction_dag.getTopJointChildren(topJoints)
    
    controledCurves = []
    for topJoint in topJoints:
        
        endJnt = cmds.listRelatives( topJoint, c=1, ad=1, f=1 )[0]
        
        controledCurve = cmds.createNode( 'sgHair_controledCurve' )
        cmds.connectAttr( topJoint+'.message', controledCurve+'.topJoint' )
        cmds.connectAttr( endJnt+'.wm', controledCurve+'.endJointMatrix' )
        curveShape = cmds.createNode( 'nurbsCurve' )
        #rebuild    = cmds.createNode( 'rebuildCurve' )
        #cmds.setAttr( rebuild+'.keepControlPoints', 1 )
        #cmds.connectAttr( controledCurve+'.outputCurve', rebuild+'.inputCurve' )
        #cmds.connectAttr( rebuild+'.outputCurve', curveShape+'.create' )
        cmds.connectAttr( controledCurve+'.outputCurve', curveShape+'.create' )
        topJointParent = cmds.listRelatives( topJoint, p=1, f=1 )
        if not topJointParent: topJointParent = topJoint
        else: topJointParent = topJointParent[0]
        curveObj = cmds.listRelatives( curveShape, p=1, f=1 )[0]
        curveObj = cmds.rename( curveObj, topJointParent.split('|')[-1]+addName )
        controledCurves.append( curveObj )

    return controledCurves



def createControledCurveB( targetDags, rebuild=False ):
    
    controledCurve = cmds.createNode( 'sgHair_controledCurveB' )
    curveShape = cmds.createNode( 'nurbsCurve' )
    if rebuild:
        rebuild = cmds.createNode( 'rebuildCurve' )
        cmds.setAttr( rebuild+'.keepControlPoints', 1 )
        cmds.connectAttr( controledCurve+'.outputCurve', rebuild+'.inputCurve' )
        cmds.connectAttr( rebuild+'.outputCurve', curveShape+'.create' )
    else:
        cmds.connectAttr( controledCurve+'.outputCurve', curveShape+'.create' )
    curve = cmds.listRelatives( curveShape, p=1, f=1 )[0]
    
    for i in range( len( targetDags ) ):
        cmds.connectAttr( targetDags[i]+'.wm', controledCurve+'.inputMatrix[%d]' % i )
    cmds.connectAttr( curve+'.wim', controledCurve+'.parentInverseMatrix' )
    
    curve = cmds.rename( curve, 'conedCrv' )
    
    return curve





def createControlJoint( curves, headJoint=None, prefix='Control_', staticRotation=False ):
    
    import sgBFunction_convert
    import sgBFunction_dag
    import sgBFunction_attribute
    import sgBFunction_connection
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )
    
    if headJoint == None: 
        headJoint = cmds.createNode( 'joint' )
    
    curves = sgBFunction_convert.singleToList(curves)
    curves = sgBFunction_dag.getChildrenShapeExists(curves)
    
    jntGrps = []
    
    gravityObjWorld  = cmds.createNode( 'transform', n = prefix+'GravityObjectWorld' )
    gravityObjLocal  = cmds.createNode( 'transform', n = prefix+'GravityObjectLocal' )
    gravityObjLocalP = cmds.createNode( 'transform', n = prefix+'GravityObjectLocalP' )
    
    sgBFunction_connection.constraint( gravityObjWorld, gravityObjLocal )
    gravityObjLocalP = cmds.parent( gravityObjLocalP, headJoint )
    gravityObjLocal = cmds.parent( gravityObjLocal, gravityObjLocalP )[0]
    
    controlJoints = []
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        fnCurve = om.MFnNurbsCurve( sgBFunction_dag.getMDagPath( curveShape ) )
        numCVs = fnCurve.numCVs()
        
        controlJointNode = cmds.createNode( 'sgHair_controlJoint' )
        cmds.setAttr( controlJointNode+'.staticRotation', 1 )
        
        cmds.connectAttr( curveShape+'.local', controlJointNode+'.inputBaseCurve' )
        cmds.connectAttr( curveShape+'.wm', controlJointNode+'.inputBaseCurveMatrix' )
        
        cmds.select( d=1 )
        jnts = []
        for i in range( numCVs ):
            jnt = cmds.joint()
            cmds.connectAttr( controlJointNode+'.output[%d].outTrans' % i, jnt+'.t' )
            cmds.connectAttr( controlJointNode+'.output[%d].outRotate' % i, jnt+'.jo' )
            jnts.append( jnt )
        
        cutInfos = sgBFunction_dag.getNodeFromHistory( curve, 'sgHair_cutInfo' )
        
        jntGrp = cmds.createNode( 'transform' )
        if cutInfos:
            follicles = cmds.listConnections( cutInfos[0]+'.outU', type='follicle' )
            targetFollicle = follicles[0]
            cmds.xform( jntGrp, ws=1, matrix= cmds.getAttr( targetFollicle+'.wm' ) )
        else:
            targetFollicle = None
            cmds.xform( jntGrp, ws=1, matrix= cmds.getAttr( jnts[0]+'.wm' ) )
        
        jnts[0] = cmds.parent( jnts[0], jntGrp )[0]
        if targetFollicle:
            cmds.connectAttr( targetFollicle+'.wm', controlJointNode+'.jointParentBaseMatrix', f=1 )
            cmds.connectAttr( targetFollicle+'.t', jntGrp+'.t' )
            cmds.connectAttr( targetFollicle+'.r', jntGrp+'.r' )
        else:
            cmds.connectAttr( jntGrp+'.wm', controlJointNode+'.jointParentBaseMatrix', f=1 )
        
        sgBFunction_attribute.addAttr( jntGrp, ln='global_param', dv=0, k=1 )
        sgBFunction_attribute.addAttr( jntGrp, ln='global_range', dv=0, k=1 )
        sgBFunction_attribute.addAttr( jntGrp, ln='global_weight', min=0.0, max=1.0, dv=1, k=1 )
        sgBFunction_attribute.addAttr( jntGrp, ln='gravityParam', min=0.0, dv=numCVs/2.0, k=1 )
        sgBFunction_attribute.addAttr( jntGrp, ln='gravityRange', min=0.0, max=numCVs, dv=numCVs/4.0, k=1 )
        sgBFunction_attribute.addAttr( jntGrp, ln='gravityWeight', min=0.0, max=1.0, dv=1, k=1 )
        
        paramAdd = cmds.createNode( 'addDoubleLinear' )
        rangeAdd = cmds.createNode( 'addDoubleLinear' )
        weightMult = cmds.createNode( 'multDoubleLinear' )
        
        cmds.connectAttr( jntGrp+'.global_param', paramAdd+'.input1' )
        cmds.connectAttr( jntGrp+'.global_range', rangeAdd+'.input1' )
        cmds.connectAttr( jntGrp+'.global_weight', weightMult+'.input1' )
        cmds.connectAttr( jntGrp+'.gravityParam', paramAdd+'.input2' )
        cmds.connectAttr( jntGrp+'.gravityRange', rangeAdd+'.input2' )
        cmds.connectAttr( jntGrp+'.gravityWeight', weightMult+'.input2' )
        
        cmds.connectAttr( paramAdd+'.output',   controlJointNode+'.gravityParam' )
        cmds.connectAttr( rangeAdd+'.output',   controlJointNode+'.gravityRange' )
        cmds.connectAttr( weightMult+'.output', controlJointNode+'.gravityWeight' )
        cmds.connectAttr( gravityObjLocal+'.m', controlJointNode+'.gravityOffsetMatrix')
        
        controlJoints.append( sgBFunction_dag.getMObject( jnts[0] ) )
        jntGrp = cmds.rename( jntGrp, prefix+curve.split( '|' )[-1] )
        jntGrps.append( jntGrp )
    
    grp = cmds.createNode( 'transform', n = prefix+'ControlJoints' )
    cmds.parent( jntGrps, grp )
    controlJointConedObj = cmds.createNode( 'transform', n= prefix+'PControlJoints' )
    sgBFunction_connection.constraintAll( headJoint, controlJointConedObj )
    grp = cmds.parent( grp, controlJointConedObj )
    
    for attr in ['global_param', 'global_range', 'global_weight']:
        sgBFunction_attribute.copyAttribute( jntGrps[0]+'.'+attr , controlJointConedObj )
    for attr in ['global_param', 'global_range', 'global_weight']:
        sgBFunction_attribute.copyAttribute( controlJointConedObj+'.'+attr , headJoint )
        cmds.connectAttr( headJoint+'.'+attr, controlJointConedObj+'.'+attr )
    
    for i in range( len( jntGrps ) ):
        for attr in ['global_param', 'global_range', 'global_weight']:
            cmds.connectAttr( controlJointConedObj+'.'+attr, jntGrps[i]+'.'+attr )
    
    return controlJoints





def startPointAttachCurve( curve, pointObj, createNew= False ):
    
    import sgBFunction_dag
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )

    curveName = curve.split( '|' )[-1]
    
    attachStartPointCurve = cmds.createNode( 'sgHair_attachStartPointCurve' )
    rebuildCurveNode = cmds.createNode( 'rebuildCurve' )
    cmds.setAttr( rebuildCurveNode+'.keepControlPoints', 1 )
    
    if createNew:
        newCurveShape = cmds.createNode( 'nurbsCurve' )
        newCurve = cmds.listRelatives( newCurveShape, p=1, f=1 )[0]
        curveShape = sgBFunction_dag.getShape( curve )
        cmds.connectAttr( curveShape+'.local', attachStartPointCurve+'.inputCurve' )
        cmds.connectAttr( curveShape+'.wm', attachStartPointCurve+'.inputCurveMatrix' )
        cmds.connectAttr( pointObj+'.wm', attachStartPointCurve+'.inputMatrix' )
        cmds.connectAttr( attachStartPointCurve+'.outputCurve', rebuildCurveNode + '.inputCurve' )
        cmds.connectAttr( rebuildCurveNode+'.outputCurve', newCurveShape+'.create' )
    
        newCurve = cmds.rename( newCurve, curveName.split( '|' )[-1]+'_new' )
        return newCurve
    else:
        curveShape = sgBFunction_dag.getShape( curve )
        srcCon = cmds.listConnections( curveShape + '.create', p=1 )
        if not srcCon:
            ioShape = sgBFunction_dag.addIOShape( curve )
            outputAttr = ioShape + '.local'
            curveMtxAttr = ioShape + '.wm'
        else:
            outputAttr = srcCon[0]
            curveMtxAttr = curveShape + '.wm'
        
        cmds.connectAttr( outputAttr, attachStartPointCurve+'.inputCurve' )
        cmds.connectAttr( curveMtxAttr, attachStartPointCurve+'.inputCurveMatrix' )
        cmds.connectAttr( pointObj+'.wm', attachStartPointCurve+'.inputMatrix' )
        cmds.connectAttr( attachStartPointCurve+'.outputCurve', rebuildCurveNode + '.inputCurve' )
        cmds.connectAttr( rebuildCurveNode+'.outputCurve', curveShape+'.create', f=1 )
        return curve




def setStartPointAttachCurvesToMesh( curves, mesh, createNew = False ):
    
    import sgBFunction_dag
    import sgBFunction_base
    import sgBFunction_mesh
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )
    points = getCuttingPoints( curves, mesh )
    
    meshShape = sgBFunction_dag.getShape( mesh )
    
    returnCurves = []
    for i in range( len( curves ) ):
        curveName = curves[i].split( '|' )[-1]
        u, v = sgBFunction_mesh.getUVAtPoint( points[i], mesh )
        follicle = cmds.createNode( 'follicle' )
        follicleObj = sgBFunction_dag.getTransform( follicle )
        
        cmds.connectAttr( meshShape+'.outMesh', follicle+'.inputMesh' )
        cmds.connectAttr( meshShape+'.wm', follicle+'.inputWorldMatrix' )
        cmds.setAttr( follicle+'.parameterU', u )
        cmds.setAttr( follicle+'.parameterV', v )
        cmds.connectAttr( follicle+'.outTranslate', follicleObj+'.t' )
        cmds.connectAttr( follicle+'.outRotate', follicleObj+'.r' )
        
        follicleObj = cmds.rename( follicleObj, 'cutFollicle_' + curveName )
        
        returnCurve = startPointAttachCurve( curves[i], follicleObj, createNew )
        returnCurves.append( returnCurve )
        
    return returnCurves





def createPfxHairFromCurves( curveGroups ):

    import sgBFunction_dag

    children = cmds.listRelatives( curveGroups, c=1, ad=1, f=1, type='transform' )

    targetCurves = []
    for child in children:
        childShape = sgBFunction_dag.getShape( child )
        if not childShape: continue
        if not cmds.nodeType( childShape ) == 'nurbsCurve': continue
        targetCurves.append( childShape )    

    hairSystem = cmds.createNode( 'hairSystem' )
    cmds.connectAttr( 'time1.outTime', hairSystem+'.currentTime' )
    pfxHair = cmds.createNode( 'pfxHair' )
    cmds.connectAttr( hairSystem+'.outputRenderHairs', pfxHair+'.renderHairs' )
    
    index = 0
    follicles = []
    for targetCurve in targetCurves:
        follicle = cmds.createNode( 'follicle' )
        cmds.setAttr( follicle+'.simulationMethod', 0 )
        cmds.setAttr( follicle+'.startDirection', 1 )
        follicleObj = cmds.listRelatives( follicle, p=1, f=1 )[0]
        follicles.append( follicleObj ) 
        cmds.connectAttr( targetCurve+'.worldSpace', follicle+'.startPosition' )
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % index )
        index += 1
    follicleGroup = cmds.createNode( 'transform', n='grpPfxFollicle' )
    follicles = cmds.parent( follicles, follicleGroup )



def createRampSurface_targetAttribute( targets, attr ):
    
    import maya.mel as mel
    import sgBFunction_attribute
    
    ramp = cmds.shadingNode( 'ramp', asTexture=1, n='ramp_%s' % attr )
    surfObject = cmds.nurbsPlane( ch=1, p=[0, 0, 0], ax=[0, 1, 0], w=1, lr=1, d=3, u=1, v=1, n= 'surf_%s' % attr )[0]
    mel.eval( 'hypergraphAssignTextureToSelection %s' % ramp )
    
    sgBFunction_attribute.addAttr( surfObject, ln='targetRampAttr', dt='string')
    sgBFunction_attribute.addAttr( surfObject, ln='targetRampNodes', dt='string')
    sgBFunction_attribute.addAttr( surfObject, ln='default', dv= cmds.getAttr( targets[0]+'.'+attr ), cb=1 )
    sgBFunction_attribute.addAttr( surfObject, ln='min', k=1 )
    sgBFunction_attribute.addAttr( surfObject, ln='max', k=1  )
    sgBFunction_attribute.addAttr( surfObject, ln='rand', k=1 )
    
    cmds.setAttr( surfObject+'.targetRampAttr', attr, type='string' )



def createCurveToEdgeLoop_():
    
    sels = cmds.ls( sl=1, fl=1 )
    selObject = cmds.ls( sl=1, o=1 )[0]
    selObject = cmds.listRelatives( selObject, p=1 )[0]
    excutedEdges = []
    curves = []
    for sel in sels:
        if sel in excutedEdges: continue
        cmds.select( sel )
        cmds.SelectEdgeLoopSp()
        excutedEdges += cmds.ls(sl=1, fl=1 )
        curves.append( cmds.polyToCurve( form=0, degree=3 )[0] )
    
    cmds.select( curves )
    cmds.DeleteHistory()
    return cmds.ls( sl=1 )


def createCurveToEdgeLoop():
    
    import sgBFunction_dag
    
    sels = cmds.ls( sl=1, fl=1 )
    selObject = cmds.ls( sl=1, o=1 )[0]
    selObject = cmds.listRelatives( selObject, p=1 )[0]
    excutedEdges = []
    curves = []
    allSpans = 0
    for sel in sels:
        if sel in excutedEdges: continue
        cmds.select( sel )
        cmds.SelectEdgeLoopSp()
        excutedEdges += cmds.ls(sl=1, fl=1 )
        curve = cmds.polyToCurve( form=0, degree=3 )[0]
        curveShape = sgBFunction_dag.getShape( curve )
        spans = cmds.getAttr( curveShape+'.spans' )
        allSpans += spans
        curves.append( curve )
    
    eachSpans = allSpans / len( curves )
    
    for curve in curves:
        cmds.rebuildCurve( curve, ch=0, 
                           rpo=1, rt=0, end=1, kr=0, kcp=0, 
                           kep=1, kt=0, s=eachSpans, d=3, tol=0.01 )
    
    cmds.select( curves )
    return curves



def setRandomColor():
    import sgBModel_data
    
    currentColorIndex = sgBModel_data.globalColorIndex % 32
    
    if sgBModel_data.globalColorIndex in [ 16, 19, 20, 1 ]:
        sgBModel_data.globalColorIndex +=1
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        selShapes = cmds.listRelatives( sel, s=1 )
        if selShapes:
            if cmds.getAttr( selShapes[0]+'.overrideEnabled' ):
                cmds.setAttr( selShapes[0]+'.overrideEnabled', 0 )
        cmds.setAttr( sel+'.overrideEnabled', 1 )
        cmds.setAttr( sel+'.overrideColor', currentColorIndex )
    
    sgBModel_data.globalColorIndex += 1
    
    
    
def clearCurveDirection( curves ):
    
    import sgBFunction_dag
    import copy
    
    tangents = []
    
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        dagPath = sgBFunction_dag.getMDagPath( curveShape ) 
        minParam = cmds.getAttr( curveShape+'.min' )
        maxParam = cmds.getAttr( curveShape+'.max' )
        fnCurve = om.MFnNurbsCurve( dagPath )
        tangent = fnCurve.tangent( (minParam+maxParam)/2.0 )
        tangents.append( tangent*dagPath.inclusiveMatrix() )
    
    rootTangent = copy.copy( tangents[0] )
    
    defaultIndices = []
    inverseIndices = []
    for i in range( len( tangents ) ):
        if rootTangent * tangents[i] > 0:
            defaultIndices.append( i )
        else:
            inverseIndices.append( i )
    
    reveseCurves = []
    if len( defaultIndices ) < len( inverseIndices ):
        for i in inverseIndices:
            reveseCurves.append( curves[i] )
            cmds.reverseCurve( curves[i] )
    else:
        for i in defaultIndices:
            reveseCurves.append( curves[i] )
            cmds.reverseCurve( curves[i] )

    cmds.select( curves )
    return reveseCurves






def createCurveFromEdgeRing( edge, num=1000000 ):
    
    import sgBFunction_selection
    
    sels = cmds.ls( sl=1, fl=1 )
    edges = sgBFunction_selection.getSpecifyNumEdgeRing( sels[0], num ) 
    
    cmds.select( edges )
    meshShape = cmds.listRelatives( edges[0], p=1 )[0]
    meshObject = cmds.listRelatives( meshShape, p=1 )[0]
    
    curves = createCurveToEdgeLoop()
    clearCurveDirection( curves )
    curves = createCenterRadiusEditCurve( curves )
    
    for curve in curves:
        cmds.setAttr( curve+'.toCenter', 0.2 )
    
    cmds.setAttr( meshObject +'.v', 0 )
    
    setRandomColor()




def createRadiusSetFromEdge( num ):
    
    import sgBFunction_selection
    
    sels = cmds.ls( sl=1, fl=1 )
    edges = sgBFunction_selection.getSpecifyNumEdgeRing( sels[0], num ) 
    
    cmds.select( edges )
    meshShape = cmds.listRelatives( edges[0], p=1 )[0]
    meshObject = cmds.listRelatives( meshShape, p=1 )[0]
    
    curves = createCurveToEdgeLoop()
    clearCurveDirection(curves)
    curves = createCenterRadiusEditCurve( curves )
    
    for curve in curves:
        cmds.setAttr( curve+'.toCenter', 0.2 )
    
    cmds.setAttr( meshObject +'.v', 0 )
    
    setRandomColor()




def reverseCurveByObject( curves, targetObject ):
    
    import sgBFunction_dag
    
    curves = sgBFunction_dag.getChildrenShapeExists( curves )
    
    trgObjPoint = om.MPoint( *cmds.xform( targetObject, q=1, ws=1, t=1 ) )
    
    for curve in curves:
        
        curveShape = sgBFunction_dag.getShape( curve )
        spans = cmds.getAttr( curveShape+'.spans' )
        degree = cmds.getAttr( curveShape+'.degree' )
        startPoint = om.MPoint( *cmds.xform( curve+'.cv[%d]' % 0, q=1, ws=1, t=1 ) )
        endPoint   = om.MPoint( *cmds.xform( curve+'.cv[%d]' % (spans+degree-1), q=1, ws=1, t=1 ) )
        
        distStart = trgObjPoint.distanceTo( startPoint )
        distEnd   = trgObjPoint.distanceTo( endPoint )
        
        if distStart > distEnd:
            cmds.reverseCurve( curve )



def rebuildCurvesSameSpans( curves, degree=3 ):
    
    import sgBFunction_dag
    
    curves = sgBFunction_dag.getChildrenShapeExists( curves )
    
    allSpans = 0
    for curve in curves:
        curveShape = sgBFunction_dag.getShape( curve )
        allSpans += cmds.getAttr( curveShape+'.spans' )
    
    eachSpans = allSpans / len( curves )
    
    for curve in curves:
        cmds.rebuildCurve( curve, constructionHistory=0, 
                           replaceOriginal=1,
                           rebuildType=0, 
                           endKnots=1, 
                           keepRange=0, 
                           keepControlPoints=0, 
                           keepEndPoints=1, 
                           keepTangents=0,
                           s=eachSpans, d=degree, tol=0.01 )




def createSurfaceFromCurve( curve, radius=1 ):
    
    import sgBFunction_dag
    import sgBFunction_attribute
    
    targetShape = sgBFunction_dag.getShape( curve )
    
    dagPath = sgBFunction_dag.getMDagPath( targetShape )
    fnNurbsCurve = om.MFnNurbsCurve( dagPath )
    minParam = fnNurbsCurve.findParamFromLength( 0 )
    tangent = fnNurbsCurve.tangent( minParam ) * dagPath.inclusiveMatrix()
    point = om.MPoint()
    fnNurbsCurve.getCV( 0, point )
    
    pointOnCurveNode = cmds.createNode( 'pointOnCurveInfo' )
    cmds.connectAttr( targetShape+'.worldSpace', pointOnCurveNode+'.inputCurve' )
    
    circleObj, circleNode = cmds.circle( sections=3, normal=[ tangent.x, tangent.y, tangent.z ], 
                                   center=[ point.x, point.y, point.z ], radius= radius )
    cmds.connectAttr( pointOnCurveNode+'.position', circleNode+'.center' )
    cmds.connectAttr( pointOnCurveNode+'.tangent', circleNode+'.normal' )
    
    surface, extrudeNode = cmds.extrude( circleObj, curve,
                  ch=1, rn=0, po=0, et=2, ucp=0, fpt=0, upn=1, rotation=0,
                  scale=1, rsp=1 )
    cmds.setAttr( extrudeNode+'.scale', 0 )
    
    sgBFunction_attribute.addAttr( surface, ln='startRadius', min=0, dv=radius, k=1 )
    sgBFunction_attribute.addAttr( surface, ln='endRadius', min=0, dv=radius, k=1 )
    
    multNode = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( multNode+'.op', 2 )
    cmds.connectAttr( surface+'.endRadius', multNode+'.input1X' )
    cmds.connectAttr( surface+'.startRadius',    multNode+'.input2X' ) 
    
    cmds.connectAttr( surface+'.startRadius', circleNode+'.radius' )
    cmds.connectAttr( multNode+'.outputX',     extrudeNode+'.scale' )
    
    return surface




def createRadiusCurveFromCenter( target, radius=1 ):

    import sgBFunction_dag
    import sgCFnc_dag
    
    targetShape = sgBFunction_dag.getShape( target )
    
    dagPath = sgBFunction_dag.getMDagPath( targetShape )
    fnNurbsCurve = om.MFnNurbsCurve( dagPath )
    minParam = fnNurbsCurve.findParamFromLength( 0 )
    tangent = fnNurbsCurve.tangent( minParam ) * dagPath.inclusiveMatrix()
    point = om.MPoint()
    fnNurbsCurve.getCV( 0, point )
    
    circleObj, node = cmds.circle( sections=3, normal=[ tangent.x, tangent.y, tangent.z ], 
                                   center=[ point.x, point.y, point.z ], radius= radius )
    
    surface, node = cmds.extrude( circleObj, target,
                  ch=1, rn=0, po=0, et=2, ucp=0, fpt=0, upn=1, rotation=0,
                  scale=1, rsp=1 )
    
    numCVs = fnNurbsCurve.numCVs()
    values = [0, 0.0723, 0.263, 0.5, 0.737, 0.928, 1]
    
    cvNums = range( numCVs )
    cvNums.reverse()
    for i in range( len( values ) ):
        cvs = surface+'.cv[0:3][%d]' % cvNums[i]
        cmds.select( cvs )
        centerPoint = om.MVector( sgCFnc_dag.getMBoundingBoxFromSelection().center() )
        
        for cv in cmds.ls( cvs, fl=1 ):
            eachPoint = om.MVector( *cmds.xform( cv, q=1, ws=1, t=1 ) ) 
            vDiff = eachPoint - centerPoint
            vDiff *= values[i]
            vPoint = vDiff + centerPoint
            cmds.move( vPoint.x, vPoint.y, vPoint.z, cv, ws=1 )
    
    curves = []
    for i in range( 4 ):
        curve = cmds.duplicateCurve( surface+'.u[%d]' % i, ch=1, rn=0, local=0 )[0]
        curves.append( curve )
    
    cmds.select( curves )
    cmds.DeleteHistory()
    
    cmds.delete( circleObj, surface )




def walkJointOnMeshTube( jnt, mesh, walkDist=1 ):
    
    import sgBFunction_dag
    import math
    import copy
    
    meshShape = sgBFunction_dag.getShape( mesh )
    dagPathMesh = sgBFunction_dag.getMDagPath( meshShape )
    fnMesh = om.MFnMesh( dagPathMesh )
    intersector = om.MMeshIntersector()
    intersector.create( dagPathMesh.node() )
    
    dagPathJnt = sgBFunction_dag.getMDagPath( jnt )
    
    mtxJnt = dagPathJnt.inclusiveMatrix()
    vX = om.MVector( mtxJnt[0] )
    vY = om.MVector( mtxJnt[1] )
    vZ = om.MVector( mtxJnt[2] )
    pP = om.MPoint( mtxJnt[3] )
    
    pJnt = cmds.listRelatives( jnt, p=1, f=1 )
    if pJnt:
        pDagPathJnt = sgBFunction_dag.getMDagPath( pJnt[0] )
        mtxPJnt = pDagPathJnt.inclusiveMatrix()
        pParentP = om.MPoint( mtxPJnt[3] )
        vX = om.MVector( pP - pParentP )
        
        vY = vZ ^ vX
        vZ = vX ^ vY
        
    vX.normalize()
    vY.normalize()
    vZ.normalize()

    eachRad = math.pi / 4
    successPoints = om.MPointArray()
    
    pointOnMesh = om.MPointOnMesh()
    resultDirection = om.MVector()
    
    intersectPoints = om.MPointArray()
    for i in range( 8 ):
        vD = vY * math.sin( eachRad * i ) + vZ * math.cos( eachRad* i )
        fnMesh.intersect( pP, vD, intersectPoints )
        if not intersectPoints.length(): continue
        
        intersector.getClosestPoint( intersectPoints[0], pointOnMesh )
        normal = om.MVector( pointOnMesh.getNormal() )
        
        #projNormal = vX * (normal * vX) / (vX.length()**2)
        
        #vertNormal = normal - projNormal
        
        cross = normal ^ vX
        dCross = cross ^ normal

        successPoints.append( intersectPoints[0] )
        resultDirection += dCross
    
    if successPoints.length() != 8:
        print "joint move out"
        return None

    bb = om.MBoundingBox()
    for i in range( successPoints.length() ):
        bb.expand( successPoints[i] )
    pP = bb.center()
    
    wP = pP
    cmds.move( wP.x, wP.y, wP.z, jnt, ws=1 )
    
    resultDirection.normalize()
    resultDirection *= walkDist
    
    
    rvX = resultDirection
    rvZ = rvX ^ om.MVector( 0,1,0 )
    rvY = rvZ ^ rvX
    walkJointPos = pP + resultDirection
    rvX.normalize()
    rvY.normalize()
    rvZ.normalize()
    
    mtx = [ rvX.x, rvX.y, rvX.z, 0.0, 
            rvY.x, rvY.y, rvY.z, 0.0,
            rvZ.x, rvZ.y, rvZ.z, 0.0,
            walkJointPos.x, walkJointPos.y, walkJointPos.z, 1.0 ]
    
    cmds.select( jnt )
    chJnt = cmds.joint( rad= cmds.getAttr( jnt+'.radius' ) )
    
    cmds.xform( chJnt, ws=1, matrix=mtx )
    
    cmds.refresh()
    
    return chJnt



def contrainCurveToMesh( curves, mesh ):
    
    import sgBFunction_dag
    import sgBFunction_connection
    
    curves = sgBFunction_dag.getChildrenCurveExists( curves )
    
    follicles = createFollicleToCuttingPoint( curves, mesh )
    jnts = []

    for i in range( len( follicles ) ):
        selName = follicles[i].split( '|' )[-1]
        jntName = selName.replace( 'cutFollicle_', 'constJnt_' )
        jnt = cmds.createNode( 'joint', n=jntName )
        sgBFunction_connection.constraint( follicles[i], jnt )
        jnts.append( jnt )
        sgBFunction_connection.bindConnect( curves[i], jnt )
    
    cmds.group( follicles, n= 'follicles_' + mesh )
    cmds.group( jnts, n= 'constJnts_' + mesh )



def bindCurveToMesh( curves, mesh ):
    
    import sgBFunction_dag
    import sgBFunction_connection
    
    curves = sgBFunction_dag.getChildrenCurveExists( curves )
    
    follicles = createFollicleToCuttingPoint( curves, mesh )
    jnts = []

    for i in range( len( follicles ) ):
        selName = follicles[i].split( '|' )[-1]
        jntName = selName.replace( 'cutFollicle_', 'constJnt_' )
        jnt = cmds.createNode( 'joint', n=jntName )
        sgBFunction_connection.constraint( follicles[i], jnt )
        jnts.append( jnt )
        cmds.skinCluster( curves[i], jnt )

    cmds.group( follicles, n= 'follicles_' + mesh  )
    cmds.group( jnts, n= 'constJnts_' + mesh )



def addTranslateMultAttributeToHair( curves, ctl ):
    
    def getOffsetObject( ctl ):
        
        import sgBFunction_connection
        
        ctlName = ctl.split( '|' )[-1]
        ctlPos = cmds.getAttr( ctlName+'.wm' )
        
        startObject = 'startPosition_' + ctlName
        dirObject   = 'dirrection_' + ctlName
        offsetObject  = 'offsetObject_' + ctlName
        
        if not cmds.objExists( startObject ):
            startObject = cmds.createNode( 'transform', n=startObject )
            cmds.xform( startObject, ws=1, matrix= ctlPos )
        if not cmds.objExists( dirObject ):
            dirObject = cmds.createNode( 'transform', n= dirObject )
            cmds.xform( dirObject, ws=1, matrix= ctlPos )
            dirObject = cmds.parent( dirObject, startObject )[0]
        if not cmds.objExists( offsetObject ):
            offsetObject = cmds.createNode( 'transform', n= offsetObject )
            cmds.xform( offsetObject, ws=1, matrix= ctlPos )
            offsetObject = cmds.parent( offsetObject, dirObject )[0]
            cmds.setAttr( offsetObject+'.dh', 1 )
            
            mmdc = cmds.createNode( 'multMatrixDecompose' )
            cmds.connectAttr( ctl+'.wm', mmdc+'.i[0]' )
            cmds.connectAttr( dirObject+'.wim', mmdc+'.i[1]' )
            cmds.connectAttr( mmdc+'.ot', offsetObject+'.t' )
    
            sgBFunction_connection.constraintOrient( ctl, offsetObject )
            sgBFunction_connection.addMultDoubleLinearConnection( offsetObject, 'tx' )
            sgBFunction_connection.addMultDoubleLinearConnection( offsetObject, 'ty' )
            sgBFunction_connection.addMultDoubleLinearConnection( offsetObject, 'tz' )
        
        cmds.setAttr( startObject + '.r', 0,0,0 )
        
        return offsetObject
    
    def getBeforeAndAfterComposeMatrix( offsetObj, ctl ):
        
        import sgBFunction_attribute
        dcmpOffsetObjCons = cmds.listConnections( offsetObj+'.wm', type='decomposeMatrix' )
        if not dcmpOffsetObjCons:
            dcmpOffsetObj = cmds.createNode( 'decomposeMatrix' )
            cmds.connectAttr( offsetObj+'.wm', dcmpOffsetObj+'.imat' )
        else:
            dcmpOffsetObj = dcmpOffsetObjCons[0]
        dcmpCtlCons = cmds.listConnections( ctl+'.wm', type='decomposeMatrix' )
        if not dcmpCtlCons:
            dcmpCtl = cmds.createNode( 'decomposeMatrix' )
            cmds.connectAttr( ctl+'.wm', dcmpCtl+'.imat' )
        else:
            dcmpCtl = dcmpCtlCons[0]
        
        sgBFunction_attribute.addAttr( offsetObj, ln='beforeCompose', at='message' )
        sgBFunction_attribute.addAttr( offsetObj, ln='afterCompose', at='message' )
        
        beforeCons = cmds.listConnections( offsetObj+'.beforeCompose', s=1, d=0, type='composeMatrix' )
        afterCons  = cmds.listConnections( offsetObj+'.afterCompose', s=1, d=0, type='composeMatrix' )
        
        if not beforeCons:
            addNodeBefore = cmds.createNode( 'plusMinusAverage' )
            beforeCompose = cmds.createNode( 'composeMatrix' )
            cmds.setAttr( addNodeBefore+'.op', 2 )
            cmds.connectAttr( dcmpOffsetObj+'.ot', addNodeBefore+'.input3D[0]' )
            cmds.connectAttr( dcmpCtl+'.ot', addNodeBefore+'.input3D[1]' )
            cmds.connectAttr( addNodeBefore+'.output3D', beforeCompose+'.it' )
        else:
            beforeCompose = beforeCons[0]

        if not afterCons:
            addNodeAfter = cmds.createNode( 'plusMinusAverage' )
            afterCompose = cmds.createNode( 'composeMatrix' )
            cmds.setAttr( addNodeAfter+'.op', 2 )
            cmds.connectAttr( dcmpOffsetObj+'.ot', addNodeAfter+'.input3D[1]' )
            cmds.connectAttr( dcmpCtl+'.ot', addNodeAfter+'.input3D[0]' )
            cmds.connectAttr( addNodeAfter+'.output3D', afterCompose+'.it' )
        else:
            afterCompose = afterCons[0]
        
        return beforeCompose, afterCompose
        
        
    
    import sgBFunction_dag
    
    curves = sgBFunction_dag.getChildrenCurveExists( curves )
    offsetObject = getOffsetObject( ctl )
    beforeCompose, afterCompose = getBeforeAndAfterComposeMatrix( offsetObject, ctl )
    
    for curve in curves:
        follicleNodes = sgBFunction_dag.getNodeFromHistory( curve, 'follicle' )
        if not follicleNodes:
            continue
        
        follicleNode = follicleNodes[0]
        
        srcCon = cmds.listConnections( follicleNode+'.startPosition', p=1 )[0]
        srcNode = srcCon.split( '.' )[0]
        rebuildCon = cmds.listConnections( srcNode, s=1, d=0, type='rebuildCurve', p=1 )[0]
        dstCon = cmds.listConnections( follicleNode+'.outCurve', p=1 )[0]
        
        trGeo = cmds.createNode( 'transformGeometry' )
        cmds.connectAttr( rebuildCon, trGeo+'.inputGeometry' )
        cmds.connectAttr( beforeCompose+'.outputMatrix', trGeo+'.transform' )
        cmds.connectAttr( trGeo+'.outputGeometry', srcNode+'.create', f=1 )
        
        trGeo = cmds.createNode( 'transformGeometry' )
        cmds.connectAttr( follicleNode+'.outCurve', trGeo+'.inputGeometry' )
        cmds.connectAttr( afterCompose+'.outputMatrix', trGeo+'.transform' )
        cmds.connectAttr( trGeo+'.outputGeometry', dstCon, f=1 )
            
            
def fixCurvePointOnMatrix( curve, mtxObj, createNewCurve=False ):
    
    import sgBFunction_dag
    import sgBFunction_attribute
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'sgHair' )
    node = cmds.createNode( 'sgHair_fixCurvePointOnMatrix' )
    
    curveShape = sgBFunction_dag.getShape( curve )
    if createNewCurve:
        newShape = cmds.createNode( 'nurbsCurve' )
        cmds.connectAttr( curveShape + '.local', node + '.inputCurve' )
        cmds.connectAttr( mtxObj + '.wm', node+'.baseMatrix' )
        cmds.connectAttr( node + '.outputCurve', newShape + '.create' )
        newCurve = sgBFunction_dag.getTransform( newShape )
        
        sgBFunction_attribute.addAttr( newCurve, ln='startCv', min=0, k=1 )
        sgBFunction_attribute.addAttr( newCurve, ln='blendArea',  min=0.1, dv=1, k=1 )
        
        cmds.connectAttr( newCurve + '.startCv', node + '.constStart' )
        cmds.connectAttr( newCurve + '.blendArea', node + '.constEnd' )
        
        curveName = sgBFunction_dag.getTransform( curve ).split( '|' )[-1]
        return cmds.rename( newCurve, 'fix_' + curveName )
    else:
        srcCon = cmds.listConnections( curveShape+'.create', p=1 )
        if not srcCon:
            ioShape = sgBFunction_dag.addIOShape( curve )
            print "io shape : ", ioShape
            srcCon = [ioShape + '.local']
        
        sgBFunction_attribute.addAttr( curve, ln='startCv', min=0, k=1 )
        sgBFunction_attribute.addAttr( curve, ln='blendArea',  min=0.1, dv=1, k=1 )
        
        cmds.connectAttr( curve + '.startCv', node + '.constStart' )
        cmds.connectAttr( curve + '.blendArea', node + '.constEnd' )
        
        cmds.connectAttr( srcCon[0], node+'.inputCurve' )
        cmds.connectAttr( mtxObj + '.wm', node+'.baseMatrix' )
        
        cmds.connectAttr( node + '.outputCurve', curveShape + '.create', f=1 )
        
        return curve