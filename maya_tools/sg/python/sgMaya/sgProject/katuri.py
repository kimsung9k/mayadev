from sgMaya import sgCmds
from maya import cmds, OpenMaya
import pymel.core
from sgMaya import sgModel
from audioop import reverse



def buildBaseMesh( inputBaseMesh ):

    
    baseMesh = pymel.core.ls( inputBaseMesh )[0]
    baseMeshShapes = baseMesh.listRelatives( s=1 )
    
    origMesh = None
    for baseMeshShape in baseMeshShapes:
        if not baseMeshShape.io.get(): continue
        if not baseMeshShape.worldMesh.listConnections( s=0, d=1 ) and not baseMeshShape.outMesh.listConnections( s=0, d=1 ): continue
        origMesh = baseMeshShape
        break
    
    newMeshShape = pymel.core.createNode( 'mesh' )
    newMesh = newMeshShape.getParent()
    origMesh.outMesh >> newMeshShape.inMesh
    pymel.core.refresh()
    origMesh.outMesh // newMeshShape.inMesh
    
    cmds.sets( newMeshShape.name(), e=1, forceElement = 'initialShadingGroup' )
    newMesh.rename( baseMesh.split('|')[-1] + '_arcbl' )




def buildArcControl( numJointUpper, numJointLower, typ='arm' ):
    
    armTops = []
    armMiddles = []
    armEnds = []
    fkIkCtls = []
    
    for side in ['_L_', '_R_' ]:
        armTops    += pymel.core.ls( 'jnt%s%s0' % ( side, typ ) )
        armMiddles += pymel.core.ls( 'jnt%s%s1' % ( side, typ ) )
        armEnds    += pymel.core.ls( 'jnt%s%s1_end' % ( side, typ ) )
        fkIkCtls += pymel.core.ls( 'anim%s%s_IKFK' % ( side, typ ) )

    if not armTops:
        for side in ['_L_', '_R_' ]:
            armTops    += pymel.core.ls( '%s01%sJNT' % ( typ.capitalize(), side ) )
            armMiddles += pymel.core.ls( '%s02%sJNT' % ( typ.capitalize(), side ) )
            armEnds    += pymel.core.ls( '%s03%sJNT' % ( typ.capitalize(), side ) )
            fkIkCtls += pymel.core.ls( '%s%sIKFKSwitch' % ( typ.capitalize(), side ) )

    for sideIndex in range( 2 ):
        coreGrp = pymel.core.createNode( 'transform', n='%sInterporationCoreGrp%s' % ( typ.capitalize(), ['_L_','_R_'][sideIndex] ) )
        pymel.core.xform( coreGrp, ws=1, matrix=pymel.core.xform( armTops[sideIndex], q=1, ws=1, matrix=1 ) )
        
        armTop = armTops[sideIndex]
        armMiddle = armMiddles[sideIndex]
        armEnd = armEnds[sideIndex]
        
        armUpper = sgCmds.addMiddleTranslateJoint( armMiddle, n='MiddleJnt_' + armMiddle )
        armRotMiddle = sgCmds.addMiddleJoint( armMiddle, n='MiddleRotJnt_' + armMiddle )
        armLower = sgCmds.addMiddleTranslateJoint( armEnd, n='MiddleJnt_' + armEnd )
        
        targets = [ armTop, armMiddle, armEnd ]
        circleSubCtls = []
        for i in range( len( targets ) ):
            circleSubCtl = pymel.core.circle( normal=[1,0,0], n=targets[i].replace( 'jnt_', 'sub_Ctl_' ), radius=0.1 )[0]
            circleSubCtlGrp = pymel.core.group( circleSubCtl, n='P' + circleSubCtl )
            pymel.core.parent( circleSubCtlGrp, coreGrp )
            pymel.core.xform( circleSubCtlGrp, ws=1, matrix=targets[i].wm.get() )
            circleSubCtls.append( circleSubCtl )
        
        firstSubCtl  = circleSubCtls[0]
        secondSubCtl = circleSubCtls[1]
        thirdSubCtl  = circleSubCtls[2]
        
        upperSubCtl = pymel.core.circle( normal=[1,0,0], n=secondSubCtl + '_upper', radius=0.1 )[0]
        upperSubCtlOffset = pymel.core.group( upperSubCtl, n='Offset' + upperSubCtl )
        upperSubCtlGrp = pymel.core.group( upperSubCtlOffset, n='P' + upperSubCtl )
        lowerSubCtl = pymel.core.circle( normal=[1,0,0], n=secondSubCtl + '_lower', radius=0.1 )[0]
        lowerSubCtlOffset = pymel.core.group( lowerSubCtl, n='Offset' + lowerSubCtl )
        lowerSubCtlGrp = pymel.core.group( lowerSubCtlOffset, n='P' + lowerSubCtl )
        
        pymel.core.parent( upperSubCtlGrp, coreGrp )
        pymel.core.parent( lowerSubCtlGrp, coreGrp )
        
        pymel.core.xform( upperSubCtlGrp, ws=1, matrix=firstSubCtl.wm.get() )
        pymel.core.xform( lowerSubCtlGrp, ws=1, matrix=secondSubCtl.wm.get() )
        
        firstPos = pymel.core.xform( firstSubCtl, q=1, ws=1, t=1 )
        secondPos = pymel.core.xform( secondSubCtl, q=1, ws=1, t=1 )
        thirdPos = pymel.core.xform( thirdSubCtl, q=1, ws=1, t=1 )
        
        upperPos = [ (firstPos[i] + secondPos[i])/2 for i in range( 3 ) ]
        lowerPos = [ (secondPos[i] + thirdPos[i])/2 for i in range( 3 ) ]
        
        pymel.core.xform( upperSubCtlGrp, ws=1, t=upperPos )
        pymel.core.xform( lowerSubCtlGrp, ws=1, t=lowerPos )

        def getPointOneTwo( pointerCtl1, pointerCtl2, baseCtl ):
            
            point1Dcmp = sgCmds.getLocalDecomposeMatrix( pointerCtl1.wm, baseCtl.wim )
            point2Dcmp = sgCmds.getLocalDecomposeMatrix( pointerCtl2.wm, baseCtl.wim )
            
            point1 = sgCmds.makeChild( baseCtl, n='pointer1_' + baseCtl )
            point2 = sgCmds.makeChild( baseCtl, n='pointer2_' + baseCtl )
            
            point1Dcmp.otx >> point1.tx
            point2Dcmp.otx >> point2.tx
            
            sgCmds.convertMultDoubleConnection( point1.tx ).set( 0.5 )
            sgCmds.convertMultDoubleConnection( point2.tx ).set( 0.5 )
            
            point1.dh.set( 1 )
            point2.dh.set( 1 )
            
            return point1, point2
        
        def disconnectRotate( inputNode ):
            node = pymel.core.ls( inputNode )[0]
            cons = node.r.listConnections( s=1, d=0, p=1 )
            if cons:
                cons[0] // node.r
        
        upperPoint1, upperPoint2 = getPointOneTwo( firstSubCtl, secondSubCtl, upperSubCtl )
        lowerPoint1, lowerPoint2 = getPointOneTwo( secondSubCtl, thirdSubCtl, lowerSubCtl )
        
        upperCurve = sgCmds.makeCurveFromObjects( firstSubCtl,  upperPoint1, upperPoint2, secondSubCtl )
        lowerCurve = sgCmds.makeCurveFromObjects( secondSubCtl, lowerPoint1, lowerPoint2, thirdSubCtl  )
        upperCurve.setParent( coreGrp ); upperCurve.t.set( 0,0,0 ); upperCurve.r.set( 0,0,0 )
        lowerCurve.setParent( coreGrp ); lowerCurve.t.set( 0,0,0 ); lowerCurve.r.set( 0,0,0 )
        
        upperJoints = sgCmds.createPointOnCurve( upperCurve, numJointUpper, nodeType='joint', vector=[1,0,0] )
        lowerJoints = sgCmds.createPointOnCurve( lowerCurve, numJointLower, nodeType='joint', vector=[1,0,0] )
        
        pymel.core.parent( upperJoints, coreGrp )
        pymel.core.parent( lowerJoints, coreGrp )
        for upperJoint in upperJoints:
            upperJoint.jo.set( 0,0,0 )
        for lowerJoint in lowerJoints:
            lowerJoint.jo.set( 0,0,0 )
        
        disconnectRotate( upperJoints[0] )
        pymel.core.delete( upperJoints[-1] )
        disconnectRotate( lowerJoints[0] )
        disconnectRotate( lowerJoints[-1] )
        
        sgCmds.blendTwoMatrixConnect( upperJoints[-2], lowerJoints[1], lowerJoints[0], ct=False )
        
        ctlGrp = pymel.core.createNode( 'transform', n='%sInterporationCtlGrp%s' % ( typ.capitalize(), ['_L_','_R_'][sideIndex] ) )
        sgCmds.constrain_all(armTop, ctlGrp)
        pymel.core.xform( ctlGrp, os=1, matrix= sgCmds.getDefaultMatrix() )
        sgCmds.addAttr( fkIkCtls[sideIndex], ln='showArcCtls', cb=1, min=0, max=1, at='long' )
        fkIkCtls[sideIndex].showArcCtls >> ctlGrp.v
        fkIkCtls[sideIndex].showArcCtls.set( 1 )
        sgCmds.addAttr( fkIkCtls[sideIndex], ln='arc', k=1, min=0, max=1 )
        
        circleCtls = []
        for i in range( len( targets ) ):
            circleCtl = pymel.core.circle( normal=[1,0,0], n=targets[i].replace( 'jnt_', 'Ctl_itp_' ), radius=0.5 )[0]
            circleCtlGrp = pymel.core.group( circleCtl, n='P' + circleCtl )
            pymel.core.parent( circleCtlGrp )
            pymel.core.xform( circleCtlGrp, ws=1, matrix=targets[i].wm.get() )
            circleCtls.append( circleCtl )
        
        for i in range( len( targets ) ):
            circleCtls[i].t >> circleSubCtls[i].t
            circleCtls[i].r >> circleSubCtls[i].r

        sgCmds.constrain_parent( armTop, circleCtls[0].getParent() )
        sgCmds.constrain_parent( armRotMiddle, circleCtls[1].getParent() )
        sgCmds.constrain_parent( armEnd, circleCtls[2].getParent() )

        upperCtl = pymel.core.circle( normal=[1,0,0], n=circleCtls[1] + '_upper', radius=0.5 )[0]
        upperCtlOffset = pymel.core.group( upperCtl, n='Offset' + upperCtl )
        upperCtlGrp = pymel.core.group( upperCtlOffset, n='P' + upperCtl )
        lowerCtl = pymel.core.circle( normal=[1,0,0], n=circleCtls[1] + '_lower', radius=0.5 )[0]
        lowerCtlOffset = pymel.core.group( lowerCtl, n='Offset' + lowerCtl )
        lowerCtlGrp = pymel.core.group( lowerCtlOffset, n='P' + lowerCtl )
        
        upperCtl.t >> upperSubCtl.t
        lowerCtl.t >> lowerSubCtl.t
        upperSubCtlOffset.t >> upperCtlOffset.t
        lowerSubCtlOffset.t >> lowerCtlOffset.t
        
        sgCmds.constrain_parent( armUpper, upperCtlGrp )
        sgCmds.constrain_parent( armLower, lowerCtlGrp )
        
        pymel.core.parent( circleCtls[0].getParent(), circleCtls[1].getParent(), circleCtls[2].getParent(), upperCtlGrp, lowerCtlGrp, ctlGrp )
        
        arcNode = pymel.core.createNode( 'makeThreePointCircularArc' )
        arcNode.point1.set( 0,0,0 )
        armMiddle.t >> arcNode.point2
        dcmpEnd = sgCmds.getLocalDecomposeMatrix( armEnd.wm, armTop.wim )
        rangeNode = pymel.core.createNode( 'setRange' )
        
        if sideIndex == 0:
            rangeNode.minZ.set( 0.001 ); rangeNode.maxZ.set( 10000 )
            rangeNode.oldMinZ.set( 0.001 ); rangeNode.oldMaxZ.set( 10000 )
        else:
            rangeNode.minZ.set( -100 ); rangeNode.maxZ.set( -0.001 )
            rangeNode.oldMinZ.set( -100 ); rangeNode.oldMaxZ.set( -0.001 )

        dcmpEnd.ot >> rangeNode.value
        rangeNode.outValue >> arcNode.point3

        curveShape = pymel.core.createNode( 'nurbsCurve' )
        curveTr = curveShape.getParent()
        curveTr.setParent( armTop )
        pymel.core.xform( curveTr, os=1, matrix=sgCmds.getDefaultMatrix() )
        
        arcNode.outputCurve >> curveShape.create
        
        middleTargets = [armUpper, armLower]
        offsetCtls = [upperSubCtlOffset, lowerSubCtlOffset]
        
        for i in range( 2 ):
            nearPointChild = pymel.core.createNode( 'transform' )
            nearPointChild.setParent( curveTr )
            nearCurve = pymel.core.createNode( 'nearestPointOnCurve' )
            curveShape.local >> nearCurve.inputCurve
            middleDcmp = sgCmds.getLocalDecomposeMatrix( middleTargets[i].wm, curveTr.wim )
            middleDcmp.ot >> nearCurve.inPosition
            nearCurve.position >> nearPointChild.t
            dcmp = sgCmds.getLocalDecomposeMatrix( nearPointChild.wm, middleTargets[i].wim )
            blendColor = pymel.core.createNode( 'blendColors' )
            dcmp.ot >> blendColor.color1
            blendColor.color2.set( 0,0,0 )
            fkIkCtls[sideIndex].arc >> blendColor.blender
            blendColor.output >> offsetCtls[i].t
        
        circleCtls[0].v.set(0)
        circleCtls[2].v.set(0)
        
        for joint in upperJoints[:-1] + lowerJoints[1:]:
            sgCmds.makeParent( joint )
            attrNameX = sgCmds.addMultDoubleLinearConnection( joint.rx )
            attrNameY = sgCmds.addMultDoubleLinearConnection( joint.ry )
            attrNameZ = sgCmds.addMultDoubleLinearConnection( joint.rz )
            if not attrNameX: continue
            attrNameX.set( 0.5 )
            attrNameY.set( 0.5 )
            attrNameZ.set( 0.5 )
        



def addHipController():
    
    sideList = ['_L_', '_R_']
    
    baseCtl = pymel.core.ls( 'anim_pelvis0' )[0]
    
    for side in sideList:
        ctl = sgCmds.makeController( sgModel.Controller.pinPoints, n='Ctl_Hip%s' % side, makeParent=1 )
        pCtl = ctl.getParent()
        pCtl.setParent( baseCtl )
        
        ikLeg = pymel.core.ls( 'jnt%sleg0_IK' % side )[0]
        
        pymel.core.xform( pCtl, ws=1, matrix= pymel.core.xform( ikLeg, q=1, ws=1, matrix=1 ) )
        if side == '_L_':
            ctl.shape_rx.set( 90 )
        else:
            ctl.shape_rx.set( -90 )
        
        sgCmds.constrain_point( ctl, ikLeg )




def buildLegArcController( numJoint ):
    
    sideList = ['_L_', '_R_']
    
    baseCtl = pymel.core.ls( 'anim_pelvis0' )[0]
    
    for side in sideList:
        
        mainGrp = pymel.core.createNode( 'transform' )
        
        legStart = pymel.core.ls( 'jnt%sleg1_2_IK' % side )[0]
        legEnd    = pymel.core.ls( 'jnt%sleg2_IK' % side )[0]
        legMiddle = sgCmds.addMiddleTranslateJoint( legEnd, n='MiddleJnt_' + legEnd )
        
        pymel.core.xform( mainGrp, ws=1, matrix= legStart.wm.get() )
        
        circleCtl, circleNode = pymel.core.circle( radius=0.5, normal=[1,0,0], n='Ctl_arc_Leg%s' % side )
        pCircleCtl = pymel.core.group( circleCtl, n='PCtl_arc_Leg%s' % side )
        
        pymel.core.parentConstraint( legMiddle, pCircleCtl )
    
        pointerStart = pymel.core.createNode( 'transform' )
        pointerMiddle = pymel.core.createNode( 'transform' )
        pointerEnd   = pymel.core.createNode( 'transform' )
        pPointMiddle = sgCmds.makeParent( pointerMiddle )
        
        pymel.core.xform( pointerStart, ws=1, matrix= legStart.wm.get() )
        pymel.core.xform( pPointMiddle, ws=1, matrix= legMiddle.wm.get() )
        pymel.core.xform( pointerEnd, ws=1, matrix= legEnd.wm.get() )
        
        middleChild0 = pymel.core.createNode( 'transform' ); middleChild0.dh.set( 1 )
        middleChild1 = pymel.core.createNode( 'transform' ); middleChild1.dh.set( 1 )        
        pymel.core.parent( middleChild0, middleChild1, pointerMiddle )
        pymel.core.xform( middleChild0, os=1, matrix=sgCmds.getDefaultMatrix() )
        pymel.core.xform( middleChild1, os=1, matrix=sgCmds.getDefaultMatrix() )
    
        dcmpStart = sgCmds.getLocalDecomposeMatrix( pointerStart.wm, pointerMiddle.wim )
        dcmpEnd   = sgCmds.getLocalDecomposeMatrix( pointerEnd.wm, pointerMiddle.wim )
        
        halfTxStart = pymel.core.createNode( 'multDoubleLinear' )
        halfTxEnd = pymel.core.createNode( 'multDoubleLinear' )
        dcmpStart.otx >> halfTxStart.input1
        dcmpEnd.otx >> halfTxEnd.input1
        halfTxStart.input2.set( 0.5 )
        halfTxEnd.input2.set( 0.5 )
        
        halfTxStart.output >> middleChild0.tx
        halfTxEnd.output >> middleChild1.tx
        
        circleCtl.t >> pointerMiddle.t
        
        curve = sgCmds.makeCurveFromObjects( pointerStart, middleChild0, middleChild1, pointerEnd )
        
        joints = sgCmds.createPointOnCurve( curve, numJoint, nodeType='joint', vector=[0,-1,0] )
        
        
        def disconnectRotate( inputNode ):
            node = pymel.core.ls( inputNode )[0]
            cons = node.r.listConnections( s=1, d=0, p=1 )
            if cons:
                cons[0] // node.r

        disconnectRotate( joints[0]  )
        disconnectRotate( joints[-1] )
        
        pymel.core.parent( joints, curve, pointerStart, pPointMiddle, pointerEnd, mainGrp )
        
        for joint in joints[1:-1]:
            joint.jo.set( 0,0,0 )
            sgCmds.makeParent( joint )
            rxMultAttr = sgCmds.addMultDoubleLinearConnection( joint.rx )
            ryMultAttr = sgCmds.addMultDoubleLinearConnection( joint.ry )
            rzMultAttr = sgCmds.addMultDoubleLinearConnection( joint.rz )
            rxMultAttr.set( 0.5 )
            ryMultAttr.set( 0.5 )
            rzMultAttr.set( 0.5 )
        



def buildBearHipController():
    
    baseCtl = 'Pelvis_CTRL'
    for side in ['_L_', '_R_']:
        ikJnt = pymel.core.ls( 'Leg01%sIK_JNT' % side )[0]
        fkGrp = pymel.core.ls( 'Leg%sFK_CTRL_GP' % side )[0]
        ctl = sgCmds.makeController( sgModel.Controller.pinPoints, n='Ctl_Hip%s' % side, makeParent=1 )
        pCtl = ctl.getParent()
        pymel.core.xform( pCtl, ws=1, matrix=ikJnt.wm.get() )

        rotValue = 90
        if side == '_R_': 
            rotValue = -90
        ctl.shape_rx.set( rotValue )
        ctl.shape_sx.set( 9 )
        ctl.shape_sy.set( 9 )
        ctl.shape_sz.set( 9 )
        
        pCtl.setParent( baseCtl )
        pymel.core.pointConstraint( ctl, ikJnt )
        pymel.core.pointConstraint( ctl, fkGrp )





def leafSetting( inputTargetMesh, edgeList=[29, 34, 39, 44, 77, 128], **options ):
    
    reverseOrder = False
    if options.has_key( 'reverseOrder' ):
        reverseOrder = True
    
    targetMesh = pymel.core.ls( inputTargetMesh )[0]
    
    edges = []
    for edgeIndex in edgeList:
        edges.append( targetMesh + '.e[%d]' % edgeIndex )
    
    bindJoints = sgCmds.edgeToJointLine( edges, 4, reverseOrder=reverseOrder )
    ctls = sgCmds.createFkControl( bindJoints[0], 5 )
    
    for ctl in ctls:
        sgCmds.setIndexColor( ctl.getShape(), 6 )
    
        
    
    
