import maya.cmds as cmds
import rigdata
import initmatrixdata
import chModules.rigbase as rigbase
import copy

initCtlInfoList = initmatrixdata.string.split( '\n' )
initCtlNameList = []
initCtlMtxList = []
for initCtlInfo in initCtlInfoList:
    try:
        initCtlName, initCtlMtx = initCtlInfo.split( '=' )
    except: print 'fail is-->', initCtlInfo
    initCtlNameList.append( initCtlName.replace( ' ', '' )+'_InitCTL' )
    initCtlMtxList.append( initCtlMtx )

class FingerInitCtlRig:
    def __init__(self, initCtlNameList ):
        self.fingerInitCtlData = rigdata.FingerNameData( initCtlNameList )
        self.ArmInitCtlData = rigdata.ArmNameData( initCtlNameList )
        self.fingerCount = self.fingerInitCtlData.numOfItem()
        self.outputTransformL = []
        self.outputTransformR = []
    
    def rigEachPart( self, index, side ):
        outputTransform = []
        
        inverseAim = False
        globalMult = 1
        if side.find( 'R' ) != -1:
            inverseAim = True
            globalMult = -1
            
        aimObjectOptions = { 'axis':0, 'inverseAim':inverseAim, 'replaceTarget':'InitCTL', 'replace':'InitCtl' }
        
        fingerInitCtlNameList = self.fingerInitCtlData.getEachFingerList( index, side )
        
        firstFingerInitCtl = fingerInitCtlNameList[0]
        secondFingerInitCtl = fingerInitCtlNameList[1]
        betweenFingerInitCtls = fingerInitCtlNameList[2:-1]
        endFingerInitCtl = fingerInitCtlNameList[-1]
        
        aimObject0= rigbase.makeAimObject( secondFingerInitCtl, firstFingerInitCtl, **aimObjectOptions )[0]
        outputTransform.append( aimObject0 )
        aimObject1 = rigbase.makeAimObject( endFingerInitCtl, secondFingerInitCtl, **aimObjectOptions )[0]
        aimObject1 = cmds.rename( aimObject1, aimObject1.replace( 'AimObj', 'AimGrp' ) )
        
        rigbase.betweenRigInAimObject( betweenFingerInitCtls, aimObject1, replaceTarget='InitCTL', replace='InitCtl', globalMult = globalMult )
        
        for fingerInitCtl in betweenFingerInitCtls:
            rigbase.AttrEdit( fingerInitCtl ).lockAttrs( 'tz' )
            if side.find( 'L' ) != -1:
                cmds.transformLimits( fingerInitCtl, ty= [0.01,1], ety=[True, False] )
            else:
                cmds.transformLimits( fingerInitCtl, ty= [-1,0.01], ety=[False, True] )
        betweenFingerInitCtls.append( endFingerInitCtl )
            
        aimObjectParent = secondFingerInitCtl
        for fingerInitCtl in betweenFingerInitCtls:
            aimObject = rigbase.makeAimObject( fingerInitCtl, aimObjectParent, **aimObjectOptions )[0]
            aimObjectParent = fingerInitCtl
            outputTransform.append( aimObject )
        
        outputTransform.append( endFingerInitCtl )
        return outputTransform

    def rigSide(self, side ):
        wrist = self.ArmInitCtlData.getOneByName( 'Wrist', side )
        self.outputTransform = [[] for i in range( self.fingerCount ) ]
        
        for i in range( self.fingerCount ):
            self.outputTransform[i] = self.rigEachPart( i, side )
            
            for tr in self.fingerInitCtlData.getEachFingerList( i, side ):
                if not cmds.listRelatives( tr, p=1 ):
                    cmds.parent( tr, wrist )
            
    def rigAll(self):
        self.rigSide( '_L_' )
        self.outputTransformL = copy.copy( self.outputTransform )
        self.rigSide( '_R_' )
        self.outputTransformR = copy.copy( self.outputTransform )
        
class ArmInitCtlRig:
    def __init__(self, initCtlNameList ):
        self.armInitCtlData = rigdata.ArmNameData( initCtlNameList )
        self.armInitCtlAdd =  rigdata.ArmAddNameData( initCtlNameList )
        self.outputTransformL = []
        self.outputTransformR = []
        self.outputAddTrL = []
        self.outputAddTrR = []
    
    def rigSide(self, side ):
        inverseAim = False
        inverseUp = False
        globalMult = 1
        if side.find( 'R' ) != -1:
            inverseAim = True
            inverseUp = True
            globalMult = -1
            
        shoulder, elbow, wrist, poleV = self.armInitCtlData.getSortList( side )
        upperArm, lowerArm  = self.armInitCtlAdd.getSortList( side )
        
        aimObjectOptions = { 'axis':0, 'upAxis':2, 'inverseAim':inverseAim, 'inverseUp':inverseUp, 'upType':'object', 'upObject':poleV, 'replaceTarget':'InitCTL', 'replace':'InitCtl' }
        
        aimObject, wristPoseMltDcmp = rigbase.makeAimObject( wrist, shoulder, **aimObjectOptions )
        aimObject = cmds.rename( aimObject, aimObject.replace( 'AimObj', 'AimGrp' ) )
        
        rigbase.betweenRigInAimObject( elbow, aimObject, dcmp = wristPoseMltDcmp, replaceTarget='InitCTL', replace='InitCtl', globalMult = globalMult )
        rigbase.AttrEdit( elbow ).lockAttrs( 'ty' )
        
        aimObjectElbow = rigbase.makeAimObject( wrist, elbow, **aimObjectOptions )[0]
        aimObjectShoulder = rigbase.makeAimObject( elbow, shoulder, **aimObjectOptions )[0]
        
        cmds.parent( upperArm, aimObjectShoulder )
        cmds.parent( lowerArm, aimObjectElbow )
        
        upperArmGrp = rigbase.addParent( upperArm )
        lowerArmGrp = rigbase.addParent( lowerArm )
        
        upperMtxDcmp = rigbase.getChildMtxDcmp( elbow, aimObjectShoulder )
        lowerMtxDcmp = rigbase.getChildMtxDcmp( wrist, aimObjectElbow )
        upperMultMiddle = cmds.createNode( 'multiplyDivide', n=upperArm.replace( 'InitCTL', 'InitCtlMiddleMult' ) )
        lowerMultMiddle = cmds.createNode( 'multiplyDivide', n=lowerArm.replace( 'InitCTL', 'InitCtlMiddleMult' ) )
        
        cmds.connectAttr( upperMtxDcmp+'.ot', upperMultMiddle+'.input1' )
        cmds.connectAttr( lowerMtxDcmp+'.ot', lowerMultMiddle+'.input1' )
        
        cmds.setAttr( upperMultMiddle+'.input2', .5,.5,.5 )
        cmds.setAttr( lowerMultMiddle+'.input2', .5,.5,.5 )
        
        cmds.connectAttr( upperMultMiddle+'.output', upperArmGrp+'.t' )
        cmds.connectAttr( lowerMultMiddle+'.output', lowerArmGrp+'.t' )
        
        cmds.setAttr( upperArmGrp+'.r', 0,0,0 )
        cmds.setAttr( lowerArmGrp+'.r', 0,0,0 )
        
        if side.find( 'L' ) != -1:
            self.outputTransformL = [ aimObjectShoulder, aimObjectElbow, wrist, poleV ]
            self.outputAddTrL = [ upperArm, lowerArm ]
            cmds.transformLimits( elbow, tz= [-1,0.01], etz=[False, True] )
        else:
            self.outputTransformR = [ aimObjectShoulder, aimObjectElbow, wrist, poleV ]
            self.outputAddTrR = [ upperArm, lowerArm ]
            cmds.transformLimits( elbow, tz= [0.01,1], etz=[True, False] )
        
    def rigAll(self):
        self.rigSide( '_L_' )
        self.rigSide( '_R_' )

class LegInitCtlRig:
    def __init__(self, initCtlNameList ):
        self.legInitCtlData = rigdata.LegNameData( initCtlNameList )
        self.legInitCtlAdd  = rigdata.LegAddNameData( initCtlNameList )
        self.outputTransformL = []
        self.outputTransformR = []
        self.outputAddTrL = []
        self.outputAddTrR = []
        
    def rigLegPart(self, side ):
        inverseAim = False
        inverseUp = True
        globalMult = 1
        if side.find( 'R' ) != -1:
            inverseAim= True
            inverseUp = False
            globalMult = -1
            
        hip, knee, ankle, poleV = self.legInitCtlData.getSortList( side )[:4]
        upperLeg, lowerLeg      = self.legInitCtlAdd.getSortList( side )
        
        aimObjectOptions = { 'axis':0, 'upAxis':2, 'inverseAim':inverseAim, 'inverseUp':inverseUp, 'upType':'object', 'upObject':poleV, 'replaceTarget':'InitCTL', 'replace':'InitCtl' }
        
        aimObject, anklePoseMltDcmp = rigbase.makeAimObject( ankle, hip, **aimObjectOptions )
        aimObject = cmds.rename( aimObject, aimObject.replace( 'AimObj', 'AimGrp' ) )
        
        rigbase.betweenRigInAimObject( knee, aimObject, dcmp = anklePoseMltDcmp, replaceTarget='InitCTL', replace='InitCtl', globalMult = globalMult )
        rigbase.AttrEdit( knee ).lockAttrs( 'ty' )
        
        aimObjectKnee = rigbase.makeAimObject( ankle, knee, **aimObjectOptions )[0]
        aimObjectHip = rigbase.makeAimObject( knee, hip, **aimObjectOptions )[0]
        
        cmds.parent( upperLeg, aimObjectHip )
        cmds.parent( lowerLeg, aimObjectKnee )
        
        upperLegGrp = rigbase.addParent( upperLeg )
        lowerLegGrp = rigbase.addParent( lowerLeg )
        
        upperMtxDcmp = rigbase.getChildMtxDcmp( knee, aimObjectHip )
        lowerMtxDcmp = rigbase.getChildMtxDcmp( ankle, aimObjectKnee )
        upperMultMiddle = cmds.createNode( 'multiplyDivide', n=upperLeg.replace( 'InitCTL', 'InitCtlMiddleMult' ) )
        lowerMultMiddle = cmds.createNode( 'multiplyDivide', n=lowerLeg.replace( 'InitCTL', 'InitCtlMiddleMult' ) )
        
        cmds.connectAttr( upperMtxDcmp+'.ot', upperMultMiddle+'.input1' )
        cmds.connectAttr( lowerMtxDcmp+'.ot', lowerMultMiddle+'.input1' )
        
        cmds.setAttr( upperMultMiddle+'.input2', .5,.5,.5 )
        cmds.setAttr( lowerMultMiddle+'.input2', .5,.5,.5 )
        
        cmds.connectAttr( upperMultMiddle+'.output', upperLegGrp+'.t' )
        cmds.connectAttr( lowerMultMiddle+'.output', lowerLegGrp+'.t' )
        
        cmds.setAttr( upperLegGrp+'.r', 0,0,0 )
        cmds.setAttr( lowerLegGrp+'.r', 0,0,0 )
        
        if side.find( 'L' ) != -1:
            self.outputTransformL = [ aimObjectHip, aimObjectKnee, ankle, poleV ]
            self.outputAddTrL = [ upperLeg, lowerLeg ]
            cmds.transformLimits( knee, tz= [0.01,1], etz=[True, False] )
        else:
            self.outputTransformR = [ aimObjectHip, aimObjectKnee, ankle, poleV ]
            self.outputAddTrR = [ upperLeg, lowerLeg ]
            cmds.transformLimits( knee, tz= [-1,0.01], etz=[False, True] )

    def rigFootPart(self, side ):
        ankle = self.legInitCtlData.getSortList( side )[2]
        footInitCtls = self.legInitCtlData.getSortList( side )[4:]
        ball, toe, heel, ballPiv, bankIn, bankOut, toePiv = footInitCtls
        rigbase.parentOrder( toePiv, bankOut, bankIn, ballPiv, heel )
        rigbase.parentOrder( toe, ball )
        cmds.parent( ball, heel, ankle )
        
        for footInitCtl in footInitCtls:
            rigbase.AttrEdit( footInitCtl ).lockAttrs( 'r', 's', 'v' )
        
        if side.find( 'L' ) != -1:
            self.outputTransformL += [ ball, toe, heel, ballPiv, bankIn, bankOut, toePiv ]
        else:
            self.outputTransformR += [ ball, toe, heel, ballPiv, bankIn, bankOut, toePiv ]

    def rigSide(self, side ):
        self.rigLegPart( side )
        self.rigFootPart( side )
        
    def rigAll(self):
        self.rigSide( '_L_' )
        self.rigSide( '_R_' )
        
class TorsoInitCtlRig:
    def __init__(self, initCtlNameList ):
        self.torsoInitCtlData = rigdata.TorsoNameData( initCtlNameList )
        self.armInitCtlData = rigdata.ArmNameData( initCtlNameList )
        self.outputTransform = []
        
    def rigSelf(self):
        root, waist, chest = self.torsoInitCtlData.getSortList()[:3]
        aimObject = rigbase.makeAimObject( chest, root, axis=1, replaceTarget = 'InitCTL', replace='InitCtl' )[0]
        
        rigbase.betweenRigInAimObject( waist, aimObject, replaceTarget='InitCTL', replace='InitCtl' )
        
        rigbase.AttrEdit( root, waist, chest ).lockAttrs( 'r', 's', 'tx' )
        
        self.outputTransform = [ root, waist, chest ]
        
    def rigOther(self):
        collar_L, collar_R = self.torsoInitCtlData.getSortList()[-2:]
        shoulder_L = self.armInitCtlData.getSortList( '_L_' )[0]
        shoulder_R = self.armInitCtlData.getSortList( '_R_' )[0]
        
        aimObjectL = rigbase.makeAimObject( shoulder_L, collar_L, replaceTarget = 'InitCTL', replace='InitCtl' )[0]
        aimObjectR = rigbase.makeAimObject( shoulder_R, collar_R, replaceTarget = 'InitCTL', replace='InitCtl', inverseAim=1 )[0]
        
        rigbase.AttrEdit( aimObjectL, aimObjectR ).lockAttrs( 's' )
        
        self.outputTransform += [ aimObjectL, aimObjectR ]
        
    def rigAll(self):
        self.rigSelf()
        self.rigOther()
        
class HeadInitCtlRig:
    def __init__(self, initCtlNameList ):
        self.HeadInitCtlData = rigdata.HeadNamdData( initCtlNameList )
        self.outputTransform = []
    
    def rigAll(self):
        neck, neckMiddle, head, eyeL, eyeR, eyeAimPiv = self.HeadInitCtlData.getSortList()
        
        aimObject= rigbase.makeAimObject( head, neck, axis=1, replaceTarget = 'InitCTL', replace='InitCtl' )[0]
        aimObject = cmds.rename( aimObject, aimObject.replace( 'AimObj', 'AimGrp' ) )
        
        rigbase.betweenRigInAimObject( neckMiddle, aimObject, replaceTarget='InitCTL', replace='InitCtl' )
        rigbase.AttrEdit( neckMiddle ).lockAttrs( 'tx' )
        
        aimObjectNeck = rigbase.makeAimObject( neckMiddle, neck, axis=1, replaceTarget = 'InitCTL', replace='InitCtl' )[0]
        aimObjectNeckMiddle = rigbase.makeAimObject( head, neckMiddle, axis=1, replaceTarget = 'InitCTL', replace='InitCtl' )[0]
        
        cmds.parent( eyeL, eyeR, eyeAimPiv, head )
        
        self.outputTransform = [ neck, neckMiddle, head, eyeL, eyeR, eyeAimPiv ]

class RigAll:
    def putInitCtl( self ):
        self.initCtlNameList = []
        for i in range( len(initCtlInfoList) ):
            initCtlName = initCtlNameList[i]
            initCtlMtx = initCtlMtxList[i]
            initCtl = cmds.createNode( 'transform', n=initCtlName )
            cmds.setAttr( initCtl+'.dh', 1 )
            exec( "cmds.xform( initCtl, matrix=%s )" % initCtlMtx )
        
        self.initJntsGrp = cmds.createNode( 'transform', n='All_InitJnt' )

    def doIt(self):
        self.torsoPart = TorsoInitCtlRig( initCtlNameList )
        self.headPart = HeadInitCtlRig( initCtlNameList )
        self.armPart = ArmInitCtlRig( initCtlNameList )
        self.legPart = LegInitCtlRig( initCtlNameList )
        self.fingerPart = FingerInitCtlRig( initCtlNameList )
        
        self.torsoPart.rigAll()
        self.headPart.rigAll()
        self.armPart.rigAll()
        self.legPart.rigAll()
        self.fingerPart.rigAll()
        
        
        self.initAllCtl = cmds.circle( normal=[0,1,0], radius = 7, n='All_InitCTL' )[0]
        cmds.setAttr( self.initAllCtl+'.dh', 1 )
        rigbase.addParent( self.initAllCtl )
        rigbase.connectSameAttr( self.initAllCtl, self.initJntsGrp ).doIt( 't', 'r' )
        
        for initCtlName in initCtlNameList:
            if not cmds.listRelatives( initCtlName, p=1 ):
                cmds.parent( initCtlName, self.initAllCtl )
                
        self.initJointSet()
        cmds.parent( self.torsoInitJnts[0], self.initJntsGrp )
        rigbase.transformSetColor( self.torsoInitJnts[0], 22 )
        
        cmds.select( self.torsoInitJnts[0], hi=1 )
        for sel in cmds.ls( sl=1 ):
            cmds.setAttr( sel+'.radius', 0 )
        
        cmds.select( self.initAllCtl )
        
        INIT = cmds.group( em=1, n='INIT' )
        cmds.parent( 'All_InitJnt', 'All_InitCTL_GRP', INIT )
        
        self.rObj = cmds.createNode( 'multDoubleLinear', n='RightClickObj_Inits' )
        attrEdit = rigbase.AttrEdit( self.rObj )
        attrEdit.addAttr( ln='originalName', dt='string' )
        cmds.setAttr( self.rObj+'.originalName', self.rObj, type='string' )
        
        for initCtl in cmds.ls( '*_InitCTL' ):
            attrEdit.addAttr( ln=initCtl, at='message' )
            cmds.connectAttr( initCtl+'.message', self.rObj+'.'+initCtl )
        
        rigbase.AttrEdit( 'All_InitCTL' ).addAttr( ln=self.rObj, at='message' )
        cmds.connectAttr( self.rObj+'.message', 'All_InitCTL.'+self.rObj )    
        
    def initJointSet(self):
        self.torsoPartJointSet()
        self.armPartJointSet()
        self.legPartJointSet()
        self.headPartJointSet()
        self.fingerPartJointSet()
        
    def torsoPartJointSet(self ):
        torsoTransforms = self.torsoPart.outputTransform
        self.torsoInitJnts = []
        self.torsoInits = []
        
        cmds.select( d=1 )
        for torsoTr in torsoTransforms:
            if torsoTr.find( 'Collar' ) != -1:
                cmds.select( self.torsoInitJnts[2] )
            initJnt = cmds.joint( n='_'.join( torsoTr.split('_')[:-1] ) + '_InitJnt' )
            rigbase.constraint( torsoTr, initJnt )
            
            self.torsoInitJnts.append( initJnt )
            self.torsoInits.append( initJnt.replace( 'InitJnt', 'Init' ) )
            
            cmds.select( initJnt )
        
    def armPartJointSet(self):
        armLObjs = self.armPart.outputTransformL
        armLObjs += self.armPart.outputAddTrL
        self.armLInitJnts = []
        self.armLInits = []
        
        armRObjs = self.armPart.outputTransformR
        armRObjs += self.armPart.outputAddTrR
        self.armRInitJnts = []
        self.armRInits = []
        
        cmds.select( self.torsoInitJnts[-2] )
        for armLObj in armLObjs:
            index = armLObjs.index( armLObj )
            if index in [3,4]:
                cmds.select( self.armLInitJnts[0] )
            if index == 5:
                cmds.select( self.armLInitJnts[1] )
                
            splitName = armLObj.split( '_' )[:-1]
            jntName = '_'.join( splitName )+'_InitJnt'
            
            armLJnt = cmds.joint( n=jntName )
            if index == 3:
                rigbase.transformDefault( armLJnt )
                rigbase.constraint( armLObj, armLJnt, r=0 )
            elif index in [4,5]:
                armLObjP = cmds.listRelatives( armLObj, p=1 )[0]
                cmds.setAttr( armLObjP+'.dh', 0 )
                rigbase.constraint( armLObjP, armLJnt )
                cmds.select( armLJnt )
                cmds.rename( armLJnt, armLJnt.replace( '_InitJnt', '_InitJnt_GRP' ))
                armLJnt = cmds.joint( n=armLJnt.replace( '_GRP', '' ) )
                rigbase.constraint( armLObj, armLJnt )
            else:
                rigbase.constraint( armLObj, armLJnt )
                
            self.armLInitJnts.append( armLJnt )
            self.armLInits.append( armLJnt.replace( 'InitJnt', 'Init' ) )
            
            cmds.select( armLJnt )
            
        cmds.select( self.torsoInitJnts[-1] )
        for armRObj in armRObjs:
            index = armRObjs.index( armRObj )
            if index in [3,4]:
                cmds.select( self.armRInitJnts[0] )
            if index == 5:
                cmds.select( self.armRInitJnts[1] )
                
            splitName = armRObj.split( '_' )[:-1]
            jntName = '_'.join( splitName )+'_InitJnt'
            
            armRJnt = cmds.joint( n=jntName )
            if index == 3:
                rigbase.transformDefault( armRJnt )
                rigbase.constraint( armRObj, armRJnt, r=0 )
            elif index in [4,5]:
                armRObjP = cmds.listRelatives( armRObj, p=1 )[0]
                cmds.setAttr( armRObjP+'.dh', 0 )
                rigbase.constraint( armRObjP, armRJnt )
                cmds.select( armRJnt )
                cmds.rename( armRJnt, armRJnt.replace( '_InitJnt', '_InitJnt_GRP' ))
                armRJnt = cmds.joint( n=armRJnt.replace( '_GRP', '' ) )
                rigbase.constraint( armRObj, armRJnt )
            else:
                rigbase.constraint( armRObj, armRJnt )
            
            self.armRInitJnts.append( armRJnt )
            self.armRInits.append( armRJnt.replace( 'InitJnt', 'Init' ) )
            
            cmds.select( armRJnt )
            
    def legPartJointSet(self):
        legLObjs = self.legPart.outputTransformL
        legLObjs += self.legPart.outputAddTrL
        self.legLInitJnts = []
        self.legLInits = []
        
        legRObjs = self.legPart.outputTransformR
        legRObjs += self.legPart.outputAddTrR
        self.legRInitJnts = []
        self.legRInits = []
        
        cmds.select( self.torsoInitJnts[0] )
        for legLObj in legLObjs:
            index = legLObjs.index( legLObj )
            
            if index in [3,11]:
                cmds.select( self.legLInitJnts[0] )
            if index == 4:
                cmds.select( self.legLInitJnts[2] )
            if index == 6:
                cmds.select( self.legLInitJnts[2] )
            if index == 12:
                cmds.select( self.legLInitJnts[1] )
            
            splitName = legLObj.split( '_' )[:-1]
            jntName = '_'.join( splitName )+'_InitJnt'
            
            legLJnt = cmds.joint( n=jntName )
            if index == 3:
                rigbase.transformDefault( legLJnt )
                rigbase.constraint( legLObj, legLJnt, r=0 )
            elif index in [11,12]:
                legLObjP = cmds.listRelatives( legLObj, p=1 )[0]
                cmds.setAttr( legLObjP+'.dh', 0 )
                rigbase.constraint( legLObjP, legLJnt )
                cmds.select( legLJnt )
                cmds.rename( legLJnt, legLJnt.replace( '_InitJnt', '_InitJnt_GRP' ))
                legLJnt = cmds.joint( n=legLJnt.replace( '_GRP', '' ) )
                rigbase.constraint( legLObj, legLJnt )
            else:
                rigbase.constraint( legLObj, legLJnt )
                
            self.legLInitJnts.append( legLJnt )
            self.legLInits.append( legLJnt.replace( 'InitJnt', 'Init' ) )
            
            cmds.select( legLJnt )
        
        cmds.select( self.torsoInitJnts[0] )
        for legRObj in legRObjs:
            index = legRObjs.index( legRObj )
            
            if index in [3,11]:
                cmds.select( self.legRInitJnts[0] )
            if index == 4:
                cmds.select( self.legRInitJnts[2] )
            if index == 6:
                cmds.select( self.legRInitJnts[2] )
            if index == 12:
                cmds.select( self.legRInitJnts[1] )
                
            splitName = legRObj.split( '_' )[:-1]
            jntName = '_'.join( splitName )+'_InitJnt'
            
            legRJnt = cmds.joint( n=jntName )
            if index == 3:
                rigbase.transformDefault( legRJnt )
                rigbase.constraint( legRObj, legRJnt, r=0 )
            elif index in [11,12]:
                legRObjP = cmds.listRelatives( legRObj, p=1 )[0]
                cmds.setAttr( legRObjP+'.dh', 0 )
                rigbase.constraint( legRObjP, legRJnt )
                cmds.select( legRJnt )
                cmds.rename( legRJnt, legRJnt.replace( '_InitJnt', '_InitJnt_GRP' ))
                legRJnt = cmds.joint( n=legRJnt.replace( '_GRP', '' ) )
                rigbase.constraint( legRObj, legRJnt )
            else:
                rigbase.constraint( legRObj, legRJnt )
            
            self.legRInitJnts.append( legRJnt )
            self.legRInits.append( legRJnt.replace( 'InitJnt', 'Init' ) )
            
            cmds.select( legRJnt )
            
    def headPartJointSet(self):
        headObjs = self.headPart.outputTransform
        self.headInitJnts = []
        self.headInits = []
        
        cmds.select( self.torsoInitJnts[2] )
        for headObj in headObjs:
            index = headObjs.index( headObj )
            
            if index == 4:
                cmds.select( self.headInitJnts[2] )
                
            splitName = headObj.split( '_' )[:-1]
            jntName = '_'.join( splitName )+'_InitJnt'
                
            headJnt = cmds.joint( n=jntName )
            rigbase.constraint( headObj, headJnt )
            
            self.headInitJnts.append( headJnt )
            self.headInits.append( headJnt.replace( 'InitJnt', 'Init' ) )
            
            cmds.select( headJnt )
            if index == len( headObjs )-2:
                cmds.select( self.headInitJnts[2] )
            
    def fingerPartJointSet(self):
        handLObjs = self.fingerPart.outputTransformL
        handRObjs = self.fingerPart.outputTransformR
        
        self.fingerLInitJnts = []
        self.fingerRInitJnts = []
        self.fingerLInits = []
        self.fingerRInits = []
        
        for fingerLObjs in handLObjs:
            initJnts = []
            inits = []
            cmds.select( self.armLInitJnts[2] )
            
            for fingerObj in fingerLObjs:
                splitName = fingerObj.split( '_' )[:-1]
                jntName = '_'.join( splitName )+'_InitJnt'
                
                fingerJnt = cmds.joint( n=jntName, radius=.5 )
                rigbase.constraint( fingerObj, fingerJnt )
                initJnts.append( fingerJnt )
                inits.append( fingerJnt.replace( 'InitJnt', 'Init' ) )
                cmds.select( fingerJnt )
                
            self.fingerLInitJnts.append( initJnts )
            self.fingerLInits.append( inits )
            
        for fingerRObjs in handRObjs:
            initJnts = []
            inits = []
            cmds.select( self.armRInitJnts[2] )
            
            for fingerObj in fingerRObjs:
                splitName = fingerObj.split( '_' )[:-1]
                jntName = '_'.join( splitName )+'_InitJnt'
                
                fingerJnt = cmds.joint( n=jntName, radius=.5 )
                rigbase.constraint( fingerObj, fingerJnt )
                initJnts.append( fingerJnt )
                inits.append( fingerJnt.replace( 'InitJnt', 'Init' ) )
                cmds.select( fingerJnt )
                
            self.fingerRInitJnts.append( initJnts )
            self.fingerRInits.append( inits )