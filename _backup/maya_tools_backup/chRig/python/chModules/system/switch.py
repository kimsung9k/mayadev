import maya.cmds as cmds
import maya.OpenMaya as om
import basicfunc
import math

class SwitchData:
    def __init__(self, *datas ):
        self.topNode   = datas[0]
        self.upperDist = datas[1]
        self.lowerDist = datas[2]
        self.ik    = datas[3]
        self.poleV = datas[4]
        self.fk0   = datas[5]
        self.fk1   = datas[6]
        self.fk2   = datas[7]
        self.fk3   = datas[8]
        self.cu0   = datas[9]
        self.cu1   = datas[10]
        self.cu2   = datas[11]
        self.cu4   = datas[12]
        self.footIkJnt = datas[13]
        
        self.topMtx = basicfunc.getMMatrix( self.topNode, ws=1 )
        self.topMtxInverse = self.topMtx.inverse()
        
class IkToFk( SwitchData ):
    def __init__(self, *datas ):
        SwitchData.__init__( self, *datas )
        
        self.localIkMtx = basicfunc.getLocalMMatrix( self.cu2, self.topNode )
        self.localPoleVMtx = basicfunc.getLocalMMatrix( self.poleV, self.topNode )
        
        self.localElbowMtx = basicfunc.getLocalMMatrix( self.cu1, self.topNode )
        
        self.zeroPoint = om.MPoint( 0,0,0 )
        self.ikPoint = om.MPoint( self.localIkMtx( 3,0 ), self.localIkMtx( 3,1 ), self.localIkMtx( 3,2 ) )
        self.elbowPoint = om.MPoint( self.localElbowMtx(3,0 ), self.localElbowMtx(3,1 ), self.localElbowMtx(3,2 ) )
        self.poleVPoint = om.MPoint( self.localPoleVMtx( 3,0 ), self.localPoleVMtx( 3,1 ), self.localPoleVMtx( 3,2 ) )
        
        self.__editDistFirst()
        self.__editDistSecond()
        self.__editDistThird()
        
        self.ikEndDist = self.__getikEndDist()
        
    def __editDistFirst(self):
        upperDist = self.upperDist
        lowerDist = self.lowerDist
        
        lengthValue = cmds.getAttr( self.ik+'.length' )
        biasValue = cmds.getAttr( self.ik+'.bias' )
        
        slidDistNode = self.ik.replace( 'IK_CTL', 'SlidingDist' )
        distanceSize = cmds.getAttr( slidDistNode+'.distanceAttrSize' )
        slidingSize = cmds.getAttr( slidDistNode+'.slidingAttrSize' )
        
        multLength = 1+lengthValue/distanceSize
        
        self.upperDist_e0 = upperDist*( 1+biasValue/slidingSize )*multLength
        self.lowerDist_e0 = lowerDist*( 1-biasValue/slidingSize )*multLength
        
    def __editDistSecond(self):
        stretchDist = self.zeroPoint.distanceTo( self.ikPoint )
        sumDist = self.upperDist_e0 + self.lowerDist_e0
        stretchValue = cmds.getAttr( self.ik+'.stretchAble' )
        
        if stretchDist > sumDist:
            currentDist = ( stretchDist - sumDist )*stretchValue + sumDist
        else: currentDist = sumDist
            
        self.multValue = currentDist/sumDist
        
        self.upperDist_e1 = self.upperDist_e0*self.multValue
        self.lowerDist_e1 = self.lowerDist_e0*self.multValue 
        
    def __editDistThird(self):
        upperDist = self.zeroPoint.distanceTo( self.poleVPoint )
        lowerDist = self.poleVPoint.distanceTo( self.ikPoint )
        
        attachValue = cmds.getAttr( self.poleV+'.positionAttach' )
        
        self.upperDist_e2 = self.upperDist_e1 * (1-attachValue) + upperDist*attachValue
        self.lowerDist_e2 = self.lowerDist_e1 * (1-attachValue) + lowerDist*attachValue
        
        self.upperDist_e2 = self.zeroPoint.distanceTo( self.elbowPoint )
        self.lowerDist_e2 = self.elbowPoint.distanceTo( self.ikPoint )
        
    def __getikEndDist(self):
        editDist = self.upperDist_e2 + self.lowerDist_e2
        stretchDist = self.zeroPoint.distanceTo( self.ikPoint )
        
        if stretchDist < editDist:
            return stretchDist
        return editDist
     
    def __getDirectSeparateDistAndHeight(self, upperDist, lowerDist, directDist ):
        a = upperDist
        b = lowerDist
        c = directDist
        
        sap = (a**2 - b**2 + c**2) / (2*c)
        
        if a < sap:
            height = 0
        else:
            height = math.sqrt( a**2 - sap**2 )
        
        return sap, height
        
    def getProperVectors( self, inverseAim, inverseUp ):
        directVector = om.MVector( self.ikPoint )
        directVector.normalize()
        poleVVector = om.MVector( self.poleVPoint )
        
        mValue = 1
        if inverseAim:
            mValue *= -1
        if inverseUp:
            mValue *= -1
        
        projV = basicfunc.projVector( poleVVector, directVector )
        
        vertialV = poleVVector - projV
        
        vertialV.normalize()
        
        directDist = self.ikEndDist
        sap, height = self.__getDirectSeparateDistAndHeight( self.upperDist_e2, self.lowerDist_e2, directDist )

        #self.upV    = directVector^poleVVector
        #self.upperV = directVector*sap + vertialV*height
        #self.lowerV = directVector*directDist - self.upperV
        
        #twistValue = cmds.getAttr( self.ik+'.poleTwist' )*mValue
        #self.upV = basicfunc.twistVectorByVector( self.upV, directVector, twistValue )
        #self.upperV = basicfunc.twistVectorByVector( self.upperV, directVector, twistValue )
        #self.lowerV = basicfunc.twistVectorByVector( self.lowerV, directVector, twistValue )
        
        self.upperV = om.MVector( self.elbowPoint )
        self.lowerV = om.MVector( self.ikPoint ) - self.upperV
        
        if( self.upperV*self.lowerV < 0.001 ):
            self.upV = om.MVector( self.localElbowMtx( 1,0 ), self.localElbowMtx( 1,1 ), self.localElbowMtx( 1,2 ) )
        else:
            self.upV = self.lowerV^self.upperV
        
        if inverseUp:
            self.upV *= -1
        if inverseAim:
            self.upperV *= -1
            self.lowerV *= -1
        
    def getProperMatrices(self, upperV, lowerV, upV, endMtx, inverseTranslate=False ):
        uppOv = upperV ^ upV
        lowOv = lowerV ^ upV
        endV  = upperV+lowerV

        if inverseTranslate:
            mValue = -1
        else:
            mValue = 1
        
        upperMtxList = [ upperV.x, upperV.y, upperV.z, 0,
                         upV.x   , upV.y,    upV.z,    0,
                         uppOv.x , uppOv.y , uppOv.z,  0,
                         0,        0,        0,        1 ]
        
        lowerMtxList = [ lowerV.x, lowerV.y, lowerV.z, 0,
                         upV.x   , upV.y,    upV.z,    0,
                         lowOv.x , lowOv.y , lowOv.z , 0,
                         mValue*upperV.x, mValue*upperV.y, mValue*upperV.z, 1 ]
        
        endMtxList   = [ endMtx(0,0), endMtx(0,1), endMtx(0,2), 0,
                         endMtx(1,0), endMtx(1,1), endMtx(1,2), 0,
                         endMtx(2,0), endMtx(2,1), endMtx(2,2), 0, 
                         mValue*endV.x,mValue*endV.y,mValue*endV.z,1 ]
        
        upperMtx = om.MMatrix()
        lowerMtx = om.MMatrix()
        endMtx   = om.MMatrix()
        om.MScriptUtil.createMatrixFromList( upperMtxList,upperMtx )
        om.MScriptUtil.createMatrixFromList( lowerMtxList,lowerMtx )
        om.MScriptUtil.createMatrixFromList( endMtxList,  endMtx   )
        topNodeMtx = basicfunc.getMMatrix( self.topNode, ws=1 )
        
        self.upperCuMtxList = basicfunc.mtxToMtxList( upperMtx*topNodeMtx )
        self.lowerCuMtxList = basicfunc.mtxToMtxList( lowerMtx*topNodeMtx )
        self.endCuMtxList   = basicfunc.mtxToMtxList( endMtx  *topNodeMtx )
        
        if cmds.objExists( self.footIkJnt ):
            self.upperCuMtxList = cmds.xform( self.cu0, q=1, ws=1, matrix=1 )
            self.lowerCuMtxList = cmds.xform( self.cu1, q=1, ws=1, matrix=1 )
            self.endCuMtxList = cmds.xform( self.cu2, q=1, ws=1, matrix=1 )
        
    def setFk(self, inverseAim=False, inverseUp=False ):
        self.getProperVectors( inverseAim, inverseUp )
        
        self.getProperMatrices( self.upperV, self.lowerV, self.upV, self.localIkMtx, inverseAim )
        
        cmds.xform( self.fk0, ws=1, matrix=self.upperCuMtxList )
        cmds.xform( self.fk1, ws=1, matrix=self.lowerCuMtxList )
        cmds.xform( self.fk2, ws=1, matrix=self.endCuMtxList )
        
        if cmds.objExists( self.fk3 ):
            rot = cmds.xform( self.cu4, q=1, ws=1, ro=1 )
            cmds.rotate( rot[0], rot[1], rot[2], self.fk3, ws=1 )

class FkToIk( SwitchData ):
    def __init__(self, *datas ):
        SwitchData.__init__( self, *datas )
        
        fk1Mtx = basicfunc.getMMatrix( self.cu1, ws=1 )
        fk2Mtx = basicfunc.getMMatrix( self.cu2, ws=1 )
        self.fk1Mtx = fk1Mtx*self.topMtxInverse
        self.fk2Mtx = fk2Mtx*self.topMtxInverse
        self.upperV = om.MVector( self.fk1Mtx(3,0), self.fk1Mtx(3,1), self.fk1Mtx(3,2) )
        self.lowerV = om.MVector( self.fk2Mtx(3,0), self.fk2Mtx(3,1), self.fk2Mtx(3,2) )-self.upperV
        self.directV = self.upperV + self.lowerV
        self.endMtx = fk2Mtx
        
    def __editDist(self):
        self.upperDist_e0 = self.upperV.length()
        self.lowerDist_e0 = self.lowerV.length()
        
    def __getMiddleDirectionVector(self):
        return basicfunc.verticalVector( self.upperV, self.directV )
    
    def __getDefaultZVector(self):
        return om.MVector( self.fk1Mtx(2,0), self.fk1Mtx(2,1), self.fk1Mtx(2,2) )
    
    def __setIkAttr(self):
        slidDistNode = self.ik.replace( 'IK_CTL', 'SlidingDist' )
        distanceSize = cmds.getAttr( slidDistNode+'.distanceAttrSize' )
        slidingSize = cmds.getAttr( slidDistNode+'.slidingAttrSize' )
        
        cuRatio = self.upperDist_e0/self.lowerDist_e0

        U = self.upperDist
        L = self.lowerDist
        C = cuRatio
            
        S = (C*L-U)/(U+C*L)
        
        Ue = self.upperDist_e0
        
        D = Ue/((1+S)*U)-1
            
        biasValue = S*slidingSize    
        lengthValue = D*distanceSize
        
        cmds.setAttr( self.ik+'.poleTwist', 0 )
        cmds.setAttr( self.ik+'.length', lengthValue )
        cmds.setAttr( self.ik+'.bias', biasValue )
        
    def __setPoleVAttr(self):
        cmds.setAttr( self.poleV+'.positionAttach', 0 )
        
    def __setFootAttr( self ):
        for attr in ['tapToe', 'heelLift', 'walkRoll', 'toeRot' ]:
            cmds.setAttr( self.ik+'.'+attr, 0 )
            
        footCtl = self.ik.replace( 'IK_CTL', 'Foot_IK_CTL' )
        for attr in ['heelRot', 'ballRot', 'heelTwist', 'ballTwist', 'toeTwist', 'bank' ]:
            cmds.setAttr( footCtl+'.'+attr, 0 )
        
        ry = cmds.getAttr( self.fk3+'.ry' )
        cmds.setAttr( self.ik+'.tapToe', ry )
    
    def setIk(self):
        endMtxList = basicfunc.mtxToMtxList( self.endMtx )
        cmds.xform( self.ik, ws=1, matrix = endMtxList )
        basicfunc.setRotate_keepJointOrient( self.endMtx, self.ik )
        
        self.__editDist()
        allDist = self.upperDist_e0 + self.lowerDist_e0
        middleDirV = self.__getMiddleDirectionVector()
        if middleDirV.length() > 0.001:
            middleDirV.normalize()
            zV = self.upperV + middleDirV*allDist
        else:
            zV = self.__getDefaultZVector()
            zV.normalize()
            zV *= allDist
        
        poleVLocal = om.MPoint( zV )
        poleVWorld = poleVLocal*self.topMtx
        
        self.__setIkAttr()
        self.__setPoleVAttr()
        cmds.move( poleVWorld.x, poleVWorld.y, poleVWorld.z, self.poleV, ws=1 )
        if cmds.objExists( self.fk3 ):
            self.__setFootAttr()
            
        basicfunc.setRotate_keepJointOrient( self.endMtx, self.ik.replace( '_IK_', '_IkItp_' ) )