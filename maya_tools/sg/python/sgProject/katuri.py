from sgMaya import sgCmds
from maya import cmds
import pymel.core
from sgMaya.sgCmds import convertMultDoubleConnection



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
    newMesh.v.set( 0 )



def buildArcControl( numJointUpper, numJointLower ):
    
    armTops = []
    armMiddles = []
    armEnds = []
    legMiddles = []
    legEnds = []
    legOrientEnds = []
    
    for side in ['_L_', '_R_' ]:
        armTops    += pymel.core.ls( 'jnt%sarm0' % side )
        armMiddles += pymel.core.ls( 'jnt%sarm1' % side )
        armEnds    += pymel.core.ls( 'jnt%sarm1_end' % side )
        
        legMiddles += pymel.core.ls( 'jnt%sleg1_2_IK' % side )
        legEnds += pymel.core.ls( 'jnt%sleg2_IK' % side )
        legOrientEnds += pymel.core.ls( 'anim%sleg2_IK' % side )
    
    for i in range( 2 ):
        topGrp = pymel.core.createNode( 'transform', n='ArmInterporationGrp%s' % ['_L_','_R_'][i] )
        pymel.core.xform( topGrp, ws=1, matrix=pymel.core.xform( armTops[i], q=1, ws=1, matrix=1 ) )
        
        armTop = armTops[i]
        armMiddle = armMiddles[i]
        armEnd = armEnds[i]
        
        armUpper = sgCmds.addMiddleTranslateJoint( armMiddle, n='MiddleJnt_' + armMiddle )
        armRotMiddle = sgCmds.addMiddleJoint( armMiddle, n='MiddleRotJnt_' + armMiddle )
        armLower = sgCmds.addMiddleTranslateJoint( armEnd, n='MiddleJnt_' + armEnd )
        
        targets = [ armTop, armMiddle, armEnd ]
        circleSubCtls = []
        for i in range( len( targets ) ):
            circleSubCtl = pymel.core.circle( normal=[1,0,0], n=targets[i].replace( 'jnt_', 'sub_Ctl_' ), radius=0.1 )[0]
            circleSubCtlGrp = pymel.core.group( circleSubCtl, n='P' + circleSubCtl )
            pymel.core.parent( circleSubCtlGrp, topGrp )
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
        
        pymel.core.parent( upperSubCtlGrp, topGrp )
        pymel.core.parent( lowerSubCtlGrp, topGrp )
        
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
            
            convertMultDoubleConnection( point1.tx ).set( 0.5 )
            convertMultDoubleConnection( point2.tx ).set( 0.5 )
            
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
        upperCurve.setParent( topGrp ); upperCurve.t.set( 0,0,0 ); upperCurve.r.set( 0,0,0 )
        lowerCurve.setParent( topGrp ); lowerCurve.t.set( 0,0,0 ); lowerCurve.r.set( 0,0,0 )
        
        upperJoints = sgCmds.createPointOnCurve( upperCurve, numJointUpper, nodeType='joint', vector=[1,0,0] )
        lowerJoints = sgCmds.createPointOnCurve( lowerCurve, numJointLower, nodeType='joint', vector=[1,0,0] )
        
        pymel.core.parent( upperJoints, topGrp )
        pymel.core.parent( lowerJoints, topGrp )
        for upperJoint in upperJoints:
            upperJoint.jo.set( 0,0,0 )
        for lowerJoint in lowerJoints:
            lowerJoint.jo.set( 0,0,0 )
        
        disconnectRotate( upperJoints[0] )
        pymel.core.delete( upperJoints[-1] )
        disconnectRotate( lowerJoints[0] )
        disconnectRotate( lowerJoints[-1] )
        
        sgCmds.blendTwoMatrixConnect( upperJoints[-2], lowerJoints[1], lowerJoints[0], ct=False )
        
        circleCtls = []
        for i in range( len( targets ) ):
            circleCtl = pymel.core.circle( normal=[1,0,0], n=targets[i].replace( 'jnt_', 'sub_Ctl_' ), radius=0.1 )[0]
            circleCtlGrp = pymel.core.group( circleCtl, n='P' + circleCtl )
            pymel.core.parent( circleCtlGrp )
            pymel.core.xform( circleCtlGrp, ws=1, matrix=targets[i].wm.get() )
            circleCtls.append( circleCtl )
        
        
        
        