import maya.cmds as cmds
import chModules.rigbase as rigbase
import copy
import chModules.system.basicfunc as basicFunc

colorIndexDict = { 'L': 13, 'R': 6 }
swColorIndex = 22

class Data( object ):
    def __init__(self, rigInstance ):
        self.armLInits = rigInstance.armLInits        
        self.armRInits = rigInstance.armRInits
        self.legLInits = rigInstance.legLInits        
        self.legRInits = rigInstance.legRInits
        self.shoulderLConst = rigInstance.shoulderLConst
        self.shoulderRConst = rigInstance.shoulderRConst
        self.hipLConst = rigInstance.hipLConst
        self.hipRConst = rigInstance.hipRConst
        self.rigInstance = rigInstance
        
    def _sepArmList(self, armList ):
        return armList[0], armList[1], armList[2], armList[3]
    def _setArmAddList(self, armList ):
        return armList[-2], armList[-1]
    
    def _getProperInit( self, frontName, side ):
        if side == 'L':
            if frontName == 'Arm':
                firstInit, secondInit, thirdInit, fourthInit = self._sepArmList( self.armLInits )
                upperInit, lowerInit = self._setArmAddList(self.armLInits )
            else:
                firstInit, secondInit, thirdInit, fourthInit = self._sepArmList( self.legLInits )
                upperInit, lowerInit = self._setArmAddList(self.legLInits )
        else:
            if frontName == 'Arm':
                firstInit, secondInit, thirdInit, fourthInit = self._sepArmList( self.armRInits )
                upperInit, lowerInit = self._setArmAddList( self.armRInits )
            else:
                firstInit, secondInit, thirdInit, fourthInit = self._sepArmList( self.legRInits )
                upperInit, lowerInit = self._setArmAddList(self.legRInits )

        return firstInit, secondInit, thirdInit, fourthInit, upperInit, lowerInit
    
    def rigGroupSet( self, frontName, side, ikOrFk ):
        self.firstInit, self.secondInit, self.thirdInit, self.fourthInit, self.upperInit, self.lowerInit = self._getProperInit( frontName, side )
        firstPos = cmds.getAttr( self.firstInit+'.wm' )
        setGroup = cmds.createNode( 'transform', n='%s_%s_%s_GRP' %( frontName, side, ikOrFk ) )
        cmds.xform( setGroup, matrix=firstPos )
        self.setGroup = setGroup
        
        self.firstPose = cmds.getAttr( self.firstInit+'.wm' )
        self.secondPose = cmds.getAttr( self.secondInit+'.wm' )
        self.thirdPose = cmds.getAttr( self.thirdInit+'.wm' )
        
class IkRig( Data ):
    def __init__( self, rigInstance ):
        Data.__init__( self, rigInstance )
        
    def ikPinCtlSet(self, frontName, side ):
        size = [1,1,1]
        if side == 'R':
            size = [-1,-1,-1]
        self.ikPinCtl = rigbase.Controler( n='%s_%s_IK_Pin_CTL' %( frontName, side ) )
        self.ikPinCtl.setShape( typ='pin', size=size )
        self.ikPinCtl.setColor( colorIndexDict[side] )
        
        rigbase.AttrEdit( self.ikPinCtl.name ).lockAndHideAttrs( 'sx', 'sy', 'sz', 'v' )
        
        worldMtx = cmds.xform( self.thirdInit, q=1, ws=1, matrix=1 )
        cmds.xform( self.ikPinCtl.name, ws=1, matrix = worldMtx )
        
        if frontName == 'Arm':
            self.ikBlMtx = cmds.createNode( 'blendTwoMatrix', n='%s_%s_Ik2_blendMtx' %( frontName, side ) )
            self.ikTrMtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_IkTrMtxDcmp' %( frontName, side ) )
            self.ikRotMtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_IkRotMtxDcmp' %( frontName, side ) )
        
        self.rigInstance.ikBlMtx = self.ikBlMtx
        self.rigInstance.ikPinCtl = self.ikPinCtl
        
        cmds.parent( self.ikPinCtl.transformGrp, self.rigInstance.worldCtl )

    def followSet( self, frontName, side ):
        followMtx = cmds.createNode( 'followMatrix', n='%s_%s_FollowMtx' %( frontName, side ) )
        
        def allMtxDcmp():
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_All_F_MtxDcmp' %( frontName, side ) )
            cmds.connectAttr( self.thirdInit +'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( self.rigInstance.initAll+'.wim', mtxDcmp+'.i[1]' )
            return mtxDcmp
                    
        def setMtxDcmp( part ):
            partName = part.replace( '_Init', '' )
            dcmp    = cmds.createNode( 'decomposeMatrix', n='%s_%s_%s_F_Dcmp'    %( frontName, side, partName ) )
            comp    = cmds.createNode( 'composeMatrix',   n='%s_%s_%s_F_Comp'    %( frontName, side, partName ) )
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_%s_F_MtxDcmp' %( frontName, side, partName ) )
            
            cmds.connectAttr( self.thirdInit +'.wm', dcmp+'.imat' )
            cmds.connectAttr( dcmp+'.ot', comp+'.it' )
            cmds.connectAttr( comp+'.outputMatrix', mtxDcmp+'.i[0]' )
            cmds.connectAttr( part+'.wim', mtxDcmp+'.i[1]' )
            return mtxDcmp
        
        def getPinMatrix():
            pinMtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_PinMtxDcmp'    %( frontName, side ) )
            pinCompose = cmds.createNode( 'composeMatrix', n='%s_%s_PinComp'    %( frontName, side ) )
            
            cmds.connectAttr( self.ikPinCtl+'.t', pinCompose+'.it' )
            cmds.connectAttr( self.ikPinCtl+'.m', pinMtxDcmp+'.i[1]' )
            cmds.connectAttr( pinMtxDcmp+'.or'   , pinCompose+'.ir' )
            
            self.pinMtxDcmp = pinMtxDcmp
            
            return pinCompose+'.outputMatrix'
            
        fp_inWorld =  cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inWorld' ) )
        fp_inMove =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inMove' ) )
        fp_inFly =    cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inFly' ) )
        fp_inRoot =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inRoot' ) )
        fp_inHip =    cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inHip' ) )
        
        allFpDcmp = setMtxDcmp( self.rigInstance.initAll )
        rootFpDcmp = setMtxDcmp( self.rigInstance.rootInit )
        
        cmds.connectAttr( allFpDcmp   +'.ot', fp_inWorld +'.t' )
        cmds.connectAttr( allFpDcmp   +'.or', fp_inWorld +'.r' )
        cmds.connectAttr( allFpDcmp   +'.ot', fp_inMove  +'.t' )
        cmds.connectAttr( allFpDcmp   +'.or', fp_inMove  +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inRoot  +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inRoot  +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inFly   +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inFly   +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inHip   +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inHip   +'.r' )
        
        cmds.parent( fp_inWorld, self.rigInstance.worldCtl )
        cmds.parent( fp_inMove , self.rigInstance.moveCtl )
        cmds.parent( fp_inFly , self.rigInstance.flyCtl )
        cmds.parent( fp_inRoot , self.rigInstance.rootGrp )
        cmds.parent( fp_inHip , self.rigInstance.hipCtl )
        
        cmds.connectAttr( fp_inWorld  +'.wm', followMtx+'.originalMatrix' )
        
        pinMatrix = getPinMatrix()
        
        if frontName == 'Arm':
            fp_inChest =  cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inChest' ) )
            fp_inHead =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inHead' ) )
            fp_inCollar = cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inCollar' ) )
            
            headFpDcmp = setMtxDcmp( self.rigInstance.headInits[2] )
            chestFpDcmp = setMtxDcmp( self.rigInstance.torsoInits[2] )
        
            if side == 'L':
                collarFpDcmp = setMtxDcmp( self.rigInstance.torsoInits[3] )
            else:
                collarFpDcmp = setMtxDcmp( self.rigInstance.torsoInits[4] )
            
            cmds.connectAttr( headFpDcmp +'.ot' , fp_inHead  +'.t' )
            cmds.connectAttr( headFpDcmp +'.or' , fp_inHead  +'.r' )
            cmds.connectAttr( chestFpDcmp +'.ot', fp_inChest +'.t' )
            cmds.connectAttr( chestFpDcmp +'.or', fp_inChest +'.r' )
            cmds.connectAttr( collarFpDcmp+'.ot', fp_inCollar+'.t' )
            cmds.connectAttr( collarFpDcmp+'.or', fp_inCollar+'.r' )
            
            #rigbase.constraint( fp_inChest, self.setGroup )
        
            cmds.parent( fp_inChest , self.rigInstance.chestCtl.replace( 'Chest', 'ChestMove' ) )
            cmds.parent( fp_inHead,   self.rigInstance.headCtl )
            if side == 'L':
                cmds.parent( fp_inCollar , self.rigInstance.collarLCtl )
            else:
                cmds.parent( fp_inCollar , self.rigInstance.collarRCtl )
                
            cmds.connectAttr( fp_inCollar  +'.wm', followMtx+'.inputMatrix[0]' )
            cmds.connectAttr( fp_inHead    +'.wm', followMtx+'.inputMatrix[1]' )
            cmds.connectAttr( fp_inChest   +'.wm', followMtx+'.inputMatrix[2]' )
            cmds.connectAttr( fp_inHip     +'.wm', followMtx+'.inputMatrix[3]' )
            cmds.connectAttr( fp_inRoot    +'.wm', followMtx+'.inputMatrix[4]' )
            cmds.connectAttr( fp_inFly     +'.wm', followMtx+'.inputMatrix[5]' )
            cmds.connectAttr( fp_inMove    +'.wm', followMtx+'.inputMatrix[6]' )
            cmds.connectAttr( pinMatrix          , followMtx+'.inputMatrix[7]' )
        else:
            cmds.connectAttr( fp_inHip     +'.wm', followMtx+'.inputMatrix[0]' )
            cmds.connectAttr( fp_inRoot    +'.wm', followMtx+'.inputMatrix[1]' )
            cmds.connectAttr( fp_inFly     +'.wm', followMtx+'.inputMatrix[2]' )
            cmds.connectAttr( fp_inMove    +'.wm', followMtx+'.inputMatrix[3]' )
            cmds.connectAttr( pinMatrix          , followMtx+'.inputMatrix[4]' )
        
        self.followMtx = followMtx
        
        return followMtx

    def ctlSet( self, frontName, side ):
        thirdMMtx = basicFunc.getLocalMMatrix( self.thirdInit , 'All_InitCTL' )
        
        offsetMult = thirdMMtx( 3, 1 ) 
        if side == 'R':
            offsetMult *= -1
        
        cmds.select( d=1 )
        ctl = cmds.joint( n= '%s_%s_IK_CTL' %( frontName, side ), radius = 0 )
        rigbase.AttrEdit( ctl ).lockAndHideAttrs( 'sx','sy','sz','v','radius' )
        
        if frontName == 'Arm':    
            rigbase.addControlerShape( ctl, typ='box', size=[.05,.7,.7], n=ctl )
        else:
            rigbase.addControlerShape( ctl, typ='circle', center=[offsetMult,0,0], normal=[1,0,0], radius=1 )
        rigbase.controlerSetColor( ctl, colorIndexDict[side] )
        ctlGrp = rigbase.addParent( ctl )
        
        followMtx = self.followSet( frontName, side )
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n=followMtx.replace( 'FollowMtx', 'Follow_MtxDcmp' ) )
        cmds.connectAttr( followMtx+'.outputMatrix', mtxDcmp+'.i[0]' )
        cmds.connectAttr( ctlGrp+'.pim', mtxDcmp+'.i[1]' )
        
        cmds.connectAttr( mtxDcmp+'.ot', ctlGrp+'.t' )
        cmds.connectAttr( mtxDcmp+'.or', ctlGrp+'.r' )
        
        ctlMtxDcmp = cmds.createNode( 'multMatrixDecompose', n=followMtx.replace( 'FollowMtx', 'Init_JointOrient' ) )
        cmds.connectAttr( self.thirdInit+'.wm', ctlMtxDcmp+'.i[0]' )
        cmds.connectAttr( self.rigInstance.initAll+'.wim', ctlMtxDcmp+'.i[1]' )
        cmds.connectAttr( ctlMtxDcmp+'.outputInverseMatrix', self.pinMtxDcmp+'.i[0]' )
        
        cmds.connectAttr( ctlMtxDcmp+'.or', ctl+'.jo' )
        
        attrEdit = rigbase.AttrEdit( ctl )
        rigbase.addHelpTx( ctl, 'Middle' )
        attrEdit.addAttr( ln='poleTwist', k=1 )
        attrEdit.addAttr( ln='length', k=1, min=-50 )
        attrEdit.addAttr( ln='bias', k=1, min=-50, max=50 )
        rigbase.addHelpTx( ctl, 'Other' )
        attrEdit.addAttr( ln='stretchAble', k=1, min=0, max=1 )
        
        cmds.parent( ctlGrp, self.rigInstance.worldCtl )

        if frontName == 'Leg':
            attrEdit.addAttr( ln='kneeAutoAngle', k=1, min=0, max=1 )
            
            ikPoleVAngleObj = cmds.createNode( 'transform', n='%s_%s_IK_PoleVAngleObj' %( frontName, side ) )
            ikPoleVAngleObjGrp = cmds.group( ikPoleVAngleObj, n = ikPoleVAngleObj+'_GRP' )
            ikPoleVAngle    = cmds.createNode( 'wristAngle', n='%s_%s_IK_PoleVAngle' %( frontName, side ) )
            ikCtlCompose    = cmds.createNode( 'composeMatrix', n='%s_%s_IK_CtlCompose' %( frontName, side ) )
            
            cmds.parent( ikPoleVAngleObjGrp, ctlGrp )
            rigbase.transformDefault( ikPoleVAngleObjGrp )
            
            cmds.connectAttr( ctl+'.kneeAutoAngle', ikPoleVAngle+'.angleRate' )
            cmds.connectAttr( ctl+'.t', ikPoleVAngleObjGrp+'.t' )
            cmds.connectAttr( ctl+'.jo', ikPoleVAngleObjGrp+'.r' )
            
            cmds.connectAttr( ctl+'.r', ikCtlCompose+'.ir' ) 
            cmds.connectAttr( ikCtlCompose+'.outputMatrix', ikPoleVAngle+'.inputMatrix' )
            cmds.connectAttr( ikPoleVAngle+'.outAngle', ikPoleVAngleObj+'.rx' )
            
            self.ikPoleVAngleObj = ikPoleVAngleObj
        
        self.ikCtl = ctl
        self.ikCtlGrp = ctlGrp
        
    def poleVectorSet( self, frontName, side ):
        multDir = 1
        inverseTrans = False
        inverseDist =  False
        
        if side      == 'R'  :
            multDir *=-1
            inverseTrans = True
            
        if frontName + side in ['LegR', 'ArmL']:
            inverseDist = True
        
        poleVCtl, poleVCtlGrp = rigbase.putControler( self.fourthInit, n='%s_%s_PoleV_CTL' %( frontName, side ), typ='sphere', size=[.2,.2,.2] )
        rigbase.controlerSetColor( poleVCtl, colorIndexDict[side] )
        poleVCtlAttrEdit = rigbase.AttrEdit( poleVCtl )
        poleVCtlAttrEdit.lockAndHideAttrs( 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v' )
        rigbase.addHelpTx( poleVCtl, 'PV_opts' )
        poleVCtlAttrEdit.addAttr( ln='positionAttach', min=0, max=1, k=1 )
        
        ctlConstGrp = cmds.createNode( 'transform', n=poleVCtlGrp.replace( '_CTL_GRP', '_CTL_Const_GRP' ) )
        
        cmds.parent( ctlConstGrp, self.setGroup )
        rigbase.transformDefault( ctlConstGrp )
        cmds.parent( poleVCtlGrp, ctlConstGrp )
        
        if frontName == 'Arm':
            childMtxDcmp = rigbase.getChildMtxDcmp( self.fourthInit, self.firstInit )
            
            cmds.connectAttr( childMtxDcmp +'.ot'  , poleVCtlGrp+'.t' )
            cmds.connectAttr( childMtxDcmp +'.or'  , poleVCtlGrp+'.r' )
        
        elif frontName == 'Leg':
            if side == 'L':
                inverseObj = self.rigInstance.hipLConst_inRoot
            else:
                inverseObj = self.rigInstance.hipRConst_inRoot
            moveMtx = cmds.createNode( "multMatrix", n=poleVCtl.replace( 'CTL', 'CtlPoseMoveMtx' ) )
            cmds.connectAttr( self.fourthInit+'.wm' ,  moveMtx+'.i[0]', f=1 )
            cmds.connectAttr( self.thirdInit+'.wim' ,  moveMtx+'.i[1]', f=1 )
            cmds.connectAttr( self.ikPoleVAngleObj+'.wm' ,  moveMtx+'.i[2]' )
            cmds.connectAttr( inverseObj+'.wim',  moveMtx+'.i[3]' )
            
            staticMtx = cmds.createNode( 'multMatrix', n=poleVCtl.replace( 'CTL', 'CtlPoseStaticMtx' ) )
            cmds.connectAttr( self.fourthInit+'.wm', staticMtx+'.i[0]' )
            cmds.connectAttr( self.firstInit+'.wim', staticMtx+'.i[1]' )
            if side == 'L':
                cmds.connectAttr( self.rigInstance.hipLConstInFly+'.wm', staticMtx+'.i[2]' )
            else:
                cmds.connectAttr( self.rigInstance.hipRConstInFly+'.wm', staticMtx+'.i[2]' )
            cmds.connectAttr( ctlConstGrp+'.wim', staticMtx+'.i[3]' )
            
            blMtxDcmp = cmds.createNode( 'blendTwoMatrixDecompose', n=poleVCtl.replace( 'CTL', 'CtlPoseBlMtxDcmp' ) )
            
            cmds.connectAttr( moveMtx+'.o', blMtxDcmp+'.inMatrix1' )
            cmds.connectAttr( staticMtx+'.o', blMtxDcmp+'.inMatrix2' )
            
            cmds.connectAttr( poleVCtl+'.positionAttach', blMtxDcmp+'.ab' )
            
            cmds.connectAttr( blMtxDcmp +'.ot'  , poleVCtlGrp+'.t' )
            cmds.connectAttr( blMtxDcmp +'.or'  , poleVCtlGrp+'.r' )
        
        self.poleVCtl = poleVCtl
        self.ctlConstGrp = ctlConstGrp

    def jointSet( self, frontName, side ):
        inverse = False
        if side == 'R':
            inverse = True
        
        cmds.select( self.setGroup )
        ik0Jnt = cmds.joint( n='%s_%s_IK0_JNT' %( frontName, side ) )
        ik1Jnt = cmds.joint( n='%s_%s_IK1_JNT' %( frontName, side ) )
        ik2Jnt = cmds.joint( n='%s_%s_IK2_JNT' %( frontName, side ) )
        
        twoSide = cmds.createNode( 'twoSideSlidingDistance', n='%s_%s_SlidingDist' %( frontName, side ) )
        ikStretch = cmds.createNode( 'ikStretch', n='%s_%s_ikStretch' %( frontName, side ) )
        upperAttatch = cmds.createNode( 'multMatrixDecompose', n='%s_%s_upperAttatchMtx' %( frontName, side ) )
        lowerAttatch = cmds.createNode( 'multMatrixDecompose', n='%s_%s_lowerAttatchMtx' %( frontName, side ) )
        blendAttatch = cmds.createNode( 'blendColors'        , n='%s_%s_attatchBlend'    %( frontName, side ) )
        
        cmds.setAttr( twoSide+'.slidingAttrSize' , 10 )
        cmds.setAttr( twoSide+'.distanceAttrSize', 10 )
        cmds.setAttr( upperAttatch+'.inverseDistance', inverse )
        cmds.setAttr( lowerAttatch+'.inverseDistance', inverse )
        
        handle = cmds.ikHandle( sj=ik0Jnt, ee=ik2Jnt, sol='ikRPsolver', n='%s_%s_Handle' %( frontName, side ) )[0]
        cmds.parent( handle, self.setGroup )
        
        cmds.connectAttr( self.secondInit+'.tx', twoSide+'.inputDistance1' )
        cmds.connectAttr( self.thirdInit+'.tx', twoSide+'.inputDistance2' )
        cmds.connectAttr( self.poleVCtl+'.wm', upperAttatch+'.i[0]' )
        cmds.connectAttr( self.setGroup+'.wim'  , upperAttatch+'.i[1]' )
        cmds.connectAttr( handle  +'.wm' , lowerAttatch+'.i[0]' )
        cmds.connectAttr( self.poleVCtl+'.wim'  , lowerAttatch+'.i[1]' )
        cmds.connectAttr( twoSide+'.outputDistance1', ikStretch+'.inputDistance[0]' )
        cmds.connectAttr( twoSide+'.outputDistance2', ikStretch+'.inputDistance[1]' )
        cmds.connectAttr( ikStretch+'.outputDistance[0]', blendAttatch+'.color2R' )
        cmds.connectAttr( ikStretch+'.outputDistance[1]', blendAttatch+'.color2G' )
        cmds.connectAttr( upperAttatch+'.outputDistance', blendAttatch+'.color1R' )
        cmds.connectAttr( lowerAttatch+'.outputDistance', blendAttatch+'.color1G' )
        cmds.connectAttr( blendAttatch+'.outputR', ik1Jnt+'.tx' )
        cmds.connectAttr( blendAttatch+'.outputG', ik2Jnt+'.tx' )
        cmds.connectAttr( self.poleVCtl+'.positionAttach', blendAttatch+'.blender' )
        
        cmds.connectAttr( self.secondInit+'.r', ik1Jnt+'.pa' )
        
        childPosMtxDcmp = rigbase.getChildMtxDcmp( self.poleVCtl, self.setGroup )
        cmds.connectAttr( childPosMtxDcmp+'.ot', handle+'.poleVector' )
        rigbase.constraint( self.ikCtl, handle )
        
        tCon = rigbase.listConnections( handle, ['tx','ty','tz'] , d=0, s=1 )[1]
        cmds.connectAttr( tCon+'.outputTranslateX', ikStretch+'.inPositionX' )
        cmds.connectAttr( tCon+'.outputTranslateY', ikStretch+'.inPositionY' )
        cmds.connectAttr( tCon+'.outputTranslateZ', ikStretch+'.inPositionZ' )
        
        cmds.connectAttr( self.ikCtl+'.length', twoSide+'.distance' )
        cmds.connectAttr( self.ikCtl+'.bias'  , twoSide+'.sliding'  )
        cmds.connectAttr( self.ikCtl+'.stretchAble', ikStretch+'.stretchAble' )
        
        if( frontName == 'Arm' and side == 'R' ) or ( frontName == 'Leg' and side == 'L' ):
            multNode = cmds.createNode( 'multDoubleLinear', n='%s_%s_poleTwistInv' %( frontName, side ) )
            cmds.connectAttr( self.ikCtl+'.poleTwist', multNode+'.input1' )
            cmds.setAttr( multNode+'.input2', -1 )
            cmds.connectAttr( multNode+'.output', handle+'.twist' )
        else:
            cmds.connectAttr( self.ikCtl+'.poleTwist', handle+'.twist' )
        
        self.handle = handle
        self.ik0Jnt = ik0Jnt
        self.ik1Jnt = ik1Jnt
        self.ik2Jnt = ik2Jnt
        
        cmds.setAttr( ik0Jnt+'.v', 0 )
        cmds.setAttr( handle+'.v', 0 )

    def itpCtlSet( self, frontName, side ):
        cmds.select( d=1 )
        ctl = cmds.joint( n='%s_%s_IkItp_CTL' %( frontName, side ), radius = 0 )
        rigbase.AttrEdit( ctl ).lockAndHideAttrs( 'tx', 'ty', 'tz', 'sx','sy','sz','v','radius' )
        
        rigbase.addControlerShape( ctl, radius=1, normal=[0,1,0], center=[1,0,0] )
        ctlGrp = rigbase.addParent( ctl )
        
        trDcmp = rigbase.getChildMtxDcmp( self.ikCtl,  self.setGroup )
        orDcmp = rigbase.getChildMtxDcmp( self.ik1Jnt, self.setGroup )
        
        cmds.parent( ctlGrp, self.setGroup )
        
        cmds.connectAttr( trDcmp+'.ot', ctlGrp+'.t' )
        #cmds.connectAttr( orDcmp+'.or', ctlGrp+'.r' )
        dcmp = cmds.createNode( 'decomposeMatrix', n=ctlGrp.replace( "CTL_GRP", "Ctl_OrientDemp" ) )
        cmds.connectAttr( self.secondInit+'.m', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.or', ctlGrp+'.r' )
        
        blendTwoMtx = cmds.createNode( 'blendTwoMatrix' , n='%s_%s_Ik2_blendMtx' %( frontName, side ) )
        mtxDcmp     = cmds.createNode( 'multMatrixDecompose' , n='%s_%s_Ik2_MtxDcmp' %( frontName, side ) )
        
        cmds.connectAttr( self.ikCtl+'.wm', blendTwoMtx+'.inMatrix1' )
            
        cmds.connectAttr( ctl+'.wm', blendTwoMtx+'.inMatrix2' )
        cmds.connectAttr( blendTwoMtx+'.outMatrix', mtxDcmp+'.i[0]' )
        cmds.connectAttr( self.ik2Jnt+'.pim', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.or', self.ik2Jnt+'.r' )
        
        self.rigInstance.itpBlMtx = blendTwoMtx
        self.ikItpCtl = ctl

    def footCtlSet(self, side ):
        sideDict = { 'L':self.legLInits, 'R':self.legRInits }
        hip, knee, ankle, poleV, ball, toe, heel, ballPiv, bankIn, bankOut, toePiv = sideDict[side][:-2]
        
        cmds.select( self.ikCtl )
        self.footIkDriveJnts = []
        for target in [ heel, ballPiv, bankIn, bankOut, toePiv]:
            jnt = cmds.joint( n= target.replace( 'Init', 'FootIk_JNT' ), radius = .3 )
            cmds.connectAttr( target+'.t', jnt+'.t' )
            self.footIkDriveJnts.append( jnt )
        
        toeList = [ toePiv, toe, ball, ankle ]
        for target in toeList[1:]:
            index = toeList.index( target )
            jnt = cmds.joint( n= target.replace( 'Init', 'FootIk_JNT' ), radius = .3 )
            mtxDcmp = rigbase.getChildMtxDcmp( toeList[index], toeList[index-1] )
            cmds.connectAttr( mtxDcmp+'.ot', jnt+'.t' )
            if target == toe:
                cmds.connectAttr( mtxDcmp+'.or', jnt+'.r' )
            self.footIkDriveJnts.append( jnt )
            cmds.select( jnt )
        
        rigbase.constraint( ankle, toe, t=0, r=1 )
        
        cmds.select( self.footIkDriveJnts[5] )
        tapToe    = cmds.joint( n=toe.replace( 'Init', 'Tap_FootIk_JNT' ), radius=.4 )
        tapToeEnd = cmds.joint( n=toe.replace( 'Init', 'End_FootIk_JNT' ), radius=.4 )
        
        self.footIkDriveJnts.append( tapToe )
        self.footIkDriveJnts.append( tapToeEnd )
        
        cmds.connectAttr( toe+'.t', tapToeEnd+'.t' )
        multInv = cmds.createNode( 'multiplyDivide', n=tapToe.replace( 'JNT', 'Jnt_MultInv' ) )
        cmds.setAttr( multInv+'.input2', -1,-1,-1 )
        cmds.connectAttr( toe+'.t', multInv+'.input1' )
        cmds.connectAttr( multInv+'.output', tapToe+'.t' )
        
        thirdMMtx = basicFunc.getLocalMMatrix( self.thirdInit , 'All_InitCTL' )
        
        offsetValue = thirdMMtx( 3, 1 ) 
        if side == 'R':
            offsetValue *= -1
        footCtl, footCtlGrp = rigbase.putControler( self.ikCtl, n='Leg_%s_Foot_IK_CTL' % side, normal=[1,0,0], center=[offsetValue,offsetValue/2.0,0], radius=.2 )
        rigbase.controlerSetColor( footCtl, colorIndexDict[side] )
        cmds.parent( self.footIkDriveJnts[0], footCtl )
        cmds.parent( footCtlGrp, self.ikCtl )
        
        rigbase.addHelpTx( self.ikCtl, 'Foot' )
        attrEdit = rigbase.AttrEdit( self.ikCtl )
        attrEdit.addAttr( ln='tapToe', k=1 )
        attrEdit.addAttr( ln='toeRot', k=1 )
        attrEdit.addAttr( ln='heelLift', k=1 )
        attrEdit.addAttr( ln='walkRoll', k=1 )
        attrEdit.addAttr( ln='walkRollAngle', k=1, dv=40 )
        
        attrEdit = rigbase.AttrEdit( footCtl )
        attrEdit.lockAndHideAttrs( 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v' )
        attrEdit.addAttr( ln='heelRot', k=1 )
        attrEdit.addAttr( ln='ballRot', k=1 )
        attrEdit.addAttr( ln='heelTwist', k=1 )
        attrEdit.addAttr( ln='ballTwist', k=1 )
        attrEdit.addAttr( ln='toeTwist', k=1 )
        attrEdit.addAttr( ln='bank', k=1 )
        
        heel, ballPiv, bankIn, bankOut, toePiv, toe, ball, ankle, tapToe, tapToeEnd = self.footIkDriveJnts
        
        footControlNode = cmds.createNode( 'footControl', n='FootControl_%s' % side )
        cmds.connectAttr( heel+'.message', footControlNode+'.footStart' )
        cmds.connectAttr( footControlNode+'.output', heel+'.rz' )
        
        cmds.connectAttr( footCtl+'.heelRot', footControlNode+'.heelRot' )
        cmds.connectAttr( footCtl+'.ballRot', footControlNode+'.ballRot' )
        cmds.connectAttr( self.ikCtl+'.toeRot', footControlNode+'.toeRot' )
        cmds.connectAttr( footCtl+'.heelTwist', footControlNode+'.heelTwist' )
        cmds.connectAttr( footCtl+'.ballTwist', footControlNode+'.ballTwist' )
        cmds.connectAttr( footCtl+'.toeTwist', footControlNode+'.toeTwist' )
        cmds.connectAttr( footCtl+'.bank', footControlNode+'.bank' )
        cmds.connectAttr( self.ikCtl+'.tapToe', footControlNode+'.tapToe' )
        cmds.connectAttr( self.ikCtl+'.heelLift', footControlNode+'.heelLift' )
        cmds.connectAttr( self.ikCtl+'.walkRoll', footControlNode+'.walkRoll' )
        cmds.connectAttr( self.ikCtl+'.walkRollAngle', footControlNode+'.walkRollAngle' )
        
        mmdc = cmds.listConnections( self.handle+'.tx', type='multMatrixDecompose' )[0]
        cmds.connectAttr( ankle+'.wm', mmdc+'.i[0]', f=1 )
        
        self.rigInstance.footIkCtlGrp = footCtlGrp

    def footJointSet(self, side ):
        aimDir = 1
        if side == 'R':
            aimDir = -1
        heel, ballPiv, bankIn, bankOut, toePiv, toe, ball, ankle, tapToe, tapToeEnd = self.footIkDriveJnts
        
        targetList = [ ankle, ball, toe ]
        
        self.ikFootTrs = []
        self.ikFootItpTrs = []
        self.ikFootJnts = []
        
        parentTr = ''
        parentItpTr = ''
        
        cmds.select( self.ik2Jnt )
        for i in range( 3,6 ):
            jnt = cmds.joint( n= self.ik2Jnt.replace( '2', str( i ) ) )
            tr = rigbase.Transform( n=jnt.replace( 'JNT', 'TR' ) )
            itr = rigbase.Transform( n=jnt.replace( 'JNT', 'ITR' ) )
            self.ikFootJnts.append( jnt )
            self.ikFootTrs.append( tr )
            self.ikFootItpTrs.append( itr )
            if parentTr: tr.setParent( parentTr )
            if parentItpTr: itr.setParent( parentItpTr )
            cmds.select( jnt )
            parentTr = copy.copy( tr )
            parentItpTr = copy.copy( itr )
        
        cmds.parent( self.ikFootTrs[0].name, self.ikFootItpTrs[0].name, self.ik2Jnt )
        ikFootItpGrp = rigbase.addParent( self.ikFootItpTrs[0].name )
        rigbase.constraint( self.ikItpCtl, ikFootItpGrp )
        
        blTwoMtx = cmds.createNode( 'blendTwoMatrix', n='Foot_%s_IK3_blMtx' % side )
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Foot_%s_IK_MtxDcmp' % side  )
        
        cmds.connectAttr( self.ikFootTrs[0]+'.wm', blTwoMtx+'.inMatrix1')
        cmds.connectAttr( self.ikFootItpTrs[0]+'.wm', blTwoMtx+'.inMatrix2' )
        cmds.connectAttr( blTwoMtx+'.outMatrix', mtxDcmp+'.i[0]' )
        cmds.connectAttr( self.ik2Jnt+'.wim', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.or', self.ikFootJnts[0]+'.r' )
        
        blMtxDcmp = cmds.createNode( 'blendTwoMatrixDecompose', n='Foot_%s_IK4_blMtxDcmp' % side )
        
        cmds.connectAttr( self.ikFootTrs[1]+'.m', blMtxDcmp+'.inMatrix1' )
        cmds.connectAttr( self.ikFootItpTrs[1]+'.m', blMtxDcmp+'.inMatrix2' )
        cmds.connectAttr( blMtxDcmp+'.ot', self.ikFootJnts[1]+'.t' )
        cmds.connectAttr( blMtxDcmp+'.or', self.ikFootJnts[1]+'.r' )
        
        for i in range( 3 ):
            self.ikFootTrs[i].defaultPos()
            cmds.connectAttr( self.ikFootTrs[i]+'.t', self.ikFootItpTrs[i]+'.t' )
            cmds.connectAttr( self.ikFootTrs[i]+'.r', self.ikFootItpTrs[i]+'.r' )
            cmds.connectAttr( self.ikFootTrs[i]+'.s', self.ikFootItpTrs[i]+'.s' )
        
        distBall = cmds.createNode( 'multMatrixDecompose', n='Ball_Ik_MtxDist' )
        distToe = cmds.createNode( 'multMatrixDecompose', n='Toe_Ik_MtxDist' )
        cmds.connectAttr( ankle+'.m', distBall+'.i[0]' )
        cmds.connectAttr( ball +'.m', distToe +'.i[0]' )
        
        if side == 'R':
            cmds.setAttr( distBall+'.inverseDistance', True )
            cmds.setAttr( distToe +'.inverseDistance', True )
        
        cmds.connectAttr( distBall+'.outputDistance', self.ikFootTrs[1]+'.tx' )
        cmds.connectAttr( distToe +'.outputDistance', self.ikFootJnts[2]+'.tx' )
        
        cmds.aimConstraint( ball,      self.ikFootTrs[0].name, aim=[aimDir,0,0], u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo=ankle )
        cmds.aimConstraint( tapToeEnd, self.ikFootTrs[1].name, aim=[aimDir,0,0], u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo=ankle )
        
        self.rigInstance.ik3Jnt = self.ikFootJnts[0]
        self.rigInstance.ik4Jnt = self.ikFootJnts[1]
        self.rigInstance.ik5Jnt = self.ikFootJnts[2]
        self.rigInstance.ikFootTrs = self.ikFootTrs
        self.rigInstance.blMtxs = [blTwoMtx, blMtxDcmp]
        
        cmds.setAttr( heel+'.v', 0 )

    def allSet(self, frontName, side ):
        self.rigGroupSet( frontName, side, 'IK' )
        self.ikPinCtlSet(frontName, side)
        self.ctlSet( frontName, side )
        self.poleVectorSet( frontName, side )
        self.jointSet( frontName, side )
        self.itpCtlSet(frontName, side)
        if frontName == 'Leg':
            self.footCtlSet( side )
            self.footJointSet( side )
        
        if frontName == 'Arm':
            if side == 'L':
                rigbase.constraint( self.rigInstance.ikGroupLConst, self.ctlConstGrp )
            else:
                rigbase.constraint( self.rigInstance.ikGroupRConst, self.ctlConstGrp )
        
        self.rigInstance.ik0Jnt = self.ik0Jnt
        self.rigInstance.ik1Jnt = self.ik1Jnt
        self.rigInstance.ik2Jnt = self.ik2Jnt
        self.rigInstance.ikCtl  = self.ikCtl
        self.rigInstance.ikItpCtl = self.ikItpCtl
        self.rigInstance.followMtx = self.followMtx
        self.rigInstance.ikSetGroup = self.setGroup
        self.rigInstance.poleVCtl   = self.poleVCtl

class FkRig( Data ):
    def __init__( self, rigInstance ):
        Data.__init__( self, rigInstance )
        
    def ctlSet( self, frontName, side ):
        ctl0, ctl0Grp = rigbase.putControler( self.firstInit,  n='%s_%s_FK0_CTL'  %( frontName, side ), typ='quadrangle', orient=[0,45,90], size=[.5,.5,.5] )
        ctl1, ctl1Grp = rigbase.putControler( self.secondInit, n='%s_%s_FK1_CTL'  %( frontName, side ), typ='quadrangle', orient=[0,45,90], size=[.5,.5,.5] )
        ctl2, ctl2Grp = rigbase.putControler( self.thirdInit,  n='%s_%s_FK2_CTL'  %( frontName, side ), typ='quadrangle', orient=[0,45,90], size=[.5,.5,.5] )
        
        for ctl in [ctl0, ctl1, ctl2]:
            rigbase.controlerSetColor( ctl, colorIndexDict[side] )
        
        cmds.parent( ctl0Grp, self.setGroup )
        cmds.parent( ctl1Grp, ctl0    )
        cmds.parent( ctl2Grp, ctl1    )
        
        cmds.connectAttr( self.secondInit+'.t', ctl1Grp+'.t' )
        cmds.connectAttr( self.secondInit+'.r', ctl1Grp+'.r' )
        cmds.connectAttr( self.thirdInit+'.t' , ctl2Grp+'.t' )
        cmds.connectAttr( self.thirdInit+'.r' , ctl2Grp+'.r' )
        
        rigbase.AttrEdit( ctl0 ).lockAndHideAttrs( 'tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v' )
        rigbase.AttrEdit( ctl1, ctl2 ).lockAndHideAttrs( 'sx', 'sy', 'sz', 'v' )
        
        self.fk0Ctl = ctl0
        self.fk1Ctl = ctl1
        self.fk2Ctl = ctl2
        
        self.rigInstance.fk2CtlGrp = ctl2Grp
        
    def jointSet(self, frontName, side ):
        inverse = False
        if side == 'R':
            inverse = True
        
        cmds.select( self.setGroup )
        jnt0 = cmds.joint( n='%s_%s_FK0_JNT' %( frontName, side ) )
        jnt1 = cmds.joint( n='%s_%s_FK1_JNT' %( frontName, side ) )
        jnt2 = cmds.joint( n='%s_%s_FK2_JNT' %( frontName, side ) )
        
        upperAimObject = rigbase.makeAimObject( self.fk1Ctl, self.fk0Ctl, inverseAim = inverse )[0]
        lowerAimObject = rigbase.makeAimObject( self.fk2Ctl, self.fk1Ctl, inverseAim = inverse )[0]
        
        rigbase.constraint( upperAimObject, jnt0 )
        rigbase.constraint( lowerAimObject, jnt1 )
        rigbase.constraint( self.fk2Ctl   , jnt2 )
        
        self.fk0Jnt = jnt0
        self.fk1Jnt = jnt1
        self.fk2Jnt = jnt2
        
        cmds.setAttr( jnt0+'.v', 0 )
        
    def footCtlSet(self, side ):
        aimDir = 1
        if side == 'R':
            aimDir = -1
        
        sideDict = { 'L':self.legLInits, 'R':self.legRInits }
        hip, knee, ankle, poleV, ball, toe, heel, ballPiv, bankIn, bankOut, toePiv = sideDict[side][:-2]
        
        fk3Ctl, fk3CtlGrp = rigbase.putControler( ball, n='Leg_%s_FK3_CTL' % side, typ='quadrangle', size=[.4,.4,.4], orient=[0,45,90])
        rigbase.controlerSetColor( fk3Ctl, colorIndexDict[side] )
        aimTarget = cmds.createNode( 'transform', n= fk3Ctl.replace( 'FK3_CTL', 'FK3_Ctl_AimTarget' ) )
        aimTargetP = cmds.createNode( 'transform', n=fk3Ctl.replace( 'FK3_CTL', 'FK3_Ctl_AimTargetP' ) )
        
        cmds.parent( aimTarget, aimTargetP )
        cmds.parent( aimTargetP, fk3CtlGrp, self.fk2Ctl )
        
        cmds.connectAttr( ball+'.t', fk3CtlGrp+'.t' )
        rigbase.connectSameAttr( ball, aimTargetP ).doIt( 't', 'r', 's' )
        rigbase.connectSameAttr( toe , aimTarget  ).doIt( 't', 'r', 's' )
        
        cmds.aimConstraint( aimTarget, fk3CtlGrp, aim=[aimDir,0,0], u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo=aimTarget )
        
        self.fk3Ctl = fk3Ctl
        self.fk3CtlGrp = fk3CtlGrp
        self.aimTarget = aimTarget
    
    def footJointSet(self, side ):
        inverse = False
        dir = 1
        if side == 'R':
            dir = -1
            inverse = True
            
        sideDict = { 'L':self.legLInits, 'R':self.legRInits }
        hip, knee, ankle, poleV, ball, toe, heel, ballPiv, bankIn, bankOut, toePiv = sideDict[side][:-2]
            
        cmds.select( self.fk2Jnt )
        jnt3 = cmds.joint( n=self.fk2Jnt.replace( '2', '3' ) )
        jnt4 = cmds.joint( n=self.fk2Jnt.replace( '2', '4' ) )
        jnt5 = cmds.joint( n=self.fk2Jnt.replace( '2', '5' ) )
        
        aimTarget = rigbase.Transform( n='Foot_FK_%s_AimTarget' % side )
        aimTarget.setParent( self.fk2Jnt )
        cmds.connectAttr( ball+'.t', aimTarget+'.t' )
        cmds.setAttr( aimTarget+'.r', 0,0,0 )
        
        cmds.aimConstraint( aimTarget.name, jnt3, aim=[dir,0,0], u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo=aimTarget.name )
        
        rigbase.constraint( self.fk3Ctl, jnt4 )
        
        jnt5PosMtxDcmp = rigbase.getChildMtxDcmp( self.aimTarget, self.fk3CtlGrp )
        cmds.connectAttr( jnt5PosMtxDcmp+'.ot', jnt5+'.t' )
        
        self.rigInstance.fk3Jnt = jnt3
        self.rigInstance.fk4Jnt = jnt4
        self.rigInstance.fk5Jnt = jnt5
        
    def allSet( self, frontName, side ):
        self.rigGroupSet( frontName, side, 'FK' )
        self.ctlSet( frontName, side )
        self.jointSet( frontName, side )
        
        if frontName == 'Leg':
            self.footCtlSet(side)
            self.footJointSet( side )
        
        self.rigInstance.fk0Jnt = self.fk0Jnt
        self.rigInstance.fk1Jnt = self.fk1Jnt
        self.rigInstance.fk2Jnt = self.fk2Jnt
        
        self.rigInstance.fkSetGroup = self.setGroup
        
class CuRig( Data ):
    def __init__(self, rigInstance ):
        Data.__init__( self, rigInstance )
        
    def transformSet( self, frontName, side ):
        cu0 = cmds.createNode( 'transform', n='%s_%s_CU0' %( frontName, side ) )
        cu1 = cmds.createNode( 'transform', n='%s_%s_CU1' %( frontName, side ) )
        cu2 = cmds.createNode( 'transform', n='%s_%s_CU2' %( frontName, side ) )

        cmds.xform( cu0, matrix = self.firstPose )
        cmds.xform( cu1, matrix = self.secondPose )
        cmds.xform( cu2, matrix = self.thirdPose )
    
        cmds.parent( cu2, cu1 )
        cmds.parent( cu1, cu0 )
        cmds.parent( cu0, self.setGroup )
        
        self.cu0 = cu0
        self.cu1 = cu1
        self.cu2 = cu2
        
        if frontName == 'Arm' and side == 'L':
            self.rigInstance.handLConst = self.cu2
        elif frontName == 'Arm' and side == 'R':
            self.rigInstance.handRConst = self.cu2
        
    def footTransform(self, side ):
        sideDict = { 'L':self.legLInits, 'R':self.legRInits }
        hip, knee, ankle, poleV, ball, toe, heel, ballPiv, bankIn, bankOut, toePiv = sideDict[side][:-2]
        
        cu3 = cmds.createNode( 'transform', n='Leg_%s_CU3' % side )
        cu4 = cmds.createNode( 'transform', n='Leg_%s_CU4' % side )
        cu5 = cmds.createNode( 'transform', n='Leg_%s_CU5' % side )
        
        cmds.parent( cu5, cu4 )
        cmds.parent( cu4, cu3 )
        cmds.parent( cu3, self.cu2 )
        
        self.rigInstance.cu3 = cu3
        self.rigInstance.cu4 = cu4
        self.rigInstance.cu5 = cu5
        
    def ctlSet(self, frontName, side ):
        upperCtl, upperCtlGrp = rigbase.putControler( self.cu0, n='%s_%s_UpperFlex_CTL' %( frontName, side ), normal=[1,0,0], radius=.5 )
        lowerCtl, lowerCtlGrp = rigbase.putControler( self.cu1, n='%s_%s_LowerFlex_CTL' %( frontName, side ), normal=[1,0,0], radius=.5 )
        upperStart = cmds.createNode( 'transform', n='%s_%s_UpperFlexStartPoint' %( frontName, side ) )
        upperEnd   = cmds.createNode( 'transform', n='%s_%s_UpperFlexEndPoint' %( frontName, side ) )
        lowerStart = cmds.createNode( 'transform', n='%s_%s_LowerFlexStartPoint' %( frontName, side ) )
        lowerEnd   = cmds.createNode( 'transform', n='%s_%s_LowerFlexEndPoint' %( frontName, side ) )
        upperStartMult = cmds.createNode( 'multDoubleLinear', n='%s_%s_UpperFlexStartMult' %( frontName, side ) )
        upperEndMult =   cmds.createNode( 'multDoubleLinear', n='%s_%s_UpperFlexEndMult' %( frontName, side ) )
        lowerStartMult = cmds.createNode( 'multDoubleLinear', n='%s_%s_LowerFlexStartMult' %( frontName, side ) )
        lowerEndMult =   cmds.createNode( 'multDoubleLinear', n='%s_%s_LowerFlexEndMult' %( frontName, side ) )
        
        rigbase.AttrEdit( upperStart, upperEnd, lowerStart, lowerEnd ).lockAttrs( 'ty', 'tz', 'r', 's', 'v' )
        
        cmds.parent( upperStart, upperEnd, upperCtl )
        cmds.parent( lowerStart, lowerEnd, lowerCtl )
        
        cmds.setAttr( upperStartMult+'.input2', -.167 )
        cmds.setAttr( upperEndMult  +'.input2',  .167 )
        cmds.setAttr( lowerStartMult+'.input2', -.167 )
        cmds.setAttr( lowerEndMult  +'.input2',  .167 )
        
        cmds.connectAttr( self.cu1+'.tx', upperStartMult+'.input1' )
        cmds.connectAttr( self.cu1+'.tx', upperEndMult  +'.input1' )
        cmds.connectAttr( self.cu2+'.tx', lowerStartMult+'.input1' )
        cmds.connectAttr( self.cu2+'.tx', lowerEndMult  +'.input1' )
        cmds.connectAttr( upperStartMult+'.output', upperStart+'.tx' )
        cmds.connectAttr( upperEndMult  +'.output', upperEnd  +'.tx' )
        cmds.connectAttr( lowerStartMult+'.output', lowerStart+'.tx' )
        cmds.connectAttr( lowerEndMult  +'.output', lowerEnd  +'.tx' )
        
        cmds.parent( upperCtlGrp, self.cu0 )
        cmds.parent( lowerCtlGrp, self.cu1 )
        rigbase.AttrEdit( upperCtlGrp, lowerCtlGrp ).setAttrs( 0, 'tx', 'ty', 'tz', 'rx', 'ry', 'rz' )
        
        upperMult = cmds.createNode( 'multDoubleLinear', n='%s_%s_UpperFlexCtl_PoseMult' %( frontName, side ) )
        lowerMult = cmds.createNode( 'multDoubleLinear', n='%s_%s_LowerFlexCtl_PoseMult' %( frontName, side ) )
        
        rigbase.AttrEdit( upperCtl, lowerCtl ).lockAndHideAttrs( 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v' )
        
        cmds.setAttr( upperMult+'.input2', .5 )
        cmds.setAttr( lowerMult+'.input2', .5 )
        
        cmds.connectAttr( self.cu1+'.tx', upperMult+'.input1' )
        cmds.connectAttr( self.cu2+'.tx', lowerMult+'.input1' )
        
        cmds.connectAttr( upperMult+'.output', upperCtlGrp+'.tx' )
        cmds.connectAttr( lowerMult+'.output', lowerCtlGrp+'.tx' )
        
        upperCtlOffset = rigbase.addParent( upperCtl, '_OffsetGrp' )
        lowerCtlOffset = rigbase.addParent( lowerCtl, '_OffsetGrp' )
        
        cmds.connectAttr( self.upperInit+'.t', upperCtlOffset+'.t' )
        cmds.connectAttr( self.lowerInit+'.t', lowerCtlOffset+'.t' )
        
        self.upperCtlPoints = [ self.cu0, upperStart, upperEnd, self.cu1 ]
        self.lowerCtlPoints = [ self.cu1, lowerStart, lowerEnd, self.cu2 ]
        
        self.upperFlexCtl = upperCtl
        self.lowerFlexCtl = lowerCtl
        
    def curveSet(self, frontName, side ):
        upperCurve = cmds.curve( d=1, p=[(0,0,0),(1,0,0)], n='%s_%s_UpperFlex_CRV' %( frontName, side ) )
        lowerCurve = cmds.curve( d=1, p=[(0,0,0),(1,0,0)], n='%s_%s_LowerFlex_CRV' %( frontName, side ) )
        
        upperShape = cmds.listRelatives( upperCurve, s=1 )[0]
        lowerShape = cmds.listRelatives( lowerCurve, s=1 )[0]
        
        cmds.rebuildCurve( upperCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=1, d=3, tol=0.01 )
        cmds.rebuildCurve( lowerCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=1, d=3, tol=0.01 )
        
        cmds.parent( upperCurve, self.cu0 )
        cmds.parent( lowerCurve, self.cu1 )
        
        
        upperDcmp = cmds.createNode( 'decomposeMatrix', n= '%s_%s_UpperFlexCrv_dcmp' %( frontName, side ) )
        lowerDcmp = cmds.createNode( 'decomposeMatrix', n= '%s_%s_LowerFlexCrv_dcmp' %( frontName, side ) )
        cmds.connectAttr( self.cu0+'.wim', upperDcmp+'.imat' )
        cmds.connectAttr( self.cu1+'.wim', lowerDcmp+'.imat' )
        cmds.connectAttr( upperDcmp+'.ot', upperCurve+'.t' )
        cmds.connectAttr( upperDcmp+'.or', upperCurve+'.r' )
        cmds.connectAttr( upperDcmp+'.os', upperCurve+'.s' )
        cmds.connectAttr( lowerDcmp+'.ot', lowerCurve+'.t' )
        cmds.connectAttr( lowerDcmp+'.or', lowerCurve+'.r' )
        cmds.connectAttr( lowerDcmp+'.os', lowerCurve+'.s' )
        
        for point in self.upperCtlPoints:
            i = self.upperCtlPoints.index( point )
            dcmp = cmds.createNode( 'decomposeMatrix', n='%s_%s_UpperFlexPoint%d_dcmp' %( frontName, side, i ) )
            cmds.connectAttr( point+'.wm', dcmp+'.imat' )
            cmds.connectAttr( dcmp+'.ot', upperShape+'.controlPoints[%d]' % i )
        
        for point in self.lowerCtlPoints:
            i = self.lowerCtlPoints.index( point )
            dcmp = cmds.createNode( 'decomposeMatrix', n='%s_%s_LowerFlexPoint%d_dcmp' %( frontName, side, i ) )
            cmds.connectAttr( point+'.wm', dcmp+'.imat' )
            cmds.connectAttr( dcmp+'.ot', lowerShape+'.controlPoints[%d]' % i )
        '''
        for point in self.upperCtlPoints:
            i = self.upperCtlPoints.index( point )
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_UpperFlexPoint%d_mtxDcmp' %( frontName, side, i ) )
            cmds.connectAttr( point+'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( self.cu0+'.wim', mtxDcmp+'.i[1]' )
            cmds.connectAttr( mtxDcmp+'.ot', upperShape+'.controlPoints[%d]' % i )
        
        for point in self.lowerCtlPoints:
            i = self.lowerCtlPoints.index( point )
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='%s_%s_LowerFlexPoint%d_mtxDcmp' %( frontName, side, i ) )
            cmds.connectAttr( point+'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( self.cu1+'.wim', mtxDcmp+'.i[1]' )
            cmds.connectAttr( mtxDcmp+'.ot', lowerShape+'.controlPoints[%d]' % i )
        '''
        rigbase.transformDefault( upperCurve )
        rigbase.transformDefault( lowerCurve )
        
        self.upperCurve = upperCurve
        self.lowerCurve = lowerCurve
        self.upperShape = upperShape
        self.lowerShape = lowerShape
        
        cmds.setAttr( upperCurve+'.v', 0 )
        cmds.setAttr( lowerCurve+'.v', 0 )
        
    def switchCtlSet(self, frontName, side ):
        ctlOffset = [0,.8,0]
        ctlOrient = [0,0,0]
        
        if side == 'R':
            ctlOffset = [0,-.8,0]
            ctlOrient = [180,0,0]
        
        ik0 = self.rigInstance.ik0Jnt
        ik1 = self.rigInstance.ik1Jnt
        ik2 = self.rigInstance.ik2Jnt
        
        fk0 = self.rigInstance.fk0Jnt
        fk1 = self.rigInstance.fk1Jnt
        fk2 = self.rigInstance.fk2Jnt
        
        cu0 = self.cu0
        cu1 = self.cu1
        cu2 = self.cu2
        
        switchCtl, switchCtlGrp = rigbase.putControler( cu2, n='%s_%s_Switch_CTL' %( frontName, side ), typ='switch', orient =ctlOrient, size=[.2,.2,.2], offset=ctlOffset )
        rigbase.controlerSetColor( switchCtl, swColorIndex )
        cmds.parent( switchCtlGrp, self.setGroup )
        
        attrEdit = rigbase.AttrEdit( switchCtl )
        attrEdit.lockAndHideAttrs( 'tx','ty','tz','rx','ry','rz','sx','sy','sz','v' )
        rigbase.constraint( cu2, switchCtlGrp )
        
        attrEdit.addAttr( ln='fkSwitch', min=0, max=1, k=1 )
        rigbase.addHelpTx( switchCtl, 'PoleVector' )
        attrEdit.addAttr( ln='upperSquash', min=0, max=1, k=1 )
        attrEdit.addAttr( ln='lowerSquash', min=0, max=1, k=1 )
        rigbase.addHelpTx( switchCtl, 'Squash' )
        attrEdit.addAttr( ln='upperScale', k=1 )
        attrEdit.addAttr( ln='lowerScale', k=1 )
        if frontName == 'Arm':
            attrEdit.addAttr( ln='handScale',  k=1 )
        else:
            attrEdit.addAttr( ln='footScale', k=1 )
        
        rigbase.addHelpTx( switchCtl, 'Interpolation' )
        attrEdit.addAttr( ln='twist', k=1 )
        rigbase.addHelpTx( switchCtl, 'Ik_Interpole' )
        attrEdit.addAttr( ln='interpoleSwitch', min=0, max=1, k=1 )
        rigbase.addHelpTx( switchCtl, 'Follow' )
        if frontName == 'Arm':
            attrEdit.addAttr( ln='collarFollow', min=0, max=10 )
            attrEdit.addAttr( ln='headFollow', min=0, max=10 )
            attrEdit.addAttr( ln='chestFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='hipFollow',  min=0, max=10 )
        attrEdit.addAttr( ln='rootFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='flyFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='moveFollow', min=0, max=10 )
        attrEdit.addAttr( ln='pinFollow', min=0, max=10, k=1 )
        rigbase.addHelpTx( switchCtl, 'Ctl_On_Off' )
        attrEdit.addAttr( ln='fingerCtl', at='long', min=0, max=1, cb=1 )
        attrEdit.addAttr( ln='flexbleCtl', at='long', min=0, max=1, cb=1 )
        
        if frontName == 'Arm':
            cmds.connectAttr( switchCtl+'.collarFollow', self.rigInstance.followMtx+'.inputWeight[0]' )
            cmds.connectAttr( switchCtl+'.headFollow',   self.rigInstance.followMtx+'.inputWeight[1]' )
            cmds.connectAttr( switchCtl+'.chestFollow',  self.rigInstance.followMtx+'.inputWeight[2]' )
            cmds.connectAttr( switchCtl+'.hipFollow',    self.rigInstance.followMtx+'.inputWeight[3]' )
            cmds.connectAttr( switchCtl+'.rootFollow',   self.rigInstance.followMtx+'.inputWeight[4]' )
            cmds.connectAttr( switchCtl+'.flyFollow',    self.rigInstance.followMtx+'.inputWeight[5]' )
            cmds.connectAttr( switchCtl+'.moveFollow',   self.rigInstance.followMtx+'.inputWeight[6]' )
            cmds.connectAttr( switchCtl+'.pinFollow',    self.rigInstance.followMtx+'.inputWeight[7]' )
        else:
            cmds.connectAttr( switchCtl+'.hipFollow',    self.rigInstance.followMtx+'.inputWeight[0]' )
            cmds.connectAttr( switchCtl+'.rootFollow',   self.rigInstance.followMtx+'.inputWeight[1]' )
            cmds.connectAttr( switchCtl+'.flyFollow',    self.rigInstance.followMtx+'.inputWeight[2]' )
            cmds.connectAttr( switchCtl+'.moveFollow',   self.rigInstance.followMtx+'.inputWeight[3]' )
            cmds.connectAttr( switchCtl+'.pinFollow',    self.rigInstance.followMtx+'.inputWeight[4]' )
        
        if frontName == 'Arm':
            cmds.connectAttr( switchCtl+'.interpoleSwitch', self.rigInstance.itpBlMtx+'.ab' )
        else:
            cmds.setAttr( self.rigInstance.itpBlMtx+'.ab', 0 )
            cmds.connectAttr( switchCtl+'.interpoleSwitch', self.rigInstance.blMtxs[0]+'.ab' )
            cmds.connectAttr( switchCtl+'.interpoleSwitch', self.rigInstance.blMtxs[1]+'.ab' )
        
        iks = [ik0, ik1, ik2]
        fks = [fk0, fk1, fk2]
        cus = [cu0, cu1, cu2]
        
        if frontName == 'Leg':
            iks.append( self.rigInstance.ik3Jnt )
            iks.append( self.rigInstance.ik4Jnt )
            iks.append( self.rigInstance.ik5Jnt )
            fks.append( self.rigInstance.fk3Jnt )
            fks.append( self.rigInstance.fk4Jnt )
            fks.append( self.rigInstance.fk5Jnt )
            cus.append( self.rigInstance.cu3 )
            cus.append( self.rigInstance.cu4 )
            cus.append( self.rigInstance.cu5 )
        
        for i in range( len( iks ) ):
            ik = iks[i]
            fk = fks[i]
            cu = cus[i]
            
            blTwoMtxDcmp = cmds.createNode( 'blendTwoMatrixDecompose' , n='%s_%s_IkFkBlend%d_blMtx' %( frontName, side, i ) )
            
            cmds.connectAttr( ik+'.m', blTwoMtxDcmp+'.inMatrix1' )
            cmds.connectAttr( fk+'.m', blTwoMtxDcmp+'.inMatrix2' )
            cmds.connectAttr( blTwoMtxDcmp+'.ot', cu+'.t' )
            cmds.connectAttr( blTwoMtxDcmp+'.or', cu+'.r' )
            
            cmds.connectAttr( switchCtl+'.fkSwitch', blTwoMtxDcmp+'.attributeBlender' )
        
        def createScaleNode( switchCtl ):
            scaleNode = cmds.createNode( 'multiplyDivide', n=switchCtl+'_footScale' )
            cmds.setAttr( scaleNode+'.op', 3 )
            cmds.connectAttr( switchCtl+'.footScale', scaleNode+'.input2X' )
            cmds.connectAttr( switchCtl+'.footScale', scaleNode+'.input2Y' )
            cmds.connectAttr( switchCtl+'.footScale', scaleNode+'.input2Z' )
            cmds.setAttr( scaleNode+'.input1X', 2 )
            cmds.setAttr( scaleNode+'.input1Y', 2 )
            cmds.setAttr( scaleNode+'.input1Z', 2 )
            return scaleNode
        
        if frontName == 'Leg':
            scaleNode = createScaleNode( switchCtl )
            cmds.connectAttr( scaleNode+'.output', self.cu2+'.s', f=1 )  
            cmds.connectAttr( scaleNode+'.output', self.rigInstance.ikFootTrs[0]+'.s', f=1 )  
            cmds.connectAttr( scaleNode+'.output', self.rigInstance.footIkCtlGrp+'.s', f=1 )
            cmds.connectAttr( scaleNode+'.output', self.rigInstance.fk3Jnt+'.s', f=1 )
            cmds.connectAttr( scaleNode+'.output', self.rigInstance.fk2CtlGrp+'.s', f=1 )
            
        self.switchCtl = switchCtl
        self.rigInstance.switchCtl = switchCtl
        
        rigbase.visConnect( switchCtl+'.interpoleSwitch' , None, self.rigInstance.ikItpCtl )
        rigbase.visConnect( switchCtl+'.pinFollow' , None, self.rigInstance.ikPinCtl.transformGrp )
        rigbase.visConnect( switchCtl+'.flexbleCtl' , None, self.upperFlexCtl )
        cmds.setAttr( self.lowerFlexCtl+'.v', e=1, lock=0 )
        cmds.connectAttr( self.upperFlexCtl+'.v', self.lowerFlexCtl+'.v' )
        rigbase.visConnect( switchCtl+'.fkSwitch' , self.rigInstance.ikCtl, self.rigInstance.fkSetGroup )
        cmds.connectAttr( self.rigInstance.ikCtl+'.v', self.rigInstance.ikSetGroup+'.v' )
        
    def allSet(self, frontName, side ):
        self.rigGroupSet( frontName, side, 'CU' )
        self.transformSet( frontName, side )
        if frontName == 'Leg':
            self.footTransform(side)
        self.ctlSet( frontName, side )
        self.curveSet( frontName, side )
        self.switchCtlSet( frontName, side )
        
        self.rigInstance.cuGrp      = self.setGroup
        self.rigInstance.cu0        = self.cu0
        self.rigInstance.cu1        = self.cu1
        self.rigInstance.cu2        = self.cu2
        self.rigInstance.upperCurve = self.upperCurve
        self.rigInstance.lowerCurve = self.lowerCurve
        self.rigInstance.upperShape = self.upperShape
        self.rigInstance.lowerShape = self.lowerShape
        
        self.rigInstance.cuSetGroup = self.setGroup
        
class SplineRig( Data ):
    def __init__(self, rigInstance ):
        Data.__init__( self, rigInstance )
        
    def upObjSet(self, frontName, side ):
        inverse = False
        if side == 'R':
            inverse = True
            
        startUpObj  = cmds.createNode( 'transform', n='%s_%s_StartUpObj'  %( frontName, side ) )
        middleUpObj = cmds.createNode( 'transform', n='%s_%s_MiddleUpObj' %( frontName, side ) )
        endUpObj    = cmds.createNode( 'transform', n='%s_%s_EndUpObj'    %( frontName, side ) )
        
        originalOrient = ''
        if frontName == 'Arm':
            if side == 'L':
                originalOrient = self.rigInstance.shoulderLOr.name
            else:
                originalOrient = self.rigInstance.shoulderROr.name
        else:
            if side == 'L':
                originalOrient = self.rigInstance.hipLOr.name
            else:
                originalOrient = self.rigInstance.hipROr.name
        
        startUpObjGrp  = rigbase.makeAimObject( self.rigInstance.cu1, originalOrient, inverseAim = inverse )[0]
        startUpObjGrp = cmds.rename( startUpObjGrp, startUpObj+'_GRP' )
        middleUpObjGrp = rigbase.addParent( middleUpObj )
        endUpObjGrp    = rigbase.addParent( endUpObj )
        
        cmds.parent( startUpObj, startUpObjGrp )
        cmds.parent( endUpObjGrp, middleUpObjGrp, self.rigInstance.cu1 )
        
        btmd = cmds.createNode( 'blendTwoMatrixDecompose', n='%s_%s_btmd'  %( frontName, side ) )
        cmds.connectAttr( self.rigInstance.cu1+'.im', btmd+'.inMatrix1' )
        cmds.connectAttr( btmd+'.or', middleUpObjGrp+'.r')
        
        wristAngle = cmds.createNode( 'wristAngle' , n='%s_%s_wristAngle'  %( frontName, side ) )
        cmds.connectAttr( self.rigInstance.cu2+'.m', wristAngle+'.inputMatrix' )
        cmds.connectAttr( wristAngle+'.outAngle', endUpObjGrp+'.rx' )
        cmds.connectAttr( self.rigInstance.cu2+'.t', endUpObjGrp + '.t' )
        
        rigbase.transformDefault( startUpObj, startUpObjGrp, middleUpObjGrp, endUpObjGrp )
        
        if side == 'L':
            shoulderCtl = self.rigInstance.shoulderLCtl
        elif side == 'R':
            shoulderCtl = self.rigInstance.shoulderRCtl
        
        if frontName == 'Arm':
            cmds.connectAttr( shoulderCtl+'.twistShoulder', startUpObj+'.rx' )
        
        self.startUp = startUpObj
        self.middleUp = middleUpObj
        self.endUp = endUpObj
        
    def jointSet( self, frontName, side, upNumBjts, loNumBjts ):
        axisValue = 0
        if side == 'R':
            axisValue = 3
        
        upperCurve = self.rigInstance.upperCurve
        lowerCurve = self.rigInstance.lowerCurve
        
        upperCurveShape = cmds.listRelatives( upperCurve, s=1 )[0]
        lowerCurveShape = cmds.listRelatives( lowerCurve, s=1 )[0]
        
        upperSpCrv = cmds.createNode( 'splineCurveInfo', n='%s_%s_Upper_SplineCrv'  %( frontName, side ) )
        lowerSpCrv = cmds.createNode( 'splineCurveInfo', n='%s_%s_lower_SplineCrv'  %( frontName, side ) )
        
        rigbase.AttrEdit( upperSpCrv, lowerSpCrv ).setAttrs( 1, 'startUpAxis', 'endUpAxis', 'targetUpAxis' )
        rigbase.AttrEdit( upperSpCrv, lowerSpCrv ).setAttrs( axisValue, 'targetAimAxis' )
        
        cmds.connectAttr( upperCurveShape+'.worldSpace', upperSpCrv+'.inputCurve' )
        cmds.connectAttr( lowerCurveShape+'.worldSpace', lowerSpCrv+'.inputCurve' )
        
        cmds.connectAttr( self.startUp+'.wm' , upperSpCrv+'.startTransform')
        cmds.connectAttr( self.middleUp+'.wm', upperSpCrv+'.endTransform')
        cmds.connectAttr( self.middleUp+'.wm', lowerSpCrv+'.startTransform')
        cmds.connectAttr( self.endUp+'.wm'   , lowerSpCrv+'.endTransform')
        
        
        upperSpPoints = []
        upperRjts = []
        cmds.select( self.setGroup )
        
        if frontName == 'Leg':
            nRjt = cmds.joint( n='%s_%s_Upper_RJT'  %( frontName, side ), radius = 2 )
            targetConst = self.rigInstance.hipLOr
            if side == 'R':
                targetConst = self.rigInstance.hipROr
            rigbase.constraint( targetConst, nRjt )
            upperRjts.append( nRjt )
            cmds.select( nRjt )
            
        for i in range( upNumBjts-1 ):
            prValue = i/( upNumBjts-1.0 )+.00001
            rjt = cmds.joint( n='%s_%s_Upper%d_RJT'  %( frontName, side, i ), radius = 1.5 )
            attrEdit = rigbase.AttrEdit( rjt )
            attrEdit.addAttr( ln='parameter', min=0, max=1, dv=prValue, k=1 )
            cmds.connectAttr( rjt+'.parameter', upperSpCrv+'.pr[%d]' %i )
            spPoint = cmds.createNode( 'transform',  n='%s_%s_Upper%d_SplinePoint'  %( frontName, side, i ) )
            cmds.parent( spPoint, upperCurve )
            cmds.connectAttr( upperSpCrv+'.o[%d].position' % i, spPoint+'.t')
            cmds.connectAttr( upperSpCrv+'.o[%d].rotate' % i, spPoint+'.r')
            rigbase.constraint( spPoint, rjt )
            cmds.connectAttr( spPoint+'.s', rjt+'.s' )
            upperSpPoints.append( spPoint )
            upperRjts.append( rjt )
            cmds.select( rjt )
        
        lowerSpPoints = []
        lowerRjts = []
        for i in range( loNumBjts ):
            prValue = i/( loNumBjts-1.0 )+.00001
            rjt = cmds.joint( n='%s_%s_Lower%d_RJT'  %( frontName, side, i ), radius = 1.5 )
            attrEdit = rigbase.AttrEdit( rjt )
            attrEdit.addAttr( ln='parameter', min=0, max=1, dv=prValue, k=1 )
            cmds.connectAttr( rjt+'.parameter', lowerSpCrv+'.pr[%d]' %i )
            spPoint = cmds.createNode( 'transform',  n='%s_%s_Lower%d_SplinePoint'  %( frontName, side, i ) )
            cmds.parent( spPoint, lowerCurve )
            cmds.connectAttr( lowerSpCrv+'.o[%d].position' % i, spPoint+'.t')
            cmds.connectAttr( lowerSpCrv+'.o[%d].rotate' % i, spPoint+'.r')
            rigbase.constraint( spPoint, rjt )
            cmds.connectAttr( spPoint+'.s', rjt+'.s' )
            lowerSpPoints.append( spPoint )
            lowerRjts.append( rjt )
            cmds.select( rjt )
        
        loRjtEnd = lowerRjts[-1]
        
        rigbase.constraint( self.rigInstance.cu2, loRjtEnd, s=1 )
        
        cmds.select( loRjtEnd )
        if frontName == 'Leg':
            footRjt0 = cmds.joint( n='Leg_%s_Foot0_RJT'  % side , radius = 1.5 )
            footRjt1 = cmds.joint( n='Leg_%s_Foot1_RJT'  % side , radius = 1.5 )
            rigbase.constraint( self.rigInstance.cu3, loRjtEnd, s=1, sh=1 )
            cmds.setAttr( loRjtEnd+'.ssc', False )
            rigbase.constraint( self.rigInstance.cu4, footRjt0 )
            rigbase.constraint( self.rigInstance.cu5, footRjt1 )
            cmds.setAttr( footRjt0+'.ssc', False )
        
        self.upperSpPoints = upperSpPoints
        self.lowerSpPoints = lowerSpPoints
        self.topJnt = upperRjts[0]
        self.loRjtEnd = loRjtEnd
        
    def squashSetting(self, frontName, side ):
        upperInfo = cmds.createNode( 'curveInfo', n='%s_%s_Upper_CrvInfo' %( frontName, side ) )
        upperDist = cmds.createNode( 'distanceBetween', n='%s_%s_Upper_InitDist' %( frontName, side ) )
        upperSquash= cmds.createNode( 'squash', n='%s_%s_Upper_Squash' %( frontName, side ) )
        
        firstMtx  = cmds.createNode( 'multMatrix', n='%s_%s_FirstInit_mmtx' %( frontName, side ) )
        secondMtx = cmds.createNode( 'multMatrix', n='%s_%s_SecondInit_mmtx' %( frontName, side ) )
        thirdMtx  = cmds.createNode( 'multMatrix', n='%s_%s_ThirdInit_mmtx' %( frontName, side ) )
        
        cmds.connectAttr( self.firstInit+'.wm' , firstMtx+'.i[0]' )
        cmds.connectAttr( self.secondInit+'.wm', secondMtx+'.i[0]' )
        cmds.connectAttr( self.thirdInit+'.wm' , thirdMtx+'.i[0]' )
        cmds.connectAttr( self.rigInstance.initAll+'.wim' , firstMtx +'.i[1]' )
        cmds.connectAttr( self.rigInstance.initAll+'.wim' , secondMtx+'.i[1]' )
        cmds.connectAttr( self.rigInstance.initAll+'.wim' , thirdMtx +'.i[1]' )
        cmds.connectAttr( self.rigInstance.moveCtl+'.wm' , firstMtx +'.i[2]' )
        cmds.connectAttr( self.rigInstance.moveCtl+'.wm' , secondMtx+'.i[2]' )
        cmds.connectAttr( self.rigInstance.moveCtl+'.wm' , thirdMtx +'.i[2]' )
        
        cmds.connectAttr( self.rigInstance.upperShape+'.local', upperInfo+'.inputCurve' )
        cmds.connectAttr( firstMtx+'.o' , upperDist+'.inMatrix1' )
        cmds.connectAttr( secondMtx+'.o', upperDist+'.inMatrix2' )
        cmds.connectAttr( upperInfo+'.arcLength', upperSquash+'.lengthModify' )
        cmds.connectAttr( upperDist+'.distance' , upperSquash+'.lengthOriginal' )
        
        for point in self.upperSpPoints[1:]:
            cmds.connectAttr( upperSquash+'.output', point+'.sy' )
            cmds.connectAttr( upperSquash+'.output', point+'.sz' )
            
        lowerInfo = cmds.createNode( 'curveInfo', n='%s_%s_Lower_CrvInfo' %( frontName, side ) )
        lowerDist = cmds.createNode( 'distanceBetween', n='%s_%s_Lower_InitDist' %( frontName, side ) )
        lowerSquash= cmds.createNode( 'squash', n='%s_%s_Lower_Squash' %( frontName, side ) )
        
        cmds.connectAttr( self.rigInstance.lowerShape+'.local', lowerInfo+'.inputCurve' )
        cmds.connectAttr( secondMtx+'.o' , lowerDist+'.inMatrix1' )
        cmds.connectAttr( thirdMtx+'.o', lowerDist+'.inMatrix2' )
        cmds.connectAttr( lowerInfo+'.arcLength', lowerSquash+'.lengthModify' )
        cmds.connectAttr( lowerDist+'.distance' , lowerSquash+'.lengthOriginal' )
        
        for point in self.lowerSpPoints:
            cmds.connectAttr( lowerSquash+'.output', point+'.sy' )
            cmds.connectAttr( lowerSquash+'.output', point+'.sz' )
        
        self.rigInstance.upperSquash = upperSquash
        self.rigInstance.lowerSquash = lowerSquash
    
    def allSet( self, frontName, side, upNumBjts, loNumBjts ):
        self.rigGroupSet( frontName, side, 'RJT' )
        self.upObjSet( frontName, side )
        self.jointSet( frontName, side, upNumBjts, loNumBjts )
        self.squashSetting( frontName, side )
        
        self.rigInstance.middleUp = self.middleUp
        
        self.rigInstance.splineSetGroup = self.setGroup
        self.rigInstance.topJnt = self.topJnt
        self.rigInstance.middleUp = self.middleUp
        
class FinalRig( Data ):
    def __init__(self, rigInstance ):
        Data.__init__( self, rigInstance )
        
    def upObjConnection( self ):
        switchCtl = self.rigInstance.switchCtl
        middleUpObj = self.rigInstance.middleUp
        
        cmds.connectAttr( switchCtl+'.twist', middleUpObj +'.rx' )
        
    def annotation(self, frontName, side ):
        poleVCtl = self.rigInstance.poleVCtl
        cu1 = self.rigInstance.cu1
        
        loc = cmds.spaceLocator( n='%s_%s_AnnotatLoc' %( frontName, side ) )[0]
        locShape = cmds.listRelatives( loc, s=1 )[0]
        annotateShape = cmds.createNode( 'annotationShape', n='%s_%s_AnnotateShape' %( frontName, side ) )
        annotate = cmds.listRelatives( annotateShape, p=1 )[0]
        cmds.rename( annotate, '%s_%s_Annotate' %( frontName, side ) )
        cmds.parent( annotate, poleVCtl )
        rigbase.constraint( cu1, annotate, r=0 )
        cmds.connectAttr( locShape+'.wm', annotateShape+'.dagObjectMatrix[0]' )
        
        cmds.parent( loc, poleVCtl )
        rigbase.transformDefault( loc )
        
        cmds.setAttr( loc+'.v', 0 )
        cmds.setAttr( annotate+'.overrideEnabled', True )
        cmds.setAttr( annotate+'.overrideDisplayType', 2 )
        
    def otherConnection( self ):
        cmds.connectAttr( self.rigInstance.switchCtl+'.upperSquash', self.rigInstance.upperSquash+'.squashRate' )
        cmds.connectAttr( self.rigInstance.switchCtl+'.lowerSquash', self.rigInstance.lowerSquash+'.squashRate' )
        cmds.connectAttr( self.rigInstance.switchCtl+'.upperScale', self.rigInstance.upperSquash+'.forceValue' )
        cmds.connectAttr( self.rigInstance.switchCtl+'.lowerScale', self.rigInstance.lowerSquash+'.forceValue' )
        
    def grouping( self, frontName, side ):
        ikGrp = self.rigInstance.ikSetGroup
        fkGrp = self.rigInstance.fkSetGroup
        cuGrp = self.rigInstance.cuSetGroup
        rjtGrp = self.rigInstance.splineSetGroup
        
        allGroup = cmds.createNode( 'transform', n='%s_%s_Set' %( frontName, side ) )
        grpPose = cmds.getAttr( ikGrp+'.wm' )
        cmds.xform( allGroup, matrix = grpPose )
        
        cmds.parent( ikGrp, fkGrp, cuGrp, rjtGrp, allGroup )
        cmds.parent( allGroup, self.rigInstance.rootGrp )
        
        self.allGroup = allGroup
        
    def constSetting( self, frontName, side ):
        targetConst = ''
        if frontName == 'Arm':
            if side == 'L':
                targetConst = self.shoulderLConst
            else:
                targetConst = self.shoulderRConst
        else:
            if side == 'L':
                targetConst = self.hipLConst
            else:
                targetConst = self.hipRConst
        rigbase.constraint( targetConst, self.allGroup )
        
    def parentRJT( self, frontName, side ):
        targetParent = ''
        if frontName == 'Arm':
            if side == 'L':
                targetParent = self.rigInstance.collarLJnts[-1]
            else:
                targetParent = self.rigInstance.collarRJnts[-1]
        else:
            targetParent = self.rigInstance.splineJnts[0]
        
        cmds.parent( self.rigInstance.topJnt, targetParent )
        cmds.setAttr( self.rigInstance.topJnt+'.jo', 0,0,0 )
        cmds.delete( self.rigInstance.splineSetGroup )
        
    def allSet(self, frontName, side ):
        self.upObjConnection()
        self.otherConnection()
        self.grouping(frontName, side )
        self.constSetting( frontName, side )
        self.parentRJT(frontName, side )
        self.annotation( frontName, side )
        
class RigAll:
    def __init__(self, rigInstance ):
        self.ikInst = IkRig( rigInstance )
        self.fkInst = FkRig( rigInstance )
        self.cuInst = CuRig( rigInstance )
        self.splineInst = SplineRig( rigInstance )
        self.finalInst = FinalRig( rigInstance )
        self.rigInstance = rigInstance

    def allSet(self, armLUpperNum, armLLowerNum, armRUpperNum, armRLowerNum, legLUpperNum, legLLowerNum, legRUpperNum, legRLowerNum ):
        for fn in ['Arm', 'Leg']:
            for sn in ['L', 'R']:
                self.ikInst.allSet( fn, sn )
                self.fkInst.allSet( fn, sn )
                self.cuInst.allSet( fn, sn )
                if fn == 'Arm':
                    if sn == 'L':
                        self.splineInst.allSet( fn, sn, armLUpperNum, armLLowerNum )
                    else:
                        self.splineInst.allSet( fn, sn, armRUpperNum, armRLowerNum )
                else:
                    if sn == 'L':
                        self.splineInst.allSet( fn, sn, legLUpperNum, legLLowerNum )
                    else:
                        self.splineInst.allSet( fn, sn, legRUpperNum, legRLowerNum )
                    
                if fn == 'Arm' and sn == 'L':
                    self.rigInstance.handLRjt = self.splineInst.loRjtEnd
                    self.rigInstance.armLSwitchCtl = self.cuInst.switchCtl
                if fn == 'Arm' and sn == 'R':
                    self.rigInstance.handRRjt = self.splineInst.loRjtEnd
                    self.rigInstance.armRSwitchCtl = self.cuInst.switchCtl
                
                self.finalInst.allSet( fn, sn )