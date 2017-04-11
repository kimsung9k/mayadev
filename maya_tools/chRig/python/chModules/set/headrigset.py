import maya.cmds as cmds
import chModules.rigbase as rigbase

class CtlSet:
    def __init__(self, rigInstance ):
        self.rigInstance = rigInstance
        self.headInits = rigInstance.headInits
        self.neckInit = self.headInits[0]
        self.neckMiddleInit = self.headInits[1]
        self.headInit = self.headInits[2]
        self.eyeLInit = self.headInits[3]
        self.eyeRInit = self.headInits[4]
        self.eyeInit  = self.headInits[5]
        self.headConst = rigInstance.headConst
        
    def getMtxDcmpInNeckSet(self):
        initAimObject = rigbase.makeAimObject( self.headInit, self.neckInit, axis=1, addName='AimObject' )[0]
        return rigbase.getChildMtxDcmp( self.neckMiddleInit, initAimObject )
        
    def neckCtlSet(self):
        self.neckCtl = rigbase.Controler( n='Neck_CTL' )
        self.neckCtl.setShape( normal=[0,1,0], radius=.6 )
        self.neckCtl.setColor( 29 )
        attrEdit = rigbase.AttrEdit( self.neckCtl )
        attrEdit.lockAndHideAttrs( 'sx','sy','sz','v' )
    
    def headCtlSet(self):
        self.headCtl = rigbase.Controler( n='Head_CTL' )
        self.headCtl.setShape( normal=[0,0,1], radius=1.2, center = [0,.8,0] )
        self.headCtl.setColor( 30 )
        
        attrEdit = rigbase.AttrEdit( self.headCtl.name )
        rigbase.addHelpTx( self.headCtl.name, 'Follow' )
        attrEdit.lockAndHideAttrs( 'sx','sy','sz','v' )
        attrEdit.addAttr( ln='neckFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='chestFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='rootFollow', min=0, max=10 )
        attrEdit.addAttr( ln='flyFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='moveFollow', min=0, max=10 )
        rigbase.addHelpTx( self.headCtl.name, 'MiddleNeckVis' )
        attrEdit.addAttr( ln='middleNeckVis', min=0, max=1, at='long', cb=1 )
        
    def neckMiddleCtlSet(self):
        self.neckMiddleCtl = rigbase.Controler( n='NeckMiddle_CTL' )
        self.neckMiddleCtl.setShape( normal=[0,1,0], radius = .5 )
        self.neckMiddleCtl.setColor( 29 )
        
        self.middlePoint1 = rigbase.Transform( n='NeckMiddle_spline_Point1' )
        self.middlePoint2 = rigbase.Transform( n='NeckMiddle_spline_Point2' )
        
        self.middlePoint1.setParent( self.neckMiddleCtl )
        self.middlePoint2.setParent( self.neckMiddleCtl )
        rigbase.transformDefault( self.middlePoint1, self.middlePoint2 )
        
        midPnt1Dist= cmds.createNode( 'distanceBetween', n='NeckMiddle_spPnt1_dist' )
        midPnt2Dist = cmds.createNode( 'distanceBetween', n='NeckMiddle_spPnt2_dist' )
        midMult1Dist = cmds.createNode( 'multDoubleLinear', n='NeckMiddle_md1' )
        midMult2Dist = cmds.createNode( 'multDoubleLinear', n='NeckMiddle_md2' )
        
        cmds.setAttr( midMult1Dist+'.input2', -.4 )
        cmds.setAttr( midMult2Dist+'.input2', .4 )
        
        cmds.connectAttr( self.neckMiddleInit+'.m', midPnt1Dist+'.inMatrix1' )
        cmds.connectAttr( self.headInit+'.m',       midPnt2Dist+'.inMatrix2' )
        cmds.connectAttr( midPnt1Dist+'.distance', midMult1Dist+'.input1' )
        cmds.connectAttr( midPnt2Dist+'.distance', midMult2Dist+'.input1' )
        cmds.connectAttr( midMult1Dist+'.output', self.middlePoint1+'.ty' )
        cmds.connectAttr( midMult2Dist+'.output', self.middlePoint2+'.ty' )
        
        attrEdit = rigbase.AttrEdit( self.neckMiddleCtl.name )
        attrEdit.lockAndHideAttrs( 'sx','sy','sz','v' )
        
        self.rigInstance.neckMiddleCtl = self.neckMiddleCtl.name
        
    def eyeCtlSet(self):
        self.eyeLCtl = rigbase.Controler( n='EyeAim_L_CTL' )
        self.eyeRCtl = rigbase.Controler( n='EyeAim_R_CTL' )
        self.eyeCtl  = rigbase.Controler( n='Eye_CTL' )
        self.eyeLCtl.setShape( normal=[0,0,1], radius =.2 )
        self.eyeRCtl.setShape( normal=[0,0,1], radius =.2 )
        self.eyeCtl.setShape(  normal=[0,0,1], radius = 1 )
        
        self.eyeLCtl.setParent( self.eyeCtl )
        self.eyeRCtl.setParent( self.eyeCtl )
        self.eyeCtl.setParent( self.headCtl )
        
        self.eyeLCtl.setColor( 13 )
        self.eyeRCtl.setColor( 6 )
        self.eyeCtl.setColor( 23 )
        
        attrEdit = rigbase.AttrEdit( self.eyeLCtl.name, self.eyeRCtl.name )
        attrEdit.lockAndHideAttrs( 'rx','ry','rz','sx','sy','sz','v' )
        
        attrEdit = rigbase.AttrEdit( self.eyeCtl.name )
        attrEdit.lockAndHideAttrs( 'sx','sy','sz','v' )
        rigbase.addHelpTx( self.eyeCtl.name, 'Follow' )
        attrEdit.addAttr( ln='chestFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='rootFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='flyFollow', min=0, max=10, k=1 )
        attrEdit.addAttr( ln='moveFollow', min=0, max=10 )
        
    def setStartUpObj(self):
        self.startUpObj = rigbase.Transform( n='Neck_SplineStartUp' )
        self.startUpObj.setParent( self.neckCtl )
        rigbase.transformDefault( self.startUpObj )
        
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Neck_SplineStartUp_mtxDcmp' )
        ffmMtx = cmds.createNode( 'fourByFourMatrix', n='Neck_SplineStartUp_ffm' )
        smOri = cmds.createNode( 'smartOrient', n='Neck_SplineStartUp_SmOri' )
        
        cmds.setAttr( smOri+'.aimAxis', 1 )
        
        cmds.connectAttr( self.headCtl+'.wm' ,mtxDcmp+'.i[0]' )
        cmds.connectAttr( self.neckCtl+'.wim' ,mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.otx'  ,ffmMtx+'.i10' )
        cmds.connectAttr( mtxDcmp+'.oty'  ,ffmMtx+'.i11' )
        cmds.connectAttr( mtxDcmp+'.otz'  ,ffmMtx+'.i12' )
        cmds.connectAttr( ffmMtx+'.output',smOri+'.inputMatrix' )
        cmds.connectAttr( smOri+'.outAngle'  ,self.startUpObj+'.r' )
        
    def setEndUpObj(self):
        self.endUpObj = rigbase.Transform( n='Neck_SplineEndUp' )
        self.endUpObj.setParent( self.headCtl )
        rigbase.transformDefault( self.endUpObj )
        
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Neck_SplineStartEnd_mtxDcmp' )
        ffmMtx = cmds.createNode( 'fourByFourMatrix', n='Neck_SplineStartEnd_ffm' )
        smOri = cmds.createNode( 'smartOrient', n='Neck_SplineStartEnd_SmOri' )
        
        cmds.setAttr( mtxDcmp+'.inverseTranslate', 1 )
        cmds.setAttr( smOri+'.aimAxis', 1 )
        
        cmds.connectAttr( self.neckCtl+'.wm' ,mtxDcmp+'.i[0]' )
        cmds.connectAttr( self.headCtl+'.wim' ,mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.otx'   ,ffmMtx+'.i10' )
        cmds.connectAttr( mtxDcmp+'.oty'   ,ffmMtx+'.i11' )
        cmds.connectAttr( mtxDcmp+'.otz'   ,ffmMtx+'.i12' )
        cmds.connectAttr( ffmMtx +'.output',smOri +'.inputMatrix' )
        cmds.connectAttr( smOri  +'.outAngle' ,self.endUpObj+'.r' )
        
    def connectInit(self, inits ):
        rigbase.connectSameAttr( inits[0], self.neckCtl.transformGrp ).doIt( 't', 'r' )
        neckMiddleMtxDcmp = self.getMtxDcmpInNeckSet()
        cmds.connectAttr( neckMiddleMtxDcmp+'.ot', self.neckMiddleCtl.transformGrp+'.t' )
        cmds.connectAttr( neckMiddleMtxDcmp+'.or', self.neckMiddleCtl.transformGrp+'.r' )
        headPosMtxDcmp = rigbase.getChildMtxDcmp( inits[2], inits[0] )
        cmds.connectAttr( headPosMtxDcmp+'.ot', self.headCtl.transformGrp+'.t' )
        cmds.connectAttr( headPosMtxDcmp+'.or', self.headCtl.transformGrp+'.r' )
        
        eyeCenterMtx = cmds.createNode( 'blendTwoMatrixDecompose', n='EyeCenterMtx' )
        eyeLMtxDcmp =  cmds.createNode( 'multMatrixDecompose', n='Eye_L_MtxDcmp' )
        eyeRMtxDcmp =  cmds.createNode( 'multMatrixDecompose', n='Eye_R_MtxDcmp' )
        
        eyeCenterObj = rigbase.Transform( n='EyeCenterObj' )
        eyeCenterObj.setParent( self.headCtl )
        
        eyeLInitTarget = rigbase.Transform( n='Eye_L_InitTarget' )
        eyeRInitTarget = rigbase.Transform( n='Eye_R_InitTarget' )
        eyeLInitTarget.setParent( self.headCtl )
        eyeRInitTarget.setParent( self.headCtl )
        rigbase.connectSameAttr( inits[3], eyeLInitTarget.name ).doIt( 't', 'r' )
        rigbase.connectSameAttr( inits[4], eyeRInitTarget.name ).doIt( 't', 'r' )
        
        cmds.connectAttr( eyeLInitTarget+'.m', eyeCenterMtx+'.inMatrix1' )
        cmds.connectAttr( eyeRInitTarget+'.m', eyeCenterMtx+'.inMatrix2' )
        cmds.connectAttr( eyeCenterMtx+'.ot', eyeCenterObj+'.t' )
        
        cmds.connectAttr( eyeLInitTarget+'.wm', eyeLMtxDcmp+'.i[0]' )
        cmds.connectAttr( eyeRInitTarget+'.wm', eyeRMtxDcmp+'.i[0]' )
        cmds.connectAttr( eyeCenterObj+'.wim', eyeLMtxDcmp+'.i[1]' )
        cmds.connectAttr( eyeCenterObj+'.wim', eyeRMtxDcmp+'.i[1]' )
        
        cmds.connectAttr( eyeLMtxDcmp+'.ot', self.eyeLCtl.transformGrp+'.t' )
        cmds.connectAttr( eyeRMtxDcmp+'.ot', self.eyeRCtl.transformGrp+'.t' )
        cmds.connectAttr( inits[-1]+'.t', self.eyeCtl.transformGrp+'.t' )
        
    def connectVis(self):
        cmds.connectAttr( self.headCtl+'.middleNeckVis', self.neckMiddleCtl.transformGrp+'.v' )
        
    def allSet(self):
        self.neckCtlSet()
        self.headCtlSet()
        self.neckMiddleCtlSet()
        self.setStartUpObj()
        self.setEndUpObj()
        self.eyeCtlSet()
        self.connectVis()
        
        self.headCtl.setParent( self.neckCtl )
        self.neckMiddleCtl.setParent( self.startUpObj )
        
        self.pointList = [ self.neckCtl, self.middlePoint1, self.middlePoint2, self.headCtl ]
        
        self.rigInstance.neckCtl = self.neckCtl.name
        self.rigInstance.headCtl = self.headCtl.name
        self.rigInstance.headCtlGrp = self.headCtl.transformGrp
        self.rigInstance.eyeCtl  = self.eyeCtl.name
        self.rigInstance.eyeCtlGrp  = self.eyeCtl.transformGrp
        self.rigInstance.eyeLCtl = self.eyeLCtl.name
        self.rigInstance.eyeRCtl = self.eyeRCtl.name


class CurveSet:
    def create(self):
        self.crvName = cmds.curve( p=[ [0,0,0],[0,0,0],[0,0,0],[0,0,0] ], n='NeckSpline_CRV' )
        self.shapeName = cmds.listRelatives( self.crvName, s=1 )[0]
        cmds.setAttr( self.crvName+'.v', 0 )
        
    def connectPoints(self, pointList ):
        for i in range( len( pointList ) ):
            dcmp = cmds.createNode( 'decomposeMatrix', n='NeckSpline_point%d_dcmp' % i )
            cmds.connectAttr( pointList[i]+'.wm', dcmp+'.imat' )
            cmds.connectAttr( dcmp+'.ot', self.shapeName+'.controlPoints[%d]' % i )

    def parentTo(self, parentObj ):
        if not type( parentObj ) in [ type('string'), type(u'string') ]:
            parentObj = parentObj.name
        invDcmp = cmds.createNode( 'decomposeMatrix', n='NeckSplineCrv_InvDcmp' )
        cmds.connectAttr( parentObj+'.wim', invDcmp+'.imat' )
        cmds.connectAttr( invDcmp+'.ot', self.crvName+'.t' )
        cmds.connectAttr( invDcmp+'.or', self.crvName+'.r' )
        cmds.connectAttr( invDcmp+'.os', self.crvName+'.s' )
        cmds.parent( self.crvName, parentObj )


class SplineSet:
    def __init__(self, jntNum ):
        self.rjts = []
        
        cmds.select( d=1 )
        for i in range( jntNum ):
            self.rjts.append( cmds.joint( n='Neck_Spline%d_RJT' % i , radius=1.5 ) )
            
    def connectCurve( self, crvShape ):
        if cmds.nodeType( crvShape ) == 'transform':
            crvShape = cmds.listRelatives( crvShape, s=1 )[0]
        crv = cmds.listRelatives( crvShape, p=1 )[0]
        
        spci = cmds.createNode( 'splineCurveInfo', n='Neck_Spline_Crv_Spci' )
        cmds.connectAttr( crvShape+'.local', spci+'.inputCurve' )
        cmds.setAttr( spci+'.sua', 2 )
        cmds.setAttr( spci+'.eua', 2 )
        cmds.setAttr( spci+'.taa', 1 )
        cmds.setAttr( spci+'.tua', 2 )
        
        for rjt in self.rjts[0:-1]:
            i = self.rjts.index( rjt )
            paramValue = (i+.0001)/(len( self.rjts )-1)
            rigbase.AttrEdit( rjt ).addAttr( ln='parameter', min=0, max=1, k=1, dv=paramValue )
            cmds.connectAttr( rjt+'.parameter', spci+'.parameter[%d]' % i )
            point = cmds.createNode( 'transform', n='NeckSpline_point%d' % i )
            cmds.parent( point, crv )
            cmds.connectAttr( spci+'.output[%d].position' % i, point+'.t' )
            cmds.connectAttr( spci+'.output[%d].rotate' % i, point+'.r' )
            rigbase.constraint( point, rjt )
        
        self.spci = spci
            
    def setStartUpObj(self, upObj ):
        cmds.connectAttr( upObj+'.wm', self.spci+'.startTransform' )
    
    def setEndUpObj(self, upObj ):
        cmds.connectAttr( upObj+'.wm', self.spci+'.endTransform' )
        
    def constrainEnd(self, endCtl ):
        rigbase.constraint( endCtl, self.rjts[-1] )
        
class EyeJointSet:
    def __init__( self, rigInstance ):
        cmds.select( d=1 )
        self.rigInstance = rigInstance
        self.eyeLJnt = cmds.joint( n='Eye_L_RJT', radius=1.5 )
        self.eyeRJnt = cmds.joint( n='Eye_R_RJT', radius=1.5 )
        
        self.rigInstance.eyeLJnt = self.eyeLJnt
        self.rigInstance.eyeRJnt = self.eyeRJnt

    def aimConstraint(self, eyeLCtl, eyeRCtl ):
        cmds.aimConstraint( eyeLCtl, self.eyeLJnt, aim=[0,0,1], u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo= eyeLCtl )
        cmds.aimConstraint( eyeRCtl, self.eyeRJnt, aim=[0,0,1], u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo= eyeRCtl )
        
    def connectInit(self, eyeLInit, eyeRInit ):
        cmds.connectAttr( eyeLInit+'.t', self.eyeLJnt+'.t' )
        cmds.connectAttr( eyeRInit+'.t', self.eyeRJnt+'.t' )
        
    def parent(self, targetRjt ):
        cmds.parent( self.eyeLJnt, self.eyeRJnt, targetRjt )

class RigAll:
    def __init__(self, rigInstance ):
        self.rigInstance = rigInstance
        self.chestJnt = rigInstance.splineJnts[-1]
        self.chestCtl = rigInstance.chestCtl
        self.inits = rigInstance.headInits
        self.eyeInit = rigInstance.headInits[-1]
        
    def annotation(self, side ):
        if side == 'L':
            eyeCtl = self.rigInstance.eyeLCtl
            eyeJnt = self.rigInstance.eyeLJnt
        else:
            eyeCtl = self.rigInstance.eyeRCtl
            eyeJnt = self.rigInstance.eyeRJnt
        
        loc = cmds.spaceLocator( n='Eye_%s_AnnotatLoc' % side )[0]
        locShape = cmds.listRelatives( loc, s=1 )[0]
        annotateShape = cmds.createNode( 'annotationShape', n='Eye_%s_AnnotateShape' % side )
        annotate = cmds.listRelatives( annotateShape, p=1 )[0]
        cmds.rename( annotate, 'Eye_%s_Annotate' % side )
        cmds.parent( annotate, eyeCtl )
        rigbase.constraint( eyeJnt, annotate, r=0 )
        cmds.connectAttr( locShape+'.wm', annotateShape+'.dagObjectMatrix[0]' )
        
        cmds.parent( loc, eyeCtl )
        rigbase.transformDefault( loc )
        
        cmds.setAttr( loc+'.v', 0 )
        cmds.setAttr( annotate+'.overrideEnabled', True )
        cmds.setAttr( annotate+'.overrideDisplayType', 2 )
        
    def followSet(self):
        followMtx = cmds.createNode( 'followMatrix', n='Head_FollowMtx' )
        
        def allMtxDcmp():
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Head_All_F_MtxDcmp' )
            cmds.connectAttr( self.inits[2] +'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( self.rigInstance.initAll+'.wim', mtxDcmp+'.i[1]' )
            return mtxDcmp
                    
        def setMtxDcmp( part ):
            partName = part.replace( '_Init', '' )
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Head_%s_F_MtxDcmp' % partName )
            cmds.connectAttr( self.inits[2]+'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( part+'.wim', mtxDcmp+'.i[1]' )
            return mtxDcmp
            
        fp_inWorld =  cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inWorld' ) )
        fp_inMove =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inMove' ) )
        fp_inFly =    cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inFly' ) )
        fp_inRoot =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inRoot' ) )
        fp_inChest =  cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inChest' ) )
        fp_inNeck =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inNeck' ) )
        
        allFpDcmp   = setMtxDcmp( self.rigInstance.initAll )
        rootFpDcmp  = setMtxDcmp( self.rigInstance.rootInit )
        chestFpDcmp = setMtxDcmp( self.rigInstance.torsoInits[2] )
        neckFpDcmp  = setMtxDcmp( self.rigInstance.headInits[0] )
        
        cmds.connectAttr( allFpDcmp   +'.ot', fp_inWorld +'.t' )
        cmds.connectAttr( allFpDcmp   +'.or', fp_inWorld +'.r' )
        cmds.connectAttr( allFpDcmp   +'.ot', fp_inMove  +'.t' )
        cmds.connectAttr( allFpDcmp   +'.or', fp_inMove  +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inRoot  +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inRoot  +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inFly   +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inFly   +'.r' )
        cmds.connectAttr( chestFpDcmp +'.ot', fp_inChest +'.t' )
        cmds.connectAttr( chestFpDcmp +'.or', fp_inChest +'.r' )
        cmds.connectAttr( neckFpDcmp  +'.ot', fp_inNeck  +'.t' )
        cmds.connectAttr( neckFpDcmp  +'.or', fp_inNeck  +'.r' )
        
        cmds.connectAttr( fp_inWorld  +'.wm', followMtx+'.originalMatrix' )
        
        cmds.parent( fp_inWorld, self.rigInstance.worldCtl )
        cmds.parent( fp_inMove , self.rigInstance.moveCtl )
        cmds.parent( fp_inFly , self.rigInstance.flyCtl )
        cmds.parent( fp_inRoot , self.rigInstance.rootGrp )
        cmds.parent( fp_inChest , self.rigInstance.chestCtl.replace( 'Chest', 'ChestMove' ) )
        cmds.parent( fp_inNeck , self.rigInstance.neckCtl )
        
        cmds.connectAttr( fp_inNeck   +'.wm', followMtx+'.inputMatrix[0]' )
        cmds.connectAttr( fp_inChest  +'.wm', followMtx+'.inputMatrix[1]' )
        cmds.connectAttr( fp_inRoot   +'.wm', followMtx+'.inputMatrix[2]' )
        cmds.connectAttr( fp_inFly    +'.wm', followMtx+'.inputMatrix[3]' )
        cmds.connectAttr( fp_inMove   +'.wm', followMtx+'.inputMatrix[4]' )
        
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Head_Follow_MtxDcmp' )
        cmds.connectAttr( followMtx+'.outputMatrix', mtxDcmp+'.i[0]')
        cmds.connectAttr( self.rigInstance.headCtlGrp+'.pim', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.or', self.rigInstance.headCtlGrp+'.r', f=1 )
        
        cmds.connectAttr( self.rigInstance.headCtl+'.neckFollow' , followMtx+'.inputWeight[0]' )
        cmds.connectAttr( self.rigInstance.headCtl+'.chestFollow', followMtx+'.inputWeight[1]' )
        cmds.connectAttr( self.rigInstance.headCtl+'.rootFollow' , followMtx+'.inputWeight[2]' )
        cmds.connectAttr( self.rigInstance.headCtl+'.flyFollow'  , followMtx+'.inputWeight[3]' )
        cmds.connectAttr( self.rigInstance.headCtl+'.moveFollow' , followMtx+'.inputWeight[4]' )
        
    def eyeFollowSet(self):
        followMtx = cmds.createNode( 'followMatrix', n='Eye_FollowMtx' )
        
        def allMtxDcmp():
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Head_All_F_MtxDcmp' )
            cmds.connectAttr( self.eyeInit +'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( self.rigInstance.initAll+'.wim', mtxDcmp+'.i[1]' )
            return mtxDcmp
                    
        def setMtxDcmp( part ):
            partName = part.replace( '_Init', '' )
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Head_%s_F_MtxDcmp' % partName )
            cmds.connectAttr( self.eyeInit+'.wm', mtxDcmp+'.i[0]' )
            cmds.connectAttr( part+'.wim', mtxDcmp+'.i[1]' )
            return mtxDcmp
        
        fp_inWorld =  cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inWorld' ) )
        fp_inMove =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inMove' ) )
        fp_inFly =    cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inFly' ) )
        fp_inRoot =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inRoot' ) )
        fp_inChest =  cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inChest' ) )
        fp_inHead =   cmds.createNode( 'transform', n=followMtx.replace( 'FollowMtx', 'FP_inHead' ) )
            
        allFpDcmp   = setMtxDcmp( self.rigInstance.initAll )
        rootFpDcmp  = setMtxDcmp( self.rigInstance.rootInit )
        chestFpDcmp = setMtxDcmp( self.rigInstance.torsoInits[2] )
        headFpDcmp  = setMtxDcmp( self.rigInstance.headInits[2] )
        
        cmds.connectAttr( allFpDcmp   +'.ot', fp_inWorld +'.t' )
        cmds.connectAttr( allFpDcmp   +'.or', fp_inWorld +'.r' )
        cmds.connectAttr( allFpDcmp   +'.ot', fp_inMove  +'.t' )
        cmds.connectAttr( allFpDcmp   +'.or', fp_inMove  +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inRoot  +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inRoot  +'.r' )
        cmds.connectAttr( rootFpDcmp  +'.ot', fp_inFly   +'.t' )
        cmds.connectAttr( rootFpDcmp  +'.or', fp_inFly   +'.r' )
        cmds.connectAttr( chestFpDcmp +'.ot', fp_inChest +'.t' )
        cmds.connectAttr( chestFpDcmp +'.or', fp_inChest +'.r' )
        cmds.connectAttr( headFpDcmp  +'.ot', fp_inHead  +'.t' )
        cmds.connectAttr( headFpDcmp  +'.or', fp_inHead  +'.r' )
        
        cmds.parent( fp_inWorld , self.rigInstance.worldCtl )
        cmds.parent( fp_inMove , self.rigInstance.moveCtl )
        cmds.parent( fp_inFly , self.rigInstance.flyCtl )
        cmds.parent( fp_inRoot , self.rigInstance.rootGrp )
        cmds.parent( fp_inChest , self.rigInstance.chestCtl )
        cmds.parent( fp_inHead , self.rigInstance.headCtl )
        
        cmds.connectAttr( fp_inHead  +'.wm', followMtx+'.originalMatrix' )
        cmds.connectAttr( fp_inChest  +'.wm', followMtx+'.inputMatrix[0]' )
        cmds.connectAttr( fp_inRoot   +'.wm', followMtx+'.inputMatrix[1]' )
        cmds.connectAttr( fp_inFly    +'.wm', followMtx+'.inputMatrix[2]' )
        cmds.connectAttr( fp_inMove   +'.wm', followMtx+'.inputMatrix[3]' )
        
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='eye_Follow_MtxDcmp' )
        cmds.connectAttr( followMtx+'.outputMatrix', mtxDcmp+'.i[0]')
        cmds.connectAttr( self.rigInstance.eyeCtlGrp+'.pim', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.ot', self.rigInstance.eyeCtlGrp+'.t', f=1 )
        cmds.connectAttr( mtxDcmp+'.or', self.rigInstance.eyeCtlGrp+'.r', f=1 )
        
        cmds.connectAttr( self.rigInstance.eyeCtl+'.chestFollow', followMtx+'.inputWeight[0]' )
        cmds.connectAttr( self.rigInstance.eyeCtl+'.rootFollow' , followMtx+'.inputWeight[1]' )
        cmds.connectAttr( self.rigInstance.eyeCtl+'.flyFollow'  , followMtx+'.inputWeight[2]' )
        cmds.connectAttr( self.rigInstance.eyeCtl+'.moveFollow' , followMtx+'.inputWeight[3]' )
        
    def allSet(self, jntNum ):
        ctlSet = CtlSet( self.rigInstance )
        ctlSet.allSet()
        curveSet = CurveSet()
        curveSet.create()
        splineSet = SplineSet( jntNum )
        eyeJointSet = EyeJointSet( self.rigInstance )
        self.annotation( 'L' )
        self.annotation( 'R' )
        
        curveSet.connectPoints( ctlSet.pointList )
        splineSet.connectCurve( curveSet.shapeName )
        splineSet.setStartUpObj( ctlSet.startUpObj )
        splineSet.setEndUpObj( ctlSet.endUpObj )
        splineSet.constrainEnd( ctlSet.headCtl )
        
        cmds.parent( splineSet.rjts[0], self.chestJnt )
        cmds.parent( ctlSet.neckCtl.transformGrp, self.chestCtl.replace( 'Chest', 'ChestMove' ) )
        ctlSet.connectInit( self.inits )
        curveSet.parentTo( ctlSet.neckCtl )
        eyeJointSet.parent( splineSet.rjts[-1] )
        eyeJointSet.aimConstraint( ctlSet.eyeLCtl.name, ctlSet.eyeRCtl.name )
        eyeJointSet.connectInit( self.inits[-3], self.inits[-2] )
        
        self.followSet()
        self.eyeFollowSet()
        