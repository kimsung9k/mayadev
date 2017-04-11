import maya.cmds as cmds
import maya.OpenMaya as om

import functions.autoLoadPlugin

functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgLocusChRig' )
functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgLocusChRig_t2' )


def connectFk( axisIndex ):
    
    axisList = ['x','y','z']
    targetAttr = 't%s' % axisList[ axisIndex%3 ]
    
    sels = cmds.ls( sl=1 )
    
    endJnt = sels[0]
    startJnt = sels[1]
    endJntPos = cmds.xform( endJnt, q=1, ws=1, matrix=1 )
    startJntPos = cmds.xform( startJnt, q=1, ws=1, matrix=1 )
    normalVector = [0,0,0]
    normalVector[ axisIndex ] = 1.0
    endCtl = cmds.circle( normal=normalVector )[0]
    startCtl = cmds.circle( normal=normalVector )[0]
    cmds.xform( endCtl, matrix=endJntPos )
    cmds.xform( startCtl, matrix=startJntPos )
    cmds.parent( endCtl, startCtl )
    
    endCtlTransValue = cmds.getAttr( endCtl+'.t' )[0]
    if om.MVector( *endCtlTransValue ).length() > 0.0001:
        ctlPos = cmds.getAttr( endCtl+'.wm' )
        ctlGrp = cmds.group( em=1, n='P'+endCtl )
        cmds.xform( ctlGrp, ws=1, matrix=ctlPos )
        cmds.parent( ctlGrp, startCtl )
        cmds.parent( endCtl, ctlGrp )
        pCtl = ctlGrp
    else:
        pCtl = cmds.listRelatives( endCtl, p=1 )[0]
        
    if not cmds.attributeQuery( 'keepDistance', node=endCtl, ex=1 ):
        cmds.addAttr( endCtl, ln='keepDistance', min=0, max=1 )
        cmds.setAttr( endCtl+'.keepDistance', e=1, k=1 )
    if not cmds.attributeQuery( 'showParent', node=endCtl, ex=1 ):
        cmds.addAttr( endCtl, ln='showParent', min=0, max=1, at='long' )
        cmds.setAttr( endCtl+'.showParent', e=1, cb=1 )
    startCtlShape= cmds.listRelatives( startCtl, s=1 )[0]
    cmds.connectAttr( endCtl+'.showParent', startCtlShape+'.v' )
    
    aimObjNode = cmds.createNode( 'aimObjectMatrix' )
    
    cmds.connectAttr( startCtl+'.wm', aimObjNode+'.baseMatrix' )
    cmds.connectAttr( endCtl+'.wm', aimObjNode+'.targetMatrix' )
    cmds.connectAttr( startJnt+'.pim', aimObjNode+'.parentInverseMatrix' )
    cmds.setAttr( aimObjNode+'.worldSpaceOutput', 1 )
    if axisIndex > 2:
        cmds.setAttr( aimObjNode+'.inverseAim', 1 )
    cmds.setAttr( aimObjNode+'.aimAxis', axisIndex%3 )
    cmds.connectAttr( aimObjNode+'.outTranslate', startJnt+'.t' )
    cmds.connectAttr( aimObjNode+'.outRotate', startJnt+'.r' )
    cmds.setAttr( startJnt+'.jo', 0,0,0 )
    
    distNode = cmds.createNode( 'distanceBetween' )
    multLinear = cmds.createNode( 'multDoubleLinear' )
    condNode = cmds.createNode( 'condition' )
    multNode = cmds.createNode( 'multiplyDivide' )
    multNode2 = cmds.createNode( 'multiplyDivide' )
    blendColor = cmds.createNode( 'blendColors' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( endCtl+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( endJnt+'.pim',mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.or', endJnt+'.r' )
    cmds.connectAttr( mmdc+'.os', endJnt+'.s' )
    cmds.connectAttr( mmdc+'.osh', endJnt+'.sh' )
    
    cmds.connectAttr( mmdc+'.ot', distNode+'.point1' )
    cmds.connectAttr( distNode+'.distance', multLinear+'.input1' )
    if axisIndex > 2:
        cmds.setAttr( multLinear+'.input2', -1 )
    else:
        cmds.setAttr( multLinear+'.input2', 1 )
    cmds.setAttr( multNode+'.op', 2 )
    cmds.connectAttr( multLinear+'.output', condNode+'.firstTerm' )
    cmds.connectAttr( multLinear+'.output', condNode+'.colorIfFalseR' )
    cmds.connectAttr( mmdc+'.ot', multNode+'.input1' )
    cmds.connectAttr( condNode+'.outColorR', multNode+'.input2X' )
    cmds.connectAttr( condNode+'.outColorR', multNode+'.input2Y' )
    cmds.connectAttr( condNode+'.outColorR', multNode+'.input2Z' )
    cmds.connectAttr( multNode+'.output', multNode2+'.input1' )
    cmds.connectAttr( pCtl+'.'+targetAttr, multNode2+'.input2X' )
    cmds.connectAttr( pCtl+'.'+targetAttr, multNode2+'.input2Y' )
    cmds.connectAttr( pCtl+'.'+targetAttr, multNode2+'.input2Z' )
    cmds.connectAttr( multNode2+'.output', blendColor+'.color1' )
    cmds.connectAttr( mmdc+'.ot', blendColor+'.color2' )
    cmds.connectAttr( blendColor+'.output', endJnt+'.t' )
    cmds.connectAttr( endCtl+'.keepDistance', blendColor+'.blender' )
    
    cmds.connectAttr( startCtl+'.s', startJnt+'.s' )