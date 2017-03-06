import maya.cmds as cmds
import chModules.rigbase as rigbase
import armandlegCtls
import chModules.system.switch as switch
import math

import ctlsAll


class FK_CTL( ctlsAll.CtlsAll ):
    def selectFKs(self, target, *args ):
        switchCtl = target.replace( 'IK_CTL', 'Switch_CTL' ).replace( '_Foot', '' )
        fkCtl = switchCtl.replace( 'Switch', 'FK*' )
        print fkCtl


class IK_CTL( ctlsAll.CtlsAll ):
    def __setNoneFollow(self, target ):
        attrs = cmds.listAttr( target, ud=1 )
        
        for attr in attrs:
            if attr.find( 'Follow' ):
                cmds.setAttr( target+'.'+attr, 0 )
    
    def pinFollow(self, target, *args ):
        ns = self.getNamespace(target)
        
        targetOriginName = target.replace( ns, '' )
        pinCtl    = ns+targetOriginName.replace( 'Switch_CTL', 'IK_Pin_CTL' )
        ikCtl     = ns+targetOriginName.replace( 'Switch_CTL', 'IK_CTL' )
        poleVCtl  = ns+targetOriginName.replace( 'Switch_CTL', 'PoleV_CTL' )
        
        mtxList = cmds.getAttr( ikCtl+'.wm' )
        poleVmtxList = cmds.getAttr( poleVCtl+'.wm' )
        cmds.xform( pinCtl, ws=1, matrix=mtxList )
        
        self.__setNoneFollow( target )
        cmds.setAttr( target+'.pinFollow', 10 )
        
        rigbase.transformDefault( ikCtl )
        cmds.xform( poleVCtl, ws=1, matrix = poleVmtxList )
        
    def setFollow(self, target, followName, *args ):
        ns = self.getNamespace(target)
        
        targetOriginName = target.replace( ns, '' )
        ikCtl     = ns+targetOriginName.replace( 'Switch_CTL', 'IK_CTL' )
        poleVCtl  = ns+targetOriginName.replace( 'Switch_CTL', 'PoleV_CTL' )
        
        mtxList = cmds.getAttr( ikCtl+'.wm' )
        poleVmtxList = cmds.getAttr( poleVCtl+'.wm' )
        
        self.__setNoneFollow(target)
        cmds.setAttr( target+'.'+followName, 10 )
        
        cmds.xform( ikCtl, ws=1, matrix = mtxList )
        rigbase.setRotate_keepJointOrient(mtxList, ikCtl )
        cmds.xform( poleVCtl, ws=1, matrix = poleVmtxList )
        
    def noneFollow(self, target, *args ):
        ns = self.getNamespace(target)
        
        targetOriginName = target.replace( ns, '' )
        ikCtl     = ns+targetOriginName.replace( 'Switch_CTL', 'IK_CTL' )
        poleVCtl  = ns+targetOriginName.replace( 'Switch_CTL', 'PoleV_CTL' )
        
        mtxList = cmds.getAttr( ikCtl+'.wm' )
        poleVmtxList = cmds.getAttr( poleVCtl+'.wm' )
        
        self.__setNoneFollow(target)
        cmds.xform( ikCtl, ws=1, matrix = mtxList )
        rigbase.setRotate_keepJointOrient(mtxList, ikCtl )
        cmds.xform( poleVCtl, ws=1, matrix = poleVmtxList )
        
class Switch_CTL( ctlsAll.CtlsAll ):
    def __init__(self, target ):
        ns=self.getNamespace(target)
        
        targetOriginName = target.replace( ns, '' )
        
        self.switchCtl = target
        
        upValue = 1
        if targetOriginName.find('_L_') != -1:
            self.inverseAim = False
        elif targetOriginName.find('_R_') != -1:
            self.inverseAim = True
        
        if targetOriginName.find('Arm') != -1:
            secondInit = ns+targetOriginName.replace( 'Arm', 'Elbow' ).replace( 'Switch_CTL', 'Init' )
            thirdInit = ns+targetOriginName.replace( 'Arm', 'Wrist' ).replace( 'Switch_CTL', 'Init' )
        elif targetOriginName.find( 'Leg' ) != -1:
            upValue *= -1
            secondInit = ns+targetOriginName.replace( 'Leg', 'Knee' ).replace( 'Switch_CTL', 'Init' )
            thirdInit = ns+targetOriginName.replace( 'Leg', 'Ankle' ).replace( 'Switch_CTL', 'Init' )
        
        if upValue > 0:
            self.inverseUp = False
        else:
            self.inverseUp = True
        
        self.setNode = ns+targetOriginName.replace( 'Switch_CTL', 'Set' )
        self.upperDist = math.fabs( cmds.getAttr( secondInit+'.tx' ) )
        self.lowerDist = math.fabs( cmds.getAttr( thirdInit+'.tx' ) )
        self.ikCtl = ns+targetOriginName.replace( 'Switch_CTL', 'IK_CTL',  )
        self.poleVCtl  = ns+targetOriginName.replace( 'Switch_CTL', 'PoleV_CTL' )
        self.fk0Ctl = target.replace( 'Switch_CTL', 'FK0_CTL' )
        self.fk1Ctl = target.replace( 'Switch_CTL', 'FK1_CTL' )
        self.fk2Ctl = target.replace( 'Switch_CTL', 'FK2_CTL' )
        self.fk3Ctl = target.replace( 'Switch_CTL', 'FK3_CTL' )
        self.cu0 = target.replace( 'Switch_CTL', 'CU0' )
        self.cu1 = target.replace( 'Switch_CTL', 'CU1' )
        self.cu2 = target.replace( 'Switch_CTL', 'CU2' )
        self.cu4 = target.replace( 'Switch_CTL', 'CU4' )
        self.footIkJnt = target.replace( 'Switch_CTL', 'FootIk_JNT' ).replace( 'Leg', 'Ankle' )
        
    def setFk( self, *args ):
        ikToFk = switch.IkToFk( self.setNode, self.upperDist, self.lowerDist, self.ikCtl, self.poleVCtl, self.fk0Ctl, self.fk1Ctl, self.fk2Ctl, self.fk3Ctl, self.cu0, self.cu1, self.cu2, self.cu4, self.footIkJnt )
        
        ikToFk.setFk( self.inverseAim, self.inverseUp )
        
        cmds.setAttr( self.switchCtl+'.fkSwitch', 1 )
        
    def setIk( self, *args ):
        fkToIk = switch.FkToIk( self.setNode, self.upperDist, self.lowerDist, self.ikCtl, self.poleVCtl, self.fk0Ctl, self.fk1Ctl, self.fk2Ctl, self.fk3Ctl, self.cu0, self.cu1, self.cu2, self.cu4, self.footIkJnt )
        
        fkToIk.setIk()
        
        cmds.setAttr( self.switchCtl+'.fkSwitch', 0 )