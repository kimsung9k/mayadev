import maya.cmds as cmds

class All:
    
    def __init__(self):
        
        pass
    

    
    def sepSideItem(self, name ):
        
        left  = name.replace( '_SIDE_', '_L_' )
        right = name.replace( '_SIDE_', '_R_' )
        
        return left, right
    
    
    def getLastNum(self, name ):
        
        return cmds.ls( name.replace( 'LAST', '*' ), type='joint' )[-1]


    def makeDriver(self, target, driverName, axisNum ):
        
        targetP = cmds.listRelatives( target, p=1 )[0]
        targetBase = cmds.createNode( 'transform', n=driverName+'_DriverBase' )
        cmds.parent( targetBase, targetP )
        
        targetMtx = cmds.xform( target, q=1, matrix=1 )
        cmds.xform( targetBase, matrix=targetMtx )
        cmds.connectAttr( target+'.t', targetBase+'.t' )
        
        angleDriver = cmds.createNode( 'angleDriver', n=driverName+'_angleDriver' )
        cmds.setAttr( angleDriver+'.axis', axisNum )
        multMtx     = cmds.createNode( 'multMatrix', n=driverName+'_multMtx' )
        
        cmds.connectAttr( target+'.m', multMtx+'.i[0]' )
        cmds.connectAttr( targetBase+'.im', multMtx+'.i[1]' )
        
        cmds.connectAttr( multMtx+'.o', angleDriver+'.angleMatrix' )
        cmds.connectAttr( multMtx+'.o', angleDriver+'.upVectorMatrix')
        
        driverTransform = cmds.createNode( 'transform', n=driverName+'_driverVisTr' )
        transformDcmp   = cmds.createNode( 'decomposeMatrix', n=driverName+'_trDcmp' )
        
        cmds.connectAttr( angleDriver+'.outMatrix', transformDcmp+'.imat' )
        cmds.connectAttr( transformDcmp+'.or', driverTransform+'.r' )
        cmds.parent( driverTransform, targetBase )
        cmds.setAttr( driverTransform+'.t', 0,0,0 )
        #cmds.setAttr( driverTransform+'.dla', 1 )
        


    def makeUpSplineDriver(self, upper, lower, driverName, inverseAim = False ):
        
        upperP = cmds.listRelatives( upper, p=1 )[0]
        upperBase = cmds.createNode( 'transform', n=driverName+'_DriverBase' )
        cmds.parent( upperBase, upperP )
        loChild = cmds.createNode( 'transform', n=driverName+'_LowerChild' )
        cmds.parent( loChild, lower )
        cmds.setAttr( loChild+'.t', 0,0,0 )
        rot = cmds.xform( upper, q=1, ws=1, ro=1 )[:3]
        cmds.rotate( rot[0], rot[1], rot[2], loChild, ws=1 )
        
        upperMtx = cmds.xform( upper, q=1, matrix=1 )
        cmds.xform( upperBase, matrix = upperMtx )
        
        angleDriver = cmds.createNode( 'angleDriver', n=driverName+'_angleDriver' )
        
        multMtx     = cmds.createNode( 'multMatrix' , n=driverName+'_multMtx' )
        loMultMtx   = cmds.createNode( 'multMatrix',  n=driverName+'_loMultMtx' )
        
        cmds.connectAttr( upper+'.m', multMtx+'.i[0]' )
        cmds.connectAttr( upperBase+'.im', multMtx+'.i[1]')
        cmds.connectAttr( loChild+'.wm', loMultMtx+'.i[0]' )
        cmds.connectAttr( upperBase+'.wim', loMultMtx+'.i[1]')
        cmds.connectAttr( upper+'.t', upperBase+'.t' )
        
        cmds.connectAttr( multMtx+'.o', angleDriver+'.angleMatrix' )
        cmds.connectAttr( loMultMtx+'.o', angleDriver+'.upVectorMatrix' )
        
        driverTransform = cmds.createNode( 'transform', n=driverName+'_driverVisTr' )
        transformDcmp   = cmds.createNode( 'decomposeMatrix', n=driverName+'_trDcmp' )
        
        cmds.connectAttr( angleDriver+'.outMatrix', transformDcmp+'.imat' )
        cmds.connectAttr( transformDcmp+'.or', driverTransform+'.r' )
        #cmds.setAttr( driverTransform+'.dla',1 )
        cmds.parent( driverTransform, upperBase )
        cmds.setAttr( driverTransform+'.t', 0,0,0 )
        
        
        
    def makeMiddleSplineDriver(self, target, driverName, axisNum ):

        targetP = cmds.listRelatives( target, p=1 )[0]
        targetBase = cmds.createNode( 'transform', n=driverName+'_DriverBase' )
        cmds.parent( targetBase, targetP )
        
        targetMtx = cmds.xform( target, q=1, matrix=1 )
        cmds.xform( targetBase, matrix=targetMtx )
        cmds.connectAttr( target+'.t', targetBase+'.t' )
        
        fbfMtx = cmds.createNode( 'fourByFourMatrix', n=driverName+'_baseFbf' )
        mtxToThree = cmds.createNode( 'matrixToThreeByThree', n=driverName+'_baseToThreeByThree' )
        cmds.connectAttr( target+'.m', mtxToThree+'.inMatrix' )
        for i in range( 3 ):
            for j in range( 3 ):
                cmds.setAttr( fbfMtx+'.i%d%d' %( i, j ), cmds.getAttr( mtxToThree+'.out%d%d' %( i, j ) ) )
        for i in range( 3 ):
            cmds.connectAttr( mtxToThree+'.out%d%d' %( axisNum+1, i ), fbfMtx+'.i%d%d' %( axisNum+1, i ) )
        baseDcmp = cmds.createNode( 'decomposeMatrix', n=driverName+'_baseDcmp' )
        cmds.connectAttr( fbfMtx+'.output', baseDcmp+'.imat' )
        cmds.connectAttr( baseDcmp+'.or', targetBase+'.r' )
        
        angleDriver = cmds.createNode( 'angleDriver', n=driverName+'_angleDriver' )
        cmds.setAttr( angleDriver+'.axis', axisNum )
        multMtx     = cmds.createNode( 'multMatrix', n=driverName+'_multMtx' )
        
        cmds.connectAttr( target+'.m', multMtx+'.i[0]' )
        cmds.connectAttr( targetBase+'.im', multMtx+'.i[1]' )
        
        cmds.connectAttr( multMtx+'.o', angleDriver+'.angleMatrix' )
        cmds.connectAttr( multMtx+'.o', angleDriver+'.upVectorMatrix')
        
        driverTransform = cmds.createNode( 'transform', n=driverName+'_driverVisTr' )
        transformDcmp   = cmds.createNode( 'decomposeMatrix', n=driverName+'_trDcmp' )
        
        cmds.connectAttr( angleDriver+'.outMatrix', transformDcmp+'.imat' )
        cmds.connectAttr( transformDcmp+'.or', driverTransform+'.r' )
        cmds.parent( driverTransform, targetBase )
        cmds.setAttr( driverTransform+'.t', 0,0,0 )
        #cmds.setAttr( driverTransform+'.dla', 1 )
        

    def makeLoSplineDriver(self, upper, lower, driverName ):
        
        lowerP = cmds.listRelatives( lower, p=1 )[0]
        lowerBase = cmds.createNode( 'transform', n=driverName+'_DriverBase' )
        cmds.parent( lowerBase, lowerP )
        
        baseMultMtx = cmds.createNode( 'multMatrixDecompose', n=driverName+'_baseMultMtx' )
        cmds.connectAttr( upper+'.wm', baseMultMtx+'.i[0]' )
        cmds.connectAttr( lowerP+'.wim', baseMultMtx+'.i[1]' )
        cmds.connectAttr( baseMultMtx+'.or', lowerBase+'.r' )
        cmds.connectAttr( lower+'.t', lowerBase+'.t' )
        
        angleDriver = cmds.createNode( 'angleDriver', n=driverName+'_angleDriver' )
        
        multMtx     = cmds.createNode( 'multMatrix' , n=driverName+'_multMtx' )
        
        lowerChild = cmds.createNode( 'transform', n=driverName+'_LowerChild' )
        cmds.parent( lowerChild, lowerBase )
        cmds.setAttr( lowerChild+'.t', 0,0,0 )
        cmds.setAttr( lowerChild+'.r', 0,0,0 )
        cmds.parent( lowerChild, lower )
        cmds.connectAttr( lowerChild+'.wm', multMtx+'.i[0]' )
        cmds.connectAttr( lowerBase+'.wim', multMtx+'.i[1]' )
        
        cmds.connectAttr( multMtx+'.o', angleDriver+'.angleMatrix' )
        cmds.connectAttr( multMtx+'.o', angleDriver+'.upVectorMatrix' )
        
        driverTransform = cmds.createNode( 'transform', n=driverName+'_driverVisTr' )
        transformDcmp   = cmds.createNode( 'decomposeMatrix', n=driverName+'_trDcmp' )
        
        cmds.parent( driverTransform, lowerBase )
        
        cmds.connectAttr( angleDriver+'.outMatrix', transformDcmp+'.imat' )
        cmds.connectAttr( transformDcmp+'.or', driverTransform+'.r' )
        #cmds.setAttr( driverTransform+'.dla',1 )
        cmds.setAttr( driverTransform+'.t', 0,0,0 )
        

        
    def makeBodyDriver(self, targetList, driverName ):
        
        targetListP = cmds.listRelatives( targetList[0], p=1 )[0]
        
        driverBase = cmds.createNode( 'transform', n=driverName+'_DriverBase' )
        cmds.parent( driverBase, targetListP )
        cmds.setAttr( driverBase+'.t', 0,0,0 )
        cmds.setAttr( driverBase+'.r', 0,0,0 )
        
        multMtx = cmds.createNode( 'multMatrix', n=driverName+'_BodyMult' )
        
        for i in range( len( targetList ) ):
            cmds.connectAttr( targetList[i]+'.m', multMtx+'.i[%d]' % i )
            
        angleDriver = cmds.createNode( 'angleDriver', n=driverName+'_angleDriver' )
        cmds.setAttr( angleDriver+'.axis', 1 )
        cmds.connectAttr( multMtx+'.o', angleDriver+'.angleMatrix' )
        cmds.connectAttr( multMtx+'.o', angleDriver+'.upVectorMatrix' )
        
        driverTransform = cmds.createNode( 'transform', n= driverName+'_driverTr' )
        dcmp            = cmds.createNode( 'decomposeMatrix', n=driverName+'_driverDcmp' )
        
        cmds.connectAttr( angleDriver+'.outMatrix', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.or', driverTransform+'.r' )
        cmds.parent( driverTransform, driverBase )
        cmds.setAttr( driverTransform+'.t', 0,0,0 )
        
        #cmds.setAttr( driverTransform+'.dla', 1 )



class UpperSplineSet( All ):
    
    def __init__(self, startName, endName ):
        
        self._startName = startName
        self._endName   = endName
        
        self.core()
    
    
    def core(self):
        
        upperList = self.sepSideItem( self._startName )
        lowerList = self.sepSideItem( self._endName )
        
        if not cmds.objExists( upperList[0].replace( '_BJT', '_DriverBase' ) ):
            self.makeUpSplineDriver( upperList[0], lowerList[0], upperList[0].replace( '_BJT', '' ), False )
        if not cmds.objExists( upperList[1].replace( '_BJT', '_DriverBase' ) ):
            self.makeUpSplineDriver( upperList[1], lowerList[1], upperList[1].replace( '_BJT', '' ), True )
            
            

          
class MiddleSplineSet( All ):
    
    def __init__(self, targetName, axisNum = 0 ):
        
        self._targetName = targetName
        self._axisNum    = axisNum
        
        self.core()


    def core(self):

        targetList = []
        if self._targetName.find( '_SIDE_' ) != -1:
            targetList = self.sepSideItem( self._targetName )

        else:
            targetList.append( self._targetName )

        for targetName in targetList:
            if not cmds.objExists( targetName.replace( '_BJT', '_DriverBase' ) ):
                self.makeMiddleSplineDriver( targetName, targetName.replace( '_BJT', '' ), self._axisNum )




class LowerSplineSet( All ):
    
    def __init__(self, startName, endName ):
        
        self._startName = startName
        self._endName   = endName
        
        self.core()
    
    
    def core(self):
        
        upperList = self.sepSideItem( self._startName )
        lowerList = self.sepSideItem( self._endName )
        
        lowerList = list(lowerList)
        for i in range( len( lowerList ) ):
            lowerList[i] = self.getLastNum( lowerList[i] )
        
        if not cmds.objExists( lowerList[0].replace( '_BJT', '_DriverBase' ) ):
            self.makeLoSplineDriver( upperList[0], lowerList[0], lowerList[0].replace( '_BJT', '' ) )
        if not cmds.objExists( lowerList[1].replace( '_BJT', '_DriverBase' ) ):
            self.makeLoSplineDriver( upperList[1], lowerList[1], lowerList[1].replace( '_BJT', '' ) )
            


            
class DirectSet( All ):
    
    def __init__(self, targetName, axisNum = 0 ):
        
        self._targetName = targetName
        self._axisNum    = axisNum
        
        self.core()


    def core(self):
        
        targetList = []
        if self._targetName.find( '_SIDE_' ) != -1:
            targetList = self.sepSideItem( self._targetName )
        elif self._targetName.find( 'ENDNUM' ) != -1:
            endTarget = cmds.ls( self._targetName.replace( 'ENDNUM', '*' ) )[-1]
            targetList.append( endTarget )
        else:
            targetList.append( self._targetName )
            
        for targetName in targetList:
            if not cmds.objExists( targetName ): continue
            if not cmds.objExists( targetName.replace( '_BJT', '_DriverBase' ) ):
                self.makeDriver( targetName, targetName.replace( '_BJT', '' ), self._axisNum )


                
class BodyLineSet( All ):
    
    def __init__(self, targetName ):
        
        self._targetName = targetName
        
        self.core()
        
        
    def core(self):
        
        targets = cmds.ls( self._targetName.replace( 'NUM', '*' ) )[1:-1]
        
        if not cmds.objExists( targets[0].replace( '_BJT', '_DriverBase' ) ):
            self.makeBodyDriver( targets, targets[0].replace( '_BJT', '' ) )