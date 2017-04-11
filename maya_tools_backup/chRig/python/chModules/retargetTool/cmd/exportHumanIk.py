import maya.cmds as cmds
import chModules.ctls.allCtlsCmd as createCmd


class Connect:
    
    def __init__(self, allMoc ):
        
        self._allMoc = allMoc
        self._namespace = allMoc.replace( 'All_Moc', '' )
        
        self._bodyMocList   = ['Root_MOC', 'Root_MOCPiv', 'Root_MOCSep', 'Waist_MOC', 'Chest_MOCSep', 'Chest_MOC']
        self._headMocList   = ['Neck_MOC', 'NeckMiddle_MOC', 'Head_MOC']
        self._matrixMocList = ['Hip_SIDE_MOC', 'Collar_SIDE_MOC', 'Shoulder_SIDE_MOC']
        self._directMocList = ['Knee_SIDE_MOC', 'Ankle_SIDE_MOC',
                               'Elbow_SIDE_MOC', 'Wrist_SIDE_MOC',
                               'ThumbNUM_SIDE_MOC', 'IndexNUM_SIDE_MOC', 'MiddleNUM_SIDE_MOC', 'RingNUM_SIDE_MOC', 'PinkyNUM_SIDE_MOC' ]

        self._bodyTargetList   = ['TorsoRotate_CTL', 'Hip_CTL', 'ChestMove_CTL', 'Waist_Init', 'Chest_Init']
        self._headTargetList   = ['Neck_CTL', 'NeckMiddle_CTL', 'Head_CTL']
        self._matrixTargetList = ['Leg_SIDE_CU0', 'Collar0_SIDE_RJT', 'Arm_SIDE_CU0']
        self._directTargetList = ['Leg_SIDE_CU1', 'Leg_SIDE_CU2', 
                                  'Arm_SIDE_CU1', 'Arm_SIDE_CU2',
                                  'ThumbNUM_SIDE_RJT', 'IndexNUM_SIDE_RJT', 'MiddleNUM_SIDE_RJT', 'RingNUM_SIDE_RJT', 'PinkyNUM_SIDE_RJT' ]
        
        self.connectHead()
        self.connectBody()
        self.connectMatrix()
        self.connectDirect()
        
        self.mocJointOrientDefault()

    
    def mocJointOrientDefault(self):
        
        mocs = cmds.ls( self._namespace+'*_MOC', type='joint' )
        
        for moc in mocs:
            cmds.setAttr( moc+'.jo', 0,0,0 )
        
        
    def connectHead(self):
        
        neckMoc = self._namespace+self._headMocList[0]
        middleMoc = self._namespace+self._headMocList[1]
        headMoc = self._namespace+self._headMocList[2]
        
        neckCtl = self._namespace+self._headTargetList[0]
        middleCtl = self._namespace+self._headTargetList[1]
        headCtl = self._namespace+self._headTargetList[2]
        
        neckCtlP = self._namespace+self._bodyTargetList[2]
        
        neckDcmp = cmds.createNode( 'multMatrixDecompose', n=self._namespace+'.neckDcmp' )
        cmds.connectAttr( neckCtl+'.wm', neckDcmp+'.i[0]' )
        cmds.connectAttr( neckCtlP+'.wim', neckDcmp+'.i[1]' )
        cmds.connectAttr( neckDcmp+'.ot', neckMoc+'.t' )
        cmds.connectAttr( neckDcmp+'.or', neckMoc+'.r' )
        
        middleDcmp = cmds.createNode( 'multMatrixDecompose', n=self._namespace+'.neckMiddleDcmp' )
        cmds.connectAttr( middleCtl+'.wm', middleDcmp+'.i[0]' )
        cmds.connectAttr( neckCtl+'.wim', middleDcmp+'.i[1]' )
        cmds.connectAttr( middleDcmp+'.ot', middleMoc+'.t' )
        cmds.connectAttr( middleDcmp+'.or', middleMoc+'.r' )
        
        headDcmp = cmds.createNode( 'multMatrixDecompose', n=self._namespace+'.headDcmp' )
        cmds.connectAttr( headCtl+'.wm', headDcmp+'.i[0]' )
        cmds.connectAttr( middleCtl+'.wim', headDcmp+'.i[1]' )
        cmds.connectAttr( headDcmp+'.ot', headMoc+'.t' )
        cmds.connectAttr( headDcmp+'.or', headMoc+'.r' )
        
        
    def connectBody(self):
        
        mocWorld = self._allMoc
        targetWorld = self._namespace+'World_CTL'
        
        torsoCtl  = self._namespace + self._bodyTargetList[0]
        hipCtl    = self._namespace + self._bodyTargetList[1]
        chestCtl  = self._namespace + self._bodyTargetList[2]
        waistInit = self._namespace + self._bodyTargetList[3]
        chestInit = self._namespace + self._bodyTargetList[4]
        
        rootMoc    = self._namespace + self._bodyMocList[0]
        splineMoc0 = self._namespace + self._bodyMocList[1]
        splineMoc1 = self._namespace + self._bodyMocList[2]
        splineMoc2 = self._namespace + self._bodyMocList[3]
        splineMoc3 = self._namespace + self._bodyMocList[4]
        chestMoc   = self._namespace + self._bodyMocList[5]
        
        hipCombine = cmds.createNode( 'transRotateCombineMatrix', n=self._namespace+'trCombindMtx' )
        hipCombineInv = cmds.createNode( 'inverseMatrix', n=self._namespace+'.trCombineInvMtx' )
        cmds.connectAttr( hipCtl+'.wm', hipCombine+'.inputTransMatrix' )
        cmds.connectAttr( torsoCtl+'.wm', hipCombine+'.inputRotateMatrix' )
        cmds.connectAttr( hipCombine+'.om', hipCombineInv+'.inputMatrix' )
        
        rootDcmp = cmds.createNode( 'multMatrixDecompose', n=rootMoc+'_dcmp' )
        cmds.connectAttr( hipCombine+'.om', rootDcmp+'.i[0]' )
        cmds.connectAttr( targetWorld+'.wim', rootDcmp+'.i[1]' )
        cmds.connectAttr( rootDcmp+'.ot', rootMoc+'.t' )
        cmds.connectAttr( rootDcmp+'.or', rootMoc+'.r' )
        
        bezier = cmds.curve( d=3, bezier=1, p=[[0]*3]*4 )
        bezierShape = cmds.listRelatives( bezier, s=1 )[0]
        cmds.parent( bezier, rootMoc )
        cmds.setAttr( bezier+'.t', 0,0,0 )
        cmds.setAttr( bezier+'.r', 0,0,0 )
        
        waistDist = cmds.createNode( 'distanceBetween', n=self._namespace+'Waist_distance' )
        chestDist = cmds.createNode( 'distanceBetween', n=self._namespace+'Chest_distance' )
        distSum   = cmds.createNode( 'addDoubleLinear', n=self._namespace+'body_distance' )
        
        cmds.connectAttr( waistInit+'.t', waistDist+'.point1' )
        cmds.connectAttr( chestInit+'.t', chestDist+'.point1' )
        cmds.connectAttr( waistDist+'.distance', distSum+'.input1' )
        cmds.connectAttr( chestDist+'.distance', distSum+'.input2' )
        
        bezierChestDcmp = cmds.createNode( 'multMatrixDecompose', n=self._namespace+'bezierChestDcmp')
        cmds.connectAttr( chestCtl+'.wm', bezierChestDcmp+'.i[0]' )
        cmds.connectAttr( hipCombineInv+'.outputMatrix', bezierChestDcmp+'.i[1]' )
        cmds.connectAttr( bezierChestDcmp+'.ot', bezierShape+'.cp[3]' )
        cmds.connectAttr( waistInit+'.t', bezierShape+'.cp[1]' )
        cmds.connectAttr( waistInit+'.t', bezierShape+'.cp[2]' )
        
        splineInfo = cmds.createNode( 'splineCurveInfo', n=self._namespace+'splineInfo' )
        cmds.connectAttr( bezierShape+'.local', splineInfo+'.inputCurve' )
        upMatrix = cmds.createNode( 'multMatrix', n=self._namespace+'upMatrix' )
        cmds.connectAttr( chestCtl+'.wm', upMatrix+'.i[0]' )
        cmds.connectAttr( hipCombineInv+'.outputMatrix',  upMatrix+'.i[1]' )
        cmds.connectAttr( upMatrix+'.o', splineInfo+'.endTransform' )
        
        cmds.setAttr( splineInfo+'.parameter[0]', 0.001 )
        cmds.setAttr( splineInfo+'.parameter[1]', 0.25 )
        cmds.setAttr( splineInfo+'.parameter[2]', 0.5 )
        cmds.setAttr( splineInfo+'.parameter[3]', 0.75 )
        cmds.setAttr( splineInfo+'.parameter[4]', 1.00 )
        
        cmds.setAttr( splineInfo+'.startUpAxis', 2 )
        cmds.setAttr( splineInfo+'.endUpAxis', 2 )
        cmds.setAttr( splineInfo+'.targetAimAxis', 1 )
        cmds.setAttr( splineInfo+'.targetUpAxis', 2 )
        
        cmds.setAttr( splineInfo+'.paramFromLength', 0 )
        
        
        splineList = [ None, splineMoc1, splineMoc2, splineMoc3 ]
        
        cmds.connectAttr( splineInfo+'.output[0].position', splineMoc0+'.t' )
        cmds.connectAttr( splineInfo+'.output[0].rotate'  , splineMoc0+'.r' )
        
        for i in range( 1, 4 ):
            splineP = cmds.listRelatives( splineList[i], p=1 )[0]
            compose = cmds.createNode( 'composeMatrix', n=self._namespace+'spline%d_compose' % i )
            dcmp    = cmds.createNode( 'multMatrixDecompose', n=self._namespace+'spline%d_dcmp' % i )
            cmds.connectAttr( splineInfo+'.output[%d].position' % i, compose+'.it' )
            cmds.connectAttr( splineInfo+'.output[%d].rotate'   % i, compose+'.ir' )
            cmds.connectAttr( compose+'.outputMatrix', dcmp+'.i[0]' )
            cmds.connectAttr( rootMoc+'.wm', dcmp+'.i[1]' )
            cmds.connectAttr( splineP+'.wim', dcmp+'.i[2]' )
            cmds.connectAttr( dcmp+'.ot', splineList[i]+'.t' )
            cmds.connectAttr( dcmp+'.or', splineList[i]+'.r' )
            
        chestDcmp = cmds.createNode( 'multMatrixDecompose', n=self._namespace+'chestDcmp' )
        cmds.connectAttr( chestCtl+'.wm', chestDcmp+'.i[0]' )
        cmds.connectAttr( hipCombineInv+'.outputMatrix' , chestDcmp+'.i[1]' )
        cmds.connectAttr( rootMoc+'.wm', chestDcmp+'.i[2]' )
        cmds.connectAttr( splineMoc3+'.wim', chestDcmp+'.i[3]' )
        cmds.connectAttr( chestDcmp+'.ot', chestMoc+'.t' )
        cmds.connectAttr( chestDcmp+'.or', chestMoc+'.r' )
       
    
    def connectMatrix(self):
        
        matrixLen = len( self._matrixMocList )
        
        mocWorld = self._allMoc
        targetWorld = self._namespace+'World_CTL'
        
        for i in range( matrixLen ):
            mocStr    = self._matrixMocList[i]
            targetStr = self._matrixTargetList[i]
            
            currentMocStr = mocStr.replace( 'SIDE', '*' ).replace( 'NUM', '*' )
            currentTargetStr = targetStr.replace( 'SIDE', '*' ).replace( 'NUM', '*' )
            
            mocList    = cmds.ls( self._namespace + currentMocStr, type='joint' )
            targetList = cmds.ls( self._namespace + currentTargetStr, type='transform' )

            for j in range( len( mocList ) ):
                moc = mocList[j]
                mocP = cmds.listRelatives( moc, p=1 )[0]
                target = targetList[j]
                
                dcmp = cmds.createNode( 'multMatrixDecompose', n=moc+'_dcmp' )
                cmds.connectAttr( target+'.wm', dcmp+'.i[0]' )
                cmds.connectAttr( targetWorld+'.wim', dcmp+'.i[1]' )
                cmds.connectAttr( mocWorld+'.wm', dcmp+'.i[2]' )
                cmds.connectAttr( mocP+'.wim', dcmp+'.i[3]' )
                
                cmds.connectAttr( dcmp+'.or', moc+'.r' )

    
    def connectDirect(self):
        
        directLen = len( self._directTargetList )
        
        for i in range( directLen ):
            mocStr    = self._directMocList[i]
            targetStr = self._directTargetList[i]
            
            currentMocStr = mocStr.replace( 'SIDE', '*' ).replace( 'NUM', '*' )
            currentTargetStr = targetStr.replace( 'SIDE', '*' ).replace( 'NUM', '*' )
            
            mocList    = cmds.ls( self._namespace + currentMocStr, type='joint' )
            targetList = cmds.ls( self._namespace + currentTargetStr, type='transform' )

            for j in range( len( mocList ) ):
                moc = mocList[j]
                target = targetList[j]
                
                dcmp = cmds.createNode( 'decomposeMatrix', n=moc+'_dcmp' )
                cmds.connectAttr( target+'.m', dcmp+'.imat' )
                cmds.connectAttr( dcmp+'.or', moc+'.r' )



class Main:
    
    def __init__(self, worldCtl ):
        
        self._worldCtl = worldCtl
        
        self._namespace = worldCtl.replace( "World_CTL", '' )
        
        self.getHumanIkJoint()
        
        self.connectToJoint()
    
    
    def getHumanIkJoint(self):
        
        worldCtl_inst = createCmd.World_CTL()
        
        self._allMoc = self._namespace+'All_Moc'
        
        if not cmds.objExists( self._allMoc ):
            worldCtl_inst.createMocapJoint( self._worldCtl )
            
        allMoc_inst = createCmd.All_Moc()
        
        allMoc_inst.createCharacter( self._allMoc )
        
        cmds.delete( cmds.ls( self._namespace+'*_HIK_GRP' ) )
        
    
    def connectToJoint(self):
        
        Connect( self._allMoc )