import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import dag
import convert
import attribute
import transform
import connect


def setStdToMixamo( stdGrp, mixamoHipJnt ):
    
    children = cmds.listRelatives( stdGrp, c=1, ad=1 )
    children.append( stdGrp )
    children.reverse()
    
    for child in children:
        if child.find( 'Grp_std' ) != -1:
            stdGrp = child
            break

    stdNs    = stdGrp.replace( 'Grp_std', '' )
    mixamoNs = mixamoHipJnt.replace( 'Hips', '' )
    
    root = ['Std_Root', 'Hips']
    spine0 = ['Std_Back01', 'Spine']
    spine1 = ['Std_Back02', 'Spine1']
    chest = ['Std_Chest', 'Spine2']
    neck = ['Std_Neck', 'Neck']
    head = ['Std_Head', 'Head']
    collar = ['Std_Collar%s', '%sShoulder']
    shoulder = ['Std_Shoulder%s','%sArm']
    elbow = ['Std_Elbow%s','%sForeArm']
    wrist = ['Std_Wrist%s','%sHand']
    hip = ['Std_Hip%s','%sUpLeg']
    knee = ['Std_Knee%s','%sLeg']
    ankle = ['Std_Ankle%s','%sFoot']
    
    thumbs  = ['Std_Thumb%s*', '%sHandThumb*']
    indexs  = ['Std_Index%s*', '%sHandIndex*']
    middles = ['Std_Middle%s*', '%sHandMiddle*']
    rings   = ['Std_Ring%s*', '%sHandRing*']
    pinkys  = ['Std_Pinky%s*', '%sHandPinky*']
    
    targets = []
    targets.append( ['LeftHand','Std_Wrist_L_',  [-90, 0,  90]] )
    targets.append( ['RightHand','Std_Wrist_R_', [ 90, 0, -90]] )


    for mixamoJnt, stdHandle, rotation in targets:
        rotMatrix    = convert.rotateToMatrix( rotation )
        mixamoJntMtx = convert.listToMatrix( cmds.getAttr( mixamoNs + mixamoJnt + '.wm' ) )
        mtx = convert.matrixToList( rotMatrix * mixamoJntMtx )
        cmds.xform( stdNs + stdHandle, ws=1, matrix=mtx )
    
    targets = [ root, spine0, spine1, chest, neck, head, collar, shoulder, elbow, wrist, hip, knee, ankle, thumbs, indexs, middles, rings, pinkys ]
    
    for std, mixamoJnt in targets:
        std = stdNs + std
        mixamoJnt = mixamoNs + mixamoJnt
        
        if cmds.objExists( std ):
            mixamoPos = cmds.xform( mixamoJnt, q=1, ws=1, t=1 )
            cmds.move( mixamoPos[0], mixamoPos[1], mixamoPos[2], std, ws=1 )
            continue
        
        std_L_ = std % ( '_L_' )
        std_R_ = std % ( '_R_' )
        mixamo_L_ = mixamoJnt % ( 'Left' )
        mixamo_R_ = mixamoJnt % ( 'Right' )
        
        try:
            mixamoPos_L_ = cmds.xform( mixamo_L_, q=1, ws=1, t=1 )
            cmds.move( mixamoPos_L_[0], mixamoPos_L_[1], mixamoPos_L_[2], std_L_, ws=1 )
            mixamoPos_R_ = cmds.xform( mixamo_R_, q=1, ws=1, t=1 )
            cmds.move( mixamoPos_R_[0], mixamoPos_R_[1], mixamoPos_R_[2], std_R_, ws=1 )
        except:
            stdWrist_L_ = stdNs + 'Std_Wrist_L_'
            stdWrist_R_ = stdNs + 'Std_Wrist_R_'
            
            std_L_s = cmds.ls( std_L_, type='transform' )
            mixamo_L_s = cmds.ls( mixamo_L_, type='transform' )
            std_R_s = cmds.ls( std_R_, type='transform' )
            mixamo_R_s = cmds.ls( mixamo_R_, type='transform' )
            
            lenDiff = 0
            if std_L_s[0].lower().find( 'thumb' ) == -1:
                lenDiff = 1

            def getPoint( targetSrc, targetDst ):
                posSrc = OpenMaya.MPoint( *cmds.xform( targetSrc, q=1, ws=1, t=1 ) )
                posDst = OpenMaya.MPoint( *cmds.xform( targetDst, q=1, ws=1, t=1 ) )
                return posSrc + (OpenMaya.MVector( posDst - posSrc)*2)

            vectorL = getPoint( mixamo_L_s[-2], mixamo_L_s[-1] )
            vectorR = getPoint( mixamo_R_s[-2], mixamo_R_s[-1] )
            posL = [ vectorL.x, vectorL.y, vectorL.z ]
            posR = [ vectorR.x, vectorR.y, vectorR.z ]
            cmds.move( posL[0], posL[1], posL[2], std_L_s[-1], ws=1 )
            cmds.move( posR[0], posR[1], posR[2], std_R_s[-1], ws=1 )

            for i in range( len( mixamo_L_s )-1 ):
                pos = cmds.xform( mixamo_L_s[i], q=1, ws=1, t=1 )
                cmds.move( pos[0], pos[1], pos[2], std_L_s[i+lenDiff], ws=1 )
            
            for i in range( len( mixamo_R_s )-1 ):
                pos = cmds.xform( mixamo_R_s[i], q=1, ws=1, t=1 )
                cmds.move( pos[0], pos[1], pos[2], std_R_s[i+lenDiff], ws=1 )
            
            if lenDiff == 1:
                std_L_1Pos = OpenMaya.MPoint( *cmds.xform( std_L_s[1], q=1, ws=1, t=1 ) )
                std_R_1Pos = OpenMaya.MPoint( *cmds.xform( std_R_s[1], q=1, ws=1, t=1 ) )
                wrist_L_Pos = OpenMaya.MPoint( *cmds.xform( stdWrist_L_, q=1, ws=1, t=1 ) )
                wrist_R_Pos = OpenMaya.MPoint( *cmds.xform( stdWrist_R_, q=1, ws=1, t=1 ) )
                
                vL = std_L_1Pos - wrist_L_Pos
                vR = std_R_1Pos - wrist_R_Pos
                
                posL = wrist_L_Pos + vL*0.3
                posR = wrist_R_Pos + vR*0.3
                
                cmds.move( posL[0], posL[1], posL[2], std_L_s[0], ws=1 )
                cmds.move( posR[0], posR[1], posR[2], std_R_s[0], ws=1 )
    
    elbow_L_ = stdNs + 'Std_Elbow_L_'
    elbow_R_ = stdNs + 'Std_Elbow_R_'
    cmds.setAttr( stdNs + elbow_L_ + '.tz', -0.01 )
    cmds.setAttr( stdNs + elbow_R_ + '.tz', -0.01 )
    
    import math
    
    pElbow_L_ = cmds.listRelatives( elbow_L_, p=1, f=1 )[0]
    pElbow_R_ = cmds.listRelatives( elbow_R_, p=1, f=1 )[0]
    
    cmds.setAttr( stdNs + 'Std_Armpolevector_L_.tz', -math.fabs( cmds.getAttr( pElbow_L_ + '.tx' ) ) )
    cmds.setAttr( stdNs + 'Std_Armpolevector_R_.tz', -math.fabs( cmds.getAttr( pElbow_R_ + '.tx' ) ) )
         
    knee_L_ = stdNs + 'Std_Knee_L_'
    knee_R_ = stdNs + 'Std_Knee_R_'
    pKnee_L_ = cmds.listRelatives( knee_L_, p=1, f=1 )[0]
    pKnee_R_ = cmds.listRelatives( knee_R_, p=1, f=1 )[0]
    
    cmds.setAttr( stdNs + 'Std_Legpolyvector_L_.tz', math.fabs( cmds.getAttr( pKnee_L_ + '.tx' ) ) )
    cmds.setAttr( stdNs + 'Std_Legpolyvector_R_.tz', math.fabs( cmds.getAttr( pKnee_R_ + '.tx' ) ) )
    
    try:
        cmds.setAttr( stdNs + 'Std_Eye_L_.t', *cmds.getAttr( mixamoNs + 'LeftEye.t' )[0] )
        cmds.setAttr( stdNs + 'Std_Eye_R_.t', *cmds.getAttr( mixamoNs + 'RightEye.t' )[0] )
    except: pass
                

   
def removeAnimationKey( mixamoGrp ):
    
    topJoint = dag.getTopJointChildren( mixamoGrp )
    
    jnts = cmds.listRelatives( topJoint, c=1, ad=1, f=1 )
    jnts += topJoint
    
    for jnt in jnts:
        animCurves = cmds.listConnections( jnt, s=1, d=0, type='animCurve' )
        cmds.delete( animCurves )
    



def mixamoMeshToAutoRig( mixamoMeshGrp, autoRigGrp ):
    
    meshs = cmds.listRelatives( mixamoMeshGrp, c=1, ad=1, type='mesh' )
    allJoints = []
    for mesh in meshs:
        if cmds.getAttr( mesh + '.io' ): continue
        allJoints += dag.getNodeFromHistory( mesh, 'joint' )


    def getRigNs( rigGrp ):
        
        trs = cmds.listRelatives( autoRigGrp, c=1, ad=1, type='transform', f=1 )
        rigNs = ''
        for tr in trs:
            shape = dag.getShape( tr )
            if not shape: continue
            if dag.getLocalName(tr)[-7:] != 'Ctl_All': continue
            rigNs = dag.getLocalName(tr).replace( 'Ctl_All', '' )
            break
        return rigNs

    
    def setLabelToMixamoJoints( mixamoNs, allJoints ):
        
        for joint in allJoints:
            cmds.setAttr( joint + '.type', 18 )
            cmds.setAttr( joint + '.otherType', joint.replace( mixamoNs, '' ), type='string' )


    def getMixamoNs( joints ):
        hipJoint = ''
        for i in range( len( allJoints ) ):
            if allJoints[i][-4:] == 'Hips': 
                hipJoint = allJoints[i]
                break
        
        return hipJoint.replace( 'Hips', '' )
    
    
    def setLabelToRig( rigns, mixns ):
        
        targets  = []
        targets.append( ['SkinJnt_Spline00', 'Hips'] )
        targets.append( ['SkinJnt_Spline02', 'Spine'] )
        targets.append( ['SkinJnt_Spline03', 'Spine1'] )
        targets.append( ['SkinJnt_Spline04', 'Spine2'] )
        targets.append( ['SkinJnt_Collar_%SIDE%_', '%SIDE%Shoulder'] )
        targets.append( ['SkinJnt_Arm_%SIDE%_2', '%SIDE%Arm'] )
        targets.append( ['SkinJnt_Arm_%SIDE%_3', '%SIDE%ForeArm'] )
        targets.append( ['SkinJnt_Arm_%SIDE%_6', '%SIDE%Hand'] )
        targets.append( ['SkinJnt_Leg_%SIDE%_2', '%SIDE%UpLeg'] )
        targets.append( ['SkinJnt_Leg_%SIDE%_3', '%SIDE%Leg'] )
        targets.append( ['SkinJnt_Foot_%SIDE%_', '%SIDE%Foot'] )
        targets.append( ['SkinJnt_toe_%SIDE%_', '%SIDE%ToeBase'] )
        targets.append( ['SkinJnt_Neck', 'Neck'] )
        targets.append( ['SkinJnt_head', 'Head'] )
        targets.append( ['SkinJnt_Thumb_%SIDE%_%NUM%', '%SIDE%HandThumb%NUMADD%'] )
        targets.append( ['SkinJnt_Index_%SIDE%_%NUM%', '%SIDE%HandIndex%NUM%'] )
        targets.append( ['SkinJnt_MIddle_%SIDE%_%NUM%', '%SIDE%HandMiddle%NUM%'] )
        targets.append( ['SkinJnt_Ring_%SIDE%_%NUM%', '%SIDE%HandRing%NUM%'] )
        targets.append( ['SkinJnt_Pinky_%SIDE%_%NUM%', '%SIDE%HandPinky%NUM%'] )
        
        for skinJnt, mixamoJnt in targets:
            skinJnt = rigns + skinJnt
            mixamoJnt = mixns + mixamoJnt
            if cmds.objExists( skinJnt ):
                cmds.setAttr( skinJnt + '.type', 18 )
                cmds.setAttr( skinJnt + '.otherType', cmds.getAttr( mixamoJnt + '.otherType' ), type='string' )
                continue
            
            for rigSide, mixamoSide in [['L', 'Left'], ['R', 'Right']]:
                sideSkinJnt = skinJnt.replace( '%SIDE%', rigSide )
                sideMixamoJnt = mixamoJnt.replace( '%SIDE%', mixamoSide )
                
                if cmds.objExists( sideSkinJnt ):
                    cmds.setAttr( sideSkinJnt + '.type', 18 )
                    cmds.setAttr( sideSkinJnt + '.otherType', cmds.getAttr( sideMixamoJnt + '.otherType' ), type='string' )
                    continue
                
                currentNum = 0
                while True:
                    if currentNum > 5: break
                    sideNumSkinJnt = sideSkinJnt.replace( '%NUM%', '%02d' % currentNum )
                    sideNumMixamoJnt = sideMixamoJnt.replace( '%NUM%', '%d' % currentNum ).replace( '%NUMADD%', '%d' % (currentNum+1) )
                    currentNum += 1
                    if not cmds.objExists( sideNumMixamoJnt ): continue
                    if not cmds.objExists( sideNumSkinJnt ): break
                    cmds.setAttr( sideNumSkinJnt + '.type', 18 )
                    cmds.setAttr( sideNumSkinJnt + '.otherType', cmds.getAttr( sideNumMixamoJnt + '.otherType' ), type='string' )
    
    
    def mixamoFacialRig( mixamoMeshs, duMeshs ):
        
        import DJB_Character.FacialControls
        import DJB_Character.CharacterNode
        
        facialConnector = ''
        blendShapes = []
        allMeshs = []
        for i in range( len( mixamoMeshs ) ):
            mixamoMesh = mixamoMeshs[i]
            blendNodes = dag.getNodeFromHistory( mixamoMesh, 'blendShape' )
            if not blendNodes: continue
            duMesh = duMeshs[i]
            srcMeshs = cmds.listConnections( blendNodes[0], s=1, d=0, type='mesh', shapes=1 )
            srcMeshs.append( dag.getShape( duMesh ) )
            blendShape = cmds.blendShape( srcMeshs, frontOfChain=1 )[0]
            blendShapes.append( blendShape )
            
            srcMeshTrs = cmds.listConnections( blendNodes[0], s=1, d=0, type='mesh' )
            allMeshs += srcMeshTrs
            
            if facialConnector: continue
            
            inst = DJB_Character.FacialControls.FacialControls( srcMeshs )
            leftEye = DJB_Character.CharacterNode.DJB_CharacterNode("LeftEye", optional_ = 1, parent = 'Ctl_Head', joint_namespace_ = '')
            RightEye = DJB_Character.CharacterNode.DJB_CharacterNode("RightEye", optional_ = 1, parent = 'Ctl_Head', joint_namespace_ = '')
            inst.create( 'Ctl_All', 'Ctl_Head', leftEye, RightEye, True )
            if cmds.objExists( 'Facial_Hookup' ):
                facialConnector = 'Facial_Hookup'
            #inst.connectUI( 'Ctl_All', 'Ctl_Head', leftEye, RightEye )
        
        attrs = cmds.listAttr( facialConnector, k=1 )
        for blendShape in blendShapes:
            for i in range( len( attrs )):
                if not cmds.isConnected( facialConnector+ '.' + attrs[i], blendShape + '.w[%d]' % i ):
                    cmds.connectAttr( facialConnector+ '.' + attrs[i], blendShape + '.w[%d]' % i )
        
        return facialConnector, 'Facial_CTRLS_GRP', cmds.group( allMeshs, n='mixamoBlendShapes' )


    mixns = getMixamoNs( allJoints )
    rigns = getRigNs( autoRigGrp )
    setLabelToMixamoJoints( mixns, allJoints )
    setLabelToRig( rigns, mixns )
    
    duMeshGrp = cmds.duplicate( mixamoMeshGrp )[0]
    
    mixamoMeshs = cmds.listRelatives( mixamoMeshGrp, c=1, ad=1, f=1, type='mesh' )
    duMeshs = cmds.listRelatives( duMeshGrp, c=1, ad=1, f=1, type='mesh' )
    cmds.refresh()
    
    mixamoMeshTrs = []
    for mixamoMesh in mixamoMeshs:
        if cmds.getAttr( mixamoMesh + '.io' ):
            continue
        mixamoMeshTrs.append( cmds.listRelatives( mixamoMesh, p=1, f=1 )[0] )
    
    duMeshTrs = []
    for duMesh in duMeshs:
        if cmds.getAttr( duMesh + '.io' ):
            cmds.delete( duMesh )
            continue
        duMeshTrs.append( cmds.listRelatives( duMesh, p=1, f=1 )[0] )
    
    skinJnts = cmds.ls( rigns + 'SkinJnt_*', type='joint' )
    
    bindObjs = []
    bindObjs += duMeshTrs
    bindObjs += skinJnts
    
    cmds.select( bindObjs )
    cmds.SmoothBindSkin()
    
    for i in range( len( mixamoMeshTrs ) ):
        cmds.copySkinWeights( mixamoMeshTrs[i], duMeshTrs[i], noMirror=1, surfaceAssociation='closestPoint', influenceAssociation=['label','closestJoint'] )
    try:
        Hookup, facialControls, blendShapes = mixamoFacialRig( mixamoMeshTrs, duMeshTrs )
        cmds.parent( Hookup, facialControls, 'Ctl_Head' )
        cmds.parent( blendShapes, 'SET' )
    except: pass
    
    return duMeshGrp




def createMixamoHandleForAutoRig( mixamoHip ):
    
    ns = mixamoHip.replace( 'Hips', '' )
    targets = []
    targets.append( ['Hips', 'Root', [0,0,0], [0,0,0], 1 ] )
    targets.append( ['Spine', 'Back01', [0,0,0], [0,0,0], 1 ] )
    targets.append( ['Spine1', 'Back02', [0,0,0], [0,0,0], 1 ] )
    targets.append( ['Spine2', 'Chest', [0,0,0], [0,0,0], 1 ] )
    targets.append( ['Neck', 'Neck', [0,0,0], [0,0,0], 1 ] )
    targets.append( ['Head', 'Head', [0,0,0], [0,0,0], 1 ] )
    
    targets.append( ['LeftShoulder', 'Collar_L_', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftArm', 'Shoulder_L_', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftForeArm', 'Elbow_L_', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftHand', 'Wrist_L_', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftHandThumb%NUM%', 'Thumb_L_%NUMMINUSONE%', [0,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftHandIndex%NUM%', 'Index_L_%NUM%', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftHandMiddle%NUM%', 'Middle_L_%NUM%', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftHandRing%NUM%',  'Ring_L_%NUM%', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftHandPinky%NUM%', 'Pinky_L_%NUM%', [-90,0,90], [0,0,0], 0 ] )
    targets.append( ['LeftUpLeg', 'Hip_L_',  [0,0,90], [0,0,-90], 0 ] )
    targets.append( ['LeftLeg', 'Knee_L_',   [0,0,90], [0,0,-90], 0 ] )
    targets.append( ['LeftFoot', 'Ankle_L_', [0,60,90], [0,60,-90], -1 ] )
    
    targets.append( ['RightShoulder', 'Collar_R_', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightArm', 'Shoulder_R_', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightForeArm', 'Elbow_R_', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightHand', 'Wrist_R_', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightHandThumb%NUM%', 'Thumb_R_%NUMMINUSONE%', [180,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightHandIndex%NUM%', 'Index_R_%NUM%', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightHandMiddle%NUM%', 'Middle_R_%NUM%', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightHandRing%NUM%',  'Ring_R_%NUM%', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightHandPinky%NUM%', 'Pinky_R_%NUM%', [90,0,-90], [180,0,0], 3 ] )
    targets.append( ['RightUpLeg', 'Hip_R_',  [180,0,-90],  [180,0,90], 3 ] )
    targets.append( ['RightLeg', 'Knee_R_',   [180,0,-90],  [180,0,90], 3 ] )
    targets.append( ['RightFoot', 'Ankle_R_', [180,-60,-90],  [180,-60,90], -1 ] )
    
    attribute.addAttr( mixamoHip, ln='mocType', min=0, max=1, dv=1, cb=1 )
    type1Attr = mixamoHip + '.mocType'
    revNode = cmds.createNode( 'reverse' )
    cmds.connectAttr( type1Attr, revNode + '.inputX' )
    type2Attr = revNode + '.outputX'
    
    def createHandle( handleName, rotation1, rotation2, axisIndex ):
        
        handle = cmds.createNode( 'transform', n= handleName )
        handle = cmds.parent( handle, mixamoJoint )[0]
        transform.setToDefault( handle )
        compose1 = cmds.createNode( 'composeMatrix' )
        compose2 = cmds.createNode( 'composeMatrix' )
        cmds.setAttr( compose1 + '.ir', *rotation1 )
        cmds.setAttr( compose2 + '.ir', *rotation2 )
        
        wtMtx = cmds.createNode( 'wtAddMatrix' )
        cmds.connectAttr( compose1 + '.outputMatrix', wtMtx + '.i[0].m' )
        cmds.connectAttr( compose2 + '.outputMatrix', wtMtx + '.i[1].m' )
        cmds.connectAttr( type2Attr, wtMtx + '.i[0].w' )
        cmds.connectAttr( type1Attr, wtMtx + '.i[1].w' )
        
        dcmp = connect.getDcmp( wtMtx )
        handle, handleP = dag.makeParent( handle )[0]
        cmds.connectAttr( dcmp + '.or', handleP + '.r' )
        
        cmds.setAttr( handle + '.dh', 1 )
        cmds.setAttr( handle + '.dla', 1 )
        
        mixamoJntChild = cmds.listRelatives( mixamoJoint, c=1, f=1 )
        if mixamoJntChild and axisIndex != -1:
            if len( mixamoJntChild ) == 1:
                connect.lookAtConnect( mixamoJntChild[0], handle, axisIndex )
        
    
    for mixamoName, handleName, rotation1, rotation2, axisIndex in targets:
        mixamoJoint = ns + mixamoName
        if cmds.objExists( mixamoJoint ):
            realHandleName = ns + 'handle_' + handleName
            if cmds.objExists( realHandleName ): continue
            createHandle( realHandleName, rotation1, rotation2, axisIndex )
        
        currentNum = 0
        while True:
            currentNum +=1 
            if(currentNum > 10): break
            mixamoJoint = ns + mixamoName.replace( '%NUM%', '%d' % currentNum )
            if not cmds.objExists( mixamoJoint ): break
            realHandleName = ns + 'handle_' + handleName.replace( '%NUMMINUSONE%', '%02d' % (currentNum-1) ).replace( '%NUM%', '%02d' % currentNum )
            if cmds.objExists( realHandleName ): continue
            createHandle( realHandleName, rotation1, rotation2, axisIndex )
    



def connectMixamoJointToAutoRig( mixamoHip, setGrp ):
    
    import creation
    creation.connectMocapJoint( setGrp )
    createMixamoHandleForAutoRig( mixamoHip )
    
    mocJointTop = creation.getMocapJoint( setGrp )
    mocNs = mocJointTop.replace( 'MocJnt_Root', '' )
    mixamoNs = mixamoHip.replace( 'Hips', '' )
    
    mocChildren = cmds.listRelatives( mocJointTop, c=1, ad=1 )
    mocChildren.append( mocJointTop )
    
    ctlAll = mocNs + 'Ctl_All'
    
    for mocChild in mocChildren:
        handle = mocChild.replace( mocNs + 'MocJnt_', mixamoNs + 'handle_' )
        if not cmds.objExists( handle ): continue
        
        mmBase = cmds.createNode( 'multMatrix' )
        invMm  = cmds.createNode( 'inverseMatrix' )
        mm     = cmds.createNode( 'multMatrix' )
        
        cmds.connectAttr( mocChild + '.pm', mmBase + '.i[0]' )
        cmds.connectAttr( ctlAll + '.wim',  mmBase + '.i[1]' )
        cmds.connectAttr( mmBase + '.o', invMm + '.inputMatrix' )
        cmds.connectAttr( handle + '.wm', mm + '.i[0]' )
        cmds.connectAttr( invMm + '.outputMatrix', mm + '.i[1]' )
        dcmp = connect.getDcmp( mm )
        
        if not cmds.isConnected( dcmp + '.or',  mocChild + '.r' ):
            cmds.connectAttr( dcmp + '.or',  mocChild + '.r', f=1 )
        
        if mocChild.find( 'MocJnt_Root' ) != -1:
            if not cmds.isConnected( dcmp + '.ot',  mocChild + '.t' ):
                cmds.connectAttr( dcmp + '.ot',  mocChild + '.t', f=1 )




