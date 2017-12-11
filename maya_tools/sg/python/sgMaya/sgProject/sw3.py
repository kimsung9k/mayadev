

def createGrassController( meshs, ground ):
    
    import pymel.core
    from sgMaya import sgCmds, sgModel
    reload( sgCmds )
    from maya import mel, cmds, OpenMaya
    
    curves = []
    ctlsList = []
    
    bbys = []
    for mesh in meshs:
        bb = pymel.core.exactWorldBoundingBox( mesh )
        bbys.append( bb[4] )
    meshMaxY = max( bbys )
    
    coreGrp = pymel.core.createNode( 'transform', n='grassRigCoreGrp' )
    pivCtls = []
    for mesh in meshs:
        pymel.core.select( mesh + '.e[15]' )
        mel.eval( 'SelectEdgeLoopSp;' )
        targetCurve = pymel.core.ls( mel.eval( 'polyToCurve -form 2 -degree 3;' )[0] )[0]
        curveCuted = sgCmds.cutCurve( targetCurve, ground )
        
        curveBB = pymel.core.exactWorldBoundingBox( curveCuted )
        curvePos = [ ( curveBB[0] + curveBB[3] )/2 , 0, ( curveBB[2] + curveBB[5] )/2 ]
        curveScaleY = meshMaxY/curveBB[4]
        curveP = pymel.core.createNode( 'transform' )
        curveP.t.set( curvePos )
        curveCuted.setParent( curveP )
        curveP.sy.set( curveScaleY )
        curveCuted.setParent( w=1 )
        pymel.core.makeIdentity( curveCuted, apply=1, t=1, r=1, s=1, n=0, pn=1 )
        pymel.core.delete( targetCurve, curveP )
        
        mel.eval( 'rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 7 -d 3 -tol 0.01 "%s";' % curveCuted.name() )
        wire = pymel.core.ls( mel.eval( 'wire -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w %s %s;' % ( curveCuted.name(), mesh ) )[0] )[0]
        pymel.core.setAttr( wire + '.dropoffDistance[0]', 10000 )
        curves = wire.listConnections( s=1, d=0, type='nurbsCurve' )
        
        ctls = sgCmds.createControllerByCurveCVs( curveCuted )
        
        curves.append( curveCuted )
        ctlsList.append( ctls )
        
        firstCtl = ctls[0]
        pFirstCtl = firstCtl.getParent()
        pivCtl = pymel.core.createNode( 'transform', n='Piv_' + firstCtl.nodeName() )
        pivCtl.t.set( pymel.core.xform( pFirstCtl, q=1, ws=1, t=1 ) )
        pFirstCtl.setParent( pivCtl )
        pivCtl.v.set( 0 )
        pivCtls.append( pivCtl )
        pymel.core.parent( curves, pivCtl, coreGrp )
        for curve in curves:
            curve.v.set( 0 )
    
    bbAllCtls = OpenMaya.MBoundingBox()
    for pivCtl in pivCtls:
        bbAllCtls.expand( OpenMaya.MPoint( *pymel.core.xform( pivCtl, q=1, ws=1, t=1 ) ) )
    duCurvePivPoint = bbAllCtls.center()
    duCurvePivPoint = [ duCurvePivPoint.x, duCurvePivPoint.y, duCurvePivPoint.z ]
    duCurveEndPoint = [ duCurvePivPoint[0], meshMaxY, duCurvePivPoint[2] ]
    
    duCurve = pymel.core.curve( p=[ duCurvePivPoint, duCurveEndPoint ], d=1 )
    duCurve.v.set( 0 )
    mel.eval( 'rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 7 -d 3 -tol 0.01 "%s";' % duCurve.name() )
    
    duCtls = sgCmds.createControllerByCurveCVs( duCurve )
    pivCtl = pymel.core.createNode( 'transform', n='Piv_' + duCtls[0].nodeName() )
    pivCtlPos = pymel.core.xform( duCtls[0], q=1, ws=1, t=1 )
    pivCtl.t.set( pivCtlPos )
    duCtls[0].getParent().setParent( pivCtl )
    sgCmds.makeParent( pivCtl )
    
    pivCtlMaxY = pymel.core.exactWorldBoundingBox( pivCtl )[4]
    lookAtCtl = sgCmds.makeController( sgModel.Controller.conePoints, makeParent=1, n='Ctl_LookAt_%s' % duCurve.nodeName() )
    lookAtCtl.getParent().t.set( pivCtlPos[0], pivCtlMaxY, pivCtlPos[2] )
    sgCmds.lookAtConnect( lookAtCtl, pivCtl )
    
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
    composeMatrix.outputMatrix >> wtAddMtx.i[0].m
    wtAddMtx.i[0].w.set( 0.5 )
    lookAtCtl.matrix >> wtAddMtx.i[1].m
    wtAddMtx.i[1].w.set( 0.5)
    dcmpWtAdd = sgCmds.getDecomposeMatrix( wtAddMtx.matrixSum )
    
    for i in range( len( duCtls ) ):
        sgCmds.makeParent( duCtls[i].getParent(), n= 'Piv_' + duCtls[i].nodeName() )
        dcmpWtAdd.outputRotate >> duCtls[i].getParent().r
    
    for i in range( len( duCtls ) ):
        dcmp = sgCmds.getLocalDecomposeMatrix( duCtls[i].wm, duCtls[i].getParent().pim )
        for j in range( len( ctlsList ) ):
            dcmp.outputTranslate >> ctlsList[j][i].t
            dcmp.outputRotate >> ctlsList[j][i].r
            dcmp.outputScale >> ctlsList[j][i].s
    
    for eachPiv in pivCtls:
        pivCtl.r >> eachPiv.r
    
    sgCmds.addOptionAttribute( lookAtCtl )
    sgCmds.addAttr( lookAtCtl, ln='showDetail', k=1, min=0, max=1 )
    lookAtCtl.attr( 'showDetail' ) >> pivCtl.v
    
    pymel.core.parent( coreGrp )
    coreGrp.attr( 'inheritsTransform' ).set( 0 )
    coreGrp.t.set( lock=1 )
    coreGrp.r.set( lock=1 )
    coreGrp.s.set( lock=1 )
    
    mainGrp = pymel.core.createNode( 'transform', n='grassRigMainGrp' )
    jnt = pymel.core.joint()
    pymel.core.move( mainGrp, duCurvePivPoint[0], duCurvePivPoint[1], duCurvePivPoint[2], ws=1 )
    pymel.core.parent( duCurve, coreGrp, pivCtl.getParent(), lookAtCtl.getParent(), mainGrp )
    pymel.core.skinCluster( meshs, jnt )
    
    for duCtl in duCtls:
        sgCmds.setIndexColor( duCtl, 28 )

    sgCmds.setIndexColor( lookAtCtl, 22 )
    pymel.core.select( lookAtCtl )
    
    
    