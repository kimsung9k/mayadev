import maya.cmds as cmds

import chModules


def lockAttrs( node, *attrs ):
    for attr in attrs:
        cmds.setAttr( node+'.'+attr, e=1, lock=1 )
            
def unlockAttrs( node, *attrs ):
    for attr in attrs:
        cmds.setAttr( node+'.'+attr, e=1, lock=0 )

def ikTip_repairSet():
    sels = cmds.ls( '*IkItp_Ctl_OrientDemp' )
    
    selObjs = []
    for sel in sels:
        ik1Jnt   = sel.replace( 'IkItp_Ctl_OrientDemp', 'IK1_JNT' )
        ikGrp    = sel.replace( 'IkItp_Ctl_OrientDemp', 'IK_GRP' )
        ikItpCtl = sel.replace( 'IkItp_Ctl_OrientDemp', 'IkItp_CTL_GRP' )
        
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n=sel.replace( 'OrientDemp', 'OrientMtxDcmp' ) )
        
        cmds.connectAttr( ik1Jnt+'.wm', mtxDcmp+'.i[0]' )
        cmds.connectAttr( ikGrp+'.wim', mtxDcmp+'.i[1]' )
        unlockAttrs( ikItpCtl, 'r' )
        cmds.connectAttr( mtxDcmp+'.or', ikItpCtl+'.r', f=1 )
        lockAttrs( ikItpCtl, 'r' )
        
        selObjs.append( mtxDcmp )
        
        cmds.delete( sel )
        
def poleV_repairSet():
    sels = cmds.ls( 'Leg_*_PoleV_CTL_GRP', tr=1 )
    
    for sel in sels:
        poleVInit = sel.replace( 'Leg', 'LegPoleV' ).replace( '_PoleV', '' ).replace( 'CTL_GRP', 'Init' )
        unlockAttrs( sel, 't' )
        mtxDcmp = cmds.listConnections( sel+'.t', s=1, d=0 )[0]
        cmds.disconnectAttr( mtxDcmp+'.ot', sel+'.t' )
        cmds.connectAttr( poleVInit +'.tx', sel+'.tx' )
        cmds.connectAttr( mtxDcmp+'.oty', sel+'.ty' )
        cmds.connectAttr( mtxDcmp+'.otz', sel+'.tz' )
        lockAttrs( sel, 't' )
        
def waist_repairSet():
    chestCtl = 'Chest_CTL'
    waistCtl = 'Waist_CTL'
    hipCtl = 'Hip_CTL'
    torsoGrp = 'torso_GRP'
    poseInfo = 'Waist_Ct_PoseInfo'
    waistMtxDcmp = 'Waist_CtlMtxDcmp'
    waistOrientObj = 'WaistOrient_OBJ'
    waistSmOri = 'WaistOrient_ObjSmOrient'
    twistAngle = 'Torso_TwistAllAngle'
    
    ctls = cmds.ls( 'WaistItp*_CTL', tr=1 )
    mtxDcmps = cmds.ls( 'Waist_CtlMtxDcmp*' )[1:]
    poseInfos = cmds.ls( 'Waist_Ct_PoseInfo*' )[1:]
    
    blendMtxNode = cmds.createNode( 'blendTwoMatrix', n='Hip_Chest_BlendMtx' )
    mTbt = cmds.createNode( 'matrixToThreeByThree', n='Waist_Ctl_mTBT' )
    
    cmds.connectAttr( chestCtl+'.wm', blendMtxNode+'.inMatrix1' )
    cmds.connectAttr( hipCtl+'.wm', blendMtxNode+'.inMatrix2' )
    cmds.connectAttr( blendMtxNode+'.outMatrix', mTbt+'.inMatrix' )
    
    fbf = cmds.createNode( 'fourByFourMatrix', n='Waist_Ctl_FBF' )
    vectorP = cmds.createNode( 'vectorProduct', n='Waist_CtlXVector' )
    cmds.setAttr( vectorP+'.op', 2 )
    
    cmds.connectAttr( poseInfo+'.tangent', vectorP+'.input1' )
    cmds.connectAttr( mTbt+'.out20', vectorP+'.input2X' )
    cmds.connectAttr( mTbt+'.out21', vectorP+'.input2Y' )
    cmds.connectAttr( mTbt+'.out22', vectorP+'.input2Z' )
    
    cmds.connectAttr( vectorP+'.outputX', fbf+'.i00' )
    cmds.connectAttr( vectorP+'.outputY', fbf+'.i01' )
    cmds.connectAttr( vectorP+'.outputZ', fbf+'.i02' )
    cmds.connectAttr( poseInfo+'.tangentX', fbf+'.i10' )
    cmds.connectAttr( poseInfo+'.tangentY', fbf+'.i11' )
    cmds.connectAttr( poseInfo+'.tangentZ', fbf+'.i12' )
    cmds.connectAttr( poseInfo+'.positionX', fbf+'.i30' )
    cmds.connectAttr( poseInfo+'.positionY', fbf+'.i31' )
    cmds.connectAttr( poseInfo+'.positionZ', fbf+'.i32' )
    
    cmds.connectAttr( fbf+'.output', waistMtxDcmp+'.i[0]', f=1 )
    
    cmds.parent( waistOrientObj, torsoGrp )
    
    mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='WaistOrient_ObjPosMtxDcmp' )
    cmds.connectAttr( mtxDcmp+'.outputMatrix', waistSmOri+'.inputMatrix', f=1 )
    cmds.connectAttr( waistCtl+'.wm', mtxDcmp+'.i[0]' )
    cmds.connectAttr( waistOrientObj+'.pim', mtxDcmp+'.i[1]' )
    cmds.connectAttr( mtxDcmp+'.ot', waistOrientObj+'.t',f=1 )
    
    cmds.connectAttr( waistCtl+'.m', twistAngle+'.inputMatrix', f=1 )
    
    chestAngle = cmds.createNode( 'wristAngle', n=chestCtl.replace( 'CTL', 'CtlAngle' ) )
    cmds.setAttr( chestAngle+'.axis', 1 )
    cmds.connectAttr( chestCtl+'.m', chestAngle+'.inputMatrix' )
    
    for index in range( len( mtxDcmps ) ):
        ctl = ctls[index]
        mtxDcmp = mtxDcmps[index]
        info = poseInfos[index]
        
        i = index+1
        
        grp = cmds.group( ctl, n=ctl+'_localOrient' )
        
        twistMult = cmds.createNode( 'multDoubleLinear', n='Waist_Itp%d_localTwistMult' % i )
        rotateMult = cmds.createNode( 'multDoubleLinear', n='Waist_Itp%d_RotateMult' % i )
        localAngle = cmds.createNode( 'wristAngle', n='Waist_Itp%d_wristAngle' )
        
        cmds.connectAttr( waistCtl+'.m', localAngle+'.inputMatrix' )
        cmds.setAttr( localAngle+'.axis', 1 )
        
        sum = cmds.createNode( 'addDoubleLinear', n='Waist_Itp%d_rotateValue' % i )
        cmds.connectAttr( chestAngle+'.outAngle', twistMult+'.input1' ) 
        cmds.connectAttr( info+'.parameter', twistMult+'.input2' )
        cmds.connectAttr( localAngle+'.outAngle', rotateMult+'.input1' ) 
        cmds.connectAttr( waistCtl+'.multWeight%d' % i, rotateMult+'.input2')
        
        cmds.connectAttr( twistMult+'.output', sum+'.input1' )
        cmds.connectAttr( rotateMult+'.output', sum+'.input2' )
        
        cmds.connectAttr( sum+'.output', grp+'.ry' )

def legPoleV_repairSet():
    staticMts = cmds.ls( 'Leg_*_PoleV_CtlPoseStaticMtx' )
    moveMts   = cmds.ls( 'Leg_*_PoleV_CtlPoseMoveMtx' )
    blendMtxs = cmds.ls( 'Leg_*_PoleV_CtlPoseBlMtxDcmp' )

    for i in range( 2 ):
        moveMtxDcmp = cmds.createNode( 'multMatrixDecompose', n=moveMts[i]+'Dcmp' )
        moveCompose = cmds.createNode( 'composeMatrix', n=moveMts[i].replace( 'MoveMtx', 'MoveCompose' ) )
        staticMtx   = cmds.createNode( 'multMatrix', n= staticMts[i].replace( 'CtlPoseStaticMtx', 'CtlStaticMtx' ) )
        
        cons = cmds.listConnections( moveMts[i]+'.i', s=1, d=0, c=1, p=1 )
        
        outputs = cons[1::2]
        inputs  = cons[::2]

        for j in range( len( inputs ) ):
            cmds.connectAttr( outputs[j], inputs[j].replace( moveMts[i], moveMtxDcmp ) )
        
        polvInit = moveMts[i].replace( 'Leg', 'LegPoleV' ).replace( 'PoleV_CtlPoseMoveMtx', 'Init' )
        cmds.connectAttr( polvInit+'.tx',     moveCompose+'.itx' )
        cmds.connectAttr( moveMtxDcmp+'.oty', moveCompose+'.ity' )
        cmds.connectAttr( moveMtxDcmp+'.otz', moveCompose+'.itz' )
        
        cons = cmds.listConnections( staticMts[i]+'.i', s=1, d=0, c=1, p=1 )
        
        outputs = cons[1::2]
        
        legPoleV_init = outputs[0].split( '.' )[0]
        hip_const  = outputs[2].split( '.' )[0]
        grp = outputs[3].split( '.' )[0]
        
        cmds.connectAttr( legPoleV_init+'.m', staticMtx+'.i[0]' )
        cmds.connectAttr( hip_const+'.wm', staticMtx+'.i[1]' )
        cmds.connectAttr( grp+'.wim', staticMtx+'.i[2]' )
        
        cmds.connectAttr( moveCompose+'.outputMatrix', blendMtxs[i]+'.inMatrix1', f=1 )
        cmds.connectAttr( staticMtx+'.o', blendMtxs[i]+'.inMatrix2', f=1 )
        
        dest = cmds.listConnections( blendMtxs[i]+'.oty', s=0, d=1 )[0]
        cmds.setAttr( dest+'.t', e=1, lock=0 )
        cmds.connectAttr( blendMtxs[i]+'.otx', dest+'.tx',f=1 )

def armPoleV_repairSet():
    mtxDcmps = cmds.ls( 'ArmPoleV_*_Init_childPosMtxDcmp' )
    
    rootInit = 'Root_Init'
    rootGrp = 'Root_CTL_GRP'
    
    for i in range( 2 ):
        mtxDcmp = mtxDcmps[i]
        
        mtx = cmds.createNode( 'multMatrix', n=mtxDcmp.replace( 'childPosMtxDcmp', 'childPoseMtx' ) )
        staticMtx = cmds.createNode( 'multMatrix', n=mtxDcmp.replace( 'childPosMtxDcmp', 'childPoseStaticMtx' ) )
        blMtx = cmds.createNode( 'blendTwoMatrixDecompose', n=mtxDcmp.replace( 'MtxDcmp', 'blMtxDmcp' ) )
        
        poleV_init = mtxDcmp.replace( 'Init_childPosMtxDcmp', 'Init' )
        shoulderInit = poleV_init.replace( 'ArmPoleV', 'Shoulder' )
        poleV_ctlConstGrp = poleV_init.replace( 'ArmPoleV', 'Arm' ).replace( 'Init', 'PoleV_CTL_Const_GRP' )
        poleV_ctlGrp = poleV_ctlConstGrp.replace( '_Const_GRP', '_GRP' )
        poleV_ctl = poleV_ctlGrp.replace( '_GRP', '' )
        
        cmds.connectAttr( poleV_init+'.wm', mtx+'.i[0]' )
        cmds.connectAttr( shoulderInit+'.wim', mtx+'.i[1]' )
        
        cmds.connectAttr( poleV_init+'.wm', staticMtx+'.i[0]' )
        cmds.connectAttr( rootInit+'.wim', staticMtx+'.i[1]' )
        cmds.connectAttr( rootGrp+'.wm', staticMtx+'.i[2]' )
        cmds.connectAttr( poleV_ctlConstGrp+'.wim', staticMtx+'.i[3]' )
        
        cmds.connectAttr( mtx+'.o', blMtx+'.inMatrix1' )
        cmds.connectAttr( staticMtx+'.o', blMtx+'.inMatrix2' )
        cmds.connectAttr( poleV_ctl+'.positionAttach', blMtx+'.ab' )
        
        cmds.setAttr( poleV_ctlGrp+'.t', e=1, lock=0 )
        cmds.setAttr( poleV_ctlGrp+'.r', e=1, lock=0 )
        cmds.connectAttr( blMtx+'.ot', poleV_ctlGrp+'.t',f=1 )
        cmds.connectAttr( blMtx+'.or', poleV_ctlGrp+'.r',f=1 )
    cmds.delete( mtxDcmps )

def waistVector_repairSet():
    xVector = 'Waist_CtlXVector'
    poseInfo = 'Waist_Ct_PoseInfo'
    fbf = 'Waist_Ctl_FBF'
    
    vNode = cmds.createNode( 'vectorProduct', n='Waist_CtlZVector' )
    cmds.setAttr( vNode+'.op', 2 )
    cmds.setAttr( vNode+'.no', 1 )
    
    cmds.connectAttr( xVector+'.output', vNode+'.input1' )
    cmds.connectAttr( poseInfo+'.tangentX', vNode+'.input2X' )
    cmds.connectAttr( poseInfo+'.tangentY', vNode+'.input2Y' )
    cmds.connectAttr( poseInfo+'.tangentZ', vNode+'.input2Z' )
    
    cmds.connectAttr( vNode+'.outputX', fbf+'.i20' )
    cmds.connectAttr( vNode+'.outputY', fbf+'.i21' )
    cmds.connectAttr( vNode+'.outputZ', fbf+'.i22' )


    
def chestOrigin_repairSet( ns='' ):
    
    chestInit = ns+'Chest_Init'
    rootInit =  ns+'Root_Init'
    
    mtxDcmp = cmds.createNode( 'multMatrixDecompose', n= ns+'Chest_CTL_OriginMtxDcmp' )
    origin = cmds.createNode( 'transform', n= ns+'Chest_CTL_Origin' )
    
    cmds.connectAttr( chestInit+'.wm', mtxDcmp+'.i[0]' )
    cmds.connectAttr( rootInit+'.wim', mtxDcmp+'.i[1]' )
    
    cmds.connectAttr( mtxDcmp+'.ot', origin+'.t' )
    
    cmds.parent( origin, ns+'TorsoRotate_CTL' )
    cmds.setAttr( origin+'.r', 0,0,0 )



def ikStretch_repairSet():
    
    plugList = cmds.pluginInfo( q=1, listPlugins=1 )
    
    if not 'sgIkSmoothStretch2' in plugList:
        chModules.autoLoadPlugin().load( 'sgIkSmoothStretch2' )
    
    ikStretchs = cmds.ls( type='ikStretch' )
    
    for ikStretch in ikStretchs:
        
        ikSmoothStretch = cmds.createNode( 'ikSmoothStretch' )
        
        inputCons = cmds.listConnections( ikStretch, s=1, d=0, p=1, c=1 )
        
        outputs = inputCons[1::2]
        inputs  = inputCons[::2]
        
        for i in range( len( outputs ) ):
            outputAttr = outputs[i]
            inputAttr  = inputs[i].replace( ikStretch, ikSmoothStretch )
            cmds.connectAttr( outputAttr, inputAttr )
            
        outputCons = cmds.listConnections( ikStretch, s=0, d=1, p=1, c=1 )
        
        outputs = outputCons[::2]
        inputs  = outputCons[1::2]
        
        for i in range( len( outputs ) ):
            outputAttr = outputs[i].replace( ikStretch, ikSmoothStretch )
            inputAttr  = inputs[i]
            cmds.connectAttr( outputAttr, inputAttr, f=1 )
            
        cmds.delete( ikStretch )
        cmds.rename( ikSmoothStretch, ikStretch )
        
        ikCtl = cmds.listConnections( ikStretch+'.stretchAble' )[0]
        
        cmds.addAttr( ikCtl, ln='smoothRate', min=0, max=10 )
        cmds.setAttr( ikCtl+'.smoothRate', e=1, k=1 )
        cmds.connectAttr( ikCtl+'.smoothRate', ikStretch+'.smoothArea' )
        
        
def ankleItp_repairSet():
    
    ankleInits = cmds.ls( 'Ankle_*_Init' )
    ballInits  = cmds.ls( 'Ball_*_Init'  )
    legItrs     = cmds.ls( 'Leg_*_IK3_ITR' )
    switchs     = cmds.ls( 'Leg_*_Switch_CTL' )
    blendMtxs   = cmds.ls( 'Leg_*_blendMtx' )
    
    for i in range( 2 ):
        ankleInit = ankleInits[i]
        ballInit  = ballInits[i]
        legItr    = legItrs[i]
        switch    = switchs[i]
        blendMtx  = blendMtxs[i]
        
        multMtx = cmds.createNode( 'multMatrix' )
        dcMtx = cmds.createNode( 'decomposeMatrix' )
        fbfMtx = cmds.createNode( 'fourByFourMatrix' )
        smOri  = cmds.createNode( 'smartOrient' )
        
        cmds.connectAttr( ballInit+'.wm', multMtx+'.i[0]' )
        cmds.connectAttr( ankleInit+'.wim', multMtx+'.i[1]' )
        cmds.connectAttr( multMtx+'.o', dcMtx+'.imat' )
        if( i == 1 ):
            multNode = cmds.createNode( 'multiplyDivide' )
            cmds.connectAttr( dcMtx+'.otx', multNode+'.input1X' )
            cmds.connectAttr( dcMtx+'.oty', multNode+'.input1Y' )
            cmds.connectAttr( dcMtx+'.otz', multNode+'.input1Z' )
            cmds.setAttr( multNode+'.input2', -1, -1, -1 )
            cmds.connectAttr( multNode+'.outputX',fbfMtx+'.i00' )
            cmds.connectAttr( multNode+'.outputY',fbfMtx+'.i01' )
            cmds.connectAttr( multNode+'.outputZ',fbfMtx+'.i02' )
        else:
            cmds.connectAttr( dcMtx+'.otx', fbfMtx+'.i00' )
            cmds.connectAttr( dcMtx+'.oty', fbfMtx+'.i01' )
            cmds.connectAttr( dcMtx+'.otz', fbfMtx+'.i02' )
        cmds.connectAttr( fbfMtx+'.output', smOri+'.inputMatrix' )
        
        cmds.connectAttr( smOri+'.outAngle', legItr+'.r', f=1 )
        
        cmds.connectAttr( switch+'.interpoleSwitch', blendMtx+'.attributeBlender')
        

      
def legPoleV_repairSet2():

    constGrps   = cmds.ls( 'Leg_*_PoleV_CTL_Const_GRP' )
    aimObjs     = cmds.ls( 'Hip_*_Init' )
    switchCtls  = cmds.ls( 'Leg_*_Switch_CTL' )
    moveMtxDcmps= cmds.ls( 'Leg_*_PoleV_CtlPoseMoveMtxDcmp' )
    hipCtl      = 'Hip_CTL'
    rootCtl     = 'Root_CTL'
    flyCtl      = 'Fly_CTL'
    moveCtl     = 'Move_CTL'
    worldCtl    = 'World_CTL'
    
    worldInitCtl = 'World_CTL_GRP'
    
    rootInitCtl = 'Root_InitCTL'
    
    for i in range( 2 ):
        followMtx = cmds.createNode( 'followMatrix', n=constGrps[i]+'_follow' )
        dcmp      = cmds.createNode( 'multMatrixDecompose', n=constGrps[i]+'_mtxDcmp' )
        
        worldMult = cmds.createNode( 'multMatrix', n=constGrps[i]+'_worldMult' )
        cmds.connectAttr( aimObjs[i]+'.wm', worldMult+'.i[0]' )
        cmds.connectAttr( worldInitCtl+'.wim', worldMult+'.i[1]' )
        cmds.connectAttr( worldCtl+'.wm', worldMult+'.i[2]' )
        
        hipMult = cmds.createNode( 'multMatrix', n=constGrps[i]+'_hipMult' )
        cmds.connectAttr( aimObjs[i]+'.wm', hipMult+'.i[0]' )
        cmds.connectAttr( rootInitCtl+'.wim', hipMult+'.i[1]' )
        cmds.connectAttr( hipCtl+'.wm', hipMult+'.i[2]' )
        
        rootMult = cmds.createNode( 'multMatrix', n=constGrps[i]+'_rootMult' )
        cmds.connectAttr( aimObjs[i]+'.wm', rootMult+'.i[0]' )
        cmds.connectAttr( rootInitCtl+'.wim', rootMult+'.i[1]' )
        cmds.connectAttr( rootCtl+'.wm', rootMult+'.i[2]' )
        
        flyMult = cmds.createNode( 'multMatrix', n=constGrps[i]+'_flyMult' )
        cmds.connectAttr( aimObjs[i]+'.wm', flyMult+'.i[0]' )
        cmds.connectAttr( rootInitCtl+'.wim', flyMult+'.i[1]' )
        cmds.connectAttr( flyCtl+'.wm', flyMult+'.i[2]' )
        
        moveMult = cmds.createNode( 'multMatrix', n=constGrps[i]+'_moveMult' )
        cmds.connectAttr( aimObjs[i]+'.wm', moveMult+'.i[0]' )
        cmds.connectAttr( worldInitCtl+'.wim', moveMult+'.i[1]' )
        cmds.connectAttr( moveCtl+'.wm', moveMult+'.i[2]' )
        
        cmds.connectAttr( worldMult+'.o', followMtx+'.originalMatrix' )
        cmds.connectAttr( hipMult+'.o', followMtx+'.inputMatrix[0]' )
        cmds.connectAttr( rootMult+'.o', followMtx+'.inputMatrix[1]' )
        cmds.connectAttr( flyMult+'.o', followMtx+'.inputMatrix[2]' )
        cmds.connectAttr( moveMult+'.o', followMtx+'.inputMatrix[3]' )
        
        cmds.connectAttr( switchCtls[i]+'.hipFollow', followMtx+'.inputWeight[0]')
        cmds.connectAttr( switchCtls[i]+'.rootFollow', followMtx+'.inputWeight[1]')
        cmds.connectAttr( switchCtls[i]+'.flyFollow', followMtx+'.inputWeight[2]')
        cmds.connectAttr( switchCtls[i]+'.moveFollow', followMtx+'.inputWeight[3]')
        
        cmds.connectAttr( followMtx+'.outputMatrix', dcmp+'.i[0]' )
        cmds.connectAttr( constGrps[i]+'.pim', dcmp+'.i[1]' )
        cmds.connectAttr( dcmp+'.orx', constGrps[i]+'.rx', f=1 )
        cmds.connectAttr( dcmp+'.ory', constGrps[i]+'.ry', f=1 )
        cmds.connectAttr( dcmp+'.orz', constGrps[i]+'.rz', f=1 )
        
        cmds.connectAttr( constGrps[i]+'.wim', moveMtxDcmps[i]+'.i[3]', f=1 )
        
 
        
def flyCtlRepairSet():
    
    rootInit = 'Root_Init'
    rootCtlGrp  = 'Root_CTL_GRP'
    rootCtlGrpDcmp = 'Root_CTL_GRP__mtxDcmp'
    fps_inFly   = 'Fps_inFly'
    rootCtl = 'Root_CTL'
    flyCtl = 'Fly_CTL'
    flyShapeNode = 'Fly_CtlShapeNode'
    rootGrpDcmp = 'Root_GRP_mmdc'
    
    cmds.delete( rootCtlGrpDcmp )
    
    for target in [ rootCtlGrp, fps_inFly ]:
        for attr in ['t', 'r', 's', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz' ]:
            cmds.setAttr( target+'.'+attr, e=1, lock=0 )
        cmds.connectAttr( rootInit+'.t', target+'.t' )
        cmds.connectAttr( rootInit+'.r', target+'.r' )
    
    flyControlPoint = cmds.createNode( 'transform', n='Fly_CTL_ControlPoint' )
    
    cmds.setAttr( flyControlPoint+'.dh', 1 )
    cmds.setAttr( flyControlPoint+'.overrideEnabled', 1 )
    cmds.setAttr( flyControlPoint+'.overrideDisplayType', 2 )
    
    cmds.parent( flyControlPoint, flyCtl )
    for attr in ['pivTx','pivTy','pivTz']:
        cmds.addAttr( flyCtl, ln=attr )
        cmds.setAttr( flyCtl+'.'+attr, e=1, k=1 )
        
    for attr in ['pivRx','pivRy','pivRz']:
        cmds.addAttr( flyCtl, ln=attr, at='doubleAngle' )
        cmds.setAttr( flyCtl+'.'+attr, e=1, k=1 )
    
    for axis in ['x', 'y', 'z']: 
        cmds.connectAttr( flyCtl+'.pivT'+axis, flyControlPoint+'.t'+axis )
        cmds.connectAttr( flyCtl+'.pivR'+axis, flyControlPoint+'.r'+axis )
    
    cmds.setAttr( flyShapeNode+'.controlerType', 8 )
    cmds.setAttr( flyShapeNode+'.offset', 0,0,0 )
    cmds.setAttr( flyShapeNode+'.orient', 0,0,0 )
    cmds.setAttr( flyShapeNode+'.size', 1.5,1.5,1.5 )
    
    blendMtx = cmds.createNode( 'blendTwoMatrix', n='Fly_Root_Blend' )
    
    cmds.connectAttr( blendMtx+'.outMatrix', rootGrpDcmp+'.matrixIn[0]', f=1 )
    
    for ctl in [rootCtl, flyCtl]:
        cons = cmds.listConnections( ctl+'.wm', p=1, c=1 )
        inputs = cons[1::2]
        
        for inputElement in inputs:
            cmds.connectAttr( blendMtx+'.outMatrix', inputElement, f=1 )
    
    cmds.connectAttr( rootCtl+'.wm', blendMtx+'.inMatrix1' )
    cmds.connectAttr( flyControlPoint+'.wm', blendMtx+'.inMatrix2' )
    
    cmds.addAttr( flyCtl, ln='____', at='enum', en = 'Switch:' )
    cmds.setAttr( flyCtl+'.____', e=1, cb=1 )
    
    cmds.addAttr( flyCtl, ln='blend', min=0, max=1 )
    cmds.setAttr( flyCtl+'.blend', e=1, k=1 )
    
    cmds.connectAttr( flyCtl+'.blend', blendMtx+'.ab' )
    
    followAttrCtls = ['Head_CTL', 'Collar_L_CTL', 'Collar_R_CTL',
                      'Arm_L_Switch_CTL', 'Arm_R_Switch_CTL', 
                      'Leg_L_Switch_CTL', 'Leg_R_Switch_CTL' ]
    
    for ctl in followAttrCtls:
        cmds.setAttr( ctl+'.rootFollow', e=1, k=1 )
        cmds.setAttr( ctl+'.flyFollow', e=1, k=0 )
        try:cmds.setAttr( ctl+'.pinFollow', e=1, k=0 )
        except:pass
    
    rootGrp = 'Root_GRP'
    
    for attr in ['sx', 'sy', 'sz']:
        cons = cmds.listConnections( rootGrp+'.'+attr, p=1, c=1 , s=1, d=0 )
        cmds.disconnectAttr( cons[1], cons[0] )
        cmds.setAttr( rootGrp+'.'+attr, 1 )
    
    for attr in ['shxy', 'shxz', 'shyz']:
        cons = cmds.listConnections( rootGrp+'.'+attr, p=1, c=1 , s=1, d=0 )
        cmds.disconnectAttr( cons[1], cons[0] )
        cmds.setAttr( rootGrp+'.'+attr, 0 )
        


def legTwistRepairSet():
    
    blMts    = cmds.ls( '*Leg_*_Ik2_blendMtx' )
    ankleJnts = cmds.ls( '*Ankle_*_FootIk_JNT' )
    
    for i in range( len( blMts ) ):
        if not cmds.isConnected( ankleJnts[i]+'.wm', blMts[i]+'.inMatrix1' ):
            cmds.connectAttr( ankleJnts[i]+'.wm', blMts[i]+'.inMatrix1', f=1 )
            
            
def circleCheckRepairSet( prefix = '' ):
    
    cmds.connectAttr( prefix + 'Ankle_L_FootIk_JNT.wm', prefix + 'Leg_L_lowerAttatchMtx.i[0]', f=1 )
    cmds.connectAttr( prefix + 'Ankle_R_FootIk_JNT.wm', prefix + 'Leg_R_lowerAttatchMtx.i[0]', f=1 )
    
    cmds.connectAttr( prefix + 'Arm_L_IK_CTL.wm', prefix + 'Arm_L_lowerAttatchMtx.i[0]', f=1 )
    cmds.connectAttr( prefix + 'Arm_R_IK_CTL.wm', prefix + 'Arm_R_lowerAttatchMtx.i[0]', f=1 )



def shoulderRepairSet( prefix='' ):
    
    shoulderLCtl = prefix + 'Shoulder_L_CTL'
    shoulderRCtl = prefix + 'Shoulder_R_CTL'
    
    shoulderLConst = prefix + 'Shoulder_L_Const'
    shoulderRConst = prefix + 'Shoulder_R_Const'
    
    mmdc_L = cmds.createNode( 'multMatrixDecompose' )
    mmdc_R = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( shoulderLCtl+'.wm', mmdc_L+'.i[0]' )
    cmds.connectAttr( shoulderRCtl+'.wm', mmdc_R+'.i[0]' )
    
    cmds.connectAttr( shoulderLConst+'.pim', mmdc_L+'.i[1]' )
    cmds.connectAttr( shoulderRConst+'.pim', mmdc_R+'.i[1]' )
    
    cmds.connectAttr( mmdc_L+'.ot', shoulderLConst+'.t', f=1 )
    cmds.connectAttr( mmdc_R+'.ot', shoulderRConst+'.t', f=1 )