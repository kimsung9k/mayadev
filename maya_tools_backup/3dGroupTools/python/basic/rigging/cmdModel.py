import maya.cmds as cmds
import math


def createRivet( curves ):
    
    loft = cmds.createNode( 'loft' )
    info = cmds.createNode( 'pointOnSurfaceInfo' )
    fbfm = cmds.createNode( 'fourByFourMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    null = cmds.createNode( 'transform' )
    
    surfShape = cmds.createNode( 'nurbsSurface' )
    
    for i in range( len( curves ) ):
        curve = curves[i]
        shape = cmds.listRelatives( curve, s=1 )[0]
        
        srcCons = cmds.listConnections( shape + '.create', p=1, c=1 )
        if not srcCons:
            cmds.connectAttr( shape+'.local', loft+'.inputCurve[%d]' % i )
        else:
            cmds.connectAttr( srcCons[1], loft+'.inputCurve[%d]' % i )
    
    cmds.setAttr( info+'.top', 1 )
    cmds.setAttr( info+'.u', 0.5 )
    cmds.setAttr( info+'.v', 0.5 )
    
    cmds.connectAttr( loft + '.outputSurface', info+'.inputSurface' )
    cmds.connectAttr( loft + '.outputSurface', surfShape+'.create' )
    
    cmds.connectAttr( info+'.nx', fbfm+'.i00' )
    cmds.connectAttr( info+'.ny', fbfm+'.i01' )
    cmds.connectAttr( info+'.nz', fbfm+'.i02' )
    
    cmds.connectAttr( info+'.nvx', fbfm+'.i10' )
    cmds.connectAttr( info+'.nvy', fbfm+'.i11' )
    cmds.connectAttr( info+'.nvz', fbfm+'.i12' )
    
    cmds.connectAttr( info+'.px', fbfm+'.i30' )
    cmds.connectAttr( info+'.py', fbfm+'.i31' )
    cmds.connectAttr( info+'.pz', fbfm+'.i32' )
    
    cmds.connectAttr( fbfm+'.output', mmdc+'.i[0]' )
    cmds.connectAttr( null+'.pim',   mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', null+'.t' )
    cmds.connectAttr( mmdc+'.or', null+'.r' )
    
    cmds.addAttr( null, ln='parameterU', min=0, max=1, dv=0.5 )
    cmds.setAttr( null+'.parameterU', e=1, k=1 )
    cmds.addAttr( null, ln='parameterV', min=0, max=1, dv=0.5 )
    cmds.setAttr( null+'.parameterV', e=1, k=1 )
    
    cmds.connectAttr( null+'.parameterU', info+'.u' )
    cmds.connectAttr( null+'.parameterV', info+'.v' )
    
    cmds.select( null )
    
    
    
def aimObjectConnect( base, aimObject, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    fbfm = cmds.createNode( 'fourByFourMatrix' )
    shdo = cmds.createNode( 'shoulderOrient' )
    
    cmds.connectAttr( target+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( base+'.wim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.otx', fbfm+'.i00' )
    cmds.connectAttr( mmdc+'.oty', fbfm+'.i01' )
    cmds.connectAttr( mmdc+'.otz', fbfm+'.i02' )
    cmds.connectAttr( fbfm+'.output', shdo+'.inputMatrix' )
    cmds.connectAttr( shdo+'.outAngleX', aimObject+'.rx' )
    cmds.connectAttr( shdo+'.outAngleY', aimObject+'.ry' )
    cmds.connectAttr( shdo+'.outAngleZ', aimObject+'.rz' )
    
    
    
def mmMakeChildAimObject( *args ):
    
    sels = cmds.ls( sl=1 )
    
    aimTarget = sels[0]
    base      = sels[1]
    
    mmdc   = cmds.createNode( 'multMatrixDecompose', n= base+'_aimObjMmdc' )
    fbf    = cmds.createNode( 'fourByFourMatrix', n= base+'_aimObjFbf' )
    shdOr  = cmds.createNode( 'shoulderOrient',   n= base+'_aimObjShdOr' )
    aimObj = cmds.createNode( 'transform', n=base+'_aimObj' )
    
    cmds.connectAttr( aimTarget+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( base + '.wim',   mmdc+'.i[1]' )
    
    aimVector = cmds.getAttr( mmdc+'.ot' )[0]
    
    largeIndex = 0
    if math.fabs( aimVector[largeIndex] ) < math.fabs( aimVector[1] ):
        largeIndex = 1
    if math.fabs( aimVector[largeIndex] ) < math.fabs( aimVector[2] ):
        largeIndex = 2
        
    if aimVector[largeIndex] < 0:
        cmds.setAttr( mmdc+'.inverseTranslate', 1 )
        
    cmds.connectAttr( mmdc+'.otx', fbf+'.i%d0' % largeIndex )
    cmds.connectAttr( mmdc+'.oty', fbf+'.i%d1' % largeIndex )
    cmds.connectAttr( mmdc+'.otz', fbf+'.i%d2' % largeIndex )
    
    cmds.connectAttr( fbf+'.output', shdOr+'.inputMatrix' )
    cmds.connectAttr( shdOr+'.outAngleX', aimObj+'.rx' )
    cmds.connectAttr( shdOr+'.outAngleY', aimObj+'.ry' )
    cmds.connectAttr( shdOr+'.outAngleZ', aimObj+'.rz' )
    
    cmds.parent( aimObj, base )
    cmds.setAttr( aimObj+'.t', 0,0,0 )

    
    
def mmCreateRivet( *args ):
    
    sels = cmds.ls( sl=1 )
    try: createRivet( sels )
    except:
        cmds.error( "Select Two Curve" )
        
        
        
def mmConstrainedJoint( *args ):
    
    sels = cmds.ls( sl=1 )
    
    constrainedJnts= []
    
    for sel in sels:
        jnt = cmds.createNode( 'joint', n= sel + '_constJnt' )
        mmdc = cmds.createNode( 'multMatrixDecompose', n=sel+'_constMmdc' )
        cmds.connectAttr( sel+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( jnt+'.pim', mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', jnt+'.t' )
        cmds.connectAttr( mmdc+'.or', jnt+'.r' )
        constrainedJnts.append( jnt )

    cmds.select( constrainedJnts )