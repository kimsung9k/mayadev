import maya.cmds as cmds
import chModules.rigbase as rigbase
import math

class RigAll:
    def __init__(self, rigInstance ):
        self.rootInit = rigInstance.torsoInits[0]
        self.waistInit = rigInstance.torsoInits[1]
        self.chestInit = rigInstance.torsoInits[2]
        self.collarLInit = rigInstance.torsoInits[3]
        self.collarRInit = rigInstance.torsoInits[4]
        self.shoulderLInit = rigInstance.armLInits[0]
        self.shoulderRInit = rigInstance.armRInits[0]
        self.hipLInit = rigInstance.legLInits[0]
        self.hipRInit = rigInstance.legRInits[0]
        self.headInit = rigInstance.headInits[0]
        
        self.rigInstance = rigInstance
        
        self.collarLJnts = []
        self.collarRJnts = []
        
    def controlerSetColor(self):
        rigbase.controlerSetColor( self.rootCtl, 22 )
        rigbase.controlerSetColor( self.flyCtl, 18 )
        rigbase.controlerSetColor( self.hipCtl, 10 )
        rigbase.controlerSetColor( self.torsoCtl, 24 )
        rigbase.controlerSetColor( self.waistCtl, 10 )
        rigbase.controlerSetColor( self.chestCtl, 10 )
        rigbase.controlerSetColor( self.collarLCtl, 13 )
        rigbase.controlerSetColor( self.collarRCtl, 6 )
        rigbase.controlerSetColor( self.shoulderLCtl, 13 )
        rigbase.controlerSetColor( self.shoulderRCtl, 6 )
        rigbase.controlerSetColor( self.chestMoveCtl, 24 )
        
    def controlSet(self):
        self.rootCtl, self.rootCtlGrp = rigbase.putControler( self.rootInit, n= self.rootInit.replace( 'Init', 'CTL' ), typ='box', size=[2.5,.1,2.2] )
        self.flyCtl, self.flyCtlGrp = rigbase.putControler( self.rootCtl, n=self.rootCtl.replace( 'Root', 'Fly' ), typ='fly', size=[1.2,1,1.8], orient=[90,0,0], offset=[0,0.2,-2.6] )
        self.hipCtl , self.hipCtlGrp = rigbase.putControler( self.rootCtl,  n= self.rootCtl.replace( 'Root', 'Hip' ), typ='quadrangle', size=[1.5,1.5,1.5], orient=[0,45,0] )
        self.torsoCtl , self.torsoCtlGrp = rigbase.putControler( self.rootCtl,  n= self.rootCtl.replace( 'Root', 'TorsoRotate' ), typ='bar', size=[1.5,.7,.7], orient=[90,0,0] )
        self.waistCtl, self.waistCtlGrp = rigbase.putControler( self.waistInit, n= self.waistInit.replace( 'Init', 'CTL' ), normal=[0,1,0], r=1.5 )
        self.chestCtl, self.chestCtlGrp = rigbase.putControler( self.chestInit, n= self.chestInit.replace( 'Init', 'CTL' ), typ='box', size=[1.5,.3,1.5] )
        self.chestMoveCtl, self.chestMoveCtlGrp = rigbase.putControler( self.chestInit, n= self.chestCtl.replace( 'Chest_CTL', 'ChestMove_CTL' ), normal=[0,0,1], center=[0,0,2.5], r=.5 )
        self.collarLCtl, self.collarLCtlGrp = rigbase.putControler( self.collarLInit, n=self.collarLInit.replace( 'Init', 'CTL' ), normal=[1,0,0], r=1 )
        self.collarRCtl, self.collarRCtlGrp = rigbase.putControler( self.collarRInit, n=self.collarRInit.replace( 'Init', 'CTL' ), normal=[1,0,0], r=1 )
        self.shoulderLCtl, self.shoulderLCtlGrp = rigbase.putControler( self.shoulderLInit, n=self.shoulderLInit.replace( 'Init', 'CTL' ), typ='pin', orient=[0,0,-30], size=[.6,.6,.6] )
        self.shoulderRCtl, self.shoulderRCtlGrp = rigbase.putControler( self.shoulderRInit, n=self.shoulderRInit.replace( 'Init', 'CTL' ), typ='pin', orient=[0,0,-30], size=[-.6,-.6,-.6] )
        
        self.rootGrp = cmds.createNode( 'transform', n='Root_GRP' )
        rigbase.constraint( self.rootCtl, self.rootGrp, s=1, sh=1 )
        torsoGrp = cmds.createNode( 'transform', n= 'torso_GRP' )
        #waistCtlPointObj = cmds.createNode( 'transform', n=self.waistInit.replace( 'Init', 'CtlPoint' ) )
        
        rigbase.AttrEdit( torsoGrp, self.torsoCtl ).lockAndHideAttrs( 'tx', 'ty','tz', 'sx', 'sy','sz', 'v' )
        rigbase.AttrEdit( self.flyCtl, self.rootCtl, self.hipCtl, self.waistCtl, self.chestCtl, self.chestMoveCtl, self.collarLCtl, self.collarRCtl ).lockAndHideAttrs( 'sx', 'sy','sz','v' )
        rigbase.AttrEdit( self.shoulderLCtl, self.shoulderRCtl ).lockAndHideAttrs( 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v' )
        
        cmds.parent( self.shoulderLCtlGrp, self.collarLCtl )
        cmds.parent( self.shoulderRCtlGrp, self.collarRCtl )
        cmds.parent( self.collarLCtlGrp , self.collarRCtlGrp, self.chestMoveCtl )
        cmds.parent( self.chestMoveCtlGrp, self.chestCtl )
        cmds.parent( self.chestCtlGrp, self.torsoCtl )
        cmds.parent(  self.waistCtlGrp, torsoGrp )
        cmds.parent( torsoGrp, self.torsoCtlGrp, self.hipCtlGrp, self.rootGrp )
        
        cmds.setAttr( self.shoulderLCtlGrp+'.r', 0,0,0 )
        cmds.setAttr( self.shoulderRCtlGrp+'.r', 0,0,0 )
        
        rigbase.connectSameAttr( self.rootInit, self.flyCtlGrp ).doIt( 't', 'r' )
        rigbase.connectSameAttr( self.torsoCtl, torsoGrp ).doIt( 'r' )
        #rigbase.connectSameAttr( self.waistInit, waistCtlPointObj ).doIt( 't' )
        #rigbase.connectSameAttr( self.waistInit, self.waistCtlGrp ).doIt( 't', 'r' )
        #rigbase.connectSameAttr( self.chestInit, self.chestCtlGrp ).doIt( 't', 'r' )
        rigbase.connectSameAttr( self.collarLInit, self.collarLCtlGrp ).doIt( 't', 'r' )
        rigbase.connectSameAttr( self.collarRInit, self.collarRCtlGrp ).doIt( 't', 'r' )
        rigbase.connectSameAttr( self.shoulderLInit, self.shoulderLCtlGrp ).doIt( 't' )
        rigbase.connectSameAttr( self.shoulderRInit, self.shoulderRCtlGrp ).doIt( 't' )
        
        #rigbase.constraint( self.waistCtl, waistCtlPointObj, t=0 )
        
        rigbase.followAdd( self.flyCtl, self.rootCtlGrp )
        
        cmds.parent( self.rootCtlGrp, self.flyCtlGrp, self.rigInstance.moveCtl )
        cmds.parent( self.rootGrp, self.rigInstance.worldCtl )
        
        self.rigInstance.collarLCtl = self.collarLCtl
        self.rigInstance.collarRCtl = self.collarRCtl
        self.rigInstance.chestCtl   = self.chestCtl
        self.rigInstance.chestMoveCtl   = self.chestMoveCtl
        self.rigInstance.waistCtl   = self.waistCtl
        self.rigInstance.torsoCtl    = self.torsoCtl
        self.rigInstance.hipCtl     = self.hipCtl
        self.rigInstance.flyCtl     = self.flyCtl
        self.rigInstance.rootCtl    = self.rootCtl
        self.rigInstance.rootGrp    = self.rootGrp
        
    def curveSet(self):
        #self.crv = cmds.curve( n='Torso_Spline_CRV', d=3, p=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]] )
        self.initCrv = cmds.curve( n='Torso_SplineInit_CRV', d=3, p=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]] )
        
        #cmds.setAttr( self.crv+'.v', 0 )
        cmds.setAttr( self.initCrv+'.v', 0 )
        
        #self.crvShape = cmds.listRelatives( self.crv, s=1 )[0]
        self.initCrvShape = cmds.listRelatives( self.initCrv, s=1 )[0]
        
        self.crvPoint0Obj = self.hipCtl
        self.crvPoint1Obj = cmds.createNode( 'transform', n= 'Torso_Spline_point1' )
        self.crvPoint2Obj = cmds.createNode( 'transform', n= 'Torso_Spline_point2' )
        self.crvPoint3Obj = self.chestCtl
        
        self.crvOrigPoint0Obj = self.torsoCtl
        self.crvOrigWaistObj = cmds.createNode( 'transform', n= 'Waist_CTL_SqPos' )
        self.crvOrigPoint1Obj = cmds.createNode( 'transform', n= 'Torso_Spline_SquPoint1' )
        self.crvOrigPoint2Obj = cmds.createNode( 'transform', n= 'Torso_Spline_SquPoint2' )
        self.crvOrigPoint3Obj = cmds.createNode( 'transform', n= 'Chest_CTL_SquPos' )
        
        rigbase.AttrEdit( self.crvPoint1Obj, self.crvPoint2Obj ).lockAndHideAttrs( 'tx', 'tz', 'rx', 'ry','rz', 'sx', 'sy','sz', 'v' )
        cmds.parent( self.crvPoint1Obj, self.crvPoint2Obj, self.waistCtl )
        
        cmds.parent( self.crvOrigWaistObj, self.crvOrigPoint3Obj, self.rootGrp )
        cmds.parent( self.crvOrigPoint1Obj, self.crvOrigPoint2Obj, self.crvOrigWaistObj )
        self.crvOrigSqPointGrp = cmds.group( self.crvOrigPoint1Obj, self.crvOrigPoint2Obj, n='Waist_CTL_SqSqPointGrp' )
        cmds.xform( self.crvOrigSqPointGrp, piv=[0,0,0], os=1 )
        
        rigbase.pInvRotConst( self.crvOrigSqPointGrp )
        
        rigbase.connectSameAttr( self.waistInit, self.crvOrigWaistObj ).doIt( 't','r' )
        chMtxDcmp = rigbase.getChildMtxDcmp( self.chestInit, self.rootInit )
        cmds.connectAttr( chMtxDcmp+'.ot', self.crvOrigPoint3Obj+'.t' )
        cmds.connectAttr( chMtxDcmp+'.or', self.crvOrigPoint3Obj+'.r' )
        #rigbase.connectSameAttr( self.chestCtlGrp, self.crvOrigPoint3Obj ).doIt( 't', 'r' )
        #rigbase.connectSameAttr( self.crvPoint1Obj, self.crvOrigPoint1Obj ).doIt( 't','r' )
        #rigbase.connectSameAttr( self.crvPoint2Obj, self.crvOrigPoint2Obj ).doIt( 't','r' )
        
        multPoint1Node = cmds.createNode( 'multDoubleLinear', n='Torso_Spline_point1_mult' )
        multPoint2Node = cmds.createNode( 'multDoubleLinear', n='Torso_Spline_point2_mult' )
        distPoint1Node = cmds.createNode( 'distanceBetween', n='Torso_spline_point1_dist' )
        distPoint2Node = cmds.createNode( 'distanceBetween', n='Torso_spline_point2_dist' )
        
        cmds.connectAttr( self.waistInit+'.t', distPoint1Node+'.point1' )
        cmds.connectAttr( self.chestInit+'.t', distPoint2Node+'.point2' )
        cmds.connectAttr( distPoint1Node+'.distance', multPoint1Node+'.input1' )
        cmds.connectAttr( distPoint2Node+'.distance', multPoint2Node+'.input1' )
        #cmds.connectAttr( multPoint1Node+'.output', self.crvPoint1Obj+'.ty' )
        #cmds.connectAttr( multPoint2Node+'.output', self.crvPoint2Obj+'.ty' )
        cmds.connectAttr( multPoint1Node+'.output', self.crvOrigPoint1Obj+'.ty' )
        cmds.connectAttr( multPoint2Node+'.output', self.crvOrigPoint2Obj+'.ty' )
        
        cmds.setAttr( multPoint1Node+'.input2', -.4 )
        cmds.setAttr( multPoint2Node+'.input2', .4 )
        
        '''
        for i in range( 4 ):
            dcmp = cmds.createNode( 'decomposeMatrix', n= self.crv+'_point%d_dcmp' % i )
            exec( 'cmds.connectAttr( self.crvPoint%dObj+".wm", dcmp+".imat" )' % i )
            cmds.connectAttr( dcmp+".ot", self.crvShape+'.controlPoints[%d]' %i )'''
            
        for i in range( 4 ):
            dcmp = cmds.createNode( 'multMatrixDecompose', n= self.initCrv+'_origPoint%d_dcmp' % i )
            exec( 'cmds.connectAttr( self.crvOrigPoint%dObj+".wm", dcmp+".i[0]" )' % i )
            cmds.connectAttr( self.initCrv+".wim", dcmp+".i[1]" )
            cmds.connectAttr( dcmp+".ot", self.initCrvShape+'.controlPoints[%d]' %i )
        
        rigbase.transformDefault( self.initCrv )
        
        #rigbase.connectSameAttr( self.crv, self.initCrv ).doIt( 't', 'r', 's', 'sh' )
        
        cmds.parent( self.initCrv, self.rootGrp )
        
    def _splineJointUpObjectSet(self):
        self.startUp = cmds.createNode( 'transform', n='Torso_Spline_startUp' )
        self.endUp   = cmds.createNode( 'transform', n='Torso_Spline_endUp' )
        rigbase.AttrEdit( self.startUp, self.endUp ).lockAndHideAttrs( 'tx', 'ty','tz', 'sx', 'sy','sz', 'v' )
        cmds.parent( self.endUp,  self.chestMoveCtl )
        cmds.parent( self.startUp,  self.hipCtl )
        
        chestDcmp = rigbase.getChildMtxDcmp( self.waistCtl, self.chestMoveCtl )
        hipDcmp   = rigbase.getChildMtxDcmp( self.waistCtl, self.hipCtl   )
        ffmChest  = cmds.createNode( 'fourByFourMatrix', n= self.chestMoveCtl+'_childPosFFM' )
        ffmHip    = cmds.createNode( 'fourByFourMatrix', n= self.hipCtl  +'_childPosFFM' )
        smorChest = cmds.createNode( 'smartOrient', n=self.chestMoveCtl +'_childPosSmtOri' )
        smorHip   = cmds.createNode( 'smartOrient', n=self.hipCtl   +'_childPosSmtOri' )
        
        cmds.setAttr( chestDcmp +'.invt', 1 )
        cmds.setAttr( smorChest+'.aimAxis', 1 )
        cmds.setAttr( smorHip  +'.aimAxis', 1 )
        
        cmds.connectAttr( chestDcmp+'.otx', ffmChest+'.i10' )
        cmds.connectAttr( chestDcmp+'.oty', ffmChest+'.i11' )
        cmds.connectAttr( chestDcmp+'.otz', ffmChest+'.i12' )
        cmds.connectAttr( hipDcmp+  '.otx', ffmHip+  '.i10' )
        cmds.connectAttr( hipDcmp+  '.oty', ffmHip+  '.i11' )
        cmds.connectAttr( hipDcmp+  '.otz', ffmHip+  '.i12' )
        cmds.connectAttr( ffmChest+'.output', smorChest+'.inputMatrix' )
        cmds.connectAttr( ffmHip  +'.output', smorHip  +'.inputMatrix' )
        cmds.connectAttr( smorChest+'.oa', self.endUp    +'.r' )
        cmds.connectAttr( smorHip  +'.oa', self.startUp  +'.r' )
        
    def splineJointSet( self, splineNumber ):
        self.splineJnts = []
        cmds.select( d=1 )
        
        self._splineJointUpObjectSet()
                                        
        spci = cmds.createNode( 'splineCurveInfo', n= self.initCrv+'_Spci'  )
        cmds.connectAttr( self.initCrvShape+'.local', spci+'.inputCurve' )
        #cmds.connectAttr( self.startUp+'.wm', spci+'.startTransform' )
        #cmds.connectAttr( self.endUp  +'.wm', spci+'.endTransform'   )
        
        cmds.setAttr( spci+'.startUpAxis', 2 )
        cmds.setAttr( spci+'.endUpAxis', 2 )
        cmds.setAttr( spci+'.targetAimAxis', 1 )
        cmds.setAttr( spci+'.targetUpAxis', 2 )
        
        for i in range( splineNumber ):
            self.splineJnts.append( cmds.joint( n='Spline%d_RJT' % i, radius=1.5 ) )
        
        pointObjs = []
        for i in range( 0, splineNumber ):
            pr = float(i)/(splineNumber-1)
            
            pointObj = cmds.createNode( 'transform', n='Spline%d_SplinePoint' % i )
            pointObjs.append( pointObj )
            
            cmds.addAttr( self.splineJnts[i], ln='parameter', min=0, max=1, dv=pr )
            cmds.setAttr( self.splineJnts[i]+'.parameter', e=1, k=1 )
            
            cmds.connectAttr( self.splineJnts[i]+'.parameter', spci+'.pr[%d]' % i )
            cmds.connectAttr( spci+'.o[%d].p' % i, pointObj+'.t' )
            cmds.connectAttr( spci+'.o[%d].r' % i, pointObj+'.r' )
            cmds.parent( pointObj, self.initCrv )
            
            rigbase.constraint( pointObj, self.splineJnts[i] )
            
        pointHObjs = []
        cmds.select( self.torsoCtl )
        for i in range( 0, splineNumber ):
            pointHObjs.append( cmds.joint( n=pointObjs[i].replace( 'SplinePoint', 'SplineHJnt' ) ) )
            mtxDcmp = rigbase.constraint( pointObjs[i], pointHObjs[i], r=0 )
            cmds.connectAttr( mtxDcmp+'.or', pointHObjs[i]+'.jo' )
            if i == 0:
                cmds.connectAttr( self.rootGrp+'.wim', mtxDcmp+'.i[1]', f=1 )
            else:
                cmds.connectAttr( pointObjs[i-1]+'.wim', mtxDcmp+'.i[1]', f=1 )
            cmds.select( pointHObjs[i] )
        cmds.setAttr( pointHObjs[0]+'.v', 0 )
        rigbase.constraint( pointHObjs[-1], self.chestCtlGrp, r=0 )
            
        epBindNode = cmds.createNode( 'epBindNode', n='Torso_epBindNode' )
        initEpBindNode = cmds.createNode( 'epBindNode', n='TorsoInit_epBindNode' )
        chestOrPointer = cmds.createNode( 'transform', n='Chest_OrPointer' )
        hipCuPointer = cmds.createNode( 'transform', n='Hip_CuPointer' )
        
        cmds.parent( chestOrPointer, self.chestCtlGrp )
        cmds.parent( hipCuPointer, self.hipCtlGrp )
        
        rigbase.transformDefault( chestOrPointer )
        
        cmds.connectAttr( self.chestCtl+'.r', chestOrPointer+'.r' )
        cmds.connectAttr( self.hipCtl+'.t', hipCuPointer+'.t' )
        
        cmds.connectAttr( self.hipCtlGrp+'.wm', epBindNode+'.om[0]' )
        cmds.connectAttr( chestOrPointer+'.wm', epBindNode+'.om[1]')
        cmds.connectAttr( hipCuPointer+'.wm', epBindNode+'.m[0]' )
        cmds.connectAttr( self.chestCtl+'.wm', epBindNode+'.m[1]' )
        
        for i in range( splineNumber ):
            dcmp = cmds.createNode( 'decomposeMatrix' , n=pointHObjs[i]+'_dcmp' )
            cmds.connectAttr( pointHObjs[i]+'.wm', dcmp+'.imat' )
            cmds.connectAttr( dcmp+'.ot', epBindNode+'.ip[%d]' % i )
            cmds.connectAttr( dcmp+'.ot', initEpBindNode+'.ip[%d]' % i )
        
        smOri = cmds.createNode( 'smartOrient', n='Torso_Spline_SmOri' )
        cmds.connectAttr( self.chestCtl+'.m', smOri+'.inputMatrix' )
        cmds.setAttr( smOri+'.aimAxis', 1 )
        for i in range( 1, splineNumber-1 ):
            cmds.addAttr( self.chestCtl, ln='rotRate%d' % i, min=0, max=1, dv=.333 )
            splineOrientMult = cmds.createNode( 'multiplyDivide', n='Torso_Spline_OrientMult%d' % i )
            cmds.connectAttr( smOri+'.outAngle', splineOrientMult+'.input1' )
            cmds.connectAttr( self.chestCtl+'.rotRate%d' % i, splineOrientMult+'.input2X' )
            cmds.connectAttr( self.chestCtl+'.rotRate%d' % i, splineOrientMult+'.input2Y' )
            cmds.connectAttr( self.chestCtl+'.rotRate%d' % i, splineOrientMult+'.input2Z' ) 
            cmds.connectAttr( splineOrientMult+'.output',  pointHObjs[i]+'.r' )
        
        '''
        firstCrv = cmds.circle( ch=0, n='Torso_FristCrv' )[0]
        firstCrvShape = cmds.listRelatives( firstCrv, s=1 )[0]
        cmds.connectAttr( epBindNode+'.outputCurve', firstCrvShape+'.create' )
        cmds.parent( firstCrv, self.rootGrp )
        firstCrv_dcmp = cmds.createNode( 'decomposeMatrix', n='Torso_firstCrv_invDcmp' )
        cmds.connectAttr( firstCrv+'.pim', firstCrv_dcmp+'.imat' )
        cmds.connectAttr( firstCrv_dcmp+'.ot', firstCrv+'.t' )
        cmds.connectAttr( firstCrv_dcmp+'.or', firstCrv+'.r' )
        cmds.connectAttr( firstCrv_dcmp+'.os', firstCrv+'.s' )
        cmds.connectAttr( firstCrv_dcmp+'.osh', firstCrv+'.sh' )'''
        
        def curveBasedCtlGrp( outputCurveAttr, ctlGrp, prRate=0.5 ):
            posInfo = cmds.createNode( 'pointOnCurveInfo', n='Waist_Ct;PoseInfo' )
            fbf = cmds.createNode( 'fourByFourMatrix', n='Waist_CtlFBF' )
            smOri = cmds.createNode( 'smartOrient', n='Waist_CtlSmOri' )
            compose = cmds.createNode( 'composeMatrix', n='Waist_CtlComp' )
            mtxDcmp = cmds.createNode( 'multMatrixDecompose', n='Waist_CtlMtxDcmp' )
            
            cmds.setAttr( posInfo+'.top', 1 )
            cmds.setAttr( posInfo+'.parameter', prRate )
            cmds.setAttr( smOri+'.aimAxis', 1 )
            
            cmds.connectAttr( outputCurveAttr, posInfo+'.inputCurve' )
            cmds.connectAttr( posInfo+'.tangentX', fbf+'.in10' )
            cmds.connectAttr( posInfo+'.tangentY', fbf+'.in11' )
            cmds.connectAttr( posInfo+'.tangentZ', fbf+'.in12' )
            cmds.connectAttr( fbf+'.output', smOri+'.inputMatrix' )
            cmds.connectAttr( posInfo+'.position', compose+'.it' )
            cmds.connectAttr( smOri+'.outAngle', compose+'.ir')
            cmds.connectAttr( compose+'.outputMatrix', mtxDcmp+'.i[0]' )
            cmds.connectAttr( ctlGrp+'.pim', mtxDcmp+'.i[1]' )
            cmds.connectAttr( mtxDcmp+'.ot', ctlGrp+'.t' )
            cmds.connectAttr( mtxDcmp+'.or', ctlGrp+'.r' )
        
        curveBasedCtlGrp( epBindNode+'.outputCurve', self.waistCtlGrp, prRate=0.5 )
        
        chestCuPointer = cmds.createNode( 'transform', n='ChestCuPointer' )
        cmds.parent( chestCuPointer, self.chestMoveCtlGrp )
        
        cmds.connectAttr( self.chestMoveCtl+'.t', chestCuPointer+'.t' )
        rigbase.transformDefault( chestCuPointer )
        
        epBindNode2 = cmds.createNode( 'epBindNode', n='Torso_epBindNode2' )
        
        for i in range( splineNumber ):
            cmds.connectAttr( epBindNode+'.op[%d]' % i, epBindNode2+'.ip[%d]' % i )
            
        waistOrientObj = cmds.createNode( 'transform', n='WaistOrient_OBJ' )
        cmds.parent( waistOrientObj, self.waistCtlGrp )
        rigbase.transformDefault( waistOrientObj )
        waistSmOrient = cmds.createNode( 'smartOrient', n='WaistOrient_ObjSmOrient' )
        cmds.connectAttr( self.waistCtl+'.m', waistSmOrient+'.inputMatrix' )
        cmds.setAttr( waistSmOrient+'.aimAxis', 1 )
        cmds.connectAttr( waistSmOrient+'.outAngle', waistOrientObj+'.r' )
        cmds.connectAttr( self.waistCtl+'.t', waistOrientObj+'.t' )
        
        cmds.connectAttr( hipCuPointer+'.wm', epBindNode2+'.m[0]' )
        cmds.connectAttr( hipCuPointer+'.wm', epBindNode2+'.om[0]' )
        cmds.connectAttr( waistOrientObj+'.wm', epBindNode2+'.m[1]' )
        cmds.connectAttr( self.waistCtlGrp+'.wm', epBindNode2+'.om[1]' )
        cmds.connectAttr( chestCuPointer+'.wm', epBindNode2+'.m[2]' )
        cmds.connectAttr( self.chestMoveCtlGrp+'.wm', epBindNode2+'.om[2]' )
        
        cuSpInfo = cmds.createNode( 'splineCurveInfo' , n='Torso_CurrentSplineInfo' )
        
        cmds.setAttr( cuSpInfo+'.paramFromLength', 0 )
        cmds.setAttr( cuSpInfo+'.startUpAxis', 2 )
        cmds.setAttr( cuSpInfo+'.endUpAxis', 2 )
        cmds.setAttr( cuSpInfo+'.targetAimAxis', 1 )
        cmds.setAttr( cuSpInfo+'.targetUpAxis', 2 )
        
        putCtls = []
        
        rigbase.addHelpTx( self.waistCtl, 'Itp CTL Vis' )
        rigbase.AttrEdit( self.waistCtl ).addAttr( ln='show', cb=1, min=0, max=1, at='long' )
        
        for i in range( 1, splineNumber-1 ):
            putCtl, putCtlGrp = rigbase.putControler( self.waistCtl, n='WaistItp%d_CTL' % i, normal=[0,1,0] )
            rigbase.AttrEdit( putCtl ).lockAndHideAttrs( 'sx', 'sy', 'sz' ,'v' )
            curveBasedCtlGrp( epBindNode2+'.outputCurve', putCtlGrp, i/( splineNumber-1.0 ) )
            cmds.connectAttr( self.waistCtl+'.show', putCtlGrp+'.v' )
            putCtls.append( [putCtl, putCtlGrp] )
            cmds.parent( putCtlGrp, self.rootGrp )
            
        epBindNode3 = cmds.createNode( 'epBindNode', n='Torso_epBindNode3' )
        
        for i in range( splineNumber ):
            cmds.connectAttr( epBindNode2+'.op[%d]' % i, epBindNode3+'.ip[%d]' % i )
            
        cmds.connectAttr( hipCuPointer+'.wm', epBindNode3+'.m[0]' )
        cmds.connectAttr( hipCuPointer+'.wm', epBindNode3+'.om[0]' )
        for i in range( 1, splineNumber-1 ):
            cmds.connectAttr( putCtls[i-1][0]+'.wm', epBindNode3+'.m[%d]' % i )
            cmds.connectAttr( putCtls[i-1][1]+'.wm', epBindNode3+'.om[%d]' % i )
        cmds.connectAttr( chestCuPointer+'.wm', epBindNode3+'.m[%d]' % (splineNumber-1) )
        cmds.connectAttr( self.chestMoveCtlGrp+'.wm', epBindNode3+'.om[%d]' % (splineNumber-1) )
        
        cuSpInfo = cmds.createNode( 'splineCurveInfo' , n='Torso_CurrentSplineInfo' )
        
        cmds.setAttr( cuSpInfo+'.paramFromLength', 0 )
        cmds.setAttr( cuSpInfo+'.startUpAxis', 2 )
        cmds.setAttr( cuSpInfo+'.endUpAxis', 2 )
        cmds.setAttr( cuSpInfo+'.targetAimAxis', 1 )
        cmds.setAttr( cuSpInfo+'.targetUpAxis', 2 )
        
        cmds.connectAttr( epBindNode3+'.outputCurve', cuSpInfo+'.inputCurve' )
        cmds.connectAttr( self.startUp+'.wm', cuSpInfo+'.startTransform' )
        cmds.connectAttr( self.endUp+'.wm', cuSpInfo+'.endTransform' )
        
        cuSpGrp = cmds.createNode( 'transform', n='Torso_Spline_GRP' )
        splinePtrs = []
        for i in range( splineNumber ):
            splineInfoPtr = cmds.createNode( 'transform', n='Torso%d_SplinePoint' % i )
            splinePtrs.append( splineInfoPtr )
            cmds.setAttr( cuSpInfo+'.parameter[%d]' % i, i/( splineNumber-1.0 )+0.001 )
            cmds.connectAttr( cuSpInfo+'.output[%d].position' % i, splineInfoPtr+'.t' )
            cmds.connectAttr( cuSpInfo+'.output[%d].rotate' % i, splineInfoPtr+'.r' )    
        
        cmds.parent( splinePtrs, cuSpGrp )
        
        cmds.parent( cuSpGrp, self.rootCtlGrp )
        splinePtrsInvDcmp = cmds.createNode( 'decomposeMatrix', n='Torso_SplinePtrsInvDcmp' )
        cmds.connectAttr( self.rootCtlGrp+'.wim', splinePtrsInvDcmp+'.imat' )
        cmds.connectAttr( splinePtrsInvDcmp+'.ot', cuSpGrp+'.t' )
        cmds.connectAttr( splinePtrsInvDcmp+'.or', cuSpGrp+'.r' )
        cmds.connectAttr( splinePtrsInvDcmp+'.os', cuSpGrp+'.s' )
        cmds.connectAttr( splinePtrsInvDcmp+'.osh', cuSpGrp+'.sh' )
        
        allWristAngle = cmds.createNode( 'wristAngle', n='Torso_TwistAllAngle' )
        cmds.setAttr( allWristAngle+'.axis', 1 )
        cmds.connectAttr( self.waistCtl+'.wm', allWristAngle+'.inputMatrix' )
        for i in range( 1, splineNumber-1 ):
            
            floatValue = i/(splineNumber-1.0)
            weightValue = 1-math.fabs( 0.5-floatValue )/.5
            
            cmds.addAttr( self.waistCtl, ln='multWeight%d' % i, min=0, max=1, dv=weightValue )
            
            cuSplinePtr = cmds.createNode( 'transform', n='Torso_cuSplinePtr%d' % i )
            cmds.parent( cuSplinePtr, splinePtrs[i] )
            rigbase.transformDefault( cuSplinePtr )
            rigbase.constraint( cuSplinePtr, self.splineJnts[i] )
            
            twistMultNode = cmds.createNode( 'multDoubleLinear', n='Torso_TwistMult%d' % i )
            addTwist = cmds.createNode( 'addDoubleLinear', n='Torso_TwistAdd%d' % i )
            wristAngle = cmds.createNode( 'wristAngle', n='Torso_TwistAngle%d' % i )
            cmds.setAttr( wristAngle+'.axis', 1 )
            
            cmds.connectAttr( putCtls[i-1][0]+'.m', wristAngle+'.inputMatrix' )
            cmds.connectAttr( wristAngle+'.outAngle', addTwist+'.input1' )
            
            cmds.connectAttr( allWristAngle+'.outAngle', twistMultNode+'.input1' )
            cmds.connectAttr( self.waistCtl+'.multWeight%d' % i, twistMultNode+'.input2' )
            
            cmds.connectAttr( twistMultNode+'.output', addTwist+'.input2' )
            
            cmds.connectAttr( addTwist+'.output', cuSplinePtr+'.ry' )
            
        rigbase.constraint( self.hipCtl, self.splineJnts[0] )
        rigbase.constraint( self.chestMoveCtl, self.splineJnts[-1] )
        
        cmds.parent( self.splineJnts[0], self.rootGrp )
        
        self.epBindNode_before = initEpBindNode
        self.epBindNode_after = epBindNode3
        
    def splineSquashSet(self):
        crvInfo = cmds.createNode( 'curveInfo', n=self.epBindNode_after+'_info' )
        initCrvInfo = cmds.createNode( 'curveInfo', n=self.epBindNode_before+'_info' )
        
        cmds.connectAttr( self.epBindNode_after+'.outputCurve', crvInfo+'.inputCurve' )
        cmds.connectAttr( self.epBindNode_before+'.outputCurve', initCrvInfo+'.inputCurve' )
        
        squashNode = cmds.createNode( 'squash', n='Torso_squash' )
        cmds.connectAttr( initCrvInfo+'.arcLength', squashNode+'.lengthOriginal' )
        cmds.connectAttr( crvInfo+'.arcLength', squashNode+'.lengthModify' )
        
        rigbase.addHelpTx( self.chestCtl, 'Squash' )
        attrEdit = rigbase.AttrEdit( self.chestCtl )
        attrEdit.addAttr( ln='squash', min=-1, max=1, k=1 )
        attrEdit.addAttr( ln='forceScale', k=1 )
        
        cmds.connectAttr( self.chestCtl+'.squash', squashNode+'.squashRate' )
        cmds.connectAttr( self.chestCtl+'.forceScale', squashNode+'.forceValue' )
        
        for splineJnt in self.splineJnts[1:-1]:
            cmds.connectAttr( squashNode+'.output', splineJnt+'.sx' )
            cmds.connectAttr( squashNode+'.output', splineJnt+'.sy' )
            cmds.connectAttr( squashNode+'.output', splineJnt+'.sz' )
            
    def twistAttrSet(self, side ):
        if side == 'L':
            targetCtl = self.shoulderLCtl
        elif side == 'R':
            targetCtl = self.shoulderRCtl
        
        rigbase.addHelpTx( targetCtl, 'Twist' )
        attrEdit = rigbase.AttrEdit( targetCtl )
        attrEdit.addAttr( ln='twistCollar', k=1 )
        attrEdit.addAttr( ln='twistShoulder', k=1 )
        
    def collarJointSet( self, jntNum, side ):
        if side == 'L':
            inverse = False
            si = 0
        elif side == 'R':
            inverse = True
            si = 1
            
        shoulderCtlList = [self.shoulderLCtl,self.shoulderRCtl]
        collarCtlList = [self.collarLCtl, self.collarRCtl]
        collarJntList = [self.collarLJnts, self.collarRJnts ]
            
        aimObject = rigbase.makeAimObject( shoulderCtlList[si], collarCtlList[si], inverseAim = inverse )[0]
        aimObject = cmds.rename( aimObject, "Shoulder_%s_CTL_AimObj" % side )
        mtxDcmp = rigbase.getChildMtxDcmp( shoulderCtlList[si], aimObject )
            
        cmds.setAttr( mtxDcmp+'.inverseDistance', inverse )
        
        distSep = cmds.createNode( 'distanceSeparator', n='Collar_%s_DistSep' % side )
        cmds.connectAttr( mtxDcmp+'.outputDistance', distSep+'.inputDistance' )
        
        cmds.select( self.splineJnts[-1] )
        
        collarJntList[si].append( cmds.joint( n='Collar0_%s_RJT' % side, radius=1.5 ) )
        rigbase.constraint( aimObject, collarJntList[si][0] )
        
        twistMult = cmds.createNode( 'multDoubleLinear', n='Collar_%s_twistMult' % side )
        cmds.setAttr( twistMult+'.input2', 1.0/(len( collarJntList )-1) )
        cmds.connectAttr( shoulderCtlList[si]+'.twistCollar', twistMult+'.input1' )
        
        cmds.select( collarJntList[si][0] )
        for i in range( jntNum-1 ):
            prValue = float(i+1)/jntNum
            jnt = cmds.joint( n='Collar%d_%s_RJT' %( i+1, side ), radius=1.5 )
            collarJntList[si].append( jnt )
            
            cmds.addAttr( jnt, ln='parameter', min=0, max=1, dv=prValue )
            cmds.setAttr( jnt+'.parameter', e=1, k=1 )
            
            cmds.connectAttr( jnt+'.parameter', distSep+'.pr[%d]' % (i+1) )
            cmds.connectAttr( distSep+'.sd[%d]' % (i+1), jnt+'.tx', f=1 )
            
            cmds.connectAttr( twistMult+'.output', jnt+'.rx' )
            
    def collarConstSet(self, side ):
        si = 0
        if side == 'R':
            si = 1
        
        shoulderInitList = [self.shoulderLInit, self.shoulderRInit ]
        shoulderCtlList = [self.shoulderLCtl,self.shoulderRCtl]
        collarCtlList = [self.collarLCtl, self.collarRCtl]
        
        const    = cmds.createNode( 'transform', n='Shoulder_%s_Const'          % side )
        inCollar = cmds.createNode( 'transform', n='Shoulder_%s_Const_inCollar' % side )
        inChest  = cmds.createNode( 'transform', n='Shoulder_%s_Const_inChest'  % side )
        inRoot   = cmds.createNode( 'transform', n='Shoulder_%s_Const_inRoot'   % side )
        inFly    = cmds.createNode( 'transform', n='Shoulder_%s_Const_inFly'    % side )
        inMove    = cmds.createNode( 'transform', n='Shoulder_%s_Const_inMove'   % side )
        
        cmds.parent( const   , shoulderCtlList[si] )
        cmds.parent( inCollar, collarCtlList[si]   )
        cmds.parent( inChest , self.chestCtl.replace( 'Chest', 'ChestMove' ) )
        cmds.parent( inRoot  , self.rootGrp  )
        cmds.parent( inFly   , self.rootCtlGrp )
        cmds.parent( inMove  , self.rigInstance.moveCtl )
        
        rigbase.transformDefault( const )#; cmds.setAttr( const+'.dla', 1 )
        rigbase.connectSameAttr( shoulderInitList[si], inCollar ).doIt( 't', 'r' )
        chestDcmp = rigbase.getChildMtxDcmp( shoulderInitList[si], self.chestInit )
        cmds.connectAttr( chestDcmp+'.ot', inChest+'.t' )
        cmds.connectAttr( chestDcmp+'.or', inChest+'.r' )
        rootDcmp = rigbase.getChildMtxDcmp( shoulderInitList[si], self.rootInit )
        cmds.connectAttr( rootDcmp+'.ot', inRoot+'.t' )
        cmds.connectAttr( rootDcmp+'.or', inRoot+'.r' )
        cmds.connectAttr( rootDcmp+'.ot', inFly+'.t' )
        cmds.connectAttr( rootDcmp+'.or', inFly+'.r' )
        cmds.connectAttr( rootDcmp+'.ot', inMove+'.t' )
        cmds.connectAttr( rootDcmp+'.or', inMove+'.r' )
        
        followMtx = cmds.createNode( 'followMatrix', n='Shoulder_%s_ConstFollow' % side )
        mtxDcmp   = cmds.createNode( 'multMatrixDecompose', n='Shoulder_%s_ConstMtxDcmp' % side )
        
        cmds.connectAttr( inCollar+'.wm', followMtx+'.originalMatrix' )
        cmds.connectAttr( inChest +'.wm', followMtx+'.inputMatrix[0]' )
        cmds.connectAttr( inRoot  +'.wm', followMtx+'.inputMatrix[1]' )
        cmds.connectAttr( inFly   +'.wm', followMtx+'.inputMatrix[2]' )
        cmds.connectAttr( inMove  +'.wm', followMtx+'.inputMatrix[3]' )
        
        cmds.connectAttr( followMtx+'.outputMatrix', mtxDcmp+'.i[0]' )
        cmds.connectAttr( const +'.pim', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.or', const+'.r' )
        
        rigbase.addHelpTx( collarCtlList[si], 'Follow' )
        attrEdit = rigbase.AttrEdit( collarCtlList[si] )
        attrEdit.addAttr( ln='chestFollow', min=0, max=10 )
        attrEdit.addAttr( ln='rootFollow' , min=0, max=10 )
        attrEdit.addAttr( ln='flyFollow'  , min=0, max=10, k=1 )
        attrEdit.addAttr( ln='moveFollow'  , min=0, max=10 )
        
        cmds.connectAttr( collarCtlList[si]+'.chestFollow', followMtx+'.inputWeight[0]' )
        cmds.connectAttr( collarCtlList[si]+'.rootFollow' , followMtx+'.inputWeight[1]' )
        cmds.connectAttr( collarCtlList[si]+'.flyFollow'  , followMtx+'.inputWeight[2]' )
        cmds.connectAttr( collarCtlList[si]+'.moveFollow' , followMtx+'.inputWeight[3]' )
        
        if side == 'L':
            self.shoulderLConst = const
            self.rigInstance.ikGroupLConst = inChest
        else:
            self.shoulderRConst = const
            self.rigInstance.ikGroupRConst = inChest
        
    def hipConstSet(self):
        hipLConst_inFly = cmds.createNode( 'transform', n='Hip_L_Const_inFly' )
        hipRConst_inFly = cmds.createNode( 'transform', n='Hip_R_Const_inFly' )
        hipLConst_inRoot = cmds.createNode( 'transform', n='Hip_L_Const_inRoot' )
        hipRConst_inRoot = cmds.createNode( 'transform', n='Hip_R_Const_inRoot' )
        hipLConst_inHip = cmds.createNode( 'transform', n='Hip_L_Const_inHip' )
        hipRConst_inHip = cmds.createNode( 'transform', n='Hip_R_Const_inHip' )
        hipLConst = cmds.createNode( 'transform', n='Hip_L_Const' )
        hipRConst = cmds.createNode( 'transform', n='Hip_R_Const' )
        
        cmds.parent( hipLConst_inFly, hipRConst_inFly, self.rootCtlGrp )
        cmds.parent( hipLConst_inRoot, hipRConst_inRoot, self.rootGrp )
        cmds.parent( hipLConst, hipRConst, hipLConst_inHip, hipRConst_inHip, self.hipCtl )
        
        rigbase.connectSameAttr( self.hipLInit, hipLConst_inFly ).doIt( 't','r' )
        rigbase.connectSameAttr( self.hipRInit, hipRConst_inFly ).doIt( 't','r' )
        
        rigbase.connectSameAttr( self.hipLInit, hipLConst_inRoot ).doIt( 't' )
        rigbase.connectSameAttr( self.hipRInit, hipRConst_inRoot ).doIt( 't' )
        
        rigbase.constraint( hipLConst_inFly, hipLConst_inRoot, t=0 )
        rigbase.constraint( hipRConst_inFly, hipRConst_inRoot, t=0 )
        
        rigbase.connectSameAttr( self.hipLInit, hipLConst_inHip ).doIt( 't','r' )
        rigbase.connectSameAttr( self.hipRInit, hipRConst_inHip ).doIt( 't','r' )
        
        #cmds.setAttr( hipLConst_inHip+'.rz', -90 )
        #cmds.setAttr( hipLConst_inRoot+'.rz', -90 )
        
        #cmds.setAttr( hipRConst_inHip+'.rx', 180 )
        #cmds.setAttr( hipRConst_inHip+'.rz', 90 )
        #cmds.setAttr( hipRConst_inRoot+'.rx', 180 )
        #cmds.setAttr( hipRConst_inRoot+'.rz', 90 )
        
        blendMtxL = cmds.createNode( 'blendTwoMatrix', n='Hip_L_Const_blendMtx' )
        blendMtxR = cmds.createNode( 'blendTwoMatrix', n='Hip_R_Const_blendMtx' )
        
        multMtxDcmpL = cmds.createNode( 'multMatrixDecompose', n='Hip_L_Const_MtxDcmp' )
        multMtxDcmpR = cmds.createNode( 'multMatrixDecompose', n='Hip_R_Const_MtxDcmp' )
        
        cmds.connectAttr( hipLConst_inRoot+'.wm', blendMtxL+'.inMatrix1' )
        cmds.connectAttr( hipRConst_inRoot+'.wm', blendMtxR+'.inMatrix1' )
        cmds.connectAttr( hipLConst_inHip+'.wm', blendMtxL+'.inMatrix2' )
        cmds.connectAttr( hipRConst_inHip+'.wm', blendMtxR+'.inMatrix2' )
        
        cmds.connectAttr( blendMtxL+'.outMatrix', multMtxDcmpL+'.i[0]' )
        cmds.connectAttr( blendMtxR+'.outMatrix', multMtxDcmpR+'.i[0]' )
        
        cmds.connectAttr( hipLConst+'.pim', multMtxDcmpL+'.i[1]' )
        cmds.connectAttr( hipRConst+'.pim', multMtxDcmpR+'.i[1]' )
        
        cmds.connectAttr( hipLConst_inHip+'.t', hipLConst+'.t' )
        cmds.connectAttr( hipRConst_inHip+'.t', hipRConst+'.t' )
        cmds.connectAttr( multMtxDcmpL+'.or', hipLConst+'.r' )
        cmds.connectAttr( multMtxDcmpR+'.or', hipRConst+'.r' )
        
        rigbase.addHelpTx( self.hipCtl, 'Options' )
        attrEdit = rigbase.AttrEdit( self.hipCtl )
        attrEdit.addAttr( ln='legFollowL', min=0, max=1, k=1 )
        attrEdit.addAttr( ln='legFollowR', min=0, max=1, k=1 )
        
        cmds.connectAttr( self.hipCtl+'.legFollowL', blendMtxL+'.attributeBlender' )
        cmds.connectAttr( self.hipCtl+'.legFollowR', blendMtxR+'.attributeBlender' )
        
        self.rigInstance.hipLConst_inRoot = hipLConst_inRoot
        self.rigInstance.hipRConst_inRoot = hipRConst_inRoot
        self.rigInstance.hipLConst_inHip = hipLConst_inHip
        self.rigInstance.hipRConst_inHip = hipRConst_inHip
        self.rigInstance.hipLConstInFly = hipLConst_inFly
        self.rigInstance.hipRConstInFly = hipRConst_inFly
        self.hipLConst = hipLConst
        self.hipRConst = hipRConst
        
    def headConstSet(self):
        headConst = rigbase.Transform( n='Head_Const' )
        headConst.goto( self.headInit )
        headConst.setParent( self.chestCtl )
        self.rigInstance.headConst = headConst.name
        
    def originalOrientSet(self):
        shoulderLOr = rigbase.Transform( n='Shoulder_L_OriginalOrient' )
        shoulderROr = rigbase.Transform( n='Shoulder_R_OriginalOrient' )
        shoulderLOr.setParent( self.shoulderLCtl )
        shoulderROr.setParent( self.shoulderRCtl )
        rigbase.transformDefault( shoulderLOr, shoulderROr )
        cmds.setAttr( shoulderLOr+'.t', 0,0,0 )
        cmds.setAttr( shoulderLOr+'.r', 0,0,-45 )
        cmds.setAttr( shoulderROr+'.t', 0,0,0 )
        cmds.setAttr( shoulderROr+'.r', 0,0,-45 )
        
        hipLOr = rigbase.Transform( n='Hip_L_OriginalOrient' )
        hipROr = rigbase.Transform( n='Hip_R_OriginalOrient' )
        hipLOr.setParent( self.hipCtl )
        hipROr.setParent( self.hipCtl )
        cmds.connectAttr( self.hipLInit+'.t', hipLOr+'.t' )
        cmds.connectAttr( self.hipRInit+'.t', hipROr+'.t' )
        cmds.setAttr( hipLOr+'.r', 0,0,-90 )
        cmds.setAttr( hipROr+'.r', -180,0, 90 )
        
        self.rigInstance.shoulderLOr = shoulderLOr
        self.rigInstance.shoulderROr = shoulderROr
        self.rigInstance.hipLOr = hipLOr
        self.rigInstance.hipROr = hipROr
        
    def addAttributeAndConnect(self):
        def shoulderLTwistConnection():
            cmds.addAttr( self.collarLCtl, ln='twist' )
            cmds.setAttr( self.collarLCtl+'.twist', e=1, k=1 )
            
            for jnt in self.collarLJnts[1:]:
                multNode = cmds.createNode( 'multDoubleLinear', n='Collar_L_twistMult' )
                cmds.connectAttr( self.collarLCtl+'.twist', multNode+'.input1' )
                cmds.connectAttr( jnt          +'.parameter', multNode+'.input2' )
                cmds.connectAttr( multNode+'.output', jnt+'.rx' )
        def shoulderRTwistConnection():
            cmds.addAttr( self.collarRCtl, ln='twist' )
            cmds.setAttr( self.collarRCtl+'.twist', e=1, k=1 )
            
            for jnt in self.collarRJnts[1:]:
                multNode = cmds.createNode( 'multDoubleLinear', n='Collar_R_twistMult' )
                cmds.connectAttr( self.collarRCtl+'.twist', multNode+'.input1' )
                cmds.connectAttr( jnt          +'.parameter', multNode+'.input2' )
                cmds.connectAttr( multNode+'.output', jnt+'.rx' )
                
        shoulderLTwistConnection()
        shoulderRTwistConnection()
        
    def allSet(self, sepNumber1, sepNumber2 ):
        self.controlSet()
        self.curveSet()
        self.splineJointSet( sepNumber1 )
        self.splineSquashSet()
        self.twistAttrSet( 'L' )
        self.twistAttrSet( 'R' )
        self.collarJointSet( sepNumber2, 'L' )
        self.collarJointSet( sepNumber2, 'R' )
        self.collarConstSet( 'L' )
        self.collarConstSet( 'R' )
        self.hipConstSet()
        self.headConstSet()
        self.originalOrientSet()
        self.controlerSetColor()
        
        self.rigInstance.shoulderLCtl = self.shoulderLCtl
        self.rigInstance.shoulderRCtl = self.shoulderRCtl
        self.rigInstance.shoulderLConst = self.shoulderLConst
        self.rigInstance.shoulderRConst = self.shoulderRConst
        self.rigInstance.hipLConst      = self.hipLConst
        self.rigInstance.hipRConst      = self.hipRConst
        self.rigInstance.splineJnts     = self.splineJnts
        self.rigInstance.collarLJnts    = self.collarLJnts
        self.rigInstance.collarRJnts    = self.collarRJnts