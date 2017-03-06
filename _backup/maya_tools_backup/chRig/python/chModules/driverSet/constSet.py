import maya.cmds as cmds


class All_DRV:
    
    _ns = ''
    
    def __init__(self):
        
        pass
    
    
    def setNameSpace(self, ns ):
        
        self._ns = ns
    
    
    def getDrivers(self):
        
        className = self.__class__.__name__
        
        drivers = []
        
        if className.find( '_SIDE_' ) != -1:
            drivers.append( className.replace( '_SIDE_', '_L_' ) )
            drivers.append( className.replace( '_SIDE_', '_R_' ) )
        else:
            drivers.append( className )
            
        return drivers
            
            
    def getSplineCrv( self, upperJnt, lowerJnt ):
        
        parentGrp = cmds.listRelatives( upperJnt, p=1 )[0]
        crv = cmds.curve( p=[[0,0,0],[0,0,0]], d=1 )
        crvShape = cmds.listRelatives( crv, s=1 )[0]
        cmds.connectAttr( upperJnt+'.t', crvShape+'.controlPoints[0]' )
        mtxDcmp = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( lowerJnt+'.m', mtxDcmp+'.i[0]' )
        cmds.connectAttr( upperJnt+'.m', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.ot', crvShape+'.controlPoints[1]' )
        cmds.parent( crv, parentGrp )
        cmds.setAttr( crv+'.t', 0,0,0 )
        cmds.setAttr( crv+'.r', 0,0,0 )
        return crv
    
    
    def createUpperTargets( self, crv, upper, lower, upperList ):
        
        upperP = cmds.listRelatives( upper, p=1 )[0]
        
        drvNode = cmds.createNode( 'angleDriver' )
        multMtx = cmds.createNode( 'multMatrix' )
        
        cmds.connectAttr( upper+'.m', drvNode+'.angleMatrix' )
        cmds.connectAttr( upper+'.m', drvNode+'.baseMatrix' )
        cmds.disconnectAttr( upper+'.m', drvNode+'.baseMatrix' )
        cmds.connectAttr( lower+'.m', multMtx+'.i[0]' )
        cmds.connectAttr( upper+'.m', multMtx+'.i[1]' )
        
        splineInfo = cmds.createNode( 'splineCurveInfo' )
        cmds.setAttr( splineInfo+'.startUpAxis', 1 )
        cmds.setAttr( splineInfo+'.endUpAxis', 1 )
        cmds.setAttr( splineInfo+'.targetUpAxis', 1 )
        
        if upperList[0].find( '_L_' ) == -1:
            cmds.setAttr( splineInfo+'.targetAimAxis', 3 )
        
        rebuild    = cmds.createNode( 'rebuildCurve' )
        crvShape   = cmds.listRelatives( crv, s=1 )[0]
        cmds.connectAttr( crvShape+'.local', rebuild+'.inputCurve' )
        
        cmds.connectAttr( rebuild+'.outputCurve', splineInfo+'.inputCurve' )
        cmds.connectAttr( drvNode+'.outMatrix', splineInfo+'.startTransform' )
        cmds.connectAttr( multMtx+'.o', splineInfo+'.endTransform' )
        
        
        for i in range( len( upperList ) ):
            if cmds.attributeQuery( 'parameter', node= upperList[i], ex=1 ):
                cmds.connectAttr( upperList[i]+'.parameter', splineInfo+'.parameter[%d]' % i )
            target = cmds.createNode( 'transform', n=upperList[i].replace( '_BJT', '_CONST' ) )
            cmds.connectAttr( splineInfo+'.output[%d].position' % i, target+'.t' )
            cmds.connectAttr( splineInfo+'.output[%d].rotate' % i, target+'.r' )
            
            cmds.parent( target, upperP )


    def createLowerTargets( self, crv, upper, lower, lowerList ):
    
        upperP = cmds.listRelatives( upper, p=1 )[0]
        
        wristAngle = cmds.createNode( 'wristAngle' )
        angleTarget = cmds.createNode( 'transform' )
        cmds.parent( angleTarget, upper )
        cmds.setAttr( angleTarget+'.t', 0,0,0 )
        cmds.setAttr( angleTarget+'.r', 0,0,0 )
        cmds.connectAttr( wristAngle+'.outAngle', angleTarget+'.rx' )
        
        cmds.connectAttr( lower+'.m', wristAngle+'.inputMatrix' )
        
        splineInfo = cmds.createNode( 'splineCurveInfo' )
        cmds.setAttr( splineInfo+'.startUpAxis', 1 )
        cmds.setAttr( splineInfo+'.endUpAxis', 1 )
        cmds.setAttr( splineInfo+'.targetUpAxis', 1 )
        
        if lowerList[0].find( '_L_' ) != -1:
            cmds.setAttr( splineInfo+'.targetAimAxis', 0 )
        else:
            cmds.setAttr( splineInfo+'.targetAimAxis', 3 )
        
        rebuild    = cmds.createNode( 'rebuildCurve' )
        crvShape   = cmds.listRelatives( crv, s=1 )[0]
        cmds.connectAttr( crvShape+'.local', rebuild+'.inputCurve' )
        
        cmds.connectAttr( rebuild+'.outputCurve', splineInfo+'.inputCurve' )
        cmds.connectAttr( upper+'.m', splineInfo+'.startTransform' )
        endTrMult = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( angleTarget+'.m', endTrMult+'.i[0]' )
        cmds.connectAttr( upper+'.m'      , endTrMult+'.i[1]' )
        cmds.connectAttr( endTrMult+'.o', splineInfo+'.endTransform' )
        
        
        for i in range( len( lowerList ) ):
            cmds.connectAttr( lowerList[i]+'.parameter', splineInfo+'.parameter[%d]' % i )    
            target = cmds.createNode( 'transform', n=lowerList[i].replace( '_BJT', '_CONST' )  )
            cmds.connectAttr( splineInfo+'.output[%d].position' % i, target+'.t' )
            cmds.connectAttr( splineInfo+'.output[%d].rotate' % i, target+'.r' )
            
            cmds.parent( target, upperP )




class Root_DRV( All_DRV ):

    def __init__(self):
        
        pass




class Hip_SIDE_DRV( All_DRV ):
    
    def __init__(self):    
        
        driverL, driverR = self.getDrivers()
        
        childL = cmds.listRelatives( driverL, c=1 )[0]
        childR = cmds.listRelatives( driverR, c=1 )[0]

        targetListL = self.getSplineTargetListL()
        targetListR = self.getSplineTargetListR()
        
        crvL = self.getSplineCrv( driverL, childL )
        crvR = self.getSplineCrv( driverR, childR )
        
        self.createUpperTargets( crvL, driverL, childL, targetListL )
        self.createUpperTargets( crvR, driverR, childR, targetListR )
    

    def getSplineTargetListR(self):
        
        targetListR = cmds.ls( self._ns+'Leg_R_Upper*_BJT' )
        targetListR.remove( self._ns+'Leg_R_Upper_BJT' )

        return targetListR
    
    
    def getSplineTargetListL(self):
        
        targetListL = cmds.ls( self._ns+'Leg_L_Upper*_BJT' )
        targetListL.remove( self._ns+'Leg_L_Upper_BJT' )
        
        return targetListL
        
    
    

class Knee_SIDE_DRV( All_DRV ):
    
    def __init__(self):    
        
        driverL, driverR = self.getDrivers()
        
        childL = cmds.listRelatives( driverL, c=1 )[0]
        childR = cmds.listRelatives( driverR, c=1 )[0]

        targetListL = self.getSplineTargetListL()
        targetListR = self.getSplineTargetListR()
        
        crvL = self.getSplineCrv( driverL, childL )
        crvR = self.getSplineCrv( driverR, childR )
        
        self.createLowerTargets( crvL, driverL, childL, targetListL )
        self.createLowerTargets( crvR, driverR, childR, targetListR )
    

    def getSplineTargetListR(self):
        
        targetListR = cmds.ls( self._ns+'Leg_R_Lower*_BJT' )

        return targetListR[:-1]
    
    
    def getSplineTargetListL(self):
        
        targetListL = cmds.ls( self._ns+'Leg_L_Lower*_BJT' )
        
        return targetListL[:-1]
    
    
    

class Ankle_SIDE_DRV( All_DRV ):
    
    def __init__(self):    
        
        driverL, driverR = self.getDrivers()
        targetL = self.getTargetObjectL()
        targetR = self.getTargetObjectR()
        
        constObjL = cmds.createNode( 'transform', n=targetL.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjL, driverL )
        constObjR = cmds.createNode( 'transform', n=targetR.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjR, driverR )
        
        cmds.setAttr( constObjL+'.t', 0,0,0 )
        cmds.setAttr( constObjL+'.r', 0,0,0 )
        cmds.setAttr( constObjR+'.t', 0,0,0 )
        cmds.setAttr( constObjR+'.r', 0,0,0 )


    def getTargetObjectL(self):
        
        targetList = cmds.ls( self._ns+'Leg_L_Lower*_BJT' )
        return targetList[-1]
    
    def getTargetObjectR(self):
        
        targetList = cmds.ls( self._ns+'Leg_R_Lower*_BJT' )
        return targetList[-1]
    


class Ball_SIDE_DRV( All_DRV ):
    
    def __init__(self):    
        
        driverL, driverR = self.getDrivers()
        targetL = self.getTargetObjectL()
        targetR = self.getTargetObjectR()
        
        constObjL = cmds.createNode( 'transform', n=targetL.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjL, driverL )
        constObjR = cmds.createNode( 'transform', n=targetR.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjR, driverR )
        
        cmds.setAttr( constObjL+'.t', 0,0,0 )
        cmds.setAttr( constObjL+'.r', 0,0,0 )
        cmds.setAttr( constObjR+'.t', 0,0,0 )
        cmds.setAttr( constObjR+'.r', 0,0,0 )


    def getTargetObjectL(self):
        
        targetList = cmds.ls( self._ns+'Leg_L_Foot0_BJT' )
        return targetList[-1]
    
    def getTargetObjectR(self):
        
        targetList = cmds.ls( self._ns+'Leg_R_Foot0_BJT' )
        return targetList[-1]
    

class BodyRot_DRV( All_DRV ):
    
    def __init__(self):
    
        driver = self.getDrivers()[0]
        rootDrv = cmds.listRelatives( driver, p=1 )[0]
        
        splineList = self.getSplineTargetList()
        drvSplines = []
        
        parent = rootDrv
        
        angleNode = cmds.createNode( 'wristAngle' )
        cmds.setAttr( angleNode+'.axis', 1 )
        cmds.connectAttr( driver+'.m', angleNode+'.inputMatrix' )
        
        splineLen = len( splineList )
        for spline in splineList:
            
            index = splineList.index( spline )
            
            drvSpline = cmds.createNode( 'joint', n=spline.replace( '_BJT', '_NDRV' ) )
            const     = cmds.createNode( 'transform', n=spline.replace( '_BJT', '_CONST' ) )
            cmds.parent( const, drvSpline )
            cmds.parent( drvSpline, parent )
            cmds.setAttr( drvSpline+'.t',  *cmds.getAttr( spline+'.t' )[0] )
            cmds.setAttr( drvSpline+'.r',  *cmds.getAttr( spline+'.r' )[0] )
            cmds.setAttr( drvSpline+'.jo', *cmds.getAttr( spline+'.jo' )[0] )
            
            multNode = cmds.createNode( 'multDoubleLinear' )
            twistValue = float( index )/splineLen
            cmds.connectAttr( angleNode+'.outAngle', multNode+'.input1' )
            cmds.setAttr( multNode+'.input2', twistValue )
            cmds.connectAttr( multNode+'.output', const+'.ry' )
            
            parent = drvSpline
            
            drvSplines.append( drvSpline )
            
            if index == splineLen-1:
                cmds.delete( const )
            
        self.drvSplineConnect(driver, drvSplines )
        
        cmds.setAttr( drvSplines[ 0 ]+'.v', 0 )
        
        
    def drvSplineConnect(self, driver, drvSplines ):
        
        driverP = cmds.listRelatives( driver, p=1 )[0]
        driverGrp = cmds.createNode( 'transform', n=driver+'_GRP' )
        
        mtx = cmds.getAttr( driver+'.wm' )
        cmds.xform( driverGrp, matrix = mtx )
        
        cmds.parent( driverGrp, driverP )
        cmds.parent( driver, driverGrp )
        
        splineNum = len( drvSplines )
        divValue = 1.0/( splineNum-2 )
        
        angleDriver = cmds.createNode( 'angleDriver' )
        dcMtx = cmds.createNode( 'decomposeMatrix' )
        multNode = cmds.createNode( 'multiplyDivide' )
        
        cmds.connectAttr( driver+'.m', angleDriver+'.angleMatrix' )
        cmds.connectAttr( angleDriver+'.outMatrix', dcMtx+'.imat' )
        cmds.setAttr( angleDriver+'.axis', 1 )
        
        cmds.connectAttr( dcMtx+'.or', multNode+'.input1' )
        cmds.setAttr( multNode+'.input2', divValue, divValue, divValue )
        
        for i in range( 1, splineNum -1  ):
            cmds.connectAttr( multNode+'.output', drvSplines[i]+'.r' )
        
        mtxDcmp = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( drvSplines[-1]+'.wm', mtxDcmp+'.i[0]' )
        cmds.connectAttr( driverP+'.wim', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.ot', driverGrp+'.t' )
        

        
    def getSplineTargetList(self):
        
        targetList = cmds.ls( self._ns+'Spline*_BJT' )
        return targetList
    


class Chest_DRV( All_DRV ):
    
    def __init__(self):
        
        driver = self.getDrivers()[0]
        target = self.getTargetObject()
        
        constObj = cmds.createNode( 'transform', n=target.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObj, driver )
        
        cmds.setAttr( constObj+'.t', 0,0,0 )
        cmds.setAttr( constObj+'.r', 0,0,0 )
        
        
    def getTargetObject(self):
        
        targetList = cmds.ls( self._ns+'Spline*_BJT' )
        return targetList[-1]
    
    

class Neck_DRV( All_DRV ):
    
    def __init__(self):
        
        driver = self.getDrivers()[0]
        target = self.getTargetObject()
        
        constObj = cmds.createNode( 'transform', n=target.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObj, driver )
        
        cmds.setAttr( constObj+'.t', 0,0,0 )
        cmds.setAttr( constObj+'.r', 0,0,0 )
        
        
    def getTargetObject(self):
        
        targetList = cmds.ls( self._ns+'Neck_Spline0_BJT' )
        return targetList[-1]
    
    
    
class Head_DRV( All_DRV ):
    
    def __init__(self):
        
        driver = self.getDrivers()[0]
        target = self.getTargetObject()
        
        constObj = cmds.createNode( 'transform', n=target.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObj, driver )
        
        cmds.setAttr( constObj+'.t', 0,0,0 )
        cmds.setAttr( constObj+'.r', 0,0,0 )
        
        
    def getTargetObject(self):
        
        targetList = cmds.ls( self._ns+'Neck_Spline*_BJT' )
        return targetList[-1]
    


class Collar_SIDE_DRV( All_DRV ):
    
    def __init__(self):
        
        driverL, driverR = self.getDrivers()
        targetL, targetR = self.getTargetObjects()
        
        constObjL = cmds.createNode( 'transform', n=targetL.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjL, driverL )
        constObjR = cmds.createNode( 'transform', n=targetR.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjR, driverR )
        
        cmds.setAttr( constObjL+'.t', 0,0,0 )
        cmds.setAttr( constObjL+'.r', 0,0,0 )
        cmds.setAttr( constObjR+'.t', 0,0,0 )
        cmds.setAttr( constObjR+'.r', 0,0,0 )
        
        
    def getTargetObjects(self):
        
        targetList = cmds.ls( self._ns+'Collar0_*_BJT' )
        return targetList
    
    

class Shoulder_SIDE_DRV( All_DRV ):
    
    def __init__(self):    
        
        driverL, driverR = self.getDrivers()
        
        childL = cmds.listRelatives( driverL, c=1 )[0]
        childR = cmds.listRelatives( driverR, c=1 )[0]

        targetListL = self.getSplineTargetListL()
        targetListR = self.getSplineTargetListR()
        
        crvL = self.getSplineCrv( driverL, childL )
        crvR = self.getSplineCrv( driverR, childR )
        
        self.createUpperTargets( crvL, driverL, childL, targetListL )
        self.createUpperTargets( crvR, driverR, childR, targetListR )
    

    def getSplineTargetListR(self):
        
        targetListR = cmds.ls( self._ns+'Arm_R_Upper*_BJT' )

        return targetListR
    
    
    def getSplineTargetListL(self):
        
        targetListL = cmds.ls( self._ns+'Arm_L_Upper*_BJT' )
        
        return targetListL



class Elbow_SIDE_DRV( All_DRV ):
    
    def __init__(self): 
        
        driverL, driverR = self.getDrivers()
        
        childL = cmds.listRelatives( driverL, c=1 )[0]
        childR = cmds.listRelatives( driverR, c=1 )[0]

        targetListL = self.getSplineTargetListL()
        targetListR = self.getSplineTargetListR()
        
        crvL = self.getSplineCrv( driverL, childL )
        crvR = self.getSplineCrv( driverR, childR )
        
        self.createLowerTargets( crvL, driverL, childL, targetListL )
        self.createLowerTargets( crvR, driverR, childR, targetListR )
    

    def getSplineTargetListR(self):
        
        targetListR = cmds.ls( self._ns+'Arm_R_Lower*_BJT' )

        return targetListR[:-1]
    
    
    def getSplineTargetListL(self):
        
        targetListL = cmds.ls( self._ns+'Arm_L_Lower*_BJT' )
        
        return targetListL[:-1]
    


class Hand_SIDE_DRV( All_DRV ):
    
    def __init__(self):    
        
        driverL, driverR = self.getDrivers()
        targetL = self.getTargetObjectL()
        targetR = self.getTargetObjectR()
        
        constObjL = cmds.createNode( 'transform', n=targetL.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjL, driverL )
        constObjR = cmds.createNode( 'transform', n=targetR.replace( '_BJT', '_CONST' ) )
        cmds.parent( constObjR, driverR )
        
        cmds.setAttr( constObjL+'.t', 0,0,0 )
        cmds.setAttr( constObjL+'.r', 0,0,0 )
        cmds.setAttr( constObjR+'.t', 0,0,0 )
        cmds.setAttr( constObjR+'.r', 0,0,0 )


    def getTargetObjectL(self):
        
        targetList = cmds.ls( self._ns+'Arm_L_Lower*_BJT' )
        return targetList[-1]
    
    def getTargetObjectR(self):
        
        targetList = cmds.ls( self._ns+'Arm_R_Lower*_BJT' )
        return targetList[-1]



def constConnect( ns='' ):
    
    consts = cmds.ls( ns+'*_CONST' )

    for const in consts:
        target = const.replace( '_CONST', '_BJT' )
        
        dcmp = cmds.createNode( 'multMatrixDecompose' )
        cmds.connectAttr( const+'.wm', dcmp+'.i[0]' )
        cmds.connectAttr( target+'.pim', dcmp+'.i[1]' )
        
        joCons = cmds.listConnections( target+'.jo', type='multMatrixDecompose', s=1, d=0 )
        if joCons:
            cmds.delete( joCons )
        
        cmds.connectAttr( dcmp+'.or', target+'.jo' )
        
